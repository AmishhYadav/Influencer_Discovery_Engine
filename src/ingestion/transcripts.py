"""Fetch YouTube video transcripts with graceful error handling."""

import logging
from typing import Optional

from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import (
    TranscriptsDisabled,
    NoTranscriptFound,
    VideoUnavailable,
)
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
)

logger = logging.getLogger(__name__)

# Shared instance — lightweight, no state
_api = YouTubeTranscriptApi()


@retry(
    retry=retry_if_exception_type(ConnectionError),
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=15),
    reraise=True,
)
def fetch_transcript(video_id: str) -> Optional[list[dict]]:
    """Fetch transcript for a YouTube video.

    Returns a list of dicts with keys: text, start, duration.
    Returns None if the video has no available transcript.

    Only retries on transient network errors; permanent failures
    (transcripts disabled, video unavailable) return None immediately.
    """
    try:
        fetched = _api.fetch(video_id)
        return fetched.to_raw_data()
    except (TranscriptsDisabled, NoTranscriptFound):
        logger.info(
            "Transcript not available for video %s (disabled or missing)",
            video_id,
        )
        return None
    except VideoUnavailable:
        logger.warning("Video %s is unavailable", video_id)
        return None
    except Exception as exc:
        logger.error(
            "Unexpected error fetching transcript for %s: %s",
            video_id,
            exc,
        )
        return None
