"""Briefings API router — generate and retrieve briefings."""

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from sqlalchemy.orm import Session

from src.api.deps import get_db, DATABASE_URL
from src.api.schemas import BriefingRequest, BriefingResponse, BriefingAcceptedResponse
from src.api.tasks import generate_briefing_task
from src.db.dao import create_briefing, get_briefing
from src.db.models import Creator, Briefing

router = APIRouter(prefix="/api/briefings", tags=["briefings"])


@router.post("/generate", response_model=BriefingAcceptedResponse, status_code=202)
def trigger_briefing(
    request: BriefingRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    """Trigger async briefing generation for a creator."""
    # Verify creator exists
    creator = db.get(Creator, request.creator_id)
    if creator is None:
        raise HTTPException(status_code=404, detail="Creator not found")

    # Create pending briefing record
    briefing = create_briefing(db, request.creator_id)
    db.commit()

    # Schedule background generation
    background_tasks.add_task(
        generate_briefing_task,
        briefing_id=briefing.id,
        creator_id=request.creator_id,
        db_url=DATABASE_URL,
        campaign_context=request.campaign_context,
    )

    return BriefingAcceptedResponse(briefing_id=briefing.id)


@router.get("/debug")
def debug_briefings(db: Session = Depends(get_db)):
    """Debug endpoint to see recent briefings and their statuses."""
    briefings = db.query(Briefing).order_by(Briefing.created_at.desc()).limit(5).all()
    return [{"id": b.id, "status": b.status, "content": b.content} for b in briefings]


@router.get("/{briefing_id}", response_model=BriefingResponse)
def get_briefing_endpoint(briefing_id: str, db: Session = Depends(get_db)):
    """Retrieve a briefing by ID."""
    briefing = get_briefing(db, briefing_id)
    if briefing is None:
        raise HTTPException(status_code=404, detail="Briefing not found")
    return BriefingResponse.model_validate(briefing)
