from datetime import timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError, jwt

from . import crud, models, security
from .config import settings
from .database import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def authenticate_user(db: Session, username: str, password: str) -> models.User | bool:
    """
    Authenticates a user by username and password.
    """
    user = crud.get_user_by_username(db, username=username)
    if not user:
        return False
    if not security.verify_password(password, user.hashed_password):
        return False
    return user

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> models.User:
    """
    Decodes the JWT token to get the current user.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = crud.get_user_by_username(db, username=username)
    if user is None:
        raise credentials_exception
    return user

def get_current_active_user(current_user: models.User = Depends(get_current_user)) -> models.User:
    """
    Dependency to get the current active user.
    """
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

def get_current_admin_user(current_user: models.User = Depends(get_current_active_user)) -> models.User:
    """
    Dependency to get the current active user who is also an admin.
    """
    if not current_user.is_staff:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The user does not have administrative privileges."
        )
    return current_user
