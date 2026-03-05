# Requirements: Influencer Discovery Engine

## Core Workflow
1.  **Ingestion**: User inputs a YouTube channel URL or keyword search. System fetches transcripts, descriptions, tags, and audience metrics.
2.  **Analysis**: System cleans transcripts (removing sponsor reads) and uses NLP to score content for topic alignment (e.g., plant-based health) and professional tone, penalizing explicit activism.
3.  **Discovery**: User views a ranked list of creators in a dashboard, sortable by alignment score, audience size, and engagement.
4.  **Briefing**: User selects a creator and clicks "Generate Briefing," which produces a bulleted cheat sheet for human outreach coordinators.

## Functional Requirements

### Data Collection (YouTube-First)
- [ ] Must fetch video transcripts for a given channel without relying on browser automation (e.g., via `youtube-transcript-api`).
- [ ] Must fetch channel metadata (subscriber count, video count, engagement metrics) via YouTube Data API.
- [ ] Must include a light text-cleaning step to strip known sponsor reads and auto-generated filler before NLP analysis.

### Analysis Engine
- [ ] Must score content for semantic alignment with target advocacy topics (e.g., sustainability, ethical food systems, plant-based health).
- [ ] **Critical**: Must penalize polarizing, protest-oriented, or explicit activist language to surface "soft activists" and credible professionals.
- [ ] Must extract and save representative quotes/timestamps that justify the alignment score.

### Core API & Database
- [ ] Must store creators, metrics, transcripts, and alignment scores in a PostgreSQL database (utilizing `pgvector` for semantic search).
- [ ] Must expose REST endpoints (via FastAPI) for searching, filtering, and retrieving creator profiles.
- [ ] Must handle the asynchronous triggering of the LLM briefing generation.

### Frontend Dashboard
- [ ] Must display a searchable, filterable list of ranked creators.
- [ ] Must show individual creator profiles with their metrics, alignment scores, and justifying quotes.
- [ ] Must include a prominent UI action to generate and view the outreach briefing kit.

### Outreach Briefing Generator
- [ ] Must prompt an LLM (Sonnet or GPT-4o-mini) with the creator's profile, metrics, and top aligned quotes.
- [ ] Must output a strictly formatted, bulleted cheat sheet containing: creator profile, mission relevance, key topics, metrics, example content, and suggested talking points.

## Non-Functional Requirements
- [ ] **Performance**: Dashboard queries must return in under 500ms. Ingestion and analysis can run asynchronously.
- [ ] **Reliability**: API quotas for YouTube must be managed (e.g., heavy caching, using transcript API over search API where possible).

## Out of Scope (MVP)
- [ ] Ingesting from blogs, academic papers, Instagram, TikTok.
- [ ] Automated email sending or full CRM capabilities.
- [ ] Complex custom embedding models (use foundational models first).
