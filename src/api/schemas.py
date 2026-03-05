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
