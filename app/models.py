from sqlalchemy import (
    Boolean, Column, ForeignKey, Integer, String, DateTime, Table,
    UniqueConstraint
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .database import Base

# Association table for Challenge and Tag many-to-many relationship
challenge_tag_association = Table(
    'challenge_tag_association', Base.metadata,
    Column('challenge_id', Integer, ForeignKey('challenges.id')),
    Column('tag_id', Integer, ForeignKey('tags.id'))
)

# Association table for Challenge self-referential many-to-many relationship (dependencies)
challenge_dependencies = Table(
    'challenge_dependencies', Base.metadata,
    Column('challenge_id', Integer, ForeignKey('challenges.id'), primary_key=True),
    Column('dependency_id', Integer, ForeignKey('challenges.id'), primary_key=True)
)

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
    points = Column(Integer, nullable=False)  # For static scoring
    flag = Column(String, nullable=False)
    is_visible = Column(Boolean, default=False, nullable=False)

    # Fields for dynamic scoring
    initial_points = Column(Integer, nullable=True)
    minimum_points = Column(Integer, nullable=True)
    decay_factor = Column(Integer, nullable=True)

    tags = relationship("Tag", secondary=challenge_tag_association, back_populates="challenges")
    solves = relationship("Solve", back_populates="challenge")
    
    # Self-referential relationship for dependencies
    dependencies = relationship(
        "Challenge",
        secondary=challenge_dependencies,
        primaryjoin=id == challenge_dependencies.c.challenge_id,
        secondaryjoin=id == challenge_dependencies.c.dependency_id,
        backref="dependent_challenges"
    )

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
