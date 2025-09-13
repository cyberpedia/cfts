from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .. import auth, crud, schemas
from ..database import get_db

router = APIRouter()

@router.get("/", response_model=List[schemas.LeaderboardEntry])
def read_leaderboard(
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(auth.get_current_active_user)
):
    """
    Retrieve the competition leaderboard.
    """
    board_data = crud.get_leaderboard(db)
    leaderboard = []
    for i, (team_id, team_name, total_score, last_submission) in enumerate(board_data):
        leaderboard.append(
            schemas.LeaderboardEntry(
                rank=i + 1,
                team_id=team_id,
                team_name=team_name,
                total_score=total_score or 0,
                last_submission=last_submission
            )
        )
    return leaderboard
