#!/usr/bin/env python3
"""CLI entrypoint for the Influencer Discovery Engine ingestion pipeline.

Usage:
    # YouTube (default)
    python ingest.py --query "plant based health"
    python ingest.py --query "sustainable food systems" --max-channels 5

    # Blog scraping
    python ingest.py --query "https://example-health-blog.com" --source blog

    # Academic search
    python ingest.py --query "plant-based diet health outcomes" --source academic

    # Social media
    python ingest.py --query "@drgreger" --source twitter
    python ingest.py --query "@simnett_nutrition" --source instagram
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
from src.db.dao import (
    upsert_channel, upsert_video,
    upsert_creator, upsert_content_item, update_creator_scores,
)

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("ingest")

VALID_SOURCES = ["youtube", "blog", "academic", "twitter", "instagram"]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Discover and ingest creators aligned with advocacy topics.",
    )
    parser.add_argument(
        "--query",
        required=True,
        help="Search query, blog URL, or social media handle.",
    )
    parser.add_argument(
        "--source",
        default="youtube",
        choices=VALID_SOURCES,
        help=f"Data source to search ({', '.join(VALID_SOURCES)}). Default: youtube.",
    )
    parser.add_argument(
        "--max-channels",
        type=int,
        default=10,
        help="Maximum number of channels/creators to discover (default: 10).",
    )
    parser.add_argument(
        "--videos-per-channel",
        type=int,
        default=25,
        help="Number of latest videos to ingest per channel (default: 25, YouTube only).",
    )
    parser.add_argument(
        "--db-url",
        default=None,
        help="Database URL (default: from DATABASE_URL env var or SQLite).",
    )
    return parser


# ── YouTube Pipeline (original) ──────────────────────────────────────────

def run_youtube_pipeline(
    query: str,
    max_channels: int,
    videos_per_channel: int,
    db_url: str,
) -> dict:
    """Execute the full YouTube ingestion pipeline.

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
        "source": "youtube",
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

    logger.info("YouTube pipeline complete: %s", summary)
    return summary


# ── Blog Pipeline ────────────────────────────────────────────────────────

def run_blog_pipeline(query: str, max_results: int, db_url: str) -> dict:
    """Scrape blog articles and store as creator + content items."""
    from src.ingestion.blog_scraper import scrape_blog
    from src.analysis.scoring import score_creator

    engine = create_engine(db_url, echo=False)
    create_tables(engine)

    summary = {"source": "blog", "articles_found": 0, "creators_created": 0}

    if not query.startswith("http"):
        logger.error("Blog source requires a URL. Got: %r", query)
        return summary

    articles = scrape_blog(query, max_posts=max_results)
    summary["articles_found"] = len(articles)

    with Session(engine) as session:
        # Group by author
        author_map: dict[str, list] = {}
        for article in articles:
            author = article.get("author", "Unknown Author")
            author_map.setdefault(author, []).append(article)

        for author_name, author_articles in author_map.items():
            creator = upsert_creator(session, {
                "name": author_name,
                "platform": "blog",
                "platform_id": query,
                "profile_url": query,
                "bio": "",
            })

            for article in author_articles:
                upsert_content_item(session, {
                    "creator_id": creator.id,
                    "source_type": "blog_post",
                    "title": article.get("title", ""),
                    "text_content": article.get("text_content", ""),
                    "url": article.get("url", ""),
                    "published_at": article.get("published_at", ""),
                })

            # Score
            breakdown = score_creator(platform="blog", bio="")
            update_creator_scores(
                session, creator.id,
                credibility_score=breakdown.credibility_score,
                engagement_score=breakdown.engagement_score,
                reach_score=breakdown.reach_score,
                composite_score=breakdown.composite_score,
            )
            summary["creators_created"] += 1

        session.commit()

    logger.info("Blog pipeline complete: %s", summary)
    return summary


# ── Academic Pipeline ────────────────────────────────────────────────────

