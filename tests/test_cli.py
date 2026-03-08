"""Tests for ingest.py — multi-source pipeline orchestration (mocked)."""

import pytest
from unittest.mock import patch, MagicMock

from ingest import (
    run_youtube_pipeline,
    run_blog_pipeline,
    run_academic_pipeline,
    run_social_pipeline,
)


@patch.dict("os.environ", {"YOUTUBE_API_KEY": "FAKE_KEY"})
@patch("ingest.YouTubeDataAPI")
@patch("ingest.fetch_transcript")
def test_youtube_pipeline(mock_fetch, mock_yt_cls):
    """YouTube pipeline discovers channels and fetches transcripts."""
    mock_yt = MagicMock()
    mock_yt_cls.return_value = mock_yt
    mock_yt.search_channels.return_value = [
        {"channel_id": "c1", "title": "C1", "subscriber_count": 100}
    ]
    mock_yt.get_latest_videos.return_value = [{"video_id": "v1", "title": "V1"}]

    mock_fetch.return_value = [{"text": "Hello", "start": 0, "duration": 1}]

    summary = run_youtube_pipeline(
        query="test",
        max_channels=1,
        videos_per_channel=1,
        db_url="sqlite:///:memory:",
    )

    assert summary["channels_found"] == 1
    assert summary["videos_fetched"] == 1
    assert summary["transcripts_fetched"] == 1


@patch("src.ingestion.blog_scraper.scrape_blog")
@patch("src.analysis.scoring.score_creator")
def test_blog_pipeline(mock_score, mock_scrape):
    """Blog pipeline scrapes articles and creates creators."""
    mock_scrape.return_value = [
        {"title": "Post 1", "author": "Blogger A", "url": "url1", "text_content": "A"},
        {"title": "Post 2", "author": "Blogger A", "url": "url2", "text_content": "B"},
    ]
    mock_score.return_value = MagicMock(composite_score=50.0)

    summary = run_blog_pipeline(
        query="https://test.blog",
        max_results=5,
        db_url="sqlite:///:memory:",
    )

    assert summary["articles_found"] == 2
    assert summary["creators_created"] == 1


@patch("src.ingestion.academic.search_academic")
@patch("src.ingestion.academic.extract_academic_creators")
@patch("src.analysis.scoring.score_creator")
def test_academic_pipeline(mock_score, mock_extract, mock_search):
    """Academic pipeline searches papers and extracts authors."""
    mock_search.return_value = [{"title": "Paper 1"}]
    mock_extract.return_value = {
        "Dr. Test": {"author_id": "1", "papers": [{"title": "Paper 1"}]}
    }
    mock_score.return_value = MagicMock(composite_score=80.0)

    summary = run_academic_pipeline(
        query="test diet",
        max_results=5,
        db_url="sqlite:///:memory:",
    )

    assert summary["papers_found"] == 1
    assert summary["authors_found"] == 1


@patch("src.ingestion.social_media.scrape_twitter_profile")
@patch("src.ingestion.social_media.normalize_social_content")
@patch("src.analysis.scoring.score_creator")
def test_social_pipeline_twitter(mock_score, mock_normalize, mock_scrape):
    """Social pipeline scrapes Twitter profiles."""
    mock_scrape.return_value = {"name": "Twitter User", "handle": "test"}
    mock_normalize.return_value = [{"source_type": "tweet", "text_content": "T", "title": "T"}]
    mock_score.return_value = MagicMock(composite_score=40.0)

    summary = run_social_pipeline(
        query="@test",
        platform="twitter",
        db_url="sqlite:///:memory:",
    )

    assert summary["profile_found"] is True
    assert summary["content_items"] == 1
