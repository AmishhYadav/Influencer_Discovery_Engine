#!/usr/bin/env python3
"""CLI entrypoint for the Influencer Discovery Engine ingestion pipeline.

Usage:
    python ingest.py --query "plant based health"
    python ingest.py --query "sustainable food systems" --max-channels 5
"""

import argparse
import logging
import os
import sys

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from src.ingestion.youtube_api import YouTubeDataAPI
from src.ingestion.transcripts import fetch_transcript
from src.ingestion.cleaner import clean_transcript
from src.db.models import create_tables
from src.db.dao import upsert_channel, upsert_video

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("ingest")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Discover and ingest YouTube creators aligned with advocacy topics.",
    )
    parser.add_argument(
        "--query",
        required=True,
        help="Search query for discovering relevant YouTube channels.",
    )
    parser.add_argument(
        "--max-channels",
        type=int,
        default=10,
        help="Maximum number of channels to discover (default: 10).",
    )
    parser.add_argument(
        "--videos-per-channel",
        type=int,
        default=25,
        help="Number of latest videos to ingest per channel (default: 25).",
    )
    parser.add_argument(
        "--db-url",
        default=None,
        help="Database URL (default: from DATABASE_URL env var or SQLite).",
    )
    return parser


def run_pipeline(
    query: str,
    max_channels: int,
    videos_per_channel: int,
    db_url: str,
) -> dict:
    """Execute the full ingestion pipeline.

    Returns a summary dict with counts.
    """
    api_key = os.getenv("YOUTUBE_API_KEY")
    if not api_key:
        logger.error("YOUTUBE_API_KEY environment variable is not set")
        sys.exit(1)

    yt = YouTubeDataAPI(api_key)
    engine = create_engine(db_url, echo=False)
    create_tables(engine)

    summary = {
        "channels_found": 0,
        "videos_fetched": 0,
        "transcripts_fetched": 0,
        "transcripts_skipped": 0,
    }

    # Step 1: Discover channels
    logger.info("Searching YouTube for: %r", query)
    channels = yt.search_channels(query, max_results=max_channels)
    summary["channels_found"] = len(channels)
    logger.info("Found %d channels", len(channels))

    with Session(engine) as session:
        for ch_data in channels:
            channel_id = ch_data["channel_id"]
            logger.info(
                "Processing channel: %s (%s)",
                ch_data["title"],
                channel_id,
            )
            upsert_channel(session, ch_data)

            # Step 2: Get latest videos
            videos = yt.get_latest_videos(channel_id, count=videos_per_channel)
            logger.info("  Found %d videos", len(videos))

            for vid in videos:
                summary["videos_fetched"] += 1
                video_id = vid["video_id"]

                # Step 3: Fetch transcript
                raw_transcript = fetch_transcript(video_id)

                if raw_transcript is None:
                    summary["transcripts_skipped"] += 1
                    upsert_video(session, {
                        "video_id": video_id,
                        "channel_id": channel_id,
                        "title": vid["title"],
                        "published_at": vid.get("published_at", ""),
                        "transcript": None,
                    })
                    continue

                # Step 4: Clean transcript
                cleaned = clean_transcript(raw_transcript)
                summary["transcripts_fetched"] += 1

                upsert_video(session, {
                    "video_id": video_id,
                    "channel_id": channel_id,
                    "title": vid["title"],
                    "published_at": vid.get("published_at", ""),
                    "transcript": cleaned,
                })

            session.commit()

    logger.info("Pipeline complete: %s", summary)
    return summary


def main():
    parser = build_parser()
    args = parser.parse_args()

    db_url = args.db_url or os.getenv(
        "DATABASE_URL", "sqlite:///influencer_discovery.db"
    )

    run_pipeline(
        query=args.query,
        max_channels=args.max_channels,
        videos_per_channel=args.videos_per_channel,
        db_url=db_url,
    )


if __name__ == "__main__":
    main()
