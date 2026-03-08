"""Social media scraper — public profile data from Twitter/X and Instagram.

Uses httpx + BeautifulSoup for scraping public profile pages.
No API keys required, but scraping may be fragile and rate-limited.
"""

import logging
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

# Nitter instances for accessing Twitter data (public proxy)
_NITTER_INSTANCES = [
    "https://nitter.net",
    "https://nitter.privacydev.net",
    "https://nitter.poast.org",
]


# ── Twitter / X ──────────────────────────────────────────────────────────

def scrape_twitter_profile(handle: str) -> Optional[dict]:
    """Scrape public Twitter/X profile data via Nitter instances.

    Parameters
    ----------
    handle : Twitter handle without the @ sign

    Returns
    -------
    dict with keys: name, handle, bio, follower_count, tweet_count,
                    profile_url, recent_tweets
    or None if scraping fails.
    """
    handle = handle.lstrip("@")

    for instance in _NITTER_INSTANCES:
        result = _try_nitter_instance(instance, handle)
        if result:
            return result

    # All Nitter instances failed — try direct Twitter embed as last resort
    logger.warning(
        "All Nitter instances failed for @%s. Twitter scraping unavailable.",
        handle,
    )
    return _scrape_twitter_fallback(handle)


def _try_nitter_instance(instance: str, handle: str) -> Optional[dict]:
    """Try to scrape a profile from a single Nitter instance."""
    url = f"{instance}/{handle}"
    try:
        resp = httpx.get(url, headers=_HEADERS, timeout=_TIMEOUT, follow_redirects=True)
        if resp.status_code != 200:
            return None
    except httpx.HTTPError:
        return None

    soup = BeautifulSoup(resp.text, "lxml")

    # Extract profile data
    name_el = soup.find(class_="profile-card-fullname")
    bio_el = soup.find(class_="profile-bio")

    # Extract stats
    stats = {}
    stat_items = soup.find_all(class_="profile-stat-num")
    stat_labels = soup.find_all(class_="profile-stat-header")
    for num_el, label_el in zip(stat_items, stat_labels):
        label = label_el.get_text(strip=True).lower()
        num_text = num_el.get_text(strip=True).replace(",", "")
        try:
            stats[label] = _parse_count(num_text)
        except ValueError:
            pass

    # Extract recent tweets
    tweets = []
    tweet_containers = soup.find_all(class_="timeline-item", limit=10)
    for container in tweet_containers:
        content_el = container.find(class_="tweet-content")
        if content_el:
            tweets.append({
                "text": content_el.get_text(strip=True)[:500],
                "source_type": "tweet",
            })

    return {
        "name": name_el.get_text(strip=True) if name_el else handle,
        "handle": handle,
        "bio": bio_el.get_text(strip=True) if bio_el else "",
        "follower_count": stats.get("followers", 0),
        "tweet_count": stats.get("tweets", stats.get("posts", 0)),
        "profile_url": f"https://twitter.com/{handle}",
        "recent_tweets": tweets,
        "platform": "twitter",
    }


def _scrape_twitter_fallback(handle: str) -> Optional[dict]:
    """Minimal fallback that returns a shell profile when Nitter is down."""
    return {
        "name": handle,
        "handle": handle,
        "bio": "",
        "follower_count": 0,
        "tweet_count": 0,
        "profile_url": f"https://twitter.com/{handle}",
        "recent_tweets": [],
        "platform": "twitter",
        "_scrape_status": "fallback_only",
    }


# ── Instagram ────────────────────────────────────────────────────────────

