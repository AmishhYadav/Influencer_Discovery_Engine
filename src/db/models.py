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


class Creator(Base):
    """A platform-agnostic creator/author discovered from any source.

    This is the core entity that unifies YouTube channels, blog authors,
    social media profiles, and academic researchers into a single
    scorable record.
    """

    __tablename__ = "creators"

    id = Column(String, primary_key=True, default=lambda: uuid.uuid4().hex)
    name = Column(String, nullable=False)
    platform = Column(
        String, nullable=False,
        doc="Source platform: youtube | blog | twitter | instagram | academic",
    )
    platform_id = Column(
        String, nullable=True,
        doc="Platform-specific identifier (channel ID, URL, handle, author ID)",
    )
    profile_url = Column(String, nullable=True)
    bio = Column(Text, default="")
    follower_count = Column(Integer, default=0)

    # ── Scoring dimensions ───────────────────────────────────────────
    credibility_score = Column(Float, nullable=True, doc="0-100 credibility score")
    engagement_score = Column(Float, nullable=True, doc="0-100 engagement score")
    reach_score = Column(Float, nullable=True, doc="0-100 audience reach score")
    alignment_score = Column(Float, nullable=True, doc="0-100 values alignment score")
    composite_score = Column(Float, nullable=True, doc="Weighted composite score")

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    content_items = relationship(
        "ContentItem", back_populates="creator", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Creator id={self.id!r} name={self.name!r} platform={self.platform!r}>"


class ContentItem(Base):
    """A single piece of content from any source.

    Blog posts, tweets, academic papers, etc. are all stored here.
    """

    __tablename__ = "content_items"

    id = Column(String, primary_key=True, default=lambda: uuid.uuid4().hex)
    creator_id = Column(String, ForeignKey("creators.id"), nullable=False)
    source_type = Column(
        String, nullable=False,
        doc="Content type: blog_post | tweet | paper | instagram_post",
    )
    title = Column(String, default="")
    text_content = Column(Text, default="")
    url = Column(String, nullable=True)
    published_at = Column(String, default="")
    engagement_metrics = Column(
        JSON, nullable=True,
        doc="Platform-specific engagement data (likes, shares, citations, etc.)",
    )
    created_at = Column(DateTime, default=datetime.utcnow)

    creator = relationship("Creator", back_populates="content_items")

    def __repr__(self):
        return f"<ContentItem id={self.id!r} type={self.source_type!r}>"


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
