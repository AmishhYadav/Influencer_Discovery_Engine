"""Data Access Object — upsert helpers for channels, videos, and chunks."""

from typing import Optional
from sqlalchemy.orm import Session

from src.db.models import Channel, Video, TranscriptChunk


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
