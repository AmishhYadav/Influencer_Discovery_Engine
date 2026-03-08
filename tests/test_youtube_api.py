"""Tests for src.ingestion.youtube_api — all API calls are mocked."""

import pytest
from unittest.mock import MagicMock, patch

from src.ingestion.youtube_api import YouTubeDataAPI


# ── Fixtures ─────────────────────────────────────────────────────────────

@pytest.fixture
def mock_service():
    """Return a fully mocked googleapiclient service object."""
    with patch("src.ingestion.youtube_api.build") as mock_build:
        service = MagicMock()
        mock_build.return_value = service
        yield service


@pytest.fixture
def api(mock_service):
    """YouTubeDataAPI instance backed by mocked service."""
    return YouTubeDataAPI(api_key="FAKE_KEY")


# ── search_channels ──────────────────────────────────────────────────────

class TestSearchChannels:
    def test_returns_channel_list(self, api, mock_service):
        # Mock search().list().execute()
        mock_service.search().list().execute.return_value = {
            "items": [
                {"snippet": {"channelId": "UC_abc123"}},
                {"snippet": {"channelId": "UC_def456"}},
            ]
        }
        # Mock channels().list().execute()
        mock_service.channels().list().execute.return_value = {
            "items": [
                {
                    "id": "UC_abc123",
                    "snippet": {"title": "Dr. Green", "description": "Health"},
                    "statistics": {"subscriberCount": "50000", "videoCount": "200"},
                },
                {
                    "id": "UC_def456",
                    "snippet": {"title": "Chef Plant", "description": "Cooking"},
                    "statistics": {"subscriberCount": "30000", "videoCount": "150"},
                },
            ]
        }

        results = api.search_channels("plant based health", max_results=2)

        assert len(results) == 2
        assert results[0]["channel_id"] == "UC_abc123"
        assert results[0]["subscriber_count"] == 50000
        assert results[1]["title"] == "Chef Plant"

    def test_returns_empty_list_when_no_results(self, api, mock_service):
        mock_service.search().list().execute.return_value = {"items": []}

        results = api.search_channels("nonexistent query")
        assert results == []


# ── get_channel_metadata ─────────────────────────────────────────────────

class TestGetChannelMetadata:
    def test_returns_metadata(self, api, mock_service):
        mock_service.channels().list().execute.return_value = {
            "items": [
                {
                    "id": "UC_abc123",
                    "snippet": {"title": "Dr. Green", "description": "Health"},
                    "statistics": {"subscriberCount": "50000", "videoCount": "200"},
                }
            ]
        }

        result = api.get_channel_metadata("UC_abc123")

        assert result is not None
        assert result["channel_id"] == "UC_abc123"
        assert result["subscriber_count"] == 50000

    def test_returns_none_for_unknown_channel(self, api, mock_service):
        mock_service.channels().list().execute.return_value = {"items": []}

        result = api.get_channel_metadata("UC_nonexistent")
        assert result is None


# ── get_latest_videos ────────────────────────────────────────────────────

class TestGetLatestVideos:
    def test_returns_video_list(self, api, mock_service):
        # Mock channel lookup for uploads playlist
        mock_service.channels().list().execute.return_value = {
            "items": [
                {
                    "contentDetails": {
                        "relatedPlaylists": {"uploads": "UU_abc123"}
                    }
                }
            ]
        }

        # Mock playlistItems
        mock_service.playlistItems().list().execute.return_value = {
            "items": [
                {
                    "snippet": {
                        "resourceId": {"videoId": "vid_001"},
                        "title": "Why Plants Matter",
                        "publishedAt": "2026-01-15T00:00:00Z",
                    }
                },
                {
                    "snippet": {
                        "resourceId": {"videoId": "vid_002"},
                        "title": "Sustainability 101",
                        "publishedAt": "2026-01-10T00:00:00Z",
                    }
                },
            ],
            "nextPageToken": None,
        }

        videos = api.get_latest_videos("UC_abc123", count=5)

        assert len(videos) == 2
        assert videos[0]["video_id"] == "vid_001"
        assert videos[1]["title"] == "Sustainability 101"

    def test_returns_empty_for_unknown_channel(self, api, mock_service):
        mock_service.channels().list().execute.return_value = {"items": []}

        result = api.get_latest_videos("UC_nope")
        assert result == []
