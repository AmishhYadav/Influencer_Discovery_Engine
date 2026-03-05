# Roadmap: Influencer Discovery Engine

**5 phases** | **14 requirements mapped** | All v1 requirements covered ✓

| # | Phase | Goal | Requirements | Success Criteria |
|---|-------|------|--------------|------------------|
| 1 | Ingestion | Reliable YouTube transcript and metadata fetching | DATA-01, DATA-02, DATA-03 | 3 |
| 2 | Analysis Engine | NLP scoring for soft activism and topic alignment | NLP-01, NLP-02, NLP-03 | 3 |
| 3 | Core Data API | Store and serve creator profiles and scores | API-01, API-02, API-03 | 3 |
| 4 | Frontend Dashboard | UI to explore and filter ranked creators | UI-01, UI-02, UI-03 | 3 |
| 5 | Briefing Generator | AI-powered outreach cheat sheet generation | AI-01, AI-02 | 2 |

### Phase Details

**Phase 1: Ingestion**
Goal: Reliable YouTube transcript and metadata fetching
Requirements: DATA-01, DATA-02, DATA-03
Success criteria:
1. Given a channel URL, system downloads transcripts for recent videos without browser automation.
2. System fetches valid channel metadata (subscribers, views) from YouTube API.
3. Transcripts are stripped of common sponsor reads ("NordVPN") and auto-generated filler.

**Phase 2: Analysis Engine**
Goal: NLP scoring for soft activism and topic alignment
Requirements: NLP-01, NLP-02, NLP-03
Success criteria:
1. System assigns a >0 score for content discussing plant-based health or sustainability.
2. System heavily penalizes or flags transcripts containing explicit protest/activist language.
3. System extracts the top 3 most aligned quotes per analyzed channel with timestamps.

**Phase 3: Core Data API**
Goal: Store and serve creator profiles and scores
Requirements: API-01, API-02, API-03
Success criteria:
1. Creator profiles, transcripts, and scores are successfully saved to PostgreSQL.
2. A REST endpoint returns a list of creators sorted by alignment score.
3. A REST endpoint can trigger the async briefing generation task.

**Phase 4: Frontend Dashboard**
Goal: UI to explore and filter ranked creators
Requirements: UI-01, UI-02, UI-03
Success criteria:
1. React dashboard loads a list of fetched creators.
2. User can filter creators by minimum subscriber count and minimum alignment score.
3. Clicking a creator shows their profile, metrics, and the top justifying quotes.

**Phase 5: Briefing Generator**
Goal: AI-powered outreach cheat sheet generation
Requirements: AI-01, AI-02
Success criteria:
1. System successfully prompts the LLM with creator context and receives a response.
2. Outreach briefing is strictly formatted as a bulleted cheat sheet containing relevance, key topics, metrics, and talking points.
