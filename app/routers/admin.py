from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .. import auth, crud, models, schemas
from ..database import get_db

router = APIRouter()

@router.get("/settings/", response_model=schemas.CTFSetting)
def read_settings(
    db: Session = Depends(get_db),
    current_admin: models.User = Depends(auth.get_current_admin_user)
):
    """
    Retrieve the full CTF settings (Admin only).
    """
    return crud.get_settings(db)

@router.put("/settings/", response_model=schemas.CTFSetting)
def update_settings(
    settings_data: schemas.CTFSettingUpdate,
    db: Session = Depends(get_db),
    current_admin: models.User = Depends(auth.get_current_admin_user)
):
    """
    Update the CTF settings (Admin only).
    """
    return crud.update_settings(db, settings_data)
