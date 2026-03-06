"""Tests for social_media scraper module."""

import pytest
from unittest.mock import patch, MagicMock

from src.ingestion.social_media import (
    _parse_count,
    normalize_social_content,
    scrape_twitter_profile,
    scrape_instagram_profile,
)


class TestParseCount:
    def test_plain_number(self):
        assert _parse_count("1234") == 1234

    def test_with_commas(self):
        assert _parse_count("1,234,567") == 1234567

    def test_k_suffix(self):
        assert _parse_count("1.2K") == 1200

    def test_m_suffix(self):
        assert _parse_count("3.5M") == 3500000

    def test_b_suffix(self):
        assert _parse_count("1B") == 1000000000

    def test_zero(self):
        assert _parse_count("0") == 0


class TestNormalizeSocialContent:
    def test_normalizes_tweets(self):
        profile = {
            "name": "Test User",
            "handle": "testuser",
            "platform": "twitter",
            "profile_url": "https://twitter.com/testuser",
            "bio": "Health researcher",
            "recent_tweets": [
                {"text": "Great plant-based meal today!"},
                {"text": "New study on nutrition"},
            ],
            "recent_posts": [],
        }

        items = normalize_social_content(profile)
        assert len(items) == 2
        assert items[0]["source_type"] == "tweet"
        assert "plant-based" in items[0]["text_content"]

    def test_normalizes_instagram_posts(self):
        profile = {
            "name": "Chef Test",
            "handle": "cheftest",
            "platform": "instagram",
            "profile_url": "https://instagram.com/cheftest",
            "bio": "",
            "recent_tweets": [],
            "recent_posts": [
                {"caption": "Beautiful plant dish", "url": "https://instagram.com/p/123"},
            ],
        }

        items = normalize_social_content(profile)
        assert len(items) == 1
        assert items[0]["source_type"] == "instagram_post"

    def test_falls_back_to_bio(self):
        profile = {
            "name": "Dr. Bio",
            "handle": "drbio",
            "platform": "twitter",
            "profile_url": "https://twitter.com/drbio",
            "bio": "Plant-based nutrition researcher and author",
            "recent_tweets": [],
            "recent_posts": [],
        }

        items = normalize_social_content(profile)
        assert len(items) == 1
        assert items[0]["source_type"] == "twitter_bio"
        assert "nutrition" in items[0]["text_content"]

    def test_empty_profile(self):
        profile = {
            "name": "Empty",
            "handle": "empty",
            "platform": "twitter",
            "profile_url": "",
            "bio": "",
            "recent_tweets": [],
            "recent_posts": [],
        }

        items = normalize_social_content(profile)
        assert len(items) == 0


class TestTwitterScraping:
    @patch("src.ingestion.social_media._try_nitter_instance")
    def test_returns_profile_from_nitter(self, mock_nitter):
        mock_nitter.return_value = {
            "name": "Test User",
            "handle": "testuser",
            "bio": "Health advocate",
            "follower_count": 5000,
            "tweet_count": 200,
            "profile_url": "https://twitter.com/testuser",
            "recent_tweets": [],
            "platform": "twitter",
        }

        result = scrape_twitter_profile("testuser")
        assert result is not None
        assert result["name"] == "Test User"
        assert result["follower_count"] == 5000

    @patch("src.ingestion.social_media._try_nitter_instance")
    def test_falls_back_when_nitter_fails(self, mock_nitter):
        mock_nitter.return_value = None

        result = scrape_twitter_profile("testuser")
        assert result is not None
        assert result["handle"] == "testuser"
        # Fallback should still return a valid structure
        assert "profile_url" in result


class TestInstagramScraping:
    @patch("src.ingestion.social_media.httpx.get")
    def test_extracts_from_meta_tags(self, mock_get):
        html = """
        <html>
        <head>
            <meta property="og:title" content="Dr. Nutrition (@drnutrition)" />
            <meta property="og:description" content="50.5K Followers, 200 Following - Plant-based nutrition expert" />
        </head>
        <body></body>
        </html>
        """
        mock_resp = MagicMock()
        mock_resp.text = html
        mock_resp.status_code = 200
        mock_resp.raise_for_status = MagicMock()
        mock_get.return_value = mock_resp

        result = scrape_instagram_profile("drnutrition")
        assert result is not None
        assert result["name"] == "Dr. Nutrition"
        assert result["follower_count"] == 50500
        assert "nutrition" in result["bio"].lower()

    @patch("src.ingestion.social_media.httpx.get")
    def test_handles_failure(self, mock_get):
        import httpx
        mock_get.side_effect = httpx.HTTPError("Failed")

        result = scrape_instagram_profile("nouser")
        assert result is not None  # Should return fallback
        assert result["handle"] == "nouser"
