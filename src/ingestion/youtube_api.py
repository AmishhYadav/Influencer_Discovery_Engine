"""YouTube Data API v3 wrapper for channel discovery and video listing."""

import logging
from typing import Optional

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
)

logger = logging.getLogger(__name__)


class YouTubeDataAPI:
    """Thin wrapper around YouTube Data API v3.

    Handles channel search, metadata fetching, and video listing
    with built-in retry logic for transient failures.
    """

    def __init__(self, api_key: str):
        self._service = build("youtube", "v3", developerKey=api_key)

    # ── Retry decorator shared by all API calls ──────────────────────────
    _retry = retry(
        retry=retry_if_exception_type(HttpError),
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=30),
        reraise=True,
    )

    # ── Public API ───────────────────────────────────────────────────────

    @_retry
    def search_channels(
        self, query: str, max_results: int = 10
    ) -> list[dict]:
        """Search YouTube for channels matching *query*.

        Returns a list of dicts with keys: channel_id, title,
        description,  subscriber_count, video_count.
        """
        # Step 1: search for channels
        search_response = (
            self._service.search()
            .list(part="snippet", q=query, type="channel", maxResults=max_results)
            .execute()
        )

        channel_ids = [
            item["snippet"]["channelId"]
            for item in search_response.get("items", [])
        ]

        if not channel_ids:
            return []

        # Step 2: fetch detailed metadata for each channel
        channels_response = (
            self._service.channels()
            .list(
                part="snippet,statistics",
                id=",".join(channel_ids),
            )
            .execute()
        )

        results = []
        for ch in channels_response.get("items", []):
            stats = ch.get("statistics", {})
            results.append(
                {
                    "channel_id": ch["id"],
                    "title": ch["snippet"]["title"],
                    "description": ch["snippet"].get("description", ""),
                    "subscriber_count": int(stats.get("subscriberCount", 0)),
                    "video_count": int(stats.get("videoCount", 0)),
                }
            )

        return results

    @_retry
    def get_channel_metadata(self, channel_id: str) -> Optional[dict]:
        """Fetch metadata for a single channel by ID."""
        response = (
            self._service.channels()
            .list(part="snippet,statistics", id=channel_id)
            .execute()
        )

        items = response.get("items", [])
        if not items:
            return None

        ch = items[0]
        stats = ch.get("statistics", {})
        return {
            "channel_id": ch["id"],
            "title": ch["snippet"]["title"],
            "description": ch["snippet"].get("description", ""),
            "subscriber_count": int(stats.get("subscriberCount", 0)),
            "video_count": int(stats.get("videoCount", 0)),
        }

    @_retry
    def get_latest_videos(
        self, channel_id: str, count: int = 25
    ) -> list[dict]:
        """Return the latest *count* videos for *channel_id*.

        Uses the channel's uploads playlist (1 quota unit per page)
        rather than the expensive search endpoint (100 units).

        Returns list of dicts: video_id, title, published_at.
        """
        # Get uploads playlist ID
        ch_response = (
            self._service.channels()
            .list(part="contentDetails", id=channel_id)
            .execute()
        )

        items = ch_response.get("items", [])
        if not items:
            logger.warning("Channel %s not found", channel_id)
            return []

        uploads_playlist_id = items[0]["contentDetails"]["relatedPlaylists"][
            "uploads"
        ]

        # Paginate through uploads playlist
        videos: list[dict] = []
        next_page_token: Optional[str] = None

        while len(videos) < count:
            request = self._service.playlistItems().list(
                part="snippet",
                playlistId=uploads_playlist_id,
                maxResults=min(50, count - len(videos)),
                pageToken=next_page_token,
            )
            response = request.execute()

            for item in response.get("items", []):
                snippet = item["snippet"]
                videos.append(
                    {
                        "video_id": snippet["resourceId"]["videoId"],
                        "title": snippet["title"],
                        "published_at": snippet["publishedAt"],
                    }
                )

            next_page_token = response.get("nextPageToken")
            if not next_page_token:
                break

        return videos[:count]
