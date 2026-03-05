"""Tests for ingest.py — end-to-end pipeline orchestration (fully mocked)."""

import pytest
from unittest.mock import patch, MagicMock

from ingest import run_pipeline


MOCK_CHANNELS = [
    {
        "channel_id": "UC_abc123",
        "title": "Dr. Green",
        "description": "Health",
        "subscriber_count": 50000,
        "video_count": 200,
    },
]

MOCK_VIDEOS = [
    {
        "video_id": "vid_001",
        "title": "Why Plants Matter",
        "published_at": "2026-01-15T00:00:00Z",
    },
    {
        "video_id": "vid_002",
        "title": "Sustainability 101",
        "published_at": "2026-01-10T00:00:00Z",
    },
]

MOCK_RAW_TRANSCRIPT = [
    {"text": "Welcome", "start": 0.0, "duration": 3.0},
    {"text": "[Music]", "start": 3.0, "duration": 2.0},
    {"text": "Today we discuss plants", "start": 5.0, "duration": 5.0},
]


class TestRunPipeline:
    @patch.dict("os.environ", {"YOUTUBE_API_KEY": "FAKE_KEY"})
    @patch("ingest.YouTubeDataAPI")
    @patch("ingest.fetch_transcript")
    def test_full_pipeline_success(self, mock_fetch, mock_yt_cls):
        """Pipeline discovers channels, fetches videos, cleans transcripts, stores in DB."""
        # Mock YouTube API
        mock_yt = MagicMock()
        mock_yt_cls.return_value = mock_yt
        mock_yt.search_channels.return_value = MOCK_CHANNELS
        mock_yt.get_latest_videos.return_value = MOCK_VIDEOS

        # Mock transcripts — first succeeds, second fails
        mock_fetch.side_effect = [MOCK_RAW_TRANSCRIPT, None]

        summary = run_pipeline(
            query="plant based health",
            max_channels=1,
            videos_per_channel=5,
            db_url="sqlite:///:memory:",
        )

        assert summary["channels_found"] == 1
        assert summary["videos_fetched"] == 2
        assert summary["transcripts_fetched"] == 1
        assert summary["transcripts_skipped"] == 1

    @patch.dict("os.environ", {"YOUTUBE_API_KEY": "FAKE_KEY"})
    @patch("ingest.YouTubeDataAPI")
    @patch("ingest.fetch_transcript")
    def test_no_channels_found(self, mock_fetch, mock_yt_cls):
        """Pipeline handles zero search results gracefully."""
        mock_yt = MagicMock()
        mock_yt_cls.return_value = mock_yt
        mock_yt.search_channels.return_value = []

        summary = run_pipeline(
            query="nonexistent topic",
            max_channels=5,
            videos_per_channel=25,
            db_url="sqlite:///:memory:",
        )

        assert summary["channels_found"] == 0
        assert summary["videos_fetched"] == 0
        mock_fetch.assert_not_called()

    @patch.dict("os.environ", {"YOUTUBE_API_KEY": "FAKE_KEY"})
    @patch("ingest.YouTubeDataAPI")
    @patch("ingest.fetch_transcript")
    def test_all_transcripts_skipped(self, mock_fetch, mock_yt_cls):
        """Pipeline continues if all transcripts are unavailable."""
        mock_yt = MagicMock()
        mock_yt_cls.return_value = mock_yt
        mock_yt.search_channels.return_value = MOCK_CHANNELS
        mock_yt.get_latest_videos.return_value = MOCK_VIDEOS

        mock_fetch.return_value = None  # All fail

        summary = run_pipeline(
            query="plant based health",
            max_channels=1,
            videos_per_channel=5,
            db_url="sqlite:///:memory:",
        )

        assert summary["transcripts_fetched"] == 0
        assert summary["transcripts_skipped"] == 2
