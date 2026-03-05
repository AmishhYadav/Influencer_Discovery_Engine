# Phase 2: Analysis Engine - Context

**Gathered:** 2026-03-06
**Status:** Ready for planning

<domain>
## Phase Boundary

NLP scoring for soft activism and topic alignment

</domain>

<decisions>
## Implementation Decisions

### Processing Pipeline
- Chunk transcripts and embed them first.
- Only send the top N most "aligned" chunks to the LLM for final scoring to save cost and context window.

### Scoring Mechanism
- Use an LLM as a judge (evaluating the selected chunks against a rubric).
- The LLM will output a final alignment score on a 0-100 scale.

### Quote Extraction
- Extract the justifying quotes/timestamps in the same LLM call as the score.
- The LLM will return a JSON payload with both the score and the top quotes.

### API/Model Selection
- Standardize on the OpenAI Stack.
- `text-embedding-3-small` for chunk embeddings.
- `gpt-4o-mini` for the LLM judge.

### Claude's Discretion
- Chunk size and overlap for the transcript text.
- The exact prompt rubric given to the LLM.
- Number of top chunks (N) to send to the LLM.
- How to structure the `pydantic` output schema for structured JSON parsing.

</decisions>

<code_context>
## Existing Code Insights

### Established Patterns
- We have PostgreSQL with `pgvector` ready via `src/db/models.py`. We'll need to add an embedding column.
- The transcripts are currently stored as an array of JSON objects (`{text, start, duration}`).

</code_context>

<specifics>
## Specific Ideas

- Focus on "soft activism" — penalize explicitly polarizing or protest-oriented language while rewarding subject matter alignment (e.g., plant-based health, sustainability).

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope.

</deferred>

---

*Phase: 02-analysis-engine*
*Context gathered: 2026-03-06*
