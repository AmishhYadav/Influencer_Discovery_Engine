"""Web search discovery — keyword-to-URL resolver using Google search.

Uses Google Custom Search JSON API or falls back to scraping
Google search result pages to convert keyword queries into
specific blog URLs, Twitter handles, and Instagram handles.
"""

import logging
import os
import re
from typing import Optional

import httpx
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

_TIMEOUT = httpx.Timeout(15.0, connect=10.0)
_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
}


def search_google(query: str, max_results: int = 10) -> list[dict]:
    """Search Google and return result URLs + titles.

    Tries Google Custom Search API first (if GOOGLE_CSE_API_KEY +
    GOOGLE_CSE_ID are set), then falls back to HTML scraping.

    Returns list of dicts: {url, title, snippet}
    """
    # Try API-based search first
    api_key = os.getenv("GOOGLE_CSE_API_KEY") or os.getenv("YOUTUBE_API_KEY")
    cse_id = os.getenv("GOOGLE_CSE_ID")

    if api_key and cse_id:
        results = _search_via_api(query, api_key, cse_id, max_results)
        if results:
            return results

    # Fallback: scrape Google search results
    return _search_via_scrape(query, max_results)


def _search_via_api(query: str, api_key: str, cse_id: str, max_results: int) -> list[dict]:
    """Use Google Custom Search JSON API."""
    try:
        url = "https://www.googleapis.com/customsearch/v1"
        params = {
            "q": query,
            "key": api_key,
            "cx": cse_id,
            "num": min(max_results, 10),
        }
        resp = httpx.get(url, params=params, timeout=_TIMEOUT)
        resp.raise_for_status()
        data = resp.json()
        results = []
        for item in data.get("items", []):
            results.append({
                "url": item.get("link", ""),
                "title": item.get("title", ""),
                "snippet": item.get("snippet", ""),
            })
        return results
    except Exception as e:
        logger.warning("Google CSE API failed: %s", e)
        return []


def _search_via_scrape(query: str, max_results: int) -> list[dict]:
    """Scrape Google search results as fallback."""
    try:
        search_url = f"https://www.google.com/search?q={query}&num={max_results}"
        resp = httpx.get(search_url, headers=_HEADERS, timeout=_TIMEOUT, follow_redirects=True)
        if resp.status_code != 200:
            return []
    except httpx.HTTPError:
        return []

    soup = BeautifulSoup(resp.text, "lxml")
    results = []

    for g_div in soup.find_all("div", class_="g"):
        link = g_div.find("a", href=True)
        if not link:
            continue
        href = link["href"]
        if not href.startswith("http"):
            continue

        title_el = g_div.find("h3")
        title = title_el.get_text(strip=True) if title_el else ""

        snippet_el = g_div.find("div", class_=re.compile(r"VwiC3b|IsZvec"))
        snippet = snippet_el.get_text(strip=True) if snippet_el else ""

        results.append({"url": href, "title": title, "snippet": snippet})
        if len(results) >= max_results:
            break

    return results


def discover_blog_urls(query: str, max_results: int = 5) -> list[str]:
    """Find blog URLs relevant to a keyword query.

    Searches Google for blog posts related to the query and extracts
    unique blog root domains to pass to the blog scraper.
    """
    search_query = f"{query} blog articles expert"
    results = search_google(search_query, max_results=max_results * 2)

    blog_urls = []
    seen_domains = set()

    for result in results:
        url = result.get("url", "")
        if not url:
            continue

        from urllib.parse import urlparse
        parsed = urlparse(url)
        domain = parsed.netloc.lower()

        # Skip social media, search engines, and aggregator sites
        skip_domains = [
            "youtube.com", "twitter.com", "x.com", "instagram.com",
            "facebook.com", "linkedin.com", "reddit.com", "tiktok.com",
            "google.com", "bing.com", "wikipedia.org", "amazon.com",
            "pinterest.com", "quora.com",
        ]
        if any(skip in domain for skip in skip_domains):
            continue

        if domain not in seen_domains:
            seen_domains.add(domain)
            blog_urls.append(url)

        if len(blog_urls) >= max_results:
            break

    logger.info("Discovered %d blog URLs for query '%s': %s", len(blog_urls), query, blog_urls)
    return blog_urls


def discover_twitter_handles(query: str, max_results: int = 5) -> list[str]:
    """Find Twitter/X handles relevant to a keyword query.

    Searches Google for Twitter profiles related to the query topic.
    """
    search_query = f"site:twitter.com OR site:x.com {query} expert"
    results = search_google(search_query, max_results=max_results * 2)

    handles = []
    seen = set()

    for result in results:
        url = result.get("url", "")
        # Extract handle from twitter.com/handle or x.com/handle URLs
        match = re.search(r"(?:twitter\.com|x\.com)/([A-Za-z0-9_]+)/?$", url)
        if match:
            handle = match.group(1).lower()
            # Skip common non-profile pages
            if handle in ("search", "explore", "home", "hashtag", "i", "settings", "login"):
                continue
            if handle not in seen:
                seen.add(handle)
                handles.append(handle)

        if len(handles) >= max_results:
            break

    logger.info("Discovered %d Twitter handles for query '%s': %s", len(handles), query, handles)
    return handles


def discover_instagram_handles(query: str, max_results: int = 5) -> list[str]:
    """Find Instagram handles relevant to a keyword query.

    Searches Google for Instagram profiles related to the query topic.
    """
    search_query = f"site:instagram.com {query} expert"
    results = search_google(search_query, max_results=max_results * 2)

    handles = []
    seen = set()

    for result in results:
        url = result.get("url", "")
        # Extract handle from instagram.com/handle URLs
        match = re.search(r"instagram\.com/([A-Za-z0-9_.]+)/?$", url)
        if match:
            handle = match.group(1).lower()
            # Skip common non-profile pages
            if handle in ("explore", "accounts", "p", "reel", "stories", "tv", "direct"):
                continue
            if handle not in seen:
                seen.add(handle)
                handles.append(handle)

        if len(handles) >= max_results:
            break

    logger.info("Discovered %d Instagram handles for query '%s': %s", len(handles), query, handles)
    return handles
