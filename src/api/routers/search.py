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
    served_from_cache = False

    for source in request.sources:
        try:
            if source == "blog":
                creators = _ingest_blog_results(db, request.query, request.max_results, force_live=request.force_live)
            elif source == "academic":
                creators = _ingest_academic_results(db, request.query, request.max_results, force_live=request.force_live)
            elif source == "twitter":
                creators = _ingest_twitter_results(db, request.query, request.max_results, force_live=request.force_live)
            elif source == "instagram":
                creators = _ingest_instagram_results(db, request.query, request.max_results, force_live=request.force_live)
            elif source == "youtube":
                creators, was_cached = _get_youtube_creators(db, request.query, request.max_results, force_live=request.force_live)
                if was_cached:
                    served_from_cache = True
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
        from_cache=served_from_cache,
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
    # Bootstrap: Ensure top YouTube channels exist as Creator records
    if not platform or platform == "youtube":
        _get_youtube_creators(db, query="", max_results=50)
        db.commit()

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

def _ingest_blog_results(db: Session, query: str, max_results: int, force_live: bool = False) -> list[Creator]:
    """Search for blogs related to the query and ingest articles.
    
    Supports both direct URLs (http://...) and keyword queries.
    For keyword queries, uses Google search to discover relevant blog URLs.
    """
    from src.db.models import Creator
    from src.ingestion.blog_scraper import scrape_blog

    # Determine which URLs to scrape
    if query.startswith("http"):
        blog_urls = [query]
    else:
        # Check DB first for keyword queries
        if not force_live:
            existing = db.query(Creator).filter(
                Creator.platform == "blog",
                (Creator.name.ilike(f"%{query}%")) | (Creator.bio.ilike(f"%{query}%"))
            ).limit(max_results).all()
            if len(existing) >= 3:
                logger.info(f"Returning {len(existing)} local DB hits for blog query '{query}'")
                return existing

        # Discover blog URLs from keyword query
        from src.ingestion.web_discovery import discover_blog_urls
        blog_urls = discover_blog_urls(query, max_results=min(max_results, 5))
        if not blog_urls:
            logger.info(f"No blog URLs discovered for query '{query}'")
            return []

    all_creators = []

    for blog_url in blog_urls:
        try:
            articles = scrape_blog(blog_url, max_posts=3)
            if not articles:
                continue

            # Group articles by author
            author_map: dict[str, list] = {}
            for article in articles:
                author = article.get("author", "Unknown Author")
                if author not in author_map:
                    author_map[author] = []
                author_map[author].append(article)

            for author_name, author_articles in author_map.items():
                creator = upsert_creator(db, {
                    "name": author_name,
                    "platform": "blog",
                    "platform_id": blog_url,
                    "profile_url": blog_url,
                    "bio": "",
                })

                content_texts = []
                for article in author_articles:
                    upsert_content_item(db, {
                        "creator_id": creator.id,
                        "source_type": "blog_post",
                        "title": article.get("title", ""),
                        "text_content": article.get("text_content", ""),
                        "url": article.get("url", ""),
                        "published_at": article.get("published_at", ""),
                    })
                    if article.get("text_content"):
                        content_texts.append(article["text_content"])

                # LLM alignment scoring
                alignment_score = 0.0
                if content_texts:
                    try:
                        from src.analysis.nlp import score_text_content
                        align_result = score_text_content(content_texts, target_topic=query)
                        alignment_score = float(align_result.alignment_score)
                    except Exception as e:
                        logger.error("Blog alignment scoring failed: %s", e)

                from src.analysis.scoring import score_creator
                breakdown = score_creator(
                    platform="blog",
                    bio=creator.bio or "",
                    follower_count=0,
                    alignment_score=alignment_score,
                )
                update_creator_scores(
                    db, creator.id,
                    credibility_score=breakdown.credibility_score,
                    engagement_score=breakdown.engagement_score,
                    reach_score=breakdown.reach_score,
                    alignment_score=alignment_score,
                    composite_score=breakdown.composite_score,
                )

                all_creators.append(creator)

                if len(all_creators) >= max_results:
                    return all_creators
        except Exception as e:
            logger.error("Blog scraping failed for %s: %s", blog_url, e)
            continue

    return all_creators


