from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

# ==================================
# Base Schemas (for creation/updates)
# ==================================

class TagBase(BaseModel):
    name: str

class ChallengeBase(BaseModel):
    name: str
    description: str
    points: int
    initial_points: Optional[int] = None
    minimum_points: Optional[int] = None
    decay_factor: Optional[int] = None
    is_visible: bool = False

class SolveBase(BaseModel):
    user_id: int
    challenge_id: int
    team_id: Optional[int] = None

class TeamBase(BaseModel):
    name: str

class UserBase(BaseModel):
    username: str
    email: str

# ==================================
# Create Schemas (for API input)
# ==================================

class TagCreate(TagBase):
    pass

class ChallengeCreate(ChallengeBase):
    flag: str

class SolveCreate(SolveBase):
    pass

class TeamCreate(TeamBase):
    pass

class UserCreate(UserBase):
    password: str

# ==================================
# Response Schemas (for API output)
# ==================================

# Forward declaration for circular dependencies
class _User(BaseModel):
    id: int
    username: str
    email: str
    score: int
    is_staff: bool
    is_active: bool
    team_id: Optional[int] = None

    class Config:
        orm_mode = True

class _Team(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True

class Tag(TagBase):
    id: int

    class Config:
        orm_mode = True

class Solve(SolveBase):
    id: int
    created_at: datetime
    user: _User
    team: Optional[_Team] = None

    class Config:
        orm_mode = True

class ChallengeList(BaseModel):
    id: int
    name: str
    points: int
    is_locked: bool = True  # Computed field

    class Config:
        orm_mode = True

class ChallengeDetail(ChallengeBase):
    id: int
    is_locked: bool = True  # Computed field
    tags: List[Tag] = []
    solves: List[Solve] = []

    class Config:
        orm_mode = True

class Team(TeamBase):
    id: int
    members: List[_User] = []
    solves: List[Solve] = []

    class Config:
        orm_mode = True

class User(UserBase):
    id: int
    score: int
    is_staff: bool
    is_active: bool
    team_id: Optional[int] = None
    solves: List[Solve] = []

    class Config:
        orm_mode = True

# Update forward references to resolve circular dependencies
Team.update_forward_refs()
User.update_forward_refs()
