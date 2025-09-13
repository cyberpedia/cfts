from pydantic import BaseModel
from typing import List, Optional

# Forward declaration for circular dependency
class User(BaseModel):
    id: int
    username: str
    email: str
    score: int
    is_staff: bool
    is_active: bool
    team_id: Optional[int] = None

    class Config:
        orm_mode = True

# User Schemas
class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    password: str

# Team Schemas
class TeamBase(BaseModel):
    name: str

class TeamCreate(TeamBase):
    pass

class Team(TeamBase):
    id: int
    members: List[User] = []

    class Config:
        orm_mode = True

# Update forward reference
Team.update_forward_refs()
