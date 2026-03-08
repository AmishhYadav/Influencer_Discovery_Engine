# PITFALLS: Influencer Discovery Engine

## 1. The Transcript Garbage Problem
*   **Warning Sign**: NLP scores are zero across the board, or the system surfaces irrelevant creators because it's hallucinating based on auto-generated filler words (like "um", "ah", or sponsor reads).
*   **Prevention**: Implement a light cleaning step before embedding/analysis. Use an LLM or regex to summarize or clean transcripts, specifically stripping out known sponsor reads (e.g., "NordVPN", "BetterHelp") before scoring.
*   **Phase**: Data Collection / Analysis Engine.

## 2. API Quota Exhaustion
*   **Warning Sign**: The YouTube API starts returning 403 Errors (Quota Exceeded) within the first week of testing.
*   **Prevention**: Do not use the YouTube API to search for videos continuously. Rely on it only for channel metadata, and use the `youtube-transcript-api` (which doesn't use API quotas) heavily. Cache all results in the database aggressively.
*   **Phase**: Data Collection.

## 3. The "Activism False Positive" Trap
*   **Warning Sign**: The system surfaces creators who are highly aligned with the topics, but upon manual review, they are actually aggressive activists, which is exactly what the user wanted to avoid.
*   **Prevention**: Ensure the alignment prompt/embedding strategy explicitly penalizes polarizing language, call-to-action protest language, or identifying tags. The scoring must not just be "closeness to topic" but "closeness to topic + professional tone."
*   **Phase**: Analysis Engine.

## 4. Over-engineering the NLP
*   **Warning Sign**: Spending 3 weeks fine-tuning an open-source model before ever looking at real creator data.
*   **Prevention**: Start with a simple prompt chain using a foundational model (like Sonnet or GPT-4o) to prove the pipeline. Only move to custom embeddings or fine-tuning if the foundational model is too slow or expensive at scale.
*   **Phase**: Analysis Engine.
