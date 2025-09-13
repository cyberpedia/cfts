from pydantic import BaseModel
from typing import List, Optional, Any
from datetime import datetime

# Base Schemas
class FlagSubmission(BaseModel): flag: str
class TagBase(BaseModel): name: str
class ChallengeBase(BaseModel):
    name: str; description: str; points: int
    initial_points: Optional[int] = None; minimum_points: Optional[int] = None
    decay_factor: Optional[int] = None; is_visible: bool = False
class SolveBase(BaseModel): user_id: int; challenge_id: int; team_id: Optional[int] = None
class TeamBase(BaseModel): name: str
class UserBase(BaseModel): username: str; email: str
class CTFSettingBase(BaseModel):
    event_title: str; ui_theme: str; event_start_time: Optional[datetime] = None
    event_end_time: Optional[datetime] = None; allow_registrations: bool
    allow_teams: bool; scoring_mode: str
class BadgeBase(BaseModel): name: str; description: str; icon_url: Optional[str] = None
class NotificationBase(BaseModel): title: str; body: str
class DynamicChallengeInstanceBase(BaseModel):
    ip_address: str
    port: int
    expires_at: datetime

# Create & Update Schemas
class TagCreate(TagBase): pass
class ChallengeCreate(ChallengeBase): flag: str
class SolveCreate(SolveBase): pass
class TeamCreate(TeamBase): pass
class UserCreate(UserBase): password: str
class CTFSettingUpdate(BaseModel):
    event_title: Optional[str] = None; ui_theme: Optional[str] = None
    event_start_time: Optional[datetime] = None; event_end_time: Optional[datetime] = None
    allow_registrations: Optional[bool] = None; allow_teams: Optional[bool] = None
    scoring_mode: Optional[str] = None
class BadgeCreate(BadgeBase): pass
class DynamicChallengeInstanceCreate(DynamicChallengeInstanceBase):
    user_id: int
    challenge_id: int
    container_id: str

# Response Schemas
class Badge(BadgeBase): id: int; class Config: orm_mode = True
class UserBadge(BaseModel): awarded_at: datetime; badge: Badge; class Config: orm_mode = True
class _User(BaseModel): id: int; username: str; score: int; class Config: orm_mode = True
class _Team(BaseModel): id: int; name: str; class Config: orm_mode = True
class Tag(TagBase): id: int; class Config: orm_mode = True
class Solve(SolveBase): id: int; created_at: datetime; user: _User; team: Optional[_Team] = None; class Config: orm_mode = True
class ChallengeList(BaseModel): id: int; name: str; points: int; is_locked: bool = True; class Config: orm_mode = True
class ChallengeDetail(ChallengeBase): id: int; is_locked: bool = True; tags: List[Tag] = []; solves: List[Solve] = []; class Config: orm_mode = True
class Team(TeamBase): id: int; members: List[_User] = []; solves: List[Solve] = []; class Config: orm_mode = True
class User(UserBase): id: int; score: int; is_staff: bool; is_active: bool; team_id: Optional[int] = None; solves: List[Solve] = []; badges: List[UserBadge] = []; class Config: orm_mode = True
class LeaderboardEntry(BaseModel): rank: int; team_id: int; team_name: str; total_score: int; last_submission: Optional[datetime] = None
class CTFSetting(CTFSettingBase): id: int; class Config: orm_mode = True
class PublicCTFSetting(BaseModel): event_title: str; ui_theme: str; event_start_time: Optional[datetime] = None; event_end_time: Optional[datetime] = None; class Config: orm_mode = True
class Notification(NotificationBase): id: int; user_id: int; is_read: bool; created_at: datetime; class Config: orm_mode = True
class _AuditLogUser(BaseModel): id: int; username: str; class Config: orm_mode = True
class AuditLog(BaseModel): id: int; user: Optional[_AuditLogUser] = None; action: str; details: Optional[Any] = None; timestamp: datetime; class Config: orm_mode = True
class DynamicChallengeInstance(DynamicChallengeInstanceBase):
    id: int
    user_id: int
    challenge_id: int
    class Config: orm_mode = True

# Update forward references
Team.update_forward_refs()
User.update_forward_refs()
