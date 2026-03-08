"""Data Access Object — upsert helpers for channels, videos, and chunks."""

from typing import Optional
from sqlalchemy.orm import Session

from src.db.models import Channel, Video, TranscriptChunk, Briefing, Creator, ContentItem


# ── Channel ──────────────────────────────────────────────────────────────

def upsert_channel(session: Session, data: dict) -> Channel:
    """Insert or update a channel record.

    Parameters
    ----------
    data : dict with keys channel_id, title, description,
           subscriber_count, video_count
    """
    existing = session.get(Channel, data["channel_id"])
    if existing:
        existing.title = data.get("title", existing.title)
        existing.description = data.get("description", existing.description)
        existing.subscriber_count = data.get("subscriber_count", existing.subscriber_count)
        existing.video_count = data.get("video_count", existing.video_count)
        return existing

    channel = Channel(
        id=data["channel_id"],
        title=data["title"],
        description=data.get("description", ""),
        subscriber_count=data.get("subscriber_count", 0),
        video_count=data.get("video_count", 0),
    )
    session.add(channel)
    return channel


def update_channel_alignment(
    session: Session,
    channel_id: str,
    alignment_score: int,
    alignment_quotes: list[dict],
) -> Optional[Channel]:
    """Update the alignment score and quotes on a channel record."""
    channel = session.get(Channel, channel_id)
    if channel is None:
        return None
    channel.alignment_score = alignment_score
    channel.alignment_quotes = alignment_quotes
    return channel


# ── Video ────────────────────────────────────────────────────────────────

def upsert_video(session: Session, data: dict) -> Video:
    """Insert or update a video record.

    Parameters
    ----------
    data : dict with keys video_id, channel_id, title,
           published_at, transcript (list[dict] or None)
    """
    existing = session.get(Video, data["video_id"])
    if existing:
        existing.title = data.get("title", existing.title)
        existing.transcript = data.get("transcript", existing.transcript)
        return existing

    video = Video(
        id=data["video_id"],
        channel_id=data["channel_id"],
        title=data["title"],
        published_at=data.get("published_at", ""),
        transcript=data.get("transcript"),
    )
    session.add(video)
    return video


# ── Transcript Chunks ────────────────────────────────────────────────────

def upsert_chunk(session: Session, data: dict) -> TranscriptChunk:
    """Insert a transcript chunk.

    Parameters
    ----------
    data : dict with keys video_id, start_time, end_time, text, embedding
    """
    chunk = TranscriptChunk(
        video_id=data["video_id"],
        start_time=data["start_time"],
        end_time=data["end_time"],
        text=data["text"],
        embedding=data.get("embedding"),
    )
    session.add(chunk)
    return chunk


def get_top_chunks(
    session: Session,
    channel_id: str,
    target_embedding: list[float],
    limit: int = 20,
) -> list[TranscriptChunk]:
    """Return the top N most similar chunks for a channel.

    Because we store embeddings as JSON (for SQLite portability), this
    function computes cosine similarity in Python.  On a real Postgres
    deployment with pgvector, you would replace this with a native
    `<=>` operator query for performance.
    """
    # Get all chunks for the channel's videos
    video_ids = [
        v.id
        for v in session.query(Video.id).filter(Video.channel_id == channel_id).all()
    ]
    if not video_ids:
        return []

    chunks = (
        session.query(TranscriptChunk)
        .filter(TranscriptChunk.video_id.in_(video_ids))
        .filter(TranscriptChunk.embedding.isnot(None))
        .all()
    )

    if not chunks:
        return []

    # Compute cosine similarity in Python
    scored = []
    for chunk in chunks:
        sim = _cosine_similarity(target_embedding, chunk.embedding)
        scored.append((sim, chunk))

    scored.sort(key=lambda x: x[0], reverse=True)
    return [chunk for _, chunk in scored[:limit]]


def _cosine_similarity(a: list[float], b: list[float]) -> float:
    """Compute cosine similarity between two vectors."""
    import math

    dot = sum(x * y for x, y in zip(a, b))
    mag_a = math.sqrt(sum(x * x for x in a))
    mag_b = math.sqrt(sum(x * x for x in b))
    if mag_a == 0 or mag_b == 0:
        return 0.0
    return dot / (mag_a * mag_b)


# ── Briefings ────────────────────────────────────────────────────────────

def create_briefing(session: Session, channel_id: str) -> Briefing:
    """Create a new pending briefing record."""
    briefing = Briefing(channel_id=channel_id)
    session.add(briefing)
    session.flush()  # Populate the auto-generated id
    return briefing


