from sqlalchemy.orm import Session
from . import models, schemas, security

def get_user_by_email(db: Session, email: str):
    """
    Retrieve a user from the database by their email address.
    """
    return db.query(models.User).filter(models.User.email == email).first()

def get_user_by_username(db: Session, username: str):
    """
    Retrieve a user from the database by their username.
    """
    return db.query(models.User).filter(models.User.username == username).first()

def get_user_by_verification_token(db: Session, token: str):
    """
    Retrieve a user from the database by their verification token.
    """
    return db.query(models.User).filter(models.User.verification_token == token).first()

def create_user(db: Session, user: schemas.UserCreate):
    """
    Create a new user in the database.
    """
    hashed_password = security.get_password_hash(user.password)
    verification_token = security.generate_verification_token()
    db_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        verification_token=verification_token,
        is_active=False  # User is inactive until verified
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
