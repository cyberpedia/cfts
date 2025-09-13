from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

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

# ==================================
# Badge Management Endpoints
# ==================================

@router.post("/badges/", response_model=schemas.Badge, status_code=status.HTTP_201_CREATED)
def create_badge(
    badge: schemas.BadgeCreate,
    db: Session = Depends(get_db),
    current_admin: models.User = Depends(auth.get_current_admin_user)
):
    """
    Create a new badge.
    """
    db_badge = crud.get_badge_by_name(db, name=badge.name)
    if db_badge:
        raise HTTPException(status_code=400, detail="Badge with this name already exists")
    return crud.create_badge(db=db, badge=badge)

@router.get("/badges/", response_model=List[schemas.Badge])
def read_badges(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_admin: models.User = Depends(auth.get_current_admin_user)
):
    """
    Retrieve all badges.
    """
    return crud.get_badges(db, skip=skip, limit=limit)

@router.get("/badges/{badge_id}", response_model=schemas.Badge)
def read_badge(
    badge_id: int,
    db: Session = Depends(get_db),
    current_admin: models.User = Depends(auth.get_current_admin_user)
):
    """
    Retrieve a single badge by its ID.
    """
    db_badge = crud.get_badge(db, badge_id=badge_id)
    if db_badge is None:
        raise HTTPException(status_code=404, detail="Badge not found")
    return db_badge

@router.put("/badges/{badge_id}", response_model=schemas.Badge)
def update_badge(
    badge_id: int,
    badge: schemas.BadgeCreate,
    db: Session = Depends(get_db),
    current_admin: models.User = Depends(auth.get_current_admin_user)
):
    """
    Update an existing badge.
    """
    db_badge = crud.get_badge(db, badge_id=badge_id)
    if db_badge is None:
        raise HTTPException(status_code=404, detail="Badge not found")
    
    # Check if the new name is already taken by another badge
    existing_badge_with_name = crud.get_badge_by_name(db, name=badge.name)
    if existing_badge_with_name and existing_badge_with_name.id != badge_id:
        raise HTTPException(status_code=400, detail="Another badge with this name already exists")
        
    return crud.update_badge(db=db, badge_id=badge_id, badge_data=badge)

@router.delete("/badges/{badge_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_badge(
    badge_id: int,
    db: Session = Depends(get_db),
    current_admin: models.User = Depends(auth.get_current_admin_user)
):
    """
    Delete a badge.
    """
    if not crud.delete_badge(db, badge_id=badge_id):
        raise HTTPException(status_code=404, detail="Badge not found")
    return
