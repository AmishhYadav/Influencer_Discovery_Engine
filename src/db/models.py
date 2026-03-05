"""SQLAlchemy models for the Influencer Discovery Engine."""

import uuid
from datetime import datetime

from sqlalchemy import (
    Column,
    String,
    Integer,
    Float,
    Text,
    DateTime,
    ForeignKey,
    create_engine,
    event,
    text,
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
    alignment_score = Column(Integer, nullable=True, doc="0-100 alignment score from LLM")
    alignment_quotes = Column(JSON, nullable=True, doc="Quotes justifying the score")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    videos = relationship("Video", back_populates="channel", cascade="all, delete-orphan")
    briefings = relationship("Briefing", back_populates="channel", cascade="all, delete-orphan")

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


class TranscriptChunk(Base):
    """A chunk of transcript text with its embedding vector."""

    __tablename__ = "transcript_chunks"

    id = Column(Integer, primary_key=True, autoincrement=True)
    video_id = Column(String, ForeignKey("videos.id"), nullable=False)
    start_time = Column(Float, nullable=False)
    end_time = Column(Float, nullable=False)
    text = Column(Text, nullable=False)
    # Embedding stored as JSON array for portability.
    # On Postgres with pgvector, use Vector(1536) type instead.
    embedding = Column(JSON, nullable=True, doc="1536-dim embedding vector")

    video = relationship("Video")

    def __repr__(self):
        return f"<TranscriptChunk id={self.id} video_id={self.video_id!r}>"


class Briefing(Base):
    """An async-generated engagement briefing for a channel."""

    __tablename__ = "briefings"

    id = Column(String, primary_key=True, default=lambda: uuid.uuid4().hex)
    channel_id = Column(String, ForeignKey("channels.id"), nullable=False)
    content = Column(Text, nullable=True, doc="Generated markdown briefing")
    status = Column(String, default="pending", doc="pending | completed | failed")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    channel = relationship("Channel", back_populates="briefings")

    def __repr__(self):
        return f"<Briefing id={self.id!r} status={self.status!r}>"


def create_tables(engine):
    """Create all tables (idempotent).

    On PostgreSQL, also enables the pgvector extension.
    """
    dialect = engine.dialect.name
    if dialect == "postgresql":
        with engine.connect() as conn:
            conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
            conn.commit()

    Base.metadata.create_all(engine)
