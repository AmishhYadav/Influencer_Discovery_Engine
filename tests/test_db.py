"""Tests for src.db.models and src.db.dao — uses in-memory SQLite."""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from src.db.models import Base, Channel, Video, create_tables
from src.db.dao import upsert_channel, upsert_video


@pytest.fixture
def session():
    """Create an in-memory SQLite database and return a session."""
    engine = create_engine("sqlite:///:memory:", echo=False)
    create_tables(engine)
    with Session(engine) as s:
        yield s


SAMPLE_CHANNEL = {
    "channel_id": "UC_abc123",
    "title": "Dr. Green",
    "description": "Health and wellness",
    "subscriber_count": 50000,
    "video_count": 200,
}

SAMPLE_VIDEO = {
    "video_id": "vid_001",
    "channel_id": "UC_abc123",
    "title": "Why Plants Matter",
    "published_at": "2026-01-15T00:00:00Z",
    "transcript": [
        {"text": "Welcome", "start": 0.0, "duration": 3.0},
        {"text": "Today we discuss plants", "start": 3.0, "duration": 5.0},
    ],
}


class TestCreateTables:
    def test_tables_created(self, session):
        """Verify tables exist after create_tables."""
        assert session.query(Channel).count() == 0
        assert session.query(Video).count() == 0


class TestUpsertChannel:
    def test_insert_new_channel(self, session):
        ch = upsert_channel(session, SAMPLE_CHANNEL)
        session.commit()

        assert ch.id == "UC_abc123"
        assert ch.title == "Dr. Green"
        assert ch.subscriber_count == 50000
        assert session.query(Channel).count() == 1

    def test_update_existing_channel(self, session):
        upsert_channel(session, SAMPLE_CHANNEL)
        session.commit()

        updated = {**SAMPLE_CHANNEL, "subscriber_count": 75000}
        ch = upsert_channel(session, updated)
        session.commit()

        assert ch.subscriber_count == 75000
        assert session.query(Channel).count() == 1


class TestUpsertVideo:
    def test_insert_new_video(self, session):
        # Must insert channel first due to FK
        upsert_channel(session, SAMPLE_CHANNEL)
        session.commit()

        vid = upsert_video(session, SAMPLE_VIDEO)
        session.commit()

        assert vid.id == "vid_001"
        assert vid.transcript is not None
        assert len(vid.transcript) == 2
        assert session.query(Video).count() == 1

    def test_insert_video_with_none_transcript(self, session):
        upsert_channel(session, SAMPLE_CHANNEL)
        session.commit()

        data = {**SAMPLE_VIDEO, "transcript": None}
        vid = upsert_video(session, data)
        session.commit()

        assert vid.transcript is None

    def test_update_existing_video(self, session):
        upsert_channel(session, SAMPLE_CHANNEL)
        upsert_video(session, SAMPLE_VIDEO)
        session.commit()

        updated_transcript = [{"text": "Updated", "start": 0.0, "duration": 1.0}]
        vid = upsert_video(session, {**SAMPLE_VIDEO, "transcript": updated_transcript})
        session.commit()

        assert len(vid.transcript) == 1
        assert vid.transcript[0]["text"] == "Updated"
        assert session.query(Video).count() == 1


class TestRelationships:
    def test_channel_has_videos(self, session):
        upsert_channel(session, SAMPLE_CHANNEL)
        upsert_video(session, SAMPLE_VIDEO)
        upsert_video(session, {
            **SAMPLE_VIDEO,
            "video_id": "vid_002",
            "title": "Second Video",
        })
        session.commit()

        ch = session.get(Channel, "UC_abc123")
        assert len(ch.videos) == 2
