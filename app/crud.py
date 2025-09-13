from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func
from typing import List, Optional
from . import models, schemas, security
from datetime import datetime, timedelta

# ==================================
# Dynamic Challenge Instance CRUD
# ==================================

def create_instance(db: Session, user_id: int, challenge_id: int, container_id: str, ip_address: str, port: int, expires_at: datetime) -> models.DynamicChallengeInstance:
    """Creates a new dynamic challenge instance record."""
    db_instance = models.DynamicChallengeInstance(
        user_id=user_id,
        challenge_id=challenge_id,
        container_id=container_id,
        ip_address=ip_address,
        port=port,
        expires_at=expires_at
    )
    db.add(db_instance)
    db.commit()
    db.refresh(db_instance)
    return db_instance

def get_active_instance_for_user(db: Session, user_id: int, challenge_id: int) -> Optional[models.DynamicChallengeInstance]:
    """Retrieves an active (not expired) instance for a user and challenge."""
    return db.query(models.DynamicChallengeInstance).filter(
        models.DynamicChallengeInstance.user_id == user_id,
        models.DynamicChallengeInstance.challenge_id == challenge_id,
        models.DynamicChallengeInstance.expires_at > datetime.utcnow()
    ).first()

def get_instance_by_id(db: Session, instance_id: int) -> Optional[models.DynamicChallengeInstance]:
    """Retrieves an instance by its primary key."""
    return db.query(models.DynamicChallengeInstance).filter(models.DynamicChallengeInstance.id == instance_id).first()

def delete_instance(db: Session, instance_id: int):
    """Deletes an instance record from the database."""
    db_instance = get_instance_by_id(db, instance_id)
    if db_instance:
        db.delete(db_instance)
        db.commit()

# ==================================
# Audit Log CRUD Functions
# ==================================

def create_audit_log(db: Session, action: str, user_id: Optional[int] = None, details: Optional[dict] = None):
    db_log = models.AuditLog(user_id=user_id, action=action, details=details)
    db.add(db_log)
    db.commit()

def get_audit_logs(db: Session, skip: int = 0, limit: int = 100) -> List[models.AuditLog]:
    return db.query(models.AuditLog).order_by(models.AuditLog.timestamp.desc()).offset(skip).limit(limit).all()

# ==================================
# Settings CRUD Functions
# ==================================

def get_settings(db: Session) -> models.CTFSetting:
    db_settings = db.query(models.CTFSetting).first()
    if not db_settings:
        db_settings = models.CTFSetting()
        db.add(db_settings)
        db.commit()
        db.refresh(db_settings)
    return db_settings

def update_settings(db: Session, settings_data: schemas.CTFSettingUpdate) -> models.CTFSetting:
    db_settings = get_settings(db)
    for key, value in settings_data.dict(exclude_unset=True).items():
        setattr(db_settings, key, value)
    db.commit()
    db.refresh(db_settings)
    return db_settings

# ==================================
# User CRUD Functions
# ==================================

def get_user(db: Session, user_id: int) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def get_or_create_oauth_user(db: Session, user_info: dict) -> models.User:
    user = get_user_by_email(db, email=user_info['email'])
    if user: return user
    username = user_info.get('name', user_info['email'].split('@')[0]).replace(" ", "")
    original_username = username
    while get_user_by_username(db, username=username):
        username = f"{original_username}_{secrets.token_hex(2)}"
    db_user = models.User(username=username, email=user_info['email'], hashed_password=None, is_active=True)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    create_audit_log(db, action="user_register_oauth", user_id=db_user.id, details={"provider": "google"})
    return db_user

# Other functions... (omitted for brevity, no changes were made to them)
def get_user_by_verification_token(db: Session, token: str): return db.query(models.User).filter(models.User.verification_token == token).first()
def get_pending_users(db: Session, skip: int = 0, limit: int = 100) -> List[models.User]: return db.query(models.User).filter(models.User.is_active == False).offset(skip).limit(limit).all()
def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = security.get_password_hash(user.password)
    verification_token = security.generate_verification_token()
    db_user = models.User(username=user.username, email=user.email, hashed_password=hashed_password, verification_token=verification_token, is_active=False)
    db.add(db_user); db.commit(); db.refresh(db_user); return db_user
def update_user_score(db: Session, user: models.User, points: int): user.score += points; db.commit(); db.refresh(user); return user
def approve_user(db: Session, user: models.User) -> models.User: user.is_active = True; user.verification_token = None; db.commit(); db.refresh(user); return user
def get_team(db: Session, team_id: int): return db.query(models.Team).filter(models.Team.id == team_id).first()
def get_team_by_name(db: Session, name: str): return db.query(models.Team).filter(models.Team.name == name).first()
def get_teams(db: Session, skip: int = 0, limit: int = 100): return db.query(models.Team).offset(skip).limit(limit).all()
def create_team(db: Session, team: schemas.TeamCreate, user: models.User):
    db_team = models.Team(name=team.name); db.add(db_team); db.commit(); db.refresh(db_team)
    user.team_id = db_team.id; db.commit(); db.refresh(user); return db_team
