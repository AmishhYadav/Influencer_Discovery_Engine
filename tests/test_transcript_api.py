"""Tests for src.ingestion.transcripts — all transcript calls are mocked."""

import pytest
from unittest.mock import patch, MagicMock

from src.ingestion.transcripts import fetch_transcript


SAMPLE_RAW_DATA = [
    {"text": "Welcome to the show", "start": 0.0, "duration": 3.5},
    {"text": "Today we discuss plants", "start": 3.5, "duration": 4.0},
    {"text": "[Music]", "start": 7.5, "duration": 2.0},
]


def _make_fetched(raw_data):
    """Create a mock FetchedTranscript that returns raw_data."""
    mock = MagicMock()
    mock.to_raw_data.return_value = raw_data
    return mock


class TestFetchTranscript:
    @patch("src.ingestion.transcripts._api")
    def test_returns_transcript_list(self, mock_api):
        mock_api.fetch.return_value = _make_fetched(SAMPLE_RAW_DATA)

        result = fetch_transcript("vid_001")

        assert result is not None
        assert len(result) == 3
        assert result[0]["text"] == "Welcome to the show"
        mock_api.fetch.assert_called_once_with("vid_001")

    @patch("src.ingestion.transcripts._api")
    def test_returns_none_when_transcripts_disabled(self, mock_api):
        from youtube_transcript_api._errors import TranscriptsDisabled

        mock_api.fetch.side_effect = TranscriptsDisabled("vid_002")

        result = fetch_transcript("vid_002")

        assert result is None

    @patch("src.ingestion.transcripts._api")
    def test_returns_none_when_no_transcript_found(self, mock_api):
        from youtube_transcript_api._errors import NoTranscriptFound

        mock_api.fetch.side_effect = NoTranscriptFound(
            "vid_003", ["en"], "No transcript found"
        )

        result = fetch_transcript("vid_003")

        assert result is None

    @patch("src.ingestion.transcripts._api")
    def test_returns_none_when_video_unavailable(self, mock_api):
        from youtube_transcript_api._errors import VideoUnavailable

        mock_api.fetch.side_effect = VideoUnavailable("vid_004")

        result = fetch_transcript("vid_004")

        assert result is None

    @patch("src.ingestion.transcripts._api")
    def test_returns_none_on_unexpected_error(self, mock_api):
        mock_api.fetch.side_effect = RuntimeError("Something broke")

        result = fetch_transcript("vid_005")

        assert result is None
