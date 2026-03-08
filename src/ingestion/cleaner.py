"""Clean raw YouTube transcripts by removing filler and sponsor segments."""

import re
from typing import Optional

# Audio filler tags to strip entirely
_FILLER_TAGS = re.compile(
    r"^\[(?:Music|Applause|Laughter|Silence|Inaudible)\]$",
    re.IGNORECASE,
)

# Common sponsor / ad keywords (case-insensitive partial match)
_SPONSOR_KEYWORDS = [
    "nordvpn",
    "betterhelp",
    "squarespace",
    "skillshare",
    "audible",
    "raid shadow legends",
    "brilliant.org",
    "sponsor",
    "today's sponsor",
    "sponsored by",
    "this video is brought to you",
    "support the channel",
    "use code",
    "use my link",
]


def clean_transcript(
    transcript: Optional[list[dict]],
) -> list[dict]:
    """Remove filler tags and likely sponsor segments.

    Parameters
    ----------
    transcript : list of dicts with keys ``text``, ``start``, ``duration``

    Returns
    -------
    Cleaned list (may be empty if everything was filtered).
    """
    if not transcript:
        return []

    cleaned: list[dict] = []

    for segment in transcript:
        text = segment.get("text", "").strip()

        # Skip empty segments
        if not text:
            continue

        # Skip pure audio tags like [Music]
        if _FILLER_TAGS.match(text):
            continue

        # Skip segments that look like sponsor reads
        text_lower = text.lower()
        if any(kw in text_lower for kw in _SPONSOR_KEYWORDS):
            continue

        cleaned.append(segment)

    return cleaned
