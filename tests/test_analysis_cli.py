"""Tests for analyze.py — end-to-end analysis pipeline (fully mocked)."""

import pytest
from unittest.mock import patch, MagicMock
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from src.db.models import create_tables
from src.db.dao import upsert_channel, upsert_video
from src.analysis.nlp import AlignmentResult, QuoteItem, set_client
from analyze import run_analysis


@pytest.fixture
def db_url(tmp_path):
    """Create a temporary SQLite database."""
    url = f"sqlite:///{tmp_path}/test.db"
    engine = create_engine(url)
    create_tables(engine)

    # Seed with a channel and videos
    with Session(engine) as session:
        upsert_channel(session, {
            "channel_id": "UC_test",
            "title": "Test Channel",
            "description": "Test",
            "subscriber_count": 1000,
            "video_count": 5,
        })
        upsert_video(session, {
            "video_id": "vid_A",
            "channel_id": "UC_test",
            "title": "Video A",
            "published_at": "2026-01-01",
            "transcript": [
                {"text": "Welcome to plant based nutrition", "start": 0.0, "duration": 10.0},
                {"text": "Today we discuss whole food diets", "start": 10.0, "duration": 10.0},
                {"text": "Studies show benefits of vegetables", "start": 20.0, "duration": 10.0},
            ],
        })
        upsert_video(session, {
            "video_id": "vid_B",
            "channel_id": "UC_test",
            "title": "Video B",
            "published_at": "2026-01-02",
            "transcript": None,  # No transcript
        })
        session.commit()

    return url


@pytest.fixture(autouse=True)
def reset_nlp_client():
    """Reset the NLP client after each test."""
    yield
    set_client(None)


class TestRunAnalysis:
    @patch.dict("os.environ", {"OPENAI_API_KEY": "FAKE_KEY"})
    @patch("analyze.get_embeddings")
    @patch("analyze.get_embedding")
    @patch("analyze.score_chunks")
    def test_full_pipeline(self, mock_score, mock_embed, mock_embeds, db_url):
        # Mock embeddings
        mock_embeds.return_value = [[0.1] * 1536]  # One chunk
        mock_embed.return_value = [0.1] * 1536  # Target embedding

        # Mock scoring
        mock_score.return_value = AlignmentResult(
            alignment_score=78,
            reasoning="Naturally discusses plant-based nutrition",
            quotes=[
                QuoteItem(text="plant based nutrition", timestamp="0:00"),
            ],
        )

        summary = run_analysis(
            channel_id="UC_test",
            topic="plant-based health",
            top_n=20,
            db_url=db_url,
        )

        assert summary["channel_id"] == "UC_test"
        assert summary["videos_processed"] >= 1
        assert summary["chunks_created"] >= 1
        assert summary["alignment_score"] == 78

    @patch.dict("os.environ", {"OPENAI_API_KEY": "FAKE_KEY"})
    def test_channel_not_found(self, db_url):
        summary = run_analysis(
            channel_id="UC_nonexistent",
            topic="plant-based health",
            top_n=20,
            db_url=db_url,
        )

        assert summary["alignment_score"] is None
        assert summary["videos_processed"] == 0

    @patch.dict("os.environ", {"OPENAI_API_KEY": "FAKE_KEY"})
    @patch("analyze.get_embeddings")
    @patch("analyze.get_embedding")
    @patch("analyze.score_chunks")
    def test_updates_channel_record(self, mock_score, mock_embed, mock_embeds, db_url):
        mock_embeds.return_value = [[0.1] * 1536]
        mock_embed.return_value = [0.1] * 1536
        mock_score.return_value = AlignmentResult(
            alignment_score=92,
            reasoning="Excellent alignment",
            quotes=[QuoteItem(text="Great quote", timestamp="1:00")],
        )

        run_analysis(
            channel_id="UC_test",
            topic="sustainability",
            top_n=20,
            db_url=db_url,
        )

        # Verify the DB was actually updated
        from src.db.models import Channel
        engine = create_engine(db_url)
        with Session(engine) as session:
            channel = session.get(Channel, "UC_test")
            assert channel.alignment_score == 92
            assert channel.alignment_quotes is not None
            assert len(channel.alignment_quotes) == 1