def _ingest_academic_results(db: Session, query: str, max_results: int, force_live: bool = False) -> list[Creator]:
    """Search academic databases and create creator records for authors."""
    from src.db.models import Creator
    from src.ingestion.academic import search_academic, extract_academic_creators

    # 1. Check local DB first
    db_query = db.query(Creator).filter(Creator.platform == "academic")
    if query:
        db_query = db_query.filter(
            (Creator.name.ilike(f"%{query}%")) | 
            (Creator.bio.ilike(f"%{query}%"))
        )
    existing = db_query.limit(max_results).all()
    if existing and (not query or len(existing) >= min(max_results, 2)) and not force_live:
        logger.info(f"Returning {len(existing)} local DB hits for academic query '{query}'")
        return existing

    # 2. Live Search
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

        # LLM alignment scoring against paper abstracts
        alignment_score = 0.0
        paper_texts = [p.get("abstract", "") for p in author_data.get("papers", []) if p.get("abstract")]
        if paper_texts:
            try:
                from src.analysis.nlp import score_text_content
                align_result = score_text_content(paper_texts, target_topic=query)
                alignment_score = float(align_result.alignment_score)
            except Exception as e:
                logger.error("Academic alignment scoring failed: %s", e)

        # Score the creator
        from src.analysis.scoring import score_creator
        breakdown = score_creator(
            platform="academic",
            bio=creator.bio or "",
            follower_count=0,
            h_index=author_data.get("h_index", 0),
            total_citations=author_data.get("total_citations", 0),
            alignment_score=alignment_score,
        )
        update_creator_scores(
            db, creator.id,
            credibility_score=breakdown.credibility_score,
            engagement_score=breakdown.engagement_score,
            reach_score=breakdown.reach_score,
            alignment_score=alignment_score,
            composite_score=breakdown.composite_score,
        )

        creators.append(creator)

    return creators


def _ingest_twitter_results(db: Session, query: str, max_results: int, force_live: bool = False) -> list[Creator]:
    """Scrape Twitter profiles and create creator records.
    
    Supports both direct handles (@username) and keyword queries.
    For keyword queries, uses Google search to discover relevant Twitter handles.
    """
    from src.db.models import Creator
    from src.ingestion.social_media import scrape_twitter_profile, normalize_social_content

    # Determine handles to scrape
    if query.startswith("@") or "/" in query:
        # Direct handle query
        handles = [query.lstrip("@").split("/")[-1]]
    else:
        # Check DB first for keyword queries
        if not force_live:
            existing = db.query(Creator).filter(
                Creator.platform == "twitter",
                (Creator.name.ilike(f"%{query}%")) | (Creator.bio.ilike(f"%{query}%"))
            ).limit(max_results).all()
            if len(existing) >= 3:
                logger.info(f"Returning {len(existing)} local DB hits for Twitter query '{query}'")
                return existing

        # Discover handles from keyword query
        from src.ingestion.web_discovery import discover_twitter_handles
        handles = discover_twitter_handles(query, max_results=max_results)
        if not handles:
            # Fallback: try the query as a handle
            handles = [query.lstrip("@").split("/")[-1]]

    all_creators = []
    for handle in handles:
        try:
            # Check if this specific handle exists in DB
            existing = db.query(Creator).filter(
                Creator.platform == "twitter",
                Creator.platform_id.ilike(handle)
            ).first()

            if existing and not force_live:
                all_creators.append(existing)
                continue

            profile = scrape_twitter_profile(handle)
            if not profile:
                continue

            creator = upsert_creator(db, {
                "name": profile.get("name", handle),
                "platform": "twitter",
                "platform_id": handle,
                "profile_url": profile.get("profile_url", ""),
                "bio": profile.get("bio", ""),
                "follower_count": profile.get("follower_count", 0),
            })

            content_items = normalize_social_content(profile)
            for item in content_items:
                item["creator_id"] = creator.id
                upsert_content_item(db, item)

            # LLM alignment scoring
            alignment_score = 0.0
            tweet_texts = [item.get("text_content", "") for item in content_items if item.get("text_content")]
            if tweet_texts:
                try:
                    from src.analysis.nlp import score_text_content
                    align_result = score_text_content(tweet_texts, target_topic=query)
                    alignment_score = float(align_result.alignment_score)
                except Exception as e:
                    logger.error("Twitter alignment scoring failed for %s: %s", handle, e)

            from src.analysis.scoring import score_creator
            breakdown = score_creator(
                platform="twitter",
                bio=creator.bio or "",
                follower_count=profile.get("follower_count", 0),
                alignment_score=alignment_score,
            )
            update_creator_scores(
                db, creator.id,
                credibility_score=breakdown.credibility_score,
                engagement_score=breakdown.engagement_score,
                reach_score=breakdown.reach_score,
                alignment_score=alignment_score,
                composite_score=breakdown.composite_score,
            )

            all_creators.append(creator)

            if len(all_creators) >= max_results:
                break
        except Exception as e:
            logger.error("Twitter scraping failed for %s: %s", handle, e)
            continue

    return all_creators


