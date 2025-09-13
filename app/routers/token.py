from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .. import auth, crud, security
from ..config import settings
from ..database import get_db

router = APIRouter()

@router.post("/token")
def login_for_access_token(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user = auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        crud.create_audit_log(
            db=db, action="user_login_fail",
            details={"username": form_data.username, "reason": "Incorrect username or password"}
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        crud.create_audit_log(
            db=db, action="user_login_fail", user_id=user.id,
            details={"username": user.username, "reason": "Inactive user"}
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user. Please verify your email.",
        )
    
    crud.create_audit_log(db=db, action="user_login_success", user_id=user.id)
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}
