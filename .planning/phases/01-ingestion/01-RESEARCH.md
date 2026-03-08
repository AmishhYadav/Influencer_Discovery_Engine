# Phase 1: Ingestion - Research

**Date:** 2026-03-06
**Goal:** Reliable YouTube transcript and metadata fetching

## Technical Approaches

### 1. YouTube Data API v3 (Metadata & Search)
To satisfy the ingestion trigger (`--query`) and video selection process:
- **Search Endpoint (`/search`)**: Use this to find relevant channels/videos based on the user's query.
  - Set `type=channel` or `type=video` to find aligned content.
  - From videos, extract `channelId`.
- **Channels Endpoint (`/channels`)**: Fetch channel metadata (subscribers, view counts).
- **Search/PlaylistItems Endpoint**: Fetch the latest 20-30 videos for a specific `channelId`. Easiest way is to query the channel's "Uploads" playlist.

**Authentication:** Requires a YouTube Data API Key via Google Cloud Console.

### 2. Transcript Fetching (`youtube-transcript-api`)
To satisfy DATA-01 and DATA-03:
- The `youtube-transcript-api` library fetches transcripts directly without a headless browser.
- Method: `YouTubeTranscriptApi.get_transcript(video_id)`
- **Data format**: Returns a list of dictionaries with `text`, `start`, and `duration`. 
- **Cleaning (DATA-03)**:
  - We need to strip known sponsor reads (e.g., matching common sponsor names like "NordVPN", "BetterHelp", "Squarespace" or using heuristics like "sponsor", "support the channel").
  - Auto-generated filler like "[Music]" or "[Applause]" should be removed.

### 3. Database Layer (PostgreSQL)
- **Driver/ORM**: `asyncpg` or `SQLAlchemy` (for Python).
- **Schema Design (MVP)**:
  - `channels` table: `id` (YouTube ID), `title`, `subscriber_count`, `video_count`, `created_at`.
  - `videos` table: `id` (YouTube ID), `channel_id`, `title`, `published_at`, `transcript` (JSONB column to hold the `youtube-transcript-api` output).
- **JSONB**: Essential for storing the transcript arrays natively without complex relational mapping for every text segment.

### 4. Error Handling and Resilience
- **Exponential Backoff**: Use Python's `tenacity` or `backoff` library to wrap API calls. This easily handles `HttpError` from googleapiclient or `TranscriptsDisabled` from `youtube-transcript-api`.
- **Graceful degradation**: If one video fails to fetch transcripts (e.g., transcripts are disabled for that specific video), log the error and continue to the next video in the list to avoid failing the whole channel ingestion.

## Validation Architecture

To satisfy NYQUIST validation checks (Dimension 8):
- **Mocking**: We will need to mock the YouTube API responses and `youtube-transcript-api` calls in our unit tests to ensure we don't hit rate limits or require live API keys in CI.
- **Integration**: We should have a way to run a real query manually and verify the DB state locally.

## Risks & Gotchas
- **Quotas**: The YouTube Data API search endpoint costs 100 units per request. Querying 20-30 videos per channel using the Search API is expensive. 
  - *Optimization*: Fetch the channel's `uploads` playlist ID, then query `playlistItems` (only costs 1 unit per page) to get the latest videos.
- **Transcript Availability**: Some videos don't have transcripts. The script must anticipate `TranscriptsDisabled` exceptions and gracefully skip those videos.