def scrape_instagram_profile(handle: str) -> Optional[dict]:
    """Scrape public Instagram profile metadata.

    Uses the Instagram public profile page to extract bio and follower count.
    Limited to public accounts only.

    Parameters
    ----------
    handle : Instagram handle without the @ sign

    Returns
    -------
    dict with keys: name, handle, bio, follower_count, post_count,
                    profile_url, recent_posts
    or None if scraping fails.
    """
    handle = handle.lstrip("@")
    url = f"https://www.instagram.com/{handle}/"

    try:
        resp = httpx.get(url, headers=_HEADERS, timeout=_TIMEOUT, follow_redirects=True)
        if resp.status_code != 200:
            logger.warning("Instagram returned %d for @%s", resp.status_code, handle)
            return _instagram_fallback(handle)
    except httpx.HTTPError as e:
        logger.warning("Failed to fetch Instagram profile for @%s: %s", handle, e)
        return _instagram_fallback(handle)

    soup = BeautifulSoup(resp.text, "lxml")

    # Try to extract from meta tags (most reliable for public profiles)
    name = handle
    bio = ""
    follower_count = 0

    # <meta property="og:title" content="Name (@handle)">
    og_title = soup.find("meta", property="og:title")
    if og_title:
        title_text = og_title.get("content", "")
        match = re.match(r"(.+?)\s*\(@", title_text)
        if match:
            name = match.group(1).strip()

    # <meta property="og:description" content="123K Followers, ... - bio text">
    og_desc = soup.find("meta", property="og:description")
    if og_desc:
        desc_text = og_desc.get("content", "")
        # Parse follower count from description
        follower_match = re.search(r"([\d,.]+[KMB]?)\s*Followers", desc_text, re.IGNORECASE)
        if follower_match:
            follower_count = _parse_count(follower_match.group(1))

        # Extract bio (usually after the " - " separator)
        bio_match = re.search(r" - (.+)", desc_text)
        if bio_match:
            bio = bio_match.group(1).strip()

    return {
        "name": name,
        "handle": handle,
        "bio": bio,
        "follower_count": follower_count,
        "post_count": 0,
        "profile_url": url,
        "recent_posts": [],
        "platform": "instagram",
    }


def _instagram_fallback(handle: str) -> dict:
    """Return a shell profile when Instagram scraping fails."""
    return {
        "name": handle,
        "handle": handle,
        "bio": "",
        "follower_count": 0,
        "post_count": 0,
        "profile_url": f"https://www.instagram.com/{handle}/",
        "recent_posts": [],
        "platform": "instagram",
        "_scrape_status": "fallback_only",
    }


# ── Utilities ────────────────────────────────────────────────────────────

def _parse_count(text: str) -> int:
    """Parse a human-readable count like '1.2K', '3.5M', '12,345'."""
    text = text.strip().replace(",", "")

    multipliers = {"K": 1_000, "M": 1_000_000, "B": 1_000_000_000}
    for suffix, mult in multipliers.items():
        if text.upper().endswith(suffix):
            return int(float(text[:-1]) * mult)

    return int(float(text))


def normalize_social_content(profile_data: dict) -> list[dict]:
    """Convert scraped social media data into ContentItem-compatible dicts.

    Parameters
    ----------
    profile_data : dict returned by scrape_twitter_profile or
                   scrape_instagram_profile

    Returns
    -------
    list of dicts with keys: source_type, title, text_content, url
    """
    items = []
    platform = profile_data.get("platform", "social")

    # Twitter tweets
    for tweet in profile_data.get("recent_tweets", []):
        items.append({
            "source_type": "tweet",
            "title": f"Tweet by @{profile_data['handle']}",
            "text_content": tweet.get("text", ""),
            "url": profile_data.get("profile_url", ""),
            "published_at": "",
        })

    # Instagram posts
    for post in profile_data.get("recent_posts", []):
        items.append({
            "source_type": "instagram_post",
            "title": f"Post by @{profile_data['handle']}",
            "text_content": post.get("caption", ""),
            "url": post.get("url", profile_data.get("profile_url", "")),
            "published_at": "",
        })

    # If no content items, create a bio-based item so we have something to score
    if not items and profile_data.get("bio"):
        items.append({
            "source_type": f"{platform}_bio",
            "title": f"{profile_data['name']} — {platform.title()} Bio",
            "text_content": profile_data["bio"],
            "url": profile_data.get("profile_url", ""),
            "published_at": "",
        })

    return items
