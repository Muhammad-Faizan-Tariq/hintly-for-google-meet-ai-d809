import uuid
from datetime import datetime
from typing import Optional
from sqlalchemy import String, DateTime, Float, ForeignKey, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from pydantic import BaseModel


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"
    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    google_sub: Mapped[str] = mapped_column(String, unique=True, index=True)
    email: Mapped[str] = mapped_column(String)
    name: Mapped[str] = mapped_column(String)
    avatar_url: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    plan: Mapped[str] = mapped_column(String, default="free")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class Meeting(Base):
    __tablename__ = "meetings"
    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id: Mapped[str] = mapped_column(String, ForeignKey("users.id"))
    google_meet_id: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    title: Mapped[str] = mapped_column(String)
    started_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    ended_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    summary: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    action_items_json: Mapped[Optional[str]] = mapped_column(Text, nullable=True)


class Transcript(Base):
    __tablename__ = "transcripts"
    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    meeting_id: Mapped[str] = mapped_column(String, ForeignKey("meetings.id"))
    speaker: Mapped[str] = mapped_column(String)
    text: Mapped[str] = mapped_column(Text)
    ts: Mapped[float] = mapped_column(Float)


class Hint(Base):
    __tablename__ = "hints"
    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    meeting_id: Mapped[str] = mapped_column(String, ForeignKey("meetings.id"))
    type: Mapped[str] = mapped_column(String)
    text: Mapped[str] = mapped_column(Text)
    confidence: Mapped[float] = mapped_column(Float)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


# ── Pydantic schemas ──────────────────────────────────────────────────────────

class UserOut(BaseModel):
    id: str
    email: str
    name: str
    avatar_url: Optional[str]
    plan: str
    model_config = {"from_attributes": True}


class MeetingCreate(BaseModel):
    meeting_id: Optional[str] = None
    title: str


class TranscriptChunk(BaseModel):
    speaker: str
    text: str
    ts: float


class HintOut(BaseModel):
    id: str
    type: str
    text: str
    confidence: float
    created_at: datetime
    model_config = {"from_attributes": True}


class MeetingOut(BaseModel):
    id: str
    title: str
    started_at: datetime
    ended_at: Optional[datetime]
    summary: Optional[str]
    action_items_json: Optional[str]
    model_config = {"from_attributes": True}
