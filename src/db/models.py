"""SQLAlchemy models for the Influencer Discovery Engine."""

from datetime import datetime

from sqlalchemy import (
    Column,
    String,
    Integer,
    Text,
    DateTime,
    ForeignKey,
    create_engine,
)
from sqlalchemy.types import JSON
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Channel(Base):
    """A YouTube channel discovered through search."""

    __tablename__ = "channels"

    id = Column(String, primary_key=True, doc="YouTube channel ID")
    title = Column(String, nullable=False)
    description = Column(Text, default="")
    subscriber_count = Column(Integer, default=0)
    video_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    videos = relationship("Video", back_populates="channel", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Channel id={self.id!r} title={self.title!r}>"


class Video(Base):
    """A YouTube video with its transcript stored as JSONB."""

    __tablename__ = "videos"

    id = Column(String, primary_key=True, doc="YouTube video ID")
    channel_id = Column(String, ForeignKey("channels.id"), nullable=False)
    title = Column(String, nullable=False)
    published_at = Column(String, default="")
    transcript = Column(JSON, nullable=True, doc="Cleaned transcript as JSON array of {text, start, duration}")
    created_at = Column(DateTime, default=datetime.utcnow)

    channel = relationship("Channel", back_populates="videos")

    def __repr__(self):
        return f"<Video id={self.id!r} title={self.title!r}>"


def create_tables(engine):
    """Create all tables (idempotent)."""
    Base.metadata.create_all(engine)
