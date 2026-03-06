"""Blog scraper — discover and extract article content from blogs.

Uses httpx + BeautifulSoup4 for fetching and parsing, with RSS/sitemap
discovery for finding posts.
"""

import logging
import re
from typing import Optional
from urllib.parse import urljoin, urlparse

import httpx
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

# Reasonable timeout and headers for web scraping
_TIMEOUT = httpx.Timeout(15.0, connect=10.0)
_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (compatible; InfluencerDiscoveryBot/1.0; "
        "+https://github.com/influencer-discovery)"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
}

# Tags whose text content is typically not article body text
_NOISE_TAGS = {"nav", "header", "footer", "aside", "script", "style", "form", "noscript"}


# ── RSS / Sitemap Discovery ─────────────────────────────────────────────

def discover_feed_url(blog_url: str) -> Optional[str]:
    """Try to find an RSS/Atom feed URL from a blog's homepage.

    Checks for <link rel="alternate" type="application/rss+xml"> and
    common feed paths like /feed, /rss, /atom.xml.
    """
    try:
        resp = httpx.get(blog_url, headers=_HEADERS, timeout=_TIMEOUT, follow_redirects=True)
        resp.raise_for_status()
    except httpx.HTTPError as e:
        logger.warning("Failed to fetch %s for feed discovery: %s", blog_url, e)
        return None

    soup = BeautifulSoup(resp.text, "lxml")

    # Check <link> tags for RSS/Atom feeds
    for link_tag in soup.find_all("link", rel="alternate"):
        link_type = link_tag.get("type", "")
        if "rss" in link_type or "atom" in link_type:
            href = link_tag.get("href", "")
            if href:
                return urljoin(blog_url, href)

    # Try common feed paths
    common_paths = ["/feed", "/rss", "/atom.xml", "/feed.xml", "/rss.xml", "/index.xml"]
    for path in common_paths:
        feed_url = urljoin(blog_url, path)
        try:
            resp = httpx.head(feed_url, headers=_HEADERS, timeout=_TIMEOUT, follow_redirects=True)
            if resp.status_code == 200:
                return feed_url
        except httpx.HTTPError:
            continue

    return None


def discover_blog_posts(blog_url: str, max_posts: int = 20) -> list[dict]:
    """Discover blog post URLs from a blog.

    Tries RSS feed first, falls back to HTML link crawling.

    Returns list of dicts: {url, title, published_at}
    """
    posts = _discover_via_rss(blog_url, max_posts)
    if posts:
        return posts

    # Fallback: crawl HTML links
    return _discover_via_html(blog_url, max_posts)


def _discover_via_rss(blog_url: str, max_posts: int) -> list[dict]:
    """Parse RSS/Atom feed to extract post URLs."""
    feed_url = discover_feed_url(blog_url)
    if not feed_url:
        return []

    try:
        import feedparser
    except ImportError:
        logger.warning("feedparser not installed, skipping RSS discovery")
        return []

    try:
        resp = httpx.get(feed_url, headers=_HEADERS, timeout=_TIMEOUT, follow_redirects=True)
        resp.raise_for_status()
    except httpx.HTTPError as e:
        logger.warning("Failed to fetch feed %s: %s", feed_url, e)
        return []

    feed = feedparser.parse(resp.text)
    posts = []
    for entry in feed.entries[:max_posts]:
        posts.append({
            "url": entry.get("link", ""),
            "title": entry.get("title", ""),
            "published_at": entry.get("published", entry.get("updated", "")),
        })

    logger.info("Discovered %d posts via RSS from %s", len(posts), blog_url)
    return posts


def _discover_via_html(blog_url: str, max_posts: int) -> list[dict]:
    """Crawl a blog's homepage for article links as a fallback."""
    try:
        resp = httpx.get(blog_url, headers=_HEADERS, timeout=_TIMEOUT, follow_redirects=True)
        resp.raise_for_status()
    except httpx.HTTPError as e:
        logger.warning("Failed to fetch %s for HTML crawling: %s", blog_url, e)
        return []

    soup = BeautifulSoup(resp.text, "lxml")
    base_domain = urlparse(blog_url).netloc

    posts = []
    seen_urls = set()

    # Look for links inside <article> tags or common blog containers
    article_containers = soup.find_all(["article", "div"], class_=re.compile(
        r"(post|article|entry|blog|story)", re.IGNORECASE
    ))

    # If no containers found, scan all <a> tags on the page
    if not article_containers:
        article_containers = [soup]

    for container in article_containers:
        for a_tag in container.find_all("a", href=True):
            href = urljoin(blog_url, a_tag["href"])
            parsed = urlparse(href)

            # Only follow links on the same domain
            if parsed.netloc != base_domain:
                continue

            # Skip common non-article paths
            path = parsed.path.lower()
            if any(skip in path for skip in [
                "/tag", "/category", "/author", "/page/", "/login",
                "/signup", "/contact", "/about", "#",
            ]):
                continue

            # Must have a meaningful path (not just "/")
            if path in ("", "/"):
                continue

            if href not in seen_urls:
                seen_urls.add(href)
                title = a_tag.get_text(strip=True)[:200] or ""
                posts.append({
                    "url": href,
                    "title": title,
                    "published_at": "",
                })

            if len(posts) >= max_posts:
                break

        if len(posts) >= max_posts:
            break

    logger.info("Discovered %d posts via HTML crawling from %s", len(posts), blog_url)
    return posts