def update_briefing(
    session: Session,
    briefing_id: str,
    content: str,
    status: str,
) -> Optional[Briefing]:
    """Update a briefing with content and status."""
    briefing = session.get(Briefing, briefing_id)
    if briefing is None:
        return None
    briefing.content = content
    briefing.status = status
    return briefing


def get_briefing(session: Session, briefing_id: str) -> Optional[Briefing]:
    """Retrieve a briefing by its ID."""
    return session.get(Briefing, briefing_id)


# ── Creators (multi-source) ─────────────────────────────────────────────

def upsert_creator(session: Session, data: dict) -> Creator:
    """Insert or update a creator record.

    Parameters
    ----------
    data : dict with keys name, platform, platform_id, and optionally
           profile_url, bio, follower_count
    """
    # Try to find by platform + platform_id first
    existing = None
    if data.get("platform_id"):
        existing = (
            session.query(Creator)
            .filter(
                Creator.platform == data["platform"],
                Creator.platform_id == data["platform_id"],
            )
            .first()
        )

    if existing:
        existing.name = data.get("name", existing.name)
        existing.profile_url = data.get("profile_url", existing.profile_url)
        existing.bio = data.get("bio", existing.bio)
        existing.follower_count = data.get("follower_count", existing.follower_count)
        return existing

    creator = Creator(
        name=data["name"],
        platform=data["platform"],
        platform_id=data.get("platform_id"),
        profile_url=data.get("profile_url"),
        bio=data.get("bio", ""),
        follower_count=data.get("follower_count", 0),
    )
    session.add(creator)
    session.flush()
    return creator


def update_creator_scores(
    session: Session,
    creator_id: str,
    *,
    credibility_score: Optional[float] = None,
    engagement_score: Optional[float] = None,
    reach_score: Optional[float] = None,
    alignment_score: Optional[float] = None,
    composite_score: Optional[float] = None,
) -> Optional[Creator]:
    """Update scoring dimensions on a creator record."""
    creator = session.get(Creator, creator_id)
    if creator is None:
        return None
    if credibility_score is not None:
        creator.credibility_score = credibility_score
    if engagement_score is not None:
        creator.engagement_score = engagement_score
    if reach_score is not None:
        creator.reach_score = reach_score
    if alignment_score is not None:
        creator.alignment_score = alignment_score
    if composite_score is not None:
        creator.composite_score = composite_score
    return creator


def get_creators_ranked(
    session: Session,
    *,
    platform: Optional[str] = None,
    min_score: Optional[float] = None,
    limit: int = 20,
    offset: int = 0,
) -> tuple[list[Creator], int]:
    """Return creators ranked by composite score with optional filters.

    Returns (list_of_creators, total_count).
    """
    from sqlalchemy import desc

    query = session.query(Creator)

    if platform:
        query = query.filter(Creator.platform == platform)
    if min_score is not None:
        query = query.filter(Creator.composite_score >= min_score)

    total = query.count()
    creators = (
        query
        .order_by(desc(Creator.composite_score))
        .offset(offset)
        .limit(limit)
        .all()
    )
    return creators, total


# ── Content Items ────────────────────────────────────────────────────────

def upsert_content_item(session: Session, data: dict) -> ContentItem:
    """Insert or update a content item.

    Parameters
    ----------
    data : dict with keys creator_id, source_type, title, text_content,
           url, published_at, engagement_metrics
    """
    # Deduplicate by URL if available
    existing = None
    if data.get("url"):
        existing = (
            session.query(ContentItem)
            .filter(ContentItem.url == data["url"])
            .first()
        )

    if existing:
        existing.title = data.get("title", existing.title)
        existing.text_content = data.get("text_content", existing.text_content)
        existing.engagement_metrics = data.get(
            "engagement_metrics", existing.engagement_metrics
        )
        return existing

    item = ContentItem(
        creator_id=data["creator_id"],
        source_type=data["source_type"],
        title=data.get("title", ""),
        text_content=data.get("text_content", ""),
        url=data.get("url"),
        published_at=data.get("published_at", ""),
        engagement_metrics=data.get("engagement_metrics"),
    )
    session.add(item)
    session.flush()
    return item


def get_content_items(
    session: Session,
    creator_id: str,
    limit: int = 50,
) -> list[ContentItem]:
    """Return content items for a creator, newest first."""
    return (
        session.query(ContentItem)
        .filter(ContentItem.creator_id == creator_id)
        .order_by(ContentItem.created_at.desc())
        .limit(limit)
        .all()
    )
