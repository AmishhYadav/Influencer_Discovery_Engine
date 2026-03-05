# Phase 2: Analysis Engine - Research

**Date:** 2026-03-06
**Goal:** NLP scoring for soft activism and topic alignment

## Technical Approaches

### 1. Database Schema Updates (pgvector)
We need to store the chunk text and its corresponding vector embedding so we can perform similarity searches.
- **New Table (`transcript_chunks`)**:
  - `id` (Primary Key)
  - `video_id` (Foreign Key to `videos`)
  - `start_time` (Float)
  - `end_time` (Float)
  - `text` (String)
  - `embedding` (Vector column using `pgvector`)
- **pgvector Installation**: Ensured `CREATE EXTENSION IF NOT EXISTS vector;` runs during table creation. SQLAlchemy will use the `Vector` type from the `pgvector.sqlalchemy` package.

### 2. Chunking Transcripts
- Input: JSON array of `{text, start, duration}` from Phase 1.
- Output: Logical chunks of text (e.g., 30-60 seconds of continuous speech) to provide enough context for the embedding model.
- Overlapping chunks (e.g., sliding window) can prevent cutting off important context mid-sentence.

### 3. Embeddings Pipeline (`text-embedding-3-small`)
- Use the official `openai` Python SDK.
- Create an embedding for each transcript chunk.
- Create an embedding for a "target" string (e.g., "plant-based health, vegan nutrition, sustainability, environmental science").
- Store chunk embeddings in the database.

### 4. Similarity Search
- Query the `transcript_chunks` table using pgvector's cosine distance (`<=>`) operator to find the top N chunks closest to the target topic embedding for a given channel's videos.
- This acts as a highly efficient filter, drastically reducing the token count sent to the LLM.

### 5. LLM Judge (`gpt-4o-mini`)
- **Input**: The Top N most aligned chunks for a creator, along with a strict rubric defining "soft activism" and penalizing explicitly polarizing language.
- **Output Schema**: Use Pydantic and the OpenAI SDK's `response_format` (Structured Outputs) to guarantee a specific JSON structure:
  ```json
  {
    "alignment_score": 85,
    "reasoning": "Discusses plant-based nutrition scientifically...",
    "quotes": [
      {"text": "Quote 1", "timestamp": "12:34"},
      {"text": "Quote 2", "timestamp": "15:00"}
    ]
  }
  ```

## Validation Architecture

To satisfy NYQUIST validation checks (Dimension 8):
- **Mocking**: Mock the OpenAI API calls (both embeddings and chat completions) in unit tests to avoid network calls and API costs in CI.
- **Mock DB**: Test the pgvector similarity search. Note that standard SQLite does not support pgvector, so unit tests involving vector search might require mocking the DAO or using a specialized test container. For the Python logic, we can mock the DB session's queries.
- **Integration**: Provide a CLI command to run the analysis on a specific channel ID that already exists in the database.

## Risks & Gotchas
- **pgvector & SQLite**: We used SQLite as a fallback for testing in Phase 1. SQLite does not natively support `pgvector`. 
  - *Mitigation*: We will abstract the vector search in the DAO so that we can mock it during local SQLite-based unit testing, or we transition to requiring a local Postgres instance for testing if we need to test the SQL queries directly. Given the MVP constraints, DAO mocking is preferred for fast unit tests.
- **Token Limits**: Always limit the `top_n` chunks sent to the LLM to avoid exceeding `gpt-4o-mini`'s context window. (e.g., Top 20 chunks max).