def add_user_to_team(db: Session, user: models.User, team: models.Team): user.team_id = team.id; db.commit(); db.refresh(user); return user
def remove_user_from_team(db: Session, user: models.User): user.team_id = None; db.commit(); db.refresh(user); return user
def has_user_solved_challenge(db: Session, user_id: int, challenge_id: int) -> bool: return db.query(models.Solve).filter(models.Solve.user_id == user_id, models.Solve.challenge_id == challenge_id).first() is not None
def get_solve_count_for_challenge(db: Session, challenge_id: int) -> int: return db.query(models.Solve).filter(models.Solve.challenge_id == challenge_id).count()
def get_user_solved_challenge_ids(db: Session, user_id: int) -> set: return {s.challenge_id for s in db.query(models.Solve.challenge_id).filter(models.Solve.user_id == user_id).all()}
def get_visible_challenges(db: Session, user_id: int) -> List[models.Challenge]:
    challenges = db.query(models.Challenge).options(joinedload(models.Challenge.dependencies)).filter(models.Challenge.is_visible == True).all()
    solved_ids = get_user_solved_challenge_ids(db, user_id)
    for c in challenges: c.is_locked = not {d.id for d in c.dependencies}.issubset(solved_ids)
    return challenges
def get_challenge(db: Session, challenge_id: int, user_id: int) -> Optional[models.Challenge]:
    challenge = db.query(models.Challenge).options(joinedload(models.Challenge.dependencies)).filter(models.Challenge.id == challenge_id).first()
    if not challenge: return None
    solved_ids = get_user_solved_challenge_ids(db, user_id)
    challenge.is_locked = not {d.id for d in challenge.dependencies}.issubset(solved_ids)
    return challenge
def create_solve(db: Session, user: models.User, challenge: models.Challenge) -> models.Solve:
    db_solve = models.Solve(user_id=user.id, challenge_id=challenge.id, team_id=user.team_id); db.add(db_solve); db.commit(); db.refresh(db_solve); return db_solve
def get_badge(db: Session, badge_id: int) -> Optional[models.Badge]: return db.query(models.Badge).filter(models.Badge.id == badge_id).first()
def get_badge_by_name(db: Session, name: str) -> Optional[models.Badge]: return db.query(models.Badge).filter(models.Badge.name == name).first()
def get_badges(db: Session, skip: int = 0, limit: int = 100) -> List[models.Badge]: return db.query(models.Badge).offset(skip).limit(limit).all()
def create_badge(db: Session, badge: schemas.BadgeCreate) -> models.Badge:
    db_badge = models.Badge(**badge.dict()); db.add(db_badge); db.commit(); db.refresh(db_badge); return db_badge
def update_badge(db: Session, badge_id: int, badge_data: schemas.BadgeCreate) -> Optional[models.Badge]:
    db_badge = get_badge(db, badge_id)
    if db_badge:
        for k, v in badge_data.dict().items(): setattr(db_badge, k, v)
        db.commit(); db.refresh(db_badge)
    return db_badge
def delete_badge(db: Session, badge_id: int) -> bool:
    db_badge = get_badge(db, badge_id)
    if db_badge: db.delete(db_badge); db.commit(); return True
    return False
def award_badge_to_user(db: Session, user: models.User, badge: models.Badge) -> Optional[models.UserBadge]:
    if db.query(models.UserBadge).filter(models.UserBadge.user_id == user.id, models.UserBadge.badge_id == badge.id).first(): return None
    db_user_badge = models.UserBadge(user_id=user.id, badge_id=badge.id); db.add(db_user_badge); db.commit(); db.refresh(db_user_badge); return db_user_badge
def create_notification(db: Session, user_id: int, title: str, body: str) -> models.Notification:
    db_notification = models.Notification(user_id=user_id, title=title, body=body); db.add(db_notification); db.commit(); db.refresh(db_notification); return db_notification
def get_notifications_for_user(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> List[models.Notification]: return db.query(models.Notification).filter(models.Notification.user_id == user_id).order_by(models.Notification.created_at.desc()).offset(skip).limit(limit).all()
def get_notification(db: Session, notification_id: int, user_id: int) -> Optional[models.Notification]: return db.query(models.Notification).filter(models.Notification.id == notification_id, models.Notification.user_id == user_id).first()
def mark_notification_as_read(db: Session, notification_id: int, user_id: int) -> Optional[models.Notification]:
    db_notification = get_notification(db, notification_id, user_id)
    if db_notification: db_notification.is_read = True; db.commit(); db.refresh(db_notification)
    return db_notification
def get_leaderboard(db: Session): return db.query(models.Team.id, models.Team.name, func.sum(models.User.score).label("total_score"), func.max(models.Solve.created_at).label("last_submission")).join(models.User, models.Team.id == models.User.team_id).outerjoin(models.Solve, models.Team.id == models.Solve.team_id).group_by(models.Team.id).order_by(func.sum(models.User.score).desc(), func.max(models.Solve.created_at).asc()).all()
