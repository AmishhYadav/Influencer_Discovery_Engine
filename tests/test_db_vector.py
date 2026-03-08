"""Tests for TranscriptChunk model and vector DAO helpers — in-memory SQLite."""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from src.db.models import Base, Channel, Video, TranscriptChunk, create_tables
from src.db.dao import (
    upsert_channel,
    upsert_video,
    upsert_chunk,
    get_top_chunks,
    update_channel_alignment,
)


@pytest.fixture
def session():
    engine = create_engine("sqlite:///:memory:", echo=False)
    create_tables(engine)
    with Session(engine) as s:
        yield s


@pytest.fixture
def seeded_session(session):
    """Session pre-populated with a channel, video, and chunks."""
    upsert_channel(session, {
        "channel_id": "UC_abc",
        "title": "Dr. Green",
        "description": "Health",
        "subscriber_count": 50000,
        "video_count": 100,
    })
    upsert_video(session, {
        "video_id": "vid_001",
        "channel_id": "UC_abc",
        "title": "Plant Health",
        "published_at": "2026-01-01",
        "transcript": [{"text": "hi", "start": 0.0, "duration": 1.0}],
    })
    session.commit()
    return session


class TestTranscriptChunkModel:
    def test_table_created(self, session):
        assert session.query(TranscriptChunk).count() == 0

    def test_upsert_chunk(self, seeded_session):
        chunk = upsert_chunk(seeded_session, {
            "video_id": "vid_001",
            "start_time": 0.0,
            "end_time": 60.0,
            "text": "Welcome to the show",
            "embedding": [0.1] * 1536,
        })
        seeded_session.commit()

        assert chunk.id is not None
        assert chunk.video_id == "vid_001"
        assert len(chunk.embedding) == 1536
        assert seeded_session.query(TranscriptChunk).count() == 1


class TestGetTopChunks:
    def test_returns_sorted_by_similarity(self, seeded_session):
        # Insert two chunks with known embeddings
        # Chunk A: embedding pointing in same direction as target
        emb_a = [1.0, 0.0, 0.0] + [0.0] * 1533
        upsert_chunk(seeded_session, {
            "video_id": "vid_001",
            "start_time": 0.0,
            "end_time": 30.0,
            "text": "Highly aligned content",
            "embedding": emb_a,
        })
        # Chunk B: orthogonal direction
        emb_b = [0.0, 1.0, 0.0] + [0.0] * 1533
        upsert_chunk(seeded_session, {
            "video_id": "vid_001",
            "start_time": 30.0,
            "end_time": 60.0,
            "text": "Unrelated content",
            "embedding": emb_b,
        })
        seeded_session.commit()

        # Target embedding: same direction as Chunk A
        target = [1.0, 0.0, 0.0] + [0.0] * 1533

        results = get_top_chunks(seeded_session, "UC_abc", target, limit=2)

        assert len(results) == 2
        assert results[0].text == "Highly aligned content"
        assert results[1].text == "Unrelated content"

    def test_respects_limit(self, seeded_session):
        for i in range(5):
            emb = [0.0] * 1536
            emb[i] = 1.0
            upsert_chunk(seeded_session, {
                "video_id": "vid_001",
                "start_time": float(i * 10),
                "end_time": float((i + 1) * 10),
                "text": f"Chunk {i}",
                "embedding": emb,
            })
        seeded_session.commit()

        target = [1.0] + [0.0] * 1535
        results = get_top_chunks(seeded_session, "UC_abc", target, limit=3)
        assert len(results) == 3

    def test_returns_empty_for_unknown_channel(self, seeded_session):
        results = get_top_chunks(seeded_session, "UC_unknown", [0.1] * 1536)
        assert results == []


class TestUpdateChannelAlignment:
    def test_updates_score_and_quotes(self, seeded_session):
        quotes = [{"text": "Great quote", "timestamp": "1:23"}]
        result = update_channel_alignment(seeded_session, "UC_abc", 85, quotes)
        seeded_session.commit()

        assert result is not None
        assert result.alignment_score == 85
        assert result.alignment_quotes == quotes

    def test_returns_none_for_unknown_channel(self, seeded_session):
        result = update_channel_alignment(seeded_session, "UC_nope", 50, [])
        assert result is None
