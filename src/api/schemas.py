"""Pydantic response/request schemas for the API."""

from typing import Optional
from pydantic import BaseModel, ConfigDict


# ── Channel / Creator Schemas ────────────────────────────────────────────

class ChannelResponse(BaseModel):
    """Compact channel representation for list endpoints."""
    model_config = ConfigDict(from_attributes=True)

    id: str
    title: str
    description: str
    subscriber_count: int
    video_count: int
    alignment_score: Optional[int] = None


class QuoteResponse(BaseModel):
    """A quote extracted during analysis."""
    text: str
    timestamp: str


class ChannelDetailResponse(BaseModel):
    """Full channel details including alignment quotes."""
    model_config = ConfigDict(from_attributes=True)

    id: str
    title: str
    description: str
    subscriber_count: int
    video_count: int
    alignment_score: Optional[int] = None
    alignment_quotes: Optional[list[dict]] = None


class CreatorListResponse(BaseModel):
    """Paginated list of creators."""
    creators: list[ChannelResponse]
    total: int
    limit: int
    offset: int


# ── Briefing Schemas ─────────────────────────────────────────────────────

class BriefingRequest(BaseModel):
    """Request body for triggering briefing generation."""
    channel_id: str
    campaign_context: Optional[str] = None


class BriefingResponse(BaseModel):
    """Briefing record."""
    model_config = ConfigDict(from_attributes=True)

    id: str
    channel_id: str
    content: Optional[str] = None
    status: str


class BriefingAcceptedResponse(BaseModel):
    """Response for accepted briefing generation."""
    status: str = "accepted"
    briefing_id: str


# ── Multi-Source Creator Schemas ─────────────────────────────────────────

class CompositeScoreBreakdown(BaseModel):
    """Breakdown of composite scoring dimensions."""
    credibility_score: float = 0
    engagement_score: float = 0
    reach_score: float = 0
    alignment_score: float = 0
    composite_score: float = 0


class CreatorMultiResponse(BaseModel):
    """Compact multi-source creator representation."""
    model_config = ConfigDict(from_attributes=True)

    id: str
    name: str
    platform: str
    platform_id: Optional[str] = None
    profile_url: Optional[str] = None
    follower_count: int = 0
    credibility_score: Optional[float] = None
    engagement_score: Optional[float] = None
    reach_score: Optional[float] = None
    alignment_score: Optional[float] = None
    composite_score: Optional[float] = None


class ContentItemResponse(BaseModel):
    """A content item (blog post, tweet, paper, etc.)."""
    model_config = ConfigDict(from_attributes=True)

    id: str
    source_type: str
    title: str = ""
    text_content: str = ""
    url: Optional[str] = None
    published_at: str = ""
    engagement_metrics: Optional[dict] = None


class CreatorMultiDetailResponse(BaseModel):
    """Full multi-source creator details including scores and content."""
    id: str
    name: str
    platform: str
    platform_id: str = ""
    profile_url: str = ""
    bio: str = ""
    follower_count: int = 0
    scores: CompositeScoreBreakdown = CompositeScoreBreakdown()
    content_items: list[ContentItemResponse] = []


class CreatorMultiListResponse(BaseModel):
    """Paginated list of multi-source creators."""
    creators: list[CreatorMultiResponse]
    total: int
    limit: int
    offset: int


class SearchRequest(BaseModel):
    """Request body for multi-source search."""
    query: str
    sources: list[str] = ["youtube", "blog", "academic"]
    max_results: int = 10


class SearchResponse(BaseModel):
    """Response from multi-source search."""
    creators: list[CreatorMultiResponse]
    total: int
    query: str
    sources: list[str]
