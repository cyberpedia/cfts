from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import auth, crud, models, schemas
from ..database import get_db

router = APIRouter()


@router.post("/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user.
    """
    settings = crud.get_settings(db)
    if not settings.allow_registrations:
        raise HTTPException(status_code=403, detail="Registrations are currently disabled.")

    db_user_by_email = crud.get_user_by_email(db, email=user.email)
    if db_user_by_email:
        raise HTTPException(status_code=400, detail="Email already registered")

    db_user_by_username = crud.get_user_by_username(db, username=user.username)
    if db_user_by_username:
        raise HTTPException(status_code=400, detail="Username already taken")

    return crud.create_user(db=db, user=user)


@router.get("/verify/{token}")
def verify_user(token: str, db: Session = Depends(get_db)):
    """
    Verify a user's email address using the provided token.
    """
    db_user = crud.get_user_by_verification_token(db, token=token)
    if not db_user:
        raise HTTPException(
            status_code=404, detail="Verification token not found or invalid"
        )

    db_user.is_active = True
    db_user.verification_token = None
    db.commit()

    return {"message": "User verified successfully"}


@router.get("/me", response_model=schemas.User)
def read_users_me(current_user: models.User = Depends(auth.get_current_active_user)):
    """
    Get the profile of the currently authenticated user.
    """
    return current_user
