from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func
from typing import List, Optional
from . import models, schemas, security
from datetime import datetime

# ==================================
# Settings CRUD Functions
# ==================================

def get_settings(db: Session) -> models.CTFSetting:
    """
    Retrieves the CTF settings. If no settings exist, creates default ones.
    """
    db_settings = db.query(models.CTFSetting).first()
    if not db_settings:
        db_settings = models.CTFSetting(
            event_title="My CTF",
            ui_theme="dark",
            allow_registrations=True,
            allow_teams=True,
            scoring_mode="static"
        )
        db.add(db_settings)
        db.commit()
        db.refresh(db_settings)
    return db_settings

def update_settings(db: Session, settings_data: schemas.CTFSettingUpdate) -> models.CTFSetting:
    """
    Updates the CTF settings.
    """
    db_settings = get_settings(db)
    update_data = settings_data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_settings, key, value)
    db.commit()
    db.refresh(db_settings)
    return db_settings

# ==================================
# User CRUD Functions
# ==================================

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def get_user_by_verification_token(db: Session, token: str):
    return db.query(models.User).filter(models.User.verification_token == token).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = security.get_password_hash(user.password)
    verification_token = security.generate_verification_token()
    db_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        verification_token=verification_token,
        is_active=False
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user_score(db: Session, user: models.User, points: int):
    user.score += points
    db.commit()
    db.refresh(user)
    return user

# ==================================
# Team CRUD Functions
# ==================================

def get_team(db: Session, team_id: int):
    return db.query(models.Team).filter(models.Team.id == team_id).first()

def get_team_by_name(db: Session, name: str):
    return db.query(models.Team).filter(models.Team.name == name).first()

def get_teams(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Team).offset(skip).limit(limit).all()

def create_team(db: Session, team: schemas.TeamCreate, user: models.User):
    db_team = models.Team(name=team.name)
    db.add(db_team)
    db.commit()
    db.refresh(db_team)
    user.team_id = db_team.id
    db.commit()
    db.refresh(user)
    return db_team

def add_user_to_team(db: Session, user: models.User, team: models.Team):
    user.team_id = team.id
    db.commit()
    db.refresh(user)
    return user

def remove_user_from_team(db: Session, user: models.User):
    user.team_id = None
    db.commit()
    db.refresh(user)
    return user

# ==================================
# Challenge & Solve CRUD Functions
# ==================================

def has_user_solved_challenge(db: Session, user_id: int, challenge_id: int) -> bool:
    return db.query(models.Solve).filter(
        models.Solve.user_id == user_id,
        models.Solve.challenge_id == challenge_id
    ).first() is not None

def get_user_solved_challenge_ids(db: Session, user_id: int) -> set:
    solved_challenges = db.query(models.Solve.challenge_id).filter(models.Solve.user_id == user_id).all()
    return {solve.challenge_id for solve in solved_challenges}

def get_visible_challenges(db: Session, user_id: int) -> List[models.Challenge]:
    challenges = db.query(models.Challenge).filter(models.Challenge.is_visible == True).options(joinedload(models.Challenge.dependencies)).all()
    solved_ids = get_user_solved_challenge_ids(db, user_id)

    for challenge in challenges:
        dependency_ids = {dep.id for dep in challenge.dependencies}
        challenge.is_locked = not dependency_ids.issubset(solved_ids)
    
    return challenges

def get_challenge(db: Session, challenge_id: int, user_id: int) -> Optional[models.Challenge]:
    challenge = db.query(models.Challenge).filter(models.Challenge.id == challenge_id).options(joinedload(models.Challenge.dependencies)).first()
    if not challenge:
        return None
    
    solved_ids = get_user_solved_challenge_ids(db, user_id)
    dependency_ids = {dep.id for dep in challenge.dependencies}
    challenge.is_locked = not dependency_ids.issubset(solved_ids)
    
    return challenge

def create_solve(db: Session, user: models.User, challenge: models.Challenge) -> models.Solve:
    db_solve = models.Solve(
        user_id=user.id,
        challenge_id=challenge.id,
        team_id=user.team_id
    )
    db.add(db_solve)
    db.commit()
    db.refresh(db_solve)
    return db_solve

# ==================================
# Leaderboard CRUD Functions
# ==================================

def get_leaderboard(db: Session):
    leaderboard_query = (
        db.query(
            models.Team.id,
            models.Team.name,
            func.sum(models.User.score).label("total_score"),
            func.max(models.Solve.created_at).label("last_submission"),
        )
        .join(models.User, models.Team.id == models.User.team_id)
        .outerjoin(models.Solve, models.Team.id == models.Solve.team_id)
        .group_by(models.Team.id)
        .order_by(
            func.sum(models.User.score).desc(),
            func.max(models.Solve.created_at).asc(),
        )
    )
    return leaderboard_query.all()