# ── Article Extraction ───────────────────────────────────────────────────

def extract_article(url: str) -> Optional[dict]:
    """Fetch a blog post URL and extract the main article content.

    Returns dict: {url, title, author, text_content, published_at}
    or None on failure.
    """
    try:
        resp = httpx.get(url, headers=_HEADERS, timeout=_TIMEOUT, follow_redirects=True)
        resp.raise_for_status()
    except httpx.HTTPError as e:
        logger.warning("Failed to fetch article %s: %s", url, e)
        return None

    soup = BeautifulSoup(resp.text, "lxml")

    # Extract title
    title = ""
    og_title = soup.find("meta", property="og:title")
    if og_title:
        title = og_title.get("content", "")
    if not title:
        title_tag = soup.find("title")
        title = title_tag.get_text(strip=True) if title_tag else ""

    # Extract author
    author = ""
    author_meta = soup.find("meta", attrs={"name": "author"})
    if author_meta:
        author = author_meta.get("content", "")
    if not author:
        # Try common author class patterns
        author_el = soup.find(class_=re.compile(r"(author|byline)", re.IGNORECASE))
        if author_el:
            author = author_el.get_text(strip=True)[:100]

    # Extract publish date
    published_at = ""
    time_tag = soup.find("time")
    if time_tag:
        published_at = time_tag.get("datetime", time_tag.get_text(strip=True))
    if not published_at:
        date_meta = soup.find("meta", property="article:published_time")
        if date_meta:
            published_at = date_meta.get("content", "")

    # Extract main content
    text_content = _extract_main_text(soup)

    if not text_content or len(text_content) < 100:
        logger.info("Article %s has too little content (%d chars), skipping", url, len(text_content))
        return None

    return {
        "url": url,
        "title": title,
        "author": author,
        "text_content": text_content,
        "published_at": published_at,
    }


def _extract_main_text(soup: BeautifulSoup) -> str:
    """Extract the main article text from a page, stripping noise.

    Strategy: find <article> or <main> tag first; fallback to the
    largest text-dense <div>.
    """
    # Remove noise tags
    for tag in soup.find_all(list(_NOISE_TAGS)):
        tag.decompose()

    # Strategy 1: <article> tag
    article = soup.find("article")
    if article:
        return _clean_text(article.get_text(separator="\n", strip=True))

    # Strategy 2: <main> tag
    main = soup.find("main")
    if main:
        return _clean_text(main.get_text(separator="\n", strip=True))

    # Strategy 3: largest <div> by text content
    divs = soup.find_all("div")
    if divs:
        best = max(divs, key=lambda d: len(d.get_text(strip=True)))
        text = best.get_text(separator="\n", strip=True)
        if len(text) > 200:
            return _clean_text(text)

    # Fallback: body text
    body = soup.find("body")
    if body:
        return _clean_text(body.get_text(separator="\n", strip=True))

    return ""


def _clean_text(text: str) -> str:
    """Collapse whitespace and limit length."""
    # Collapse multiple newlines
    text = re.sub(r"\n{3,}", "\n\n", text)
    # Collapse multiple spaces
    text = re.sub(r"[ \t]{2,}", " ", text)
    # Limit to ~10,000 chars to keep embeddings manageable
    return text[:10000].strip()


# ── Orchestration ────────────────────────────────────────────────────────

def scrape_blog(blog_url: str, max_posts: int = 20) -> list[dict]:
    """Discover and extract articles from a blog.

    Returns list of dicts compatible with ContentItem:
    {url, title, author, text_content, published_at, source_type}
    """
    logger.info("Scraping blog: %s (max %d posts)", blog_url, max_posts)

    posts = discover_blog_posts(blog_url, max_posts)
    if not posts:
        logger.warning("No posts discovered from %s", blog_url)
        return []

    articles = []
    for post in posts:
        article = extract_article(post["url"])
        if article:
            article["source_type"] = "blog_post"
            # Prefer RSS-provided title/date if article extraction missed them
            if not article["title"] and post.get("title"):
                article["title"] = post["title"]
            if not article["published_at"] and post.get("published_at"):
                article["published_at"] = post["published_at"]
            articles.append(article)

    logger.info("Extracted %d articles from %s", len(articles), blog_url)
    return articles
