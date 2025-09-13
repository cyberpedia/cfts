from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import auth, crud, models, schemas
from ..database import get_db

router = APIRouter()

@router.get("/", response_model=List[schemas.Notification])
def get_user_notifications(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    """
    Retrieve all notifications for the currently logged-in user.
    """
    return crud.get_notifications_for_user(db, user_id=current_user.id, skip=skip, limit=limit)

@router.post("/{notification_id}/read", response_model=schemas.Notification)
def mark_as_read(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    """
    Mark a specific notification as read.
    """
    notification = crud.mark_notification_as_read(db, notification_id=notification_id, user_id=current_user.id)
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found or you do not have permission to access it.")
    return notification
