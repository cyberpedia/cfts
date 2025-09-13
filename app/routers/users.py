from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import auth, crud, models, schemas, email
from ..database import get_db

router = APIRouter()

@router.post("/", response_model=schemas.User)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    settings = crud.get_settings(db)
    if not settings.allow_registrations:
        raise HTTPException(status_code=403, detail="Registrations are currently disabled.")
    if crud.get_user_by_email(db, email=user.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    if crud.get_user_by_username(db, username=user.username):
        raise HTTPException(status_code=400, detail="Username already taken")

    new_user = crud.create_user(db=db, user=user)
    crud.create_audit_log(
        db=db, action="user_register", user_id=new_user.id,
        details={"username": new_user.username, "email": new_user.email}
    )
    await email.send_verification_email(
        email_to=new_user.email, username=new_user.username, token=new_user.verification_token
    )
    return new_user

@router.get("/verify/{token}")
def verify_user(token: str, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_verification_token(db, token=token)
    if not db_user:
        # Avoid logging the invalid token to prevent log spamming.
        raise HTTPException(status_code=404, detail="Verification token not found or invalid")

    db_user.is_active = True
    db_user.verification_token = None
    db.commit()
    crud.create_audit_log(db=db, action="user_verify_success", user_id=db_user.id)
    return {"message": "User verified successfully"}

@router.get("/me", response_model=schemas.User)
def read_users_me(current_user: models.User = Depends(auth.get_current_active_user)):
    return current_user
