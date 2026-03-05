# Research Summary: Influencer Discovery Engine

## Key Findings

**Stack:**
*   FastAPI (Python) for the backend and NLP processing.
*   React + Vite for the frontend dashboard.
*   PostgreSQL + `pgvector` for data storage and semantic similarity search.
*   `youtube-transcript-api` for transcript fetching.
*   Anthropic Claude 3.5 Sonnet or OpenAI GPT-4o-mini for generating outreach briefing kits.

**Table Stakes:**
*   YouTube Ingestion Engine (transcripts + metrics).
*   Semantic Alignment Scoring (NLP detecting topics without explicit activism).
*   Creator Dashboard (search, filter, view profiles).
*   Outreach Briefing Generator (AI-generated bulleted cheat sheets).

**Watch Out For:**
*   **The Transcript Garbage Problem**: Clean auto-generated transcripts and sponsor reads before scoring.
*   **API Quota Exhaustion**: Rely on `youtube-transcript-api` heavily; minimize official YouTube API quota usage.
*   **The "Activism False Positive" Trap**: explicitly penalize polarizing/activist language in the alignment scoring to ensure credibility.
*   **Over-engineering the NLP**: Start with foundational models (Sonnet/GPT-4o) before attempting custom embeddings.
