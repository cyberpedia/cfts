from sqlalchemy import (
    Boolean, Column, ForeignKey, Integer, String, DateTime, Table,
    UniqueConstraint, CheckConstraint, JSON
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .database import Base

# Association tables
challenge_tag_association = Table('challenge_tag_association', Base.metadata,
    Column('challenge_id', Integer, ForeignKey('challenges.id')),
    Column('tag_id', Integer, ForeignKey('tags.id')))

challenge_dependencies = Table('challenge_dependencies', Base.metadata,
    Column('challenge_id', Integer, ForeignKey('challenges.id'), primary_key=True),
    Column('dependency_id', Integer, ForeignKey('challenges.id'), primary_key=True))

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    score = Column(Integer, default=0, nullable=False)
    is_staff = Column(Boolean, default=False, nullable=False)
    is_active = Column(Boolean, default=False, nullable=False)
    verification_token = Column(String, unique=True, nullable=True)
    team_id = Column(Integer, ForeignKey("teams.id"))
    team = relationship("Team", back_populates="members")
    solves = relationship("Solve", back_populates="user")
    badges = relationship("UserBadge", back_populates="user")
    notifications = relationship("Notification", back_populates="user")
    audit_logs = relationship("AuditLog", back_populates="user")

class Team(Base):
    __tablename__ = "teams"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    members = relationship("User", back_populates="team")
    solves = relationship("Solve", back_populates="team")

class Challenge(Base):
    __tablename__ = "challenges"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    points = Column(Integer, nullable=False)
    flag = Column(String, nullable=False)
    is_visible = Column(Boolean, default=False, nullable=False)
    initial_points = Column(Integer, nullable=True)
    minimum_points = Column(Integer, nullable=True)
    decay_factor = Column(Integer, nullable=True)
    tags = relationship("Tag", secondary=challenge_tag_association, back_populates="challenges")
    solves = relationship("Solve", back_populates="challenge")
    dependencies = relationship("Challenge", secondary=challenge_dependencies,
        primaryjoin=id == challenge_dependencies.c.challenge_id,
        secondaryjoin=id == challenge_dependencies.c.dependency_id,
        backref="dependent_challenges")

class Tag(Base):
    __tablename__ = "tags"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    challenges = relationship("Challenge", secondary=challenge_tag_association, back_populates="tags")

class Solve(Base):
    __tablename__ = "solves"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    challenge_id = Column(Integer, ForeignKey("challenges.id"), nullable=False)
    team_id = Column(Integer, ForeignKey("teams.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    user = relationship("User", back_populates="solves")
    challenge = relationship("Challenge", back_populates="solves")
    team = relationship("Team", back_populates="solves")
    __table_args__ = (UniqueConstraint('user_id', 'challenge_id', name='_user_challenge_uc'),)

class CTFSetting(Base):
    __tablename__ = "ctf_settings"
    id = Column(Integer, primary_key=True, default=1)
    event_title = Column(String, default="CTF Platform")
    ui_theme = Column(String, default="dark")
    event_start_time = Column(DateTime(timezone=True), nullable=True)
    event_end_time = Column(DateTime(timezone=True), nullable=True)
    allow_registrations = Column(Boolean, default=True)
    allow_teams = Column(Boolean, default=True)
    scoring_mode = Column(String, default="static")
    __table_args__ = (CheckConstraint('id = 1', name='singleton_check'),)

class Badge(Base):
    __tablename__ = "badges"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=False)
    icon_url = Column(String, nullable=True)

class UserBadge(Base):
    __tablename__ = "user_badges"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    badge_id = Column(Integer, ForeignKey("badges.id"), nullable=False)
    awarded_at = Column(DateTime(timezone=True), server_default=func.now())
    user = relationship("User", back_populates="badges")
    badge = relationship("Badge")
    __table_args__ = (UniqueConstraint('user_id', 'badge_id', name='_user_badge_uc'),)

class Notification(Base):
    __tablename__ = "notifications"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=False)
    body = Column(String, nullable=False)
    is_read = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    user = relationship("User", back_populates="notifications")

class AuditLog(Base):
    __tablename__ = "audit_logs"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    action = Column(String, nullable=False, index=True)
    details = Column(JSON, nullable=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    user = relationship("User", back_populates="audit_logs")