def run_academic_pipeline(query: str, max_results: int, db_url: str) -> dict:
    """Search academic databases and store author profiles."""
    from src.ingestion.academic import search_academic, extract_academic_creators
    from src.analysis.scoring import score_creator

    engine = create_engine(db_url, echo=False)
    create_tables(engine)

    summary = {"source": "academic", "papers_found": 0, "authors_found": 0}

    papers = search_academic(query, limit=max_results)
    summary["papers_found"] = len(papers)

    author_map = extract_academic_creators(papers)
    summary["authors_found"] = len(author_map)

    with Session(engine) as session:
        for author_name, author_data in author_map.items():
            creator = upsert_creator(session, {
                "name": author_name,
                "platform": "academic",
                "platform_id": author_data.get("author_id", ""),
                "profile_url": author_data.get("profile_url", ""),
                "bio": ", ".join(author_data.get("affiliations", [])),
                "follower_count": 0,
            })

            for paper in author_data.get("papers", []):
                upsert_content_item(session, {
                    "creator_id": creator.id,
                    "source_type": "paper",
                    "title": paper.get("title", ""),
                    "text_content": paper.get("abstract", ""),
                    "url": paper.get("url", ""),
                    "published_at": str(paper.get("year", "")),
                    "engagement_metrics": {"citations": paper.get("citation_count", 0)},
                })

            breakdown = score_creator(
                platform="academic",
                bio=creator.bio or "",
                h_index=author_data.get("h_index", 0),
                total_citations=author_data.get("total_citations", 0),
            )
            update_creator_scores(
                session, creator.id,
                credibility_score=breakdown.credibility_score,
                engagement_score=breakdown.engagement_score,
                reach_score=breakdown.reach_score,
                composite_score=breakdown.composite_score,
            )

        session.commit()

    logger.info("Academic pipeline complete: %s", summary)
    return summary


# ── Social Media Pipeline ────────────────────────────────────────────────

def run_social_pipeline(
    query: str, platform: str, db_url: str,
) -> dict:
    """Scrape a social media profile and store as creator."""
    from src.ingestion.social_media import (
        scrape_twitter_profile,
        scrape_instagram_profile,
        normalize_social_content,
    )
    from src.analysis.scoring import score_creator

    engine = create_engine(db_url, echo=False)
    create_tables(engine)

    summary = {"source": platform, "profile_found": False, "content_items": 0}

    handle = query.lstrip("@").split("/")[-1]

    if platform == "twitter":
        profile = scrape_twitter_profile(handle)
    elif platform == "instagram":
        profile = scrape_instagram_profile(handle)
    else:
        logger.error("Unknown social platform: %s", platform)
        return summary

    if not profile:
        logger.warning("Could not scrape %s profile for %s", platform, handle)
        return summary

    summary["profile_found"] = True

    with Session(engine) as session:
        creator = upsert_creator(session, {
            "name": profile.get("name", handle),
            "platform": platform,
            "platform_id": handle,
            "profile_url": profile.get("profile_url", ""),
            "bio": profile.get("bio", ""),
            "follower_count": profile.get("follower_count", 0),
        })

        content_items = normalize_social_content(profile)
        for item in content_items:
            item["creator_id"] = creator.id
            upsert_content_item(session, item)
        summary["content_items"] = len(content_items)

        breakdown = score_creator(
            platform=platform,
            bio=creator.bio or "",
            follower_count=profile.get("follower_count", 0),
        )
        update_creator_scores(
            session, creator.id,
            credibility_score=breakdown.credibility_score,
            engagement_score=breakdown.engagement_score,
            reach_score=breakdown.reach_score,
            composite_score=breakdown.composite_score,
        )

        session.commit()

    logger.info("%s pipeline complete: %s", platform.title(), summary)
    return summary


# ── Main ─────────────────────────────────────────────────────────────────

def main():
    parser = build_parser()
    args = parser.parse_args()

    db_url = args.db_url or os.getenv(
        "DATABASE_URL", "sqlite:///influencer_discovery.db"
    )

    source = args.source

    if source == "youtube":
        run_youtube_pipeline(
            query=args.query,
            max_channels=args.max_channels,
            videos_per_channel=args.videos_per_channel,
            db_url=db_url,
        )
    elif source == "blog":
        run_blog_pipeline(
            query=args.query,
            max_results=args.max_channels,
            db_url=db_url,
        )
    elif source == "academic":
        run_academic_pipeline(
            query=args.query,
            max_results=args.max_channels,
            db_url=db_url,
        )
    elif source in ("twitter", "instagram"):
        run_social_pipeline(
            query=args.query,
            platform=source,
            db_url=db_url,
        )
    else:
        logger.error("Unknown source: %s", source)
        sys.exit(1)


if __name__ == "__main__":
    main()
