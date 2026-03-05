"""NLP analysis engine — OpenAI embeddings and LLM-based alignment scoring."""

import logging
import os
from typing import Optional

from openai import OpenAI
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


# ── Pydantic Schemas ─────────────────────────────────────────────────────

class QuoteItem(BaseModel):
    """A quote extracted from a transcript chunk."""
    text: str = Field(description="The exact quote from the transcript")
    timestamp: str = Field(description="Approximate timestamp in MM:SS format")


class AlignmentResult(BaseModel):
    """Structured output from the LLM alignment judge."""
    alignment_score: int = Field(
        ge=0, le=100,
        description="0-100 score: how well the content aligns with the target topic without being explicitly activist",
    )
    reasoning: str = Field(
        description="Brief explanation of the score",
    )
    quotes: list[QuoteItem] = Field(
        default_factory=list,
        description="Top 3-5 quotes that justify the alignment score",
    )


# ── Client ───────────────────────────────────────────────────────────────

_client: Optional[OpenAI] = None


def _get_client() -> OpenAI:
    """Lazy-initialize the OpenAI client."""
    global _client
    if _client is None:
        _client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    return _client


def set_client(client: OpenAI) -> None:
    """Override the OpenAI client (useful for testing)."""
    global _client
    _client = client


# ── Embeddings ───────────────────────────────────────────────────────────

EMBEDDING_MODEL = "text-embedding-3-small"
EMBEDDING_DIM = 1536


def get_embedding(text: str) -> list[float]:
    """Get a single embedding vector for a text string."""
    client = _get_client()
    response = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=text,
    )
    return response.data[0].embedding


def get_embeddings(texts: list[str]) -> list[list[float]]:
    """Get embedding vectors for multiple text strings in one API call."""
    if not texts:
        return []
    client = _get_client()
    response = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=texts,
    )
    # Sort by index to maintain order
    sorted_data = sorted(response.data, key=lambda x: x.index)
    return [item.embedding for item in sorted_data]


# ── LLM Scoring ──────────────────────────────────────────────────────────

SCORING_MODEL = "gpt-4o-mini"

SYSTEM_PROMPT = """You are an expert content analyst specializing in identifying creators whose content naturally aligns with advocacy topics WITHOUT being explicitly activist.

Your task is to evaluate transcript chunks from a YouTube creator and determine how well their content aligns with the target topic.

## Scoring Rubric (0-100)

### High Alignment (70-100):
- Content naturally covers the target topic through science, health, lifestyle, or education
- Creator discusses the topic with authority and genuine interest
- Content would appeal to audiences interested in the target topic
- Language is informative, positive, and accessible

### Medium Alignment (40-69):
- Content occasionally touches on the target topic
- Creator may discuss related subjects but not as a primary focus
- Some relevant content mixed with unrelated material

### Low Alignment (0-39):
- Content rarely or never relates to the target topic
- Creator focuses on completely different subjects

## CRITICAL PENALTIES (subtract 20-40 points):
- Explicitly polarizing language ("you must", "everyone should", "it's wrong to")
- Protest-oriented activism or call-to-action rhetoric
- Shaming, guilt-tripping, or moral superiority
- Aggressive debate or confrontational tone
- Political framing of the topic

The ideal creator scores HIGH: they naturally discuss the topic in a way that educates and inspires, without being preachy or explicitly activist. Think: a nutritionist discussing plant-based diets for health benefits, NOT an activist telling people to go vegan.

Extract 3-5 quotes that best justify your score. Include approximate timestamps."""


def score_chunks(
    chunks: list[dict],
    target_topic: str,
) -> AlignmentResult:
    """Score transcript chunks for alignment with a target topic.

    Parameters
    ----------
    chunks : list of dicts with keys ``text``, ``start_time``, ``end_time``
    target_topic : the advocacy topic to evaluate against

    Returns
    -------
    AlignmentResult with score, reasoning, and quotes
    """
    client = _get_client()

    # Format chunks for the prompt
    chunks_text = ""
    for i, chunk in enumerate(chunks, 1):
        start_min = int(chunk["start_time"] // 60)
        start_sec = int(chunk["start_time"] % 60)
        chunks_text += f"\n[Chunk {i} — {start_min}:{start_sec:02d}]\n{chunk['text']}\n"

    user_prompt = f"""Evaluate the following transcript chunks for alignment with the topic: "{target_topic}"

{chunks_text}

Provide your analysis as a JSON object with:
- alignment_score (0-100)
- reasoning (brief explanation)
- quotes (3-5 quotes with text and timestamp in MM:SS format)"""

    response = client.beta.chat.completions.parse(
        model=SCORING_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        response_format=AlignmentResult,
        temperature=0.3,
    )

    return response.choices[0].message.parsed
