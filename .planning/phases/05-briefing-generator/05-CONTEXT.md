# Phase 5: Briefing Generator — Context & Decisions

## Objective
Finalize the AI-powered outreach cheat sheet generation (Requirements AI-01, AI-02). The core backend async task and frontend polling mechanism were proactively built in Phases 3 and 4, so this phase focuses on polishing the LLM prompt and enhancing the UX.

## User Decisions

**1. Custom Campaign Context**
- **Decision:** Add UI Input (Option A).
- **Details:** The frontend will include an optional textarea above the "Generate Briefing" button, allowing users to specify a campaign or brand context (e.g., "Oatly sustainability campaign"). This context will be passed to the backend API via the `campaign_context` field which is already supported.

**2. Prompt Tuning (AI-02)**
- **Decision:** Strict Compliance (Option A).
- **Details:** The LLM prompt template in `src/api/tasks.py` will be updated to strictly mandate the exact sections requested in AI-02: Creator Profile, Mission Relevance, Key Topics, Metrics, Example Content, and Suggested Talking Points.

**3. Output Export**
- **Decision:** Copy to Clipboard (Option A).
- **Details:** A "Copy to Clipboard" button will be added below the rendered markdown result in the UI. When clicked, it will copy the raw markdown text so human coordinators can easily paste it into emails, Google Docs, or Notion.
