"""Creators API router — list and detail endpoints."""

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import desc
from sqlalchemy.orm import Session

from src.api.deps import get_db
from src.api.schemas import ChannelResponse, ChannelDetailResponse, CreatorListResponse
from src.db.models import Channel

router = APIRouter(prefix="/api/creators", tags=["creators"])


@router.get("", response_model=CreatorListResponse)
def list_creators(
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    min_score: Optional[int] = Query(None, ge=0, le=100),
    db: Session = Depends(get_db),
):
    """List creators sorted by alignment score, with optional score filter."""
    query = db.query(Channel)

    if min_score is not None:
        query = query.filter(Channel.alignment_score >= min_score)

    # Count total before pagination
    total = query.count()

    creators = (
        query
        .order_by(desc(Channel.alignment_score))
        .offset(offset)
        .limit(limit)
        .all()
    )

    return CreatorListResponse(
        creators=[ChannelResponse.model_validate(c) for c in creators],
        total=total,
        limit=limit,
        offset=offset,
    )


@router.get("/{channel_id}", response_model=ChannelDetailResponse)
def get_creator(channel_id: str, db: Session = Depends(get_db)):
    """Get full details for a specific creator."""
    channel = db.get(Channel, channel_id)
    if channel is None:
        raise HTTPException(status_code=404, detail="Channel not found")
    return ChannelDetailResponse.model_validate(channel)