def _ingest_instagram_results(db: Session, query: str, max_results: int, force_live: bool = False) -> list[Creator]:
    """Scrape Instagram profiles and create creator records.
    
    Supports both direct handles (@username) and keyword queries.
    For keyword queries, uses Google search to discover relevant Instagram handles.
    """
    from src.db.models import Creator
    from src.ingestion.social_media import scrape_instagram_profile, normalize_social_content

    # Determine handles to scrape
    if query.startswith("@") or "/" in query:
        handles = [query.lstrip("@").split("/")[-1]]
    else:
        # Check DB first for keyword queries
        if not force_live:
            existing = db.query(Creator).filter(
                Creator.platform == "instagram",
                (Creator.name.ilike(f"%{query}%")) | (Creator.bio.ilike(f"%{query}%"))
            ).limit(max_results).all()
            if len(existing) >= 3:
                logger.info(f"Returning {len(existing)} local DB hits for Instagram query '{query}'")
                return existing

        # Discover handles from keyword query
        from src.ingestion.web_discovery import discover_instagram_handles
        handles = discover_instagram_handles(query, max_results=max_results)
        if not handles:
            handles = [query.lstrip("@").split("/")[-1]]

    all_creators = []
    for handle in handles:
        try:
            existing = db.query(Creator).filter(
                Creator.platform == "instagram",
                Creator.platform_id.ilike(handle)
            ).first()

            if existing and not force_live:
                all_creators.append(existing)
                continue

            profile = scrape_instagram_profile(handle)
            if not profile:
                continue

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

            # LLM alignment scoring
            alignment_score = 0.0
            post_texts = [item.get("text_content", "") for item in content_items if item.get("text_content")]
            if post_texts:
                try:
                    from src.analysis.nlp import score_text_content
                    align_result = score_text_content(post_texts, target_topic=query)
                    alignment_score = float(align_result.alignment_score)
                except Exception as e:
                    logger.error("Instagram alignment scoring failed for %s: %s", handle, e)

            from src.analysis.scoring import score_creator
            breakdown = score_creator(
                platform="instagram",
                bio=creator.bio or "",
                follower_count=profile.get("follower_count", 0),
                alignment_score=alignment_score,
            )
            update_creator_scores(
                db, creator.id,
                credibility_score=breakdown.credibility_score,
                engagement_score=breakdown.engagement_score,
                reach_score=breakdown.reach_score,
                alignment_score=alignment_score,
                composite_score=breakdown.composite_score,
            )

            all_creators.append(creator)

            if len(all_creators) >= max_results:
                break
        except Exception as e:
            logger.error("Instagram scraping failed for %s: %s", handle, e)
            continue

    return all_creators


