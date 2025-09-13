from sqlalchemy.orm import Session, joinedload
from typing import List
from . import models, schemas, security

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
    """
    Updates a user's score by adding the given points.
    """
    user.score += points
    db.commit()
    db.refresh(user)
    return user

# ==================================
# Challenge & Solve CRUD Functions
# ==================================

def has_user_solved_challenge(db: Session, user_id: int, challenge_id: int) -> bool:
    """
    Checks if a user has already solved a specific challenge.
    """
    return db.query(models.Solve).filter(
        models.Solve.user_id == user_id,
        models.Solve.challenge_id == challenge_id
    ).first() is not None

def get_user_solved_challenge_ids(db: Session, user_id: int) -> set:
    """
    Gets a set of challenge IDs that the user has solved.
    """
    solved_challenges = db.query(models.Solve.challenge_id).filter(models.Solve.user_id == user_id).all()
    return {solve.challenge_id for solve in solved_challenges}

def get_visible_challenges(db: Session, user_id: int) -> List[models.Challenge]:
    """
    Retrieves all visible challenges and computes their locked status for a user.
    """
    challenges = db.query(models.Challenge).filter(models.Challenge.is_visible == True).options(joinedload(models.Challenge.dependencies)).all()
    solved_ids = get_user_solved_challenge_ids(db, user_id)

    for challenge in challenges:
        dependency_ids = {dep.id for dep in challenge.dependencies}
        challenge.is_locked = not dependency_ids.issubset(solved_ids)
    
    return challenges

def get_challenge(db: Session, challenge_id: int, user_id: int) -> models.Challenge | None:
    """
    Retrieves a single challenge and computes its locked status for a user.
    """
    challenge = db.query(models.Challenge).filter(models.Challenge.id == challenge_id).options(joinedload(models.Challenge.dependencies)).first()
    if not challenge:
        return None
    
    solved_ids = get_user_solved_challenge_ids(db, user_id)
    dependency_ids = {dep.id for dep in challenge.dependencies}
    challenge.is_locked = not dependency_ids.issubset(solved_ids)
    
    return challenge

def create_solve(db: Session, user: models.User, challenge: models.Challenge) -> models.Solve:
    """
    Creates a new solve record for a user and a challenge.
    """
    db_solve = models.Solve(
        user_id=user.id,
        challenge_id=challenge.id,
        team_id=user.team_id
    )
    db.add(db_solve)
    db.commit()
    db.refresh(db_solve)
    return db_solve
