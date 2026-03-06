"""Composite scoring engine — multi-dimensional creator scoring.

Computes four sub-scores and a weighted composite:
  - Credibility: platform authority, professional signals, h-index
  - Engagement: normalized interaction rate relative to audience size
  - Reach: log-scaled follower/subscriber count
  - Alignment: LLM-based values alignment (delegates to nlp.py)
"""

import logging
import math
from dataclasses import dataclass, field
from typing import Optional

logger = logging.getLogger(__name__)


@dataclass
class ScoreWeights:
    """Configurable weights for composite scoring.

    Weights are normalized to sum to 1.0 at scoring time.
    """
    credibility: float = 0.25
    engagement: float = 0.20
    reach: float = 0.15
    alignment: float = 0.40


@dataclass
class ScoreBreakdown:
    """Full scoring breakdown for a creator."""
    credibility_score: float = 0.0
    engagement_score: float = 0.0
    reach_score: float = 0.0
    alignment_score: float = 0.0
    composite_score: float = 0.0
    weights: ScoreWeights = field(default_factory=ScoreWeights)

    def to_dict(self) -> dict:
        return {
            "credibility_score": round(self.credibility_score, 1),
            "engagement_score": round(self.engagement_score, 1),
            "reach_score": round(self.reach_score, 1),
            "alignment_score": round(self.alignment_score, 1),
            "composite_score": round(self.composite_score, 1),
        }


# ── Individual Score Calculators ─────────────────────────────────────────

def compute_credibility_score(
    platform: str,
    *,
    bio: str = "",
    follower_count: int = 0,
    h_index: int = 0,
    is_verified: bool = False,
    total_citations: int = 0,
) -> float:
    """Compute credibility score (0-100) based on professional signals.

    Heuristic factors:
    - Professional keywords in bio (Dr., PhD, MD, Professor, etc.)
    - Platform verification status
    - Academic h-index (for academic creators)
    - Follower-to-content ratio (higher = more authority signals)
    """
    score = 0.0

    # Professional keywords in bio (up to 35 points)
    professional_keywords = [
        "dr.", "ph.d", "phd", "md", "professor", "researcher",
        "scientist", "nutritionist", "dietitian", "chef",
        "author", "expert", "specialist", "certified",
        "university", "institute", "hospital", "clinic",
    ]
    bio_lower = bio.lower()
    keyword_hits = sum(1 for kw in professional_keywords if kw in bio_lower)
    score += min(keyword_hits * 10, 35)

    # Verification status (15 points)
    if is_verified:
        score += 15

    # Academic h-index (up to 25 points)
    if platform == "academic" and h_index > 0:
        # h-index of 10 = decent, 20 = strong, 40+ = exceptional
        score += min(h_index * 1.25, 25)

    # Citation count for academics (up to 15 points)
    if platform == "academic" and total_citations > 0:
        score += min(math.log10(total_citations + 1) * 5, 15)

    # Follower count as credibility signal (up to 10 points)
    if follower_count > 0:
        # Log scale: 1K=3pts, 10K=4pts, 100K=5pts, 1M=6pts
        score += min(math.log10(follower_count + 1) * 2, 10)

    return min(score, 100.0)


def compute_engagement_score(
    *,
    follower_count: int = 0,
    avg_likes: float = 0,
    avg_comments: float = 0,
    avg_shares: float = 0,
    avg_views: float = 0,
    citation_count: int = 0,
    platform: str = "",
) -> float:
    """Compute engagement score (0-100) based on interaction rates.

    For social/YouTube: engagement rate = (likes + comments + shares) / views
    For academic: based on citation count
    """
    if platform == "academic":
        # Academic engagement = citation impact
        if citation_count <= 0:
            return 10.0
        # log scale: 10 citations = 30, 100 = 50, 1000 = 70, 10000 = 90
        return min(math.log10(citation_count + 1) * 22, 100.0)

    # Social / YouTube engagement rate
    if follower_count <= 0 and avg_views <= 0:
        return 10.0  # Default floor for unknown engagement

    total_interactions = avg_likes + avg_comments + avg_shares
    denominator = max(avg_views, follower_count, 1)

    engagement_rate = total_interactions / denominator

    # Map engagement rate to 0-100 score
    # 1% = decent (40pts), 3% = good (60pts), 5%+ = excellent (80pts+)
    if engagement_rate <= 0:
        return 10.0

    score = min(engagement_rate * 100 * 15, 100.0)
    return max(score, 5.0)


def compute_reach_score(follower_count: int) -> float:
    """Compute audience reach score (0-100) using log scaling.

    Log scale prevents mega-influencers from dominating:
    - 1K followers → ~30
    - 10K → ~40
    - 100K → ~50
    - 1M → ~65
    - 10M → ~75
    """
    if follower_count <= 0:
        return 0.0

    # log10(1000) = 3, log10(1M) = 6, log10(100M) = 8
    raw = math.log10(follower_count + 1)

    # Scale: 0-100 mapped from log10 range of roughly 1-8
    score = ((raw - 1) / 7) * 100

    return max(min(score, 100.0), 0.0)


# ── Composite Score Calculator ───────────────────────────────────────────

def compute_composite_score(
    *,
    credibility_score: float = 0.0,
    engagement_score: float = 0.0,
    reach_score: float = 0.0,
    alignment_score: float = 0.0,
    weights: Optional[ScoreWeights] = None,
) -> ScoreBreakdown:
    """Compute the weighted composite score from sub-scores.

    Parameters
    ----------
    credibility_score : 0-100
    engagement_score : 0-100
    reach_score : 0-100
    alignment_score : 0-100
    weights : optional custom weights (defaults to ScoreWeights defaults)

    Returns
    -------
    ScoreBreakdown with all scores and composite
    """
    if weights is None:
        weights = ScoreWeights()

    # Normalize weights to sum to 1.0
    total_weight = (
        weights.credibility + weights.engagement +
        weights.reach + weights.alignment
    )
    if total_weight <= 0:
        total_weight = 1.0

    composite = (
        weights.credibility * credibility_score +
        weights.engagement * engagement_score +
        weights.reach * reach_score +
        weights.alignment * alignment_score
    ) / total_weight

    return ScoreBreakdown(
        credibility_score=credibility_score,
        engagement_score=engagement_score,
        reach_score=reach_score,
        alignment_score=alignment_score,
        composite_score=composite,
        weights=weights,
    )


def score_creator(
    *,
    platform: str,
    bio: str = "",
    follower_count: int = 0,
    h_index: int = 0,
    is_verified: bool = False,
    total_citations: int = 0,
    avg_likes: float = 0,
    avg_comments: float = 0,
    avg_shares: float = 0,
    avg_views: float = 0,
    alignment_score: float = 0.0,
    weights: Optional[ScoreWeights] = None,
) -> ScoreBreakdown:
    """One-call convenience — compute all sub-scores and composite.

    The alignment_score should be pre-computed by the NLP module.
    All other scores are computed from the metadata provided here.
    """
    credibility = compute_credibility_score(
        platform,
        bio=bio,
        follower_count=follower_count,
        h_index=h_index,
        is_verified=is_verified,
        total_citations=total_citations,
    )

    engagement = compute_engagement_score(
        follower_count=follower_count,
        avg_likes=avg_likes,
        avg_comments=avg_comments,
        avg_shares=avg_shares,
        avg_views=avg_views,
        citation_count=total_citations,
        platform=platform,
    )

    reach = compute_reach_score(follower_count)

    return compute_composite_score(
        credibility_score=credibility,
        engagement_score=engagement,
        reach_score=reach,
        alignment_score=alignment_score,
        weights=weights,
    )
