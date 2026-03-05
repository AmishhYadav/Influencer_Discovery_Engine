#!/usr/bin/env python3
"""CLI entrypoint for the analysis pipeline.

Usage:
    python analyze.py --channel-id "UC_abc123"
    python analyze.py --channel-id "UC_abc123" --topic "sustainable food systems"
"""

import argparse
import logging
import os
import sys

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from src.db.models import Channel, Video, create_tables
from src.db.dao import upsert_chunk, get_top_chunks, update_channel_alignment
from src.analysis.chunker import chunk_transcript
from src.analysis.nlp import get_embeddings, get_embedding, score_chunks

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("analyze")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Analyze a YouTube channel for topic alignment.",
    )
    parser.add_argument(
        "--channel-id",
        required=True,
        help="YouTube channel ID to analyze (must already be ingested).",
    )
    parser.add_argument(
        "--topic",
        default="plant-based health, sustainable food systems, ethical nutrition",
        help="Target topic to evaluate alignment against.",
    )
    parser.add_argument(
        "--top-n",
        type=int,
        default=20,
        help="Number of top chunks to send to the LLM (default: 20).",
    )
    parser.add_argument(
        "--db-url",
        default=None,
        help="Database URL (default: from DATABASE_URL env var or SQLite).",
    )
    return parser


def run_analysis(
    channel_id: str,
    topic: str,
    top_n: int,
    db_url: str,
) -> dict:
    """Execute the full analysis pipeline for one channel.

    Returns a summary dict.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        logger.error("OPENAI_API_KEY environment variable is not set")
        sys.exit(1)

    engine = create_engine(db_url, echo=False)
    create_tables(engine)

    summary = {
        "channel_id": channel_id,
        "videos_processed": 0,
        "chunks_created": 0,
        "alignment_score": None,
    }

    with Session(engine) as session:
        # Step 1: Verify channel exists
        channel = session.get(Channel, channel_id)
        if channel is None:
            logger.error("Channel %s not found in database", channel_id)
            return summary

        # Step 2: Load videos with transcripts
        videos = (
            session.query(Video)
            .filter(Video.channel_id == channel_id)
            .filter(Video.transcript.isnot(None))
            .all()
        )
        logger.info("Found %d videos with transcripts for %s", len(videos), channel.title)

        if not videos:
            logger.warning("No videos with transcripts found for channel %s", channel_id)
            return summary

        # Step 3: Chunk all transcripts
        all_chunks = []
        for video in videos:
            summary["videos_processed"] += 1
            chunks = chunk_transcript(video.transcript)
            for chunk in chunks:
                chunk["video_id"] = video.id
            all_chunks.extend(chunks)

        logger.info("Created %d chunks from %d videos", len(all_chunks), len(videos))
        summary["chunks_created"] = len(all_chunks)

        if not all_chunks:
            logger.warning("No chunks created")
            return summary

        # Step 4: Embed all chunks
        texts = [c["text"] for c in all_chunks]
        logger.info("Generating embeddings for %d chunks...", len(texts))
        embeddings = get_embeddings(texts)

        # Step 5: Store chunks with embeddings
        for chunk_data, embedding in zip(all_chunks, embeddings):
            upsert_chunk(session, {
                "video_id": chunk_data["video_id"],
                "start_time": chunk_data["start_time"],
                "end_time": chunk_data["end_time"],
                "text": chunk_data["text"],
                "embedding": embedding,
            })
        session.commit()
        logger.info("Stored %d chunks with embeddings", len(all_chunks))

        # Step 6: Get target embedding and find top chunks
        logger.info("Finding top %d aligned chunks for topic: %r", top_n, topic)
        target_embedding = get_embedding(topic)
        top_chunks = get_top_chunks(session, channel_id, target_embedding, limit=top_n)

        if not top_chunks:
            logger.warning("No chunks found after similarity search")
            return summary

        # Step 7: Score with LLM
        logger.info("Scoring %d chunks with LLM...", len(top_chunks))
        chunks_for_scoring = [
            {
                "text": c.text,
                "start_time": c.start_time,
                "end_time": c.end_time,
            }
            for c in top_chunks
        ]
        result = score_chunks(chunks_for_scoring, topic)

        # Step 8: Update channel record
        quotes_dicts = [q.model_dump() for q in result.quotes]
        update_channel_alignment(
            session, channel_id, result.alignment_score, quotes_dicts
        )
        session.commit()

        summary["alignment_score"] = result.alignment_score
        logger.info(
            "Analysis complete for %s: score=%d, reasoning=%s",
            channel.title,
            result.alignment_score,
            result.reasoning,
        )

    return summary


def main():
    parser = build_parser()
    args = parser.parse_args()

    db_url = args.db_url or os.getenv(
        "DATABASE_URL", "sqlite:///influencer_discovery.db"
    )

    run_analysis(
        channel_id=args.channel_id,
        topic=args.topic,
        top_n=args.top_n,
        db_url=db_url,
    )


if __name__ == "__main__":
    main()
