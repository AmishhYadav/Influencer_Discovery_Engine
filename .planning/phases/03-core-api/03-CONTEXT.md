# Phase 3: Core API & Database — Context & Decisions

## Objective
Build the Core API (REST endpoints) to expose the discovery and analysis functionality to the frontend, fulfilling requirements API-01, API-02, and API-03.

## User Decisions & Constraints
The user has decided to proceed with the lean, MVP-focused recommendations for the Core API architecture:

**1. Search & Filtering Constraints (API-01)**
- **Decision:** Lean Search (Option A).
- **Details:** The primary search endpoint will allow simple filtering by minimum alignment score (`min_score`) and sorting by score descending. Advanced multi-field filtering is deferred to avoid over-engineering at this stage.

**2. Async Task Management (API-03)**
- **Decision:** FastAPI `BackgroundTasks` (Option A).
- **Details:** Briefing generation (which requires multiple LLM calls and compiling a document) will be handled as simple in-memory background tasks. This avoids the overhead of setting up Redis/Celery for an MVP, with the accepted trade-off that tasks will be lost if the server restarts. 

**3. Pagination Strategy**
- **Decision:** Standard Limit/Offset (Option A).
- **Details:** List endpoints will use simple `?limit=20&offset=40` query parameters. This is adequate for the expected MVP data volume and simpler to implement than cursor-based pagination.

## Tech Stack Implications
- **FastAPI:** Will be used as the core web framework.
- **Pydantic:** For request/response schema validation (already in use for NLP outputs).
- **Uvicorn:** ASGI server to run the FastAPI application.

## Open / Deferred Questions
- Multi-field search and advanced filtering (e.g., subscriber counts, fuzzy text matching) are deferred.
- Persistent background task queues (Celery/Redis) are deferred.
