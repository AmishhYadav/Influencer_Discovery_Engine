import logging
import os
from typing import Optional

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from src.db.models import Creator, ContentItem
from src.db.dao import update_briefing

logger = logging.getLogger(__name__)

BRIEFING_PROMPT_TEMPLATE = """You are a campaign strategist writing a one-page engagement briefing.

Based on the creator's metadata and content excerpts provided below, generate a professional, concise outreach cheat sheet.

## Source Data
- **Name:** {creator_name}
- **Platform:** {platform}
- **Followers/Reach:** {follower_count:,}
- **Alignment Score:** {alignment_score}/100
- **Campaign Topic:** {topic}

### Content Excerpts
{chunks_section}

---

## Instructions
Write the briefing in Markdown using specifically these 6 sections:
1. **Creator Profile** — Summary of who they are and their content niche.
2. **Mission Relevance** — Why this creator is a high-value/natural fit for the campaign topic "{topic}".
3. **Key Topics** — The recurring themes in their content that align with our mission.
4. **Metrics** — Highlight their subscriber/follower count and reach.
5. **Example Content** — Cite specific quotes or excerpts provided above that demonstrate their alignment.
6. **Suggested Talking Points** — 3-5 specific, natural hooks we can use for outreach.

Keep it professional, evidence-based, and exactly under one page (~400-500 words)."""


def generate_briefing_task(
    briefing_id: str,
    creator_id: str,
    db_url: str,
    campaign_context: Optional[str] = None,
    topic: str = "plant-based health, sustainable food systems",
):
    """Background task: generate an engagement briefing for any creator.

    This runs asynchronously via FastAPI BackgroundTasks.
    """
    engine = create_engine(db_url, echo=False)

    try:
        print(f"[BRIEFING] Starting generation for briefing={briefing_id}, creator={creator_id}")
        with Session(engine) as session:
            creator = session.get(Creator, creator_id)
            if creator is None:
                print(f"[BRIEFING] ERROR: Creator {creator_id} not found in DB")
                update_briefing(session, briefing_id, "Creator not found", "failed")
                session.commit()
                return

            print(f"[BRIEFING] Found creator: {creator.name} ({creator.platform})")

            # Grab their recent content items to feed the LLM
            content_items = (
                session.query(ContentItem)
                .filter(ContentItem.creator_id == creator_id)
                .order_by(ContentItem.created_at.desc())
                .limit(5)
                .all()
            )

            print(f"[BRIEFING] Found {len(content_items)} content items")

            chunks_section = ""
            for i, item in enumerate(content_items, 1):
                preview = item.text_content[:500] + "..." if len(item.text_content) > 500 else item.text_content
                chunks_section += f"\n**Excerpt {i} ({item.source_type}):**\n> {preview}\n"

            if not chunks_section.strip():
                chunks_section = "No aligned content excerpts available."

            prompt = BRIEFING_PROMPT_TEMPLATE.format(
                creator_name=creator.name,
                platform=creator.platform.title(),
                follower_count=creator.follower_count or 0,
                alignment_score=creator.alignment_score or 0,
                chunks_section=chunks_section,
                topic=topic,
            )

            if campaign_context:
                prompt += f"\n\n**Additional Campaign Context:** {campaign_context}"

            # Call Gemini
            print(f"[BRIEFING] Calling Gemini API...")
            from google import genai
            from google.genai import types

            api_key = os.getenv("GEMINI_API_KEY")
            if not api_key:
                raise ValueError("GEMINI_API_KEY environment variable is not set!")

            client = genai.Client(api_key=api_key)
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=[
                    types.Content(role="user", parts=[types.Part.from_text(text=prompt)])
                ],
                config=types.GenerateContentConfig(
                    system_instruction="You are a campaign strategist.",
                    temperature=0.5,
                    max_output_tokens=1500,
                ),
            )
            content = response.text
            print(f"[BRIEFING] ✅ Gemini responded with {len(content)} chars")

            update_briefing(session, briefing_id, content, "completed")
            session.commit()
            print(f"[BRIEFING] ✅ Briefing {briefing_id} saved as 'completed'")
            logger.info("Briefing %s completed for creator %s", briefing_id, creator_id)

    except Exception as e:
        print(f"[BRIEFING] ❌ FAILED: {e}")
        logger.error("Briefing generation failed: %s", e, exc_info=True)
        try:
            with Session(engine) as session:
                update_briefing(session, briefing_id, str(e), "failed")
                session.commit()
                print(f"[BRIEFING] Marked briefing {briefing_id} as 'failed'")
        except Exception as e2:
            print(f"[BRIEFING] ❌ Could not even mark as failed: {e2}")
            logger.exception("Failed to update briefing status")
