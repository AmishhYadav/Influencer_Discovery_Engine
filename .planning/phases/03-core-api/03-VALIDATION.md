# Phase 3: Core API & Database — Validation Strategy

## 1. Test Infrastructure Setup
*   **Framework:** `pytest` + `pytest-asyncio`
*   **Client:** `fastapi.testclient.TestClient` for synchronous route testing.
*   **Database Mocking:** We will override the FastAPI `get_db` dependency to inject a test SQLite in-memory database prepopulated with fixtures.
*   **External Mocks:** Mock `openai` API calls in the briefing generation to avoid network calls and costs.

## 2. Sampling Rates & Data

We need a consistent set of fixtures for the test database:
*   2 Channels (1 high alignment, 1 low alignment)
*   1 Video per channel
*   1 Briefing record (to test the briefing GET endpoint)

## 3. Per-Task Verification Map

| Req ID | Task Description | Verification Method | Sign-off Criteria |
| :--- | :--- | :--- | :--- |
| API-01 | Creator list endpoint with score filtering | Unit test with `TestClient` passing `?min_score=80` | Endpoint returns 200 OK and correctly filters the list of channels. |
| API-02 | Creator detail endpoint | Unit test requesting a specific `channel_id` | Endpoint returns 200 OK, includes `alignment_quotes` from DB, and 404s on bad IDs. |
| API-03 | Async briefing generator kickoff | Unit test POSTing to `/briefings/generate` | Endpoint returns 202 Accepted and creates a pending `Briefing` record in the DB. |
| API-03b | Briefing retrieval endpoint | Unit test GETing `/briefings/{id}` | Endpoint returns the generated markdown text. |

## 4. Manual Verification Steps (Run by Human)

Once the tests pass, the human operator should visually verify the MVP functionality:

1.  **Swagger UI:** Start the server (`uvicorn src.api.main:app --reload`). Open `http://localhost:8000/docs`.
2.  **List Creators:** Execute the `GET /api/creators` endpoint in Swagger.
3.  **Generate Briefing:** Use an existing `channel_id` to `POST /api/briefings/generate`. Check the server logs to ensure the background task fires off.
4.  **Fetch Briefing:** Wait a few seconds, then `GET /api/briefings/{id}` to read the synthesized markdown.

## 5. Sign-off Criteria

*   All endpoints exist and return structurally correct JSON (`Pydantic` models).
*   Test coverage for `src/api` is > 90%.
*   The `BackgroundTasks` successfully write to the database (verified via logs).
