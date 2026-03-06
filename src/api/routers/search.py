"""Search API router — unified multi-source discovery and creator listing."""

import logging
from typing import Optional

from fastapi import APIRouter, BackgroundTasks, Depends, Query
from sqlalchemy import desc
from sqlalchemy.orm import Session

from src.api.deps import get_db
from src.api.schemas import (
    CreatorMultiResponse,
    CreatorMultiDetailResponse,
    CreatorMultiListResponse,
    ContentItemResponse,
    SearchRequest,
    SearchResponse,
    CompositeScoreBreakdown,
)
from src.db.models import Creator, ContentItem
from src.db.dao import (
    get_creators_ranked,
    get_content_items,
    upsert_creator,
    upsert_content_item,
    update_creator_scores,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/search", tags=["search"])


@router.post("", response_model=SearchResponse, status_code=200)
def search_creators(
    request: SearchRequest,
    db: Session = Depends(get_db),
):
    """Search for creators across multiple sources.

    Triggers ingestion from selected sources, stores results, and
    returns discovered creators.
    """
    all_creators = []

    for source in request.sources:
        try:
            if source == "blog":
                creators = _ingest_blog_results(db, request.query, request.max_results)
            elif source == "academic":
                creators = _ingest_academic_results(db, request.query, request.max_results)
            elif source == "twitter":
                creators = _ingest_twitter_results(db, request.query, request.max_results)
            elif source == "instagram":
                creators = _ingest_instagram_results(db, request.query, request.max_results)
            elif source == "youtube":
                # YouTube uses the existing pipeline — just return existing results
                creators = _get_youtube_creators(db, request.query, request.max_results)
            else:
                continue
            all_creators.extend(creators)
        except Exception as e:
            logger.error("Search failed for source %s: %s", source, e)

    db.commit()

    return SearchResponse(
        creators=[CreatorMultiResponse.model_validate(c) for c in all_creators],
        total=len(all_creators),
        query=request.query,
        sources=request.sources,
    )


# ── Multi-source Creator Endpoints ──────────────────────────────────────

@router.get("/creators", response_model=CreatorMultiListResponse)
def list_multi_creators(
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    platform: Optional[str] = Query(None),
    min_score: Optional[float] = Query(None, ge=0, le=100),
    db: Session = Depends(get_db),
):
    """List creators from all sources, ranked by composite score."""
    creators, total = get_creators_ranked(
        db,
        platform=platform,
        min_score=min_score,
        limit=limit,
        offset=offset,
    )

    return CreatorMultiListResponse(
        creators=[CreatorMultiResponse.model_validate(c) for c in creators],
        total=total,
        limit=limit,
        offset=offset,
    )


@router.get("/creators/{creator_id}", response_model=CreatorMultiDetailResponse)
def get_multi_creator_detail(
    creator_id: str,
    db: Session = Depends(get_db),
):
    """Get full details for a specific multi-source creator."""
    from fastapi import HTTPException

    creator = db.get(Creator, creator_id)
    if creator is None:
        raise HTTPException(status_code=404, detail="Creator not found")

    content = get_content_items(db, creator_id)

    return CreatorMultiDetailResponse(
        id=creator.id,
        name=creator.name,
        platform=creator.platform,
        platform_id=creator.platform_id or "",
        profile_url=creator.profile_url or "",
        bio=creator.bio or "",
        follower_count=creator.follower_count or 0,
        scores=CompositeScoreBreakdown(
            credibility_score=creator.credibility_score or 0,
            engagement_score=creator.engagement_score or 0,
            reach_score=creator.reach_score or 0,
            alignment_score=creator.alignment_score or 0,
            composite_score=creator.composite_score or 0,
        ),
        content_items=[ContentItemResponse.model_validate(item) for item in content],
    )


# ── Source-Specific Ingestors ────────────────────────────────────────────

def _ingest_blog_results(db: Session, query: str, max_results: int) -> list[Creator]:
    """Search for blogs related to the query and ingest articles."""
    from src.ingestion.blog_scraper import scrape_blog

    # Use the query as a blog URL hint — users can pass blog URLs directly
    # For keyword queries, this won't find results (expected)
    if query.startswith("http"):
        articles = scrape_blog(query, max_posts=max_results)
        if not articles:
            return []

        # Group articles by author
        author_map: dict[str, list] = {}
        for article in articles:
            author = article.get("author", "Unknown Author")
            if author not in author_map:
                author_map[author] = []
            author_map[author].append(article)

        creators = []
        for author_name, author_articles in author_map.items():
            creator = upsert_creator(db, {
                "name": author_name,
                "platform": "blog",
                "platform_id": query,
                "profile_url": query,
                "bio": "",
            })

            for article in author_articles:
                upsert_content_item(db, {
                    "creator_id": creator.id,
                    "source_type": "blog_post",
                    "title": article.get("title", ""),
                    "text_content": article.get("text_content", ""),
                    "url": article.get("url", ""),
                    "published_at": article.get("published_at", ""),
                })

            creators.append(creator)
        return creators

    return []


def _ingest_academic_results(db: Session, query: str, max_results: int) -> list[Creator]:
    """Search academic databases and create creator records for authors."""
    from src.ingestion.academic import search_academic, extract_academic_creators

    papers = search_academic(query, limit=max_results)
    if not papers:
        return []

    author_map = extract_academic_creators(papers)
    creators = []

    for author_name, author_data in author_map.items():
        creator = upsert_creator(db, {
            "name": author_name,
            "platform": "academic",
            "platform_id": author_data.get("author_id", ""),
            "profile_url": author_data.get("profile_url", ""),
            "bio": ", ".join(author_data.get("affiliations", [])),
            "follower_count": 0,
        })

        for paper in author_data.get("papers", []):
            upsert_content_item(db, {
                "creator_id": creator.id,
                "source_type": "paper",
                "title": paper.get("title", ""),
                "text_content": paper.get("abstract", ""),
                "url": paper.get("url", ""),
                "published_at": str(paper.get("year", "")),
                "engagement_metrics": {
                    "citations": paper.get("citation_count", 0),
                },
            })

        # Score the creator
        from src.analysis.scoring import score_creator
        breakdown = score_creator(
            platform="academic",
            bio=creator.bio or "",
            follower_count=0,
            h_index=author_data.get("h_index", 0),
            total_citations=author_data.get("total_citations", 0),
        )
        update_creator_scores(
            db, creator.id,
            credibility_score=breakdown.credibility_score,
            engagement_score=breakdown.engagement_score,
            reach_score=breakdown.reach_score,
            composite_score=breakdown.composite_score,
        )

        creators.append(creator)

    return creators


def _ingest_twitter_results(db: Session, query: str, max_results: int) -> list[Creator]:
    """Scrape Twitter profile and create creator record."""
    from src.ingestion.social_media import scrape_twitter_profile, normalize_social_content

    # Query should be a Twitter handle
    handle = query.lstrip("@").split("/")[-1]
    profile = scrape_twitter_profile(handle)

    if not profile:
        return []

    creator = upsert_creator(db, {
        "name": profile.get("name", handle),
        "platform": "twitter",
        "platform_id": handle,
        "profile_url": profile.get("profile_url", ""),
        "bio": profile.get("bio", ""),
        "follower_count": profile.get("follower_count", 0),
    })

    # Store tweets as content items
    content_items = normalize_social_content(profile)
    for item in content_items:
        item["creator_id"] = creator.id
        upsert_content_item(db, item)

    # Score
    from src.analysis.scoring import score_creator
    breakdown = score_creator(
        platform="twitter",
        bio=creator.bio or "",
        follower_count=profile.get("follower_count", 0),
    )
    update_creator_scores(
        db, creator.id,
        credibility_score=breakdown.credibility_score,
        engagement_score=breakdown.engagement_score,
        reach_score=breakdown.reach_score,
        composite_score=breakdown.composite_score,
    )

    return [creator]


def _ingest_instagram_results(db: Session, query: str, max_results: int) -> list[Creator]:
    """Scrape Instagram profile and create creator record."""
    from src.ingestion.social_media import scrape_instagram_profile, normalize_social_content

    handle = query.lstrip("@").split("/")[-1]
    profile = scrape_instagram_profile(handle)

    if not profile:
        return []

    creator = upsert_creator(db, {
        "name": profile.get("name", handle),
        "platform": "instagram",
        "platform_id": handle,
        "profile_url": profile.get("profile_url", ""),
        "bio": profile.get("bio", ""),
        "follower_count": profile.get("follower_count", 0),
    })

    content_items = normalize_social_content(profile)
    for item in content_items:
        item["creator_id"] = creator.id
        upsert_content_item(db, item)

    from src.analysis.scoring import score_creator
    breakdown = score_creator(
        platform="instagram",
        bio=creator.bio or "",
        follower_count=profile.get("follower_count", 0),
    )
    update_creator_scores(
        db, creator.id,
        credibility_score=breakdown.credibility_score,
        engagement_score=breakdown.engagement_score,
        reach_score=breakdown.reach_score,
        composite_score=breakdown.composite_score,
    )

    return [creator]


def _get_youtube_creators(db: Session, query: str, max_results: int) -> list[Creator]:
    """Return existing YouTube creators matching a query (no new ingestion)."""
    from src.db.models import Channel

    channels = (
        db.query(Channel)
        .filter(Channel.title.ilike(f"%{query}%"))
        .order_by(desc(Channel.alignment_score))
        .limit(max_results)
        .all()
    )

    # Convert Channel records to Creator format on-the-fly
    creators = []
    for ch in channels:
        creator = upsert_creator(db, {
            "name": ch.title,
            "platform": "youtube",
            "platform_id": ch.id,
            "profile_url": f"https://youtube.com/channel/{ch.id}",
            "bio": ch.description or "",
            "follower_count": ch.subscriber_count or 0,
        })

        if ch.alignment_score is not None:
            from src.analysis.scoring import score_creator
            breakdown = score_creator(
                platform="youtube",
                bio=ch.description or "",
                follower_count=ch.subscriber_count or 0,
                alignment_score=float(ch.alignment_score),
            )
            update_creator_scores(
                db, creator.id,
                credibility_score=breakdown.credibility_score,
                engagement_score=breakdown.engagement_score,
                reach_score=breakdown.reach_score,
                alignment_score=float(ch.alignment_score),
                composite_score=breakdown.composite_score,
            )

        creators.append(creator)

    return creators
