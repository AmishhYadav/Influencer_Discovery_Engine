"""Tests for blog_scraper module — article extraction and RSS discovery."""

import pytest
from unittest.mock import patch, MagicMock

from src.ingestion.blog_scraper import (
    extract_article,
    _extract_main_text,
    _clean_text,
    discover_blog_posts,
    _discover_via_html,
)


# ── HTML fixtures ────────────────────────────────────────────────────────

SAMPLE_ARTICLE_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Plant-Based Nutrition Guide</title>
    <meta property="og:title" content="Plant-Based Nutrition Guide" />
    <meta name="author" content="Dr. Jane Smith" />
    <meta property="article:published_time" content="2024-01-15T10:00:00Z" />
</head>
<body>
    <nav>Navigation links here</nav>
    <article>
        <h1>Plant-Based Nutrition Guide</h1>
        <p>A comprehensive guide to plant-based nutrition covering all essential
        nutrients. This guide explains how to get adequate protein, iron, and B12
        from plant sources. Many health professionals now recommend increasing
        plant consumption for better health outcomes. Research shows that
        plant-based diets can reduce the risk of heart disease, diabetes, and
        certain cancers. This article provides practical tips for transitioning
        to a more plant-forward diet while ensuring nutritional adequacy.</p>
    </article>
    <footer>Footer content</footer>
</body>
</html>
"""

SAMPLE_BLOG_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Health Blog</title>
    <link rel="alternate" type="application/rss+xml" href="/feed.xml" />
</head>
<body>
    <article class="post">
        <a href="/posts/nutrition-101">Nutrition 101</a>
    </article>
    <article class="post">
        <a href="/posts/plant-protein">Plant Protein Sources</a>
    </article>
    <div class="blog-entry">
        <a href="/posts/meal-prep">Weekly Meal Prep</a>
    </div>
</body>
</html>
"""

MINIMAL_HTML = """
<html><body><p>Short text.</p></body></html>
"""

RSS_FEED_XML = """<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
<channel>
  <title>Health Blog</title>
  <item>
    <title>Nutrition Guide</title>
    <link>https://example.com/nutrition-guide</link>
    <pubDate>Mon, 15 Jan 2024 10:00:00 GMT</pubDate>
  </item>
  <item>
    <title>Plant Protein</title>
    <link>https://example.com/plant-protein</link>
    <pubDate>Tue, 16 Jan 2024 10:00:00 GMT</pubDate>
  </item>
</channel>
</rss>
"""


# ── Tests ────────────────────────────────────────────────────────────────

class TestExtractArticle:
    @patch("src.ingestion.blog_scraper.httpx.get")
    def test_extracts_article_content(self, mock_get):
        mock_resp = MagicMock()
        mock_resp.text = SAMPLE_ARTICLE_HTML
        mock_resp.status_code = 200
        mock_resp.raise_for_status = MagicMock()
        mock_get.return_value = mock_resp

        result = extract_article("https://example.com/article")
        assert result is not None
        assert result["title"] == "Plant-Based Nutrition Guide"
        assert result["author"] == "Dr. Jane Smith"
        assert "plant-based" in result["text_content"].lower()
        assert result["url"] == "https://example.com/article"

    @patch("src.ingestion.blog_scraper.httpx.get")
    def test_returns_none_for_short_content(self, mock_get):
        mock_resp = MagicMock()
        mock_resp.text = MINIMAL_HTML
        mock_resp.status_code = 200
        mock_resp.raise_for_status = MagicMock()
        mock_get.return_value = mock_resp

        result = extract_article("https://example.com/short")
        assert result is None

    @patch("src.ingestion.blog_scraper.httpx.get")
    def test_handles_http_error(self, mock_get):
        import httpx
        mock_get.side_effect = httpx.HTTPError("Connection failed")

        result = extract_article("https://example.com/fail")
        assert result is None


class TestDiscoverBlogPosts:
    @patch("src.ingestion.blog_scraper.httpx.get")
    @patch("src.ingestion.blog_scraper.httpx.head")
    def test_discovers_via_html(self, mock_head, mock_get):
        mock_resp = MagicMock()
        mock_resp.text = SAMPLE_BLOG_HTML
        mock_resp.status_code = 200
        mock_resp.raise_for_status = MagicMock()
        mock_get.return_value = mock_resp

        # Feed discovery should fail to trigger HTML fallback
        mock_head.return_value = MagicMock(status_code=404)

        # Mock the feed URL discovery to return None
        with patch("src.ingestion.blog_scraper.discover_feed_url", return_value=None):
            posts = discover_blog_posts("https://example.com")

        assert len(posts) >= 2
        urls = [p["url"] for p in posts]
        assert any("nutrition-101" in u for u in urls)


class TestCleanText:
    def test_collapses_whitespace(self):
        text = "Hello\n\n\n\n\nWorld    test"
        result = _clean_text(text)
        assert "\n\n\n" not in result
        assert "    " not in result

    def test_truncates_long_text(self):
        text = "A" * 20000
        result = _clean_text(text)
        assert len(result) <= 10000
