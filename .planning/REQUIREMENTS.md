# Requirements: Influencer Discovery Engine

## v1 Requirements

### Data Collection (YouTube-First)
- [ ] **DATA-01**: System can fetch video transcripts for a given channel via `youtube-transcript-api` (no browser automation).
- [ ] **DATA-02**: System can fetch channel metadata (subscriber count, video count, engagement metrics) via YouTube Data API.
- [ ] **DATA-03**: System strips known sponsor reads and auto-generated filler from transcripts before analysis.

### Analysis Engine
- [ ] **NLP-01**: System scores content for semantic alignment with target advocacy topics (sustainability, ethical food systems, plant-based health).
- [ ] **NLP-02**: System penalizes polarizing, protest-oriented, or explicit activist language to surface "soft activists."
- [ ] **NLP-03**: System extracts and saves representative quotes/timestamps that justify the alignment score.

### Core API & Database
- [ ] **API-01**: System stores creators, metrics, transcripts, and alignment scores in PostgreSQL (`pgvector`).
- [ ] **API-02**: System exposes REST endpoints for searching, filtering, and retrieving creator profiles.
- [ ] **API-03**: System handles the asynchronous triggering of the LLM briefing generation.

### Frontend Dashboard
- [ ] **UI-01**: Dashboard displays a searchable, filterable list of ranked creators.
- [ ] **UI-02**: Dashboard shows individual creator profiles with their metrics, alignment scores, and justifying quotes.
- [ ] **UI-03**: Dashboard includes a prominent UI action to generate and view the outreach briefing kit.

### Outreach Briefing Generator
- [ ] **AI-01**: System prompts an LLM with the creator's profile, metrics, and top aligned quotes to generate a briefing.
- [ ] **AI-02**: Output is strictly formatted as a bulleted cheat sheet containing: creator profile, mission relevance, key topics, metrics, example content, and suggested talking points.

## v2 Requirements (Deferred)
- [ ] Support for ingesting content from blogs and academic papers.
- [ ] Support for Instagram and TikTok data ingestion.
- [ ] Webhook integrations for updating CRMs dynamically.

## Out of Scope
- [ ] Automated email sending — Anti-goal. The system empowers human coordinators; it does not replace them.
- [ ] Full CRM capabilities — MVP focuses on discovery, not relationship management.
- [ ] Complex custom embedding models — Use foundational models first to avoid over-engineering.

## Traceability
- **DATA-01** → Phase 1
- **DATA-02** → Phase 1
- **DATA-03** → Phase 1
- **NLP-01** → Phase 2
- **NLP-02** → Phase 2
- **NLP-03** → Phase 2
- **API-01** → Phase 3
- **API-02** → Phase 3
- **API-03** → Phase 3
- **UI-01** → Phase 4
- **UI-02** → Phase 4
- **UI-03** → Phase 4
- **AI-01** → Phase 5
- **AI-02** → Phase 5
