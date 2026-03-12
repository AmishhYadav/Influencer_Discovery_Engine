import logging
import os
from typing import Optional

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from src.db.models import Creator, ContentItem
from src.db.dao import update_briefing

logger = logging.getLogger(__name__)

BRIEFING_PROMPT_TEMPLATE = """You are preparing a polished, executive-level **Influencer Engagement Briefing** for an advocacy team.

The team needs this briefing to evaluate whether to pursue a partnership with this creator. Write it as if you're presenting to a VP of Marketing.

---

## Creator Intel

| Field | Value |
|-------|-------|
| **Name** | {creator_name} |
| **Platform** | {platform} |
| **Audience** | {follower_count:,} |
| **Alignment Score** | {alignment_score}/100 |
| **Campaign Focus** | {topic} |

### Content Samples
{chunks_section}

---

## Output Format

Write an **engagement briefing** in polished Markdown using these sections. Use the exact headings below:

### 🎯 Creator Snapshot
A 2-3 sentence executive summary: who they are, why they matter, and their core content niche. Make this punchy and compelling.

### 🔗 Mission Alignment
A detailed paragraph explaining *exactly why* this creator is a natural fit for the campaign topic "{topic}". Reference specific content themes. Avoid generic statements — be precise about what makes them uniquely valuable.

### 📊 Credibility & Reach Assessment
Analyze their authority signals: platform presence, professional credentials, audience quality indicators, and any expertise markers visible in their content or bio.

### 💡 Key Content Themes
A bullet list of 4-6 recurring themes from their content that overlap with our advocacy goals. Each bullet should include a brief supporting observation.

### 📝 Evidence & Quotes
Cite 3-5 specific quotes, ideas, or content excerpts from the samples above. Format each as a blockquote with brief context.

### 🤝 Outreach Strategy
Provide 4-5 specific, actionable talking points for initial outreach. These should feel natural, reference their actual content, and avoid sounding transactional. Frame each as a conversation opener.

---

## Quality Guidelines
- Write in a confident, professional tone suitable for a strategy presentation
- Use specific evidence from the content samples — never make up quotes
- Keep the total briefing between 500-700 words
- Use Markdown formatting (headers, bold, bullet points, blockquotes) for readability
- If content samples are limited, note this honestly rather than fabricating details"""


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
                preview = item.text_content[:800] + "..." if len(item.text_content) > 800 else item.text_content
                chunks_section += f"\n**Sample {i} — {item.source_type.replace('_', ' ').title()}** ({item.title or 'Untitled'}):\n> {preview}\n"

            if not chunks_section.strip():
                chunks_section = "_No content samples available. Base the briefing on the creator's profile metadata only._"

            prompt = BRIEFING_PROMPT_TEMPLATE.format(
                creator_name=creator.name,
                platform=creator.platform.title(),
                follower_count=creator.follower_count or 0,
                alignment_score=creator.alignment_score or 0,
                chunks_section=chunks_section,
                topic=topic,
            )

            if campaign_context:
                prompt += f"\n\n---\n**Additional Campaign Context from the team:** {campaign_context}"

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
                    system_instruction="You are a senior campaign strategist at a top advocacy organization. You write polished, evidence-based influencer engagement briefings that are used by leadership to make partnership decisions. Your writing is professional, specific, and persuasive.",
                    temperature=0.4,
                    max_output_tokens=2500,
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
