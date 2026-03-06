import logging
import os
from typing import Optional

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from src.db.models import Channel, create_tables
from src.db.dao import get_top_chunks, update_briefing
from src.analysis.nlp import get_embedding, score_chunks

logger = logging.getLogger(__name__)

BRIEFING_PROMPT_TEMPLATE = """You are a campaign strategist writing a one-page engagement briefing.

Based on the creator's metadata and content excerpts provided below, generate a professional, concise outreach cheat sheet.

## Source Data
- **Name:** {channel_title}
- **Subscribers:** {subscriber_count:,}
- **Alignment Score:** {alignment_score}/100
- **Campaign Topic:** {topic}

### Key Quotes
{quotes_section}

### Content Excerpts
{chunks_section}

---

## Instructions
Write the briefing in Markdown using specifically these 6 sections:
1. **Creator Profile** — Summary of who they are and their content niche.
2. **Mission Relevance** — Why this creator is a high-value/natural fit for the campaign topic "{topic}".
3. **Key Topics** — The recurring themes in their content that align with our mission.
4. **Metrics** — Highlight their subscriber count and reach.
5. **Example Content** — Cite specific quotes or excerpts provided above that demonstrate their alignment.
6. **Suggested Talking Points** — 3-5 specific, natural hooks we can use for outreach.

Keep it professional, evidence-based, and exactly under one page (~400-500 words)."""


def generate_briefing_task(
    briefing_id: str,
    channel_id: str,
    db_url: str,
    campaign_context: Optional[str] = None,
    topic: str = "plant-based health, sustainable food systems",
):
    """Background task: generate an engagement briefing for a channel.

    This runs asynchronously via FastAPI BackgroundTasks.
    """
    engine = create_engine(db_url, echo=False)
    create_tables(engine)

    try:
        with Session(engine) as session:
            channel = session.get(Channel, channel_id)
            if channel is None:
                update_briefing(session, briefing_id, "Channel not found", "failed")
                session.commit()
                return

            # Get top aligned chunks
            target_embedding = get_embedding(topic)
            top_chunks = get_top_chunks(session, channel_id, target_embedding, limit=10)

            # Build the prompt
            quotes_section = ""
            if channel.alignment_quotes:
                for q in channel.alignment_quotes:
                    quotes_section += f'- "{q.get("text", "")}" ({q.get("timestamp", "")})\n'
            else:
                quotes_section = "- No quotes available\n"

            chunks_section = ""
            for i, chunk in enumerate(top_chunks[:5], 1):
                chunks_section += f"\n**Excerpt {i}:**\n> {chunk.text[:300]}...\n"

            if not chunks_section:
                chunks_section = "No aligned content excerpts available."

            prompt = BRIEFING_PROMPT_TEMPLATE.format(
                channel_title=channel.title,
                subscriber_count=channel.subscriber_count or 0,
                alignment_score=channel.alignment_score or 0,
                quotes_section=quotes_section,
                chunks_section=chunks_section,
                topic=topic,
            )

            if campaign_context:
                prompt += f"\n\n**Additional Campaign Context:** {campaign_context}"

            # Call Gemini
            from google import genai
            from google.genai import types

            client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
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

            update_briefing(session, briefing_id, content, "completed")
            session.commit()
            logger.info("Briefing %s completed for channel %s", briefing_id, channel_id)

    except Exception as e:
        logger.error("Briefing generation failed: %s", e)
        try:
            with Session(engine) as session:
                update_briefing(session, briefing_id, str(e), "failed")
                session.commit()
        except Exception:
            logger.exception("Failed to update briefing status")
