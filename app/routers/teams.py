from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import auth, crud, models, schemas
from ..database import get_db

router = APIRouter()

@router.post("/", response_model=schemas.Team)
def create_team(
    team: schemas.TeamCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    """
    Create a new team. The creator automatically joins the team.
    """
    if current_user.team_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You are already on a team. Leave your current team first."
        )
    
    db_team = crud.get_team_by_name(db, name=team.name)
    if db_team:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A team with this name already exists."
        )
    
    return crud.create_team(db=db, team=team, user=current_user)

@router.get("/", response_model=List[schemas.Team])
def read_teams(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    """
    Retrieve all teams.
    """
    teams = crud.get_teams(db, skip=skip, limit=limit)
    return teams

@router.get("/{team_id}", response_model=schemas.Team)
def read_team(
    team_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    """
    Retrieve details for a specific team.
    """
    db_team = crud.get_team(db, team_id=team_id)
    if db_team is None:
        raise HTTPException(status_code=404, detail="Team not found")
    return db_team

@router.post("/{team_id}/join", response_model=schemas.User)
def join_team(
    team_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    """
    Join an existing team.
    """
    if current_user.team_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You are already on a team. Leave your current team first."
        )
    
    db_team = crud.get_team(db, team_id=team_id)
    if db_team is None:
        raise HTTPException(status_code=404, detail="Team not found")
        
    return crud.add_user_to_team(db=db, user=current_user, team=db_team)

@router.post("/leave", response_model=schemas.User)
def leave_team(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    """
    Leave the current team.
    """
    if not current_user.team_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You are not on a team."
        )
    
    return crud.remove_user_from_team(db=db, user=current_user)
