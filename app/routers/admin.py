from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from .. import auth, crud, models, schemas, email
from ..database import get_db

router = APIRouter()

# ==================================
# Settings Management
# ==================================

@router.get("/settings/", response_model=schemas.CTFSetting)
def read_settings(db: Session = Depends(get_db), current_admin: models.User = Depends(auth.get_current_admin_user)):
    return crud.get_settings(db)

@router.put("/settings/", response_model=schemas.CTFSetting)
def update_settings(
    settings_data: schemas.CTFSettingUpdate, db: Session = Depends(get_db),
    current_admin: models.User = Depends(auth.get_current_admin_user)
):
    crud.create_audit_log(db=db, action="admin_update_settings", user_id=current_admin.id, details={"changes": settings_data.dict(exclude_unset=True)})
    return crud.update_settings(db, settings_data)

# ==================================
# Badge Management
# ==================================

@router.post("/badges/", response_model=schemas.Badge, status_code=status.HTTP_201_CREATED)
def create_badge(badge: schemas.BadgeCreate, db: Session = Depends(get_db), current_admin: models.User = Depends(auth.get_current_admin_user)):
    if crud.get_badge_by_name(db, name=badge.name):
        raise HTTPException(status_code=400, detail="Badge with this name already exists")
    new_badge = crud.create_badge(db=db, badge=badge)
    crud.create_audit_log(db=db, action="admin_create_badge", user_id=current_admin.id, details={"badge_id": new_badge.id, "name": new_badge.name})
    return new_badge

@router.get("/badges/", response_model=List[schemas.Badge])
def read_badges(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_admin: models.User = Depends(auth.get_current_admin_user)):
    return crud.get_badges(db, skip=skip, limit=limit)

@router.put("/badges/{badge_id}", response_model=schemas.Badge)
def update_badge(badge_id: int, badge: schemas.BadgeCreate, db: Session = Depends(get_db), current_admin: models.User = Depends(auth.get_current_admin_user)):
    if not crud.get_badge(db, badge_id=badge_id): raise HTTPException(status_code=404, detail="Badge not found")
    crud.create_audit_log(db=db, action="admin_update_badge", user_id=current_admin.id, details={"badge_id": badge_id, "changes": badge.dict()})
    return crud.update_badge(db=db, badge_id=badge_id, badge_data=badge)

@router.delete("/badges/{badge_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_badge(badge_id: int, db: Session = Depends(get_db), current_admin: models.User = Depends(auth.get_current_admin_user)):
    db_badge = crud.get_badge(db, badge_id=badge_id)
    if not db_badge: raise HTTPException(status_code=404, detail="Badge not found")
    crud.create_audit_log(db=db, action="admin_delete_badge", user_id=current_admin.id, details={"badge_id": badge_id, "badge_name": db_badge.name})
    crud.delete_badge(db, badge_id=badge_id)

# ==================================
# User Management
# ==================================

@router.get("/users/pending", response_model=List[schemas.User])
def get_pending_verification_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_admin: models.User = Depends(auth.get_current_admin_user)):
    return crud.get_pending_users(db, skip=skip, limit=limit)

@router.post("/users/{user_id}/approve", response_model=schemas.User)
def approve_user_registration(user_id: int, db: Session = Depends(get_db), current_admin: models.User = Depends(auth.get_current_admin_user)):
    db_user = crud.get_user(db, user_id=user_id)
    if not db_user: raise HTTPException(status_code=404, detail="User not found")
    if db_user.is_active: raise HTTPException(status_code=400, detail="User is already active")
    crud.create_audit_log(db=db, action="admin_approve_user", user_id=current_admin.id, details={"approved_user_id": user_id, "approved_username": db_user.username})
    crud.create_notification(db=db, user_id=db_user.id, title="Account Approved", body="Your account has been manually approved by an administrator.")
    return crud.approve_user(db=db, user=db_user)

@router.post("/users/email")
async def send_bulk_email(
    email_data: schemas.AdminMassEmail,
    db: Session = Depends(get_db),
    current_admin: models.User = Depends(auth.get_current_admin_user)
):
    """
    Send a mass email to all registered users.
    """
    users = crud.get_all_users(db)
    recipient_emails = [user.email for user in users]

    if not recipient_emails:
        return {"message": "No users to email."}

    await email.send_mass_email(
        email_to=recipient_emails,
        subject=email_data.subject,
        body=email_data.body
    )

    crud.create_audit_log(
        db=db,
        action="admin_mass_email",
        user_id=current_admin.id,
        details={"subject": email_data.subject, "recipient_count": len(recipient_emails)}
    )

    return {"message": f"Email sent to {len(recipient_emails)} users successfully."}

# ==================================
# Audit Log Viewer
# ==================================

@router.get("/logs/", response_model=List[schemas.AuditLog])
def get_audit_logs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_admin: models.User = Depends(auth.get_current_admin_user)):
    return crud.get_audit_logs(db, skip=skip, limit=limit)
