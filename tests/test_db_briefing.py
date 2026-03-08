"""Tests for Briefing model and DAO helpers."""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from src.db.models import create_tables
from src.db.dao import upsert_channel, create_briefing, update_briefing, get_briefing


@pytest.fixture
def session():
    engine = create_engine("sqlite:///:memory:", echo=False)
    create_tables(engine)
    with Session(engine) as s:
        yield s


@pytest.fixture
def seeded_session(session):
    upsert_channel(session, {
        "channel_id": "UC_brief",
        "title": "Briefing Test Channel",
        "description": "Test",
        "subscriber_count": 10000,
        "video_count": 50,
    })
    session.commit()
    return session


class TestCreateBriefing:
    def test_creates_pending_briefing(self, seeded_session):
        briefing = create_briefing(seeded_session, "UC_brief")
        seeded_session.commit()

        assert briefing.id is not None
        assert briefing.channel_id == "UC_brief"
        assert briefing.status == "pending"
        assert briefing.content is None

    def test_briefing_has_unique_id(self, seeded_session):
        b1 = create_briefing(seeded_session, "UC_brief")
        b2 = create_briefing(seeded_session, "UC_brief")
        seeded_session.commit()

        assert b1.id != b2.id


class TestUpdateBriefing:
    def test_updates_content_and_status(self, seeded_session):
        briefing = create_briefing(seeded_session, "UC_brief")
        seeded_session.commit()

        result = update_briefing(
            seeded_session, briefing.id, "# Great Briefing\nContent here", "completed"
        )
        seeded_session.commit()

        assert result.content == "# Great Briefing\nContent here"
        assert result.status == "completed"

    def test_returns_none_for_unknown_id(self, seeded_session):
        result = update_briefing(seeded_session, "nonexistent", "content", "completed")
        assert result is None


class TestGetBriefing:
    def test_retrieves_by_id(self, seeded_session):
        briefing = create_briefing(seeded_session, "UC_brief")
        seeded_session.commit()

        result = get_briefing(seeded_session, briefing.id)
        assert result is not None
        assert result.channel_id == "UC_brief"

    def test_returns_none_for_unknown(self, seeded_session):
        result = get_briefing(seeded_session, "nope")
        assert result is None
