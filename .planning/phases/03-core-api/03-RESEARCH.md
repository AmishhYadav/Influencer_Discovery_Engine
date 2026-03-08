# Phase 3: Core API & Database — Research & Technical Strategy

## Objective
Build the Core API (REST endpoints) to expose the discovery and analysis functionality to the frontend.

## API Framework: FastAPI
We will use **FastAPI** as the core web framework, served by **Uvicorn**.

* **Why FastAPI?** 
    * Native async support matches our `asyncpg`/`asyncio` stack well (though we are currently using synchronous SQLAlchemy, we can run routes with `def` which FastAPI automatically runs in a threadpool to prevent blocking the event loop).
    * Built-in Pydantic integration ensures robust request/response validation.
    * Automatic OpenAPI/Swagger documentation (`/docs`) makes frontend integration trivial.

## Endpoints (MVP)

1. **`GET /api/creators` (Discovery)**
   * **Purpose:** List influencers matching criteria (API-01).
   * **Parameters:** `limit` (int, default 20), `offset` (int, default 0), `min_alignment_score` (int, optional).
   * **Response:** Array of `Channel` objects with their `alignment_score` and `subscriber_count`.

2. **`GET /api/creators/{channel_id}` (Details)**
   * **Purpose:** Get full details for a specific creator, including analysis quotes.
   * **Parameters:** `channel_id` (path parameter).
   * **Response:** `Channel` object with `alignment_quotes` and recent `Video` metadata.

3. **`POST /api/briefings/generate` (Briefing Generation)**
   * **Purpose:** Trigger the async workflow to compile an engagement briefing (API-03).
   * **Request Body:** `{ "channel_id": "string", "campaign_context": "string (optional)" }`
   * **Response:** `{ "status": "accepted", "task_id": "string" }` (202 Accepted).
   * *Note on Implementation:* We will use FastAPI's `BackgroundTasks` to process the LLM calls asynchronously to avoid HTTP timeouts.

## Background Tasks (Briefing Generator)
To handle API-03 (Agentic Briefing Generator), we will use FastAPI's built-in `BackgroundTasks`.

* **The Workflow:**
    1. Receive `POST /api/briefings/generate`.
    2. Add task to `BackgroundTasks`.
    3. Return `202 Accepted` immediately.
    4. Task runs: Fetches channel, top chunks, quotes, and passes them to `gpt-4o` to generate a 1-page markdown briefing.
    5. Saves the markdown to the database or a local file (we'll need a new DB table or column for `Briefings`).

## Database Updates
To support the briefing generator, we need a place to store the results.
* **Update `src/db/models.py`:** Add a `Briefing` table:
    * `id` (String UUID)
    * `channel_id` (ForeignKey)
    * `content` (Text - the markdown)
    * `status` (String - "pending", "completed", "failed")
    * `created_at`, `updated_at`

This allows a future `GET /api/briefings/{channel_id}` endpoint to retrieve the result.

## Dependency Injection (Database)
FastAPI relies heavily on dependency injection. We will create a `get_db()` dependency that yields a SQLAlchemy `Session` so endpoints can safely query the database.

## Validation Strategy
* **Unit Tests:** `pytest` with `TestClient` from `fastapi.testclient`.
* **Mocks:** Mock the DB session and background task LLM calls.
* **Manual Testing:** Use the Swagger UI (`http://localhost:8000/docs`) to manually verify the endpoints.
