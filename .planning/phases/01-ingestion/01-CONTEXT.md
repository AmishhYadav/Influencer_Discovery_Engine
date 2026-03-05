# Phase 1: Ingestion - Context

**Gathered:** 2026-03-06
**Status:** Ready for planning

<domain>
## Phase Boundary

Reliable YouTube transcript and metadata fetching

</domain>

<decisions>
## Implementation Decisions

### Ingestion Trigger
- CLI command that accepts a search query (`--query`).
- First searches YouTube Data API, extracts channel IDs, then ingests latest videos.
- Does NOT require specific channel URLs up front (true discovery).

### Video Selection
- Fetch transcripts for the latest 20-30 videos per discovered channel.
- Balances representativeness with API efficiency.

### Storage Format
- Store raw transcripts directly into PostgreSQL.
- Will use `jsonb` columns for timestamped transcript arrays and metadata.

### Error Handling & Limits
- Retry failed downloads/API calls with exponential backoff to handle network hiccups.
- Do not fail fast on single video failures.

### Claude's Discretion
- Backoff parameters (max retries, wait times).
- Exact JSON database schema for transcripts.
- Exact number of videos to fetch between 20 and 30.

</decisions>

<code_context>
## Existing Code Insights

### Established Patterns
- Greenfield project. We established `pgvector` with PostgreSQL in the architecture decisions.
- Python CLI tools and `youtube-transcript-api` designated in STACK.md.

</code_context>

<specifics>
## Specific Ideas

- CLI Example provided: `python ingest.py --query "plant based health"`

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope.

</deferred>

---

*Phase: 01-ingestion*
*Context gathered: 2026-03-06*
