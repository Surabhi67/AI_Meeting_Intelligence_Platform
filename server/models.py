from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    DateTime
)

from sqlalchemy.orm import (
    declarative_base,
    relationship
)

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    email = Column(
        String,
        unique=True,
        nullable=False
    )

    hashed_password = Column(
        String,
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    meetings = relationship(
        "Meeting",
        back_populates="owner"
    )

    access_entries = relationship(
        "MeetingAccess",
        back_populates="user"
    )


class Meeting(Base):
    __tablename__ = "meetings"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    owner_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    title = Column(
        String,
        nullable=False
    )

    audio_path = Column(
        String,
        unique=True,
        nullable=False
    )

    transcript_path = Column(
        String,
        unique=True
    )

    summary_path = Column(
        String,
        unique=True
    )

    status = Column(
        String,
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    owner = relationship(
        "User",
        back_populates="meetings"
    )

    access_entries = relationship(
        "MeetingAccess",
        back_populates="meeting"
    )


class MeetingAccess(Base):
    __tablename__ = "meeting_access"

    meeting_id = Column(
        Integer,
        ForeignKey("meetings.id"),
        primary_key=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        primary_key=True
    )

    permission = Column(
        String,
        nullable=False,
        default="viewer"
    )

    meeting = relationship(
        "Meeting",
        back_populates="access_entries"
    )

    user = relationship(
        "User",
        back_populates="access_entries"
    )