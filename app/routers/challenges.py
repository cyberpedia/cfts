from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime, timezone

from .. import auth, crud, models, schemas, security
from ..database import get_db

router = APIRouter()

@router.get("/", response_model=List[schemas.ChallengeList])
def read_challenges(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    return crud.get_visible_challenges(db, user_id=current_user.id)

@router.get("/{challenge_id}", response_model=schemas.ChallengeDetail)
def read_challenge_detail(
    challenge_id: int, db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    challenge = crud.get_challenge(db, challenge_id=challenge_id, user_id=current_user.id)
    if challenge is None or not challenge.is_visible:
        raise HTTPException(status_code=404, detail="Challenge not found")
    return challenge

@router.post("/{challenge_id}/submit")
def submit_flag(
    challenge_id: int, submission: schemas.FlagSubmission, db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    settings = crud.get_settings(db)
    now = datetime.now(timezone.utc)

    if settings.event_start_time and now < settings.event_start_time:
        raise HTTPException(status_code=403, detail="The event has not started yet.")
    if settings.event_end_time and now > settings.event_end_time:
        raise HTTPException(status_code=403, detail="The event has ended.")

    challenge = crud.get_challenge(db, challenge_id=challenge_id, user_id=current_user.id)
    if challenge is None or not challenge.is_visible:
        raise HTTPException(status_code=404, detail="Challenge not found")
    if challenge.is_locked:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Challenge is locked.")
    if crud.has_user_solved_challenge(db, user_id=current_user.id, challenge_id=challenge_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You have already solved this challenge.")

    if not security.compare_flags(submission.flag, challenge.flag):
        crud.create_audit_log(
            db=db, action="flag_submit_incorrect", user_id=current_user.id,
            details={"challenge_id": challenge.id, "challenge_name": challenge.name, "submission": submission.flag}
        )
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect flag.")

    crud.create_audit_log(
        db=db, action="flag_submit_correct", user_id=current_user.id,
        details={"challenge_id": challenge.id, "challenge_name": challenge.name, "submission": submission.flag}
    )
    crud.create_solve(db=db, user=current_user, challenge=challenge)
    crud.update_user_score(db=db, user=current_user, points=challenge.points)

    solve_count = crud.get_solve_count_for_challenge(db, challenge_id=challenge_id)
    if solve_count == 1:
        first_blood_badge = crud.get_badge_by_name(db, name="First Blood")
        if first_blood_badge and crud.award_badge_to_user(db=db, user=current_user, badge=first_blood_badge):
            crud.create_notification(
                db=db, user_id=current_user.id, title="New Badge Earned!",
                body=f"Congratulations! You earned the '{first_blood_badge.name}' badge for '{challenge.name}'."
            )
    return {"message": "Correct flag!"}