def _get_youtube_creators(db: Session, query: str, max_results: int, force_live: bool = False) -> tuple[list[Creator], bool]:
    """Search for YouTube channels matching the query, fetch transcripts, and score.
    
    Returns a tuple of (creators, from_cache).
    If query is empty (e.g. dashboard load bootstrap), bypasses the live API and returns existing DB records.
    If query matches existing creators in the DB (>= 3 matches), return those first to save API quota & time.
    If force_live is True, always skip the cache and hit the YouTube API.
    """
    from src.db.models import Creator
    
    if not force_live:
        # 1. Check local DB first
        db_query = db.query(Creator).filter(Creator.platform == "youtube").order_by(desc(Creator.composite_score))
        
        if query:
            db_query = db_query.filter(
                (Creator.name.ilike(f"%{query}%")) | 
                (Creator.bio.ilike(f"%{query}%"))
            )
            
        cached_creators = db_query.limit(max_results).all()
        
        # If we found enough creators locally (>= 3 or bootstrap empty query), return them!
        if cached_creators and (not query or len(cached_creators) >= 3):
            logger.info(f"Returning {len(cached_creators)} local DB hits for query '{query}'")
            return cached_creators, True

    # 2. Active Live Search (Fallback for new queries)
    logger.info(f"No local matches found for '{query}'. Hitting YouTube API...")
    import os
    from src.ingestion.youtube_api import YouTubeDataAPI
    from src.ingestion.transcripts import fetch_transcript
    from src.ingestion.cleaner import clean_transcript
    from src.analysis.scoring import score_creator
    from src.analysis.nlp import score_text_content

    api_key = os.getenv("YOUTUBE_API_KEY")
    if not api_key:
        logger.error("YOUTUBE_API_KEY environment variable is not set")
        return []

    yt = YouTubeDataAPI(api_key)
    try:
        channels = yt.search_channels(query, max_results=max_results)
    except Exception as e:
        logger.error("YouTube search API failed: %s", e)
        return []

    creators = []
    for ch_data in channels:
        channel_id = ch_data["channel_id"]
        
        creator = upsert_creator(db, {
            "name": ch_data["title"],
            "platform": "youtube",
            "platform_id": channel_id,
            "profile_url": f"https://youtube.com/channel/{channel_id}",
            "bio": ch_data.get("description", ""),
            "follower_count": ch_data.get("subscriber_count", 0),
        })

        try:
            # Fetch 3 latest videos to grab some quick transcript text for alignment context
            videos = yt.get_latest_videos(channel_id, count=3)
        except Exception as e:
            logger.warning("Could not fetch videos for %s: %s", channel_id, e)
            videos = []
            
        transcript_texts = []
        for vid in videos:
            video_id = vid["video_id"]
            raw_transcript = fetch_transcript(video_id)
            if raw_transcript:
                cleaned = clean_transcript(raw_transcript)
                # Combine all text chunks into a single string
                full_text = " ".join(chunk.get("text", "") for chunk in cleaned)
                
                if full_text.strip():
                    transcript_texts.append(full_text)
                    
                    # Store the transcript locally in the unified content table
                    upsert_content_item(db, {
                        "creator_id": creator.id,
                        "source_type": "youtube_video",
                        "title": vid["title"],
                        "text_content": full_text,
                        "url": f"https://youtube.com/watch?v={video_id}",
                        "published_at": vid.get("published_at", ""),
                    })
        
        # Determine dynamic alignment via LLM analysis of transcripts vs the active query 
        alignment_score = 0.0
        if transcript_texts:
            try:
                align_result = score_text_content(transcript_texts, target_topic=query)
                alignment_score = float(align_result.alignment_score)
            except Exception as e:
                logger.error("LLM Alignment scoring failed for %s: %s", channel_id, e)

        breakdown = score_creator(
            platform="youtube",
            bio=creator.bio or "",
            follower_count=creator.follower_count or 0,
            alignment_score=alignment_score,
        )
        
        update_creator_scores(
            db, creator.id,
            credibility_score=breakdown.credibility_score,
            engagement_score=breakdown.engagement_score,
            reach_score=breakdown.reach_score,
            alignment_score=alignment_score,
            composite_score=breakdown.composite_score,
        )
        
        creators.append(creator)

    db.commit()
    return creators, False
