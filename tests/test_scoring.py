"""Tests for composite scoring engine."""

import pytest
from src.analysis.scoring import (
    compute_credibility_score,
    compute_engagement_score,
    compute_reach_score,
    compute_composite_score,
    score_creator,
    ScoreWeights,
    ScoreBreakdown,
)


class TestCredibilityScore:
    def test_professional_keywords_boost_score(self):
        score = compute_credibility_score(
            "blog",
            bio="Dr. Jane Smith, PhD — Nutrition researcher at Stanford University",
        )
        # Should be high due to Dr., PhD, researcher, University
        assert score >= 30

    def test_empty_bio_low_score(self):
        score = compute_credibility_score("blog", bio="")
        assert score < 15

    def test_academic_h_index(self):
        score_low = compute_credibility_score("academic", h_index=5)
        score_high = compute_credibility_score("academic", h_index=30)
        assert score_high > score_low

    def test_verified_status(self):
        score_unverified = compute_credibility_score("twitter", bio="")
        score_verified = compute_credibility_score("twitter", bio="", is_verified=True)
        assert score_verified > score_unverified

    def test_capped_at_100(self):
        score = compute_credibility_score(
            "academic",
            bio="Dr. Professor PhD MD certified expert specialist researcher University Institute",
            h_index=50,
            total_citations=100000,
            is_verified=True,
            follower_count=10000000,
        )
        assert score <= 100


class TestEngagementScore:
    def test_academic_citation_impact(self):
        score_low = compute_engagement_score(
            citation_count=10, platform="academic"
        )
        score_high = compute_engagement_score(
            citation_count=10000, platform="academic"
        )
        assert score_high > score_low

    def test_social_engagement_rate(self):
        score = compute_engagement_score(
            follower_count=10000,
            avg_likes=500,
            avg_comments=50,
            avg_shares=100,
            avg_views=5000,
        )
        assert score > 10

    def test_zero_followers(self):
        score = compute_engagement_score(follower_count=0, avg_views=0)
        assert score >= 5  # Floor

    def test_high_engagement_rate(self):
        score = compute_engagement_score(
            follower_count=1000,
            avg_likes=200,
            avg_comments=50,
            avg_shares=30,
            avg_views=1000,
        )
        assert score >= 40


class TestReachScore:
    def test_zero_followers(self):
        assert compute_reach_score(0) == 0.0

    def test_monotonically_increasing(self):
        scores = [compute_reach_score(n) for n in [100, 1000, 10000, 100000, 1000000]]
        for i in range(len(scores) - 1):
            assert scores[i + 1] > scores[i]

    def test_capped_at_100(self):
        score = compute_reach_score(10_000_000_000)
        assert score <= 100.0

    def test_log_scaling(self):
        # 1K and 1M should not be 1000x different in score
        score_1k = compute_reach_score(1000)
        score_1m = compute_reach_score(1000000)
        ratio = score_1m / score_1k if score_1k > 0 else float("inf")
        assert ratio < 5  # Should be roughly 2x due to log scaling


class TestCompositeScore:
    def test_default_weights(self):
        result = compute_composite_score(
            credibility_score=80,
            engagement_score=60,
            reach_score=50,
            alignment_score=90,
        )
        assert isinstance(result, ScoreBreakdown)
        assert result.composite_score > 0
        assert result.composite_score <= 100

    def test_custom_weights(self):
        weights = ScoreWeights(credibility=0, engagement=0, reach=0, alignment=1.0)
        result = compute_composite_score(
            credibility_score=10,
            engagement_score=10,
            reach_score=10,
            alignment_score=90,
            weights=weights,
        )
        assert result.composite_score == pytest.approx(90.0)

    def test_equal_weights(self):
        weights = ScoreWeights(
            credibility=0.25, engagement=0.25, reach=0.25, alignment=0.25
        )
        result = compute_composite_score(
            credibility_score=100,
            engagement_score=100,
            reach_score=100,
            alignment_score=100,
            weights=weights,
        )
        assert result.composite_score == pytest.approx(100.0)

    def test_all_zeros(self):
        result = compute_composite_score(
            credibility_score=0,
            engagement_score=0,
            reach_score=0,
            alignment_score=0,
        )
        assert result.composite_score == 0.0


class TestScoreCreator:
    def test_full_scoring_pipeline(self):
        breakdown = score_creator(
            platform="twitter",
            bio="Dr. Jane, PhD in Nutrition at Harvard University",
            follower_count=50000,
            avg_likes=500,
            avg_comments=50,
            alignment_score=75.0,
        )
        assert isinstance(breakdown, ScoreBreakdown)
        assert breakdown.credibility_score > 0
        assert breakdown.reach_score > 0
        assert breakdown.composite_score > 0

    def test_academic_scoring(self):
        breakdown = score_creator(
            platform="academic",
            bio="Professor of Environmental Science",
            h_index=25,
            total_citations=3000,
            alignment_score=80.0,
        )
        assert breakdown.credibility_score > 30
        assert breakdown.engagement_score > 20

    def test_to_dict(self):
        breakdown = score_creator(
            platform="blog",
            bio="Food blogger",
            follower_count=5000,
        )
        d = breakdown.to_dict()
        assert "credibility_score" in d
        assert "composite_score" in d
        assert all(isinstance(v, float) for v in d.values())
