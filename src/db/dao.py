"""Data Access Object — upsert helpers for channels and videos."""

from sqlalchemy.orm import Session

from src.db.models import Channel, Video


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
