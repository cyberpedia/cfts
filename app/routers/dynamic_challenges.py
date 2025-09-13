from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from .. import auth, crud, models, schemas, docker_service
from ..database import get_db

router = APIRouter()

@router.post("/{challenge_id}/start", response_model=schemas.DynamicChallengeInstance)
def start_challenge(
    challenge_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    """
    Starts a new dynamic challenge instance for the user.
    """
    # 1a. Check if the user already has an active instance
    active_instance = crud.get_active_instance_for_user(
        db, user_id=current_user.id, challenge_id=challenge_id
    )
    if active_instance:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You already have an active instance for this challenge."
        )

    # Check if the challenge exists
    challenge = db.query(models.Challenge).filter(models.Challenge.id == challenge_id).first()
    if not challenge:
        raise HTTPException(status_code=404, detail="Challenge not found")

    # 1b. Call the placeholder Docker service
    container_details = docker_service.start_challenge_container(challenge)

    # 1c. Save instance details to the database
    expires_at = datetime.utcnow() + timedelta(hours=1)  # Instance is valid for 1 hour
    
    new_instance = crud.create_instance(
        db=db,
        user_id=current_user.id,
        challenge_id=challenge_id,
        container_id=container_details["container_id"],
        ip_address="127.0.0.1",  # Placeholder IP
        port=container_details["port"],
        expires_at=expires_at
    )
    
    crud.create_audit_log(
        db, action="dynamic_challenge_start", user_id=current_user.id,
        details={"challenge_id": challenge_id, "instance_id": new_instance.id}
    )

    # 1d. Return connection details
    return new_instance

@router.post("/stop/{instance_id}")
def stop_challenge(
    instance_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    """
    Stops a running dynamic challenge instance for the user.
    """
    instance = crud.get_instance_by_id(db, instance_id=instance_id)

    # Ensure the instance exists and belongs to the current user
    if not instance or instance.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Instance not found or you do not have permission to stop it."
        )
    
    # Call the placeholder service to stop the container
    docker_service.stop_challenge_container(instance.container_id)
    
    # Delete the record from the database
    crud.delete_instance(db, instance_id=instance_id)

    crud.create_audit_log(
        db, action="dynamic_challenge_stop", user_id=current_user.id,
        details={"challenge_id": instance.challenge_id, "instance_id": instance_id}
    )

    return {"message": "Challenge instance stopped successfully."}
