# STACK: Influencer Discovery Engine

## Core Application Stack
- **Frontend**: React + Vite (Fast development, standard ecosystem). TailwindCSS for rapid, maintainable styling.
- **Backend/API**: FastAPI (Python). Python is mandatory for the NLP/AI ecosystem, and FastAPI provides high performance and automatic documentation.
- **Database**: PostgreSQL (Relational data: creators, scores, outreach logs) + pgvector (for semantic similarity/embeddings search).

## Data Collection & NLP Pipeline
- **YouTube API**: Official YouTube Data API v3 (for channels, videos, engagement metrics) + `youtube-transcript-api` (Python library for pulling captions without headless browsers).
- **NLP/Embeddings**: OpenAI `text-embedding-3-small` (cost-effective, high quality) or local `all-MiniLM-L6-v2` via HuggingFace for thematic/semantic alignment.
- **LLM Engine**: Anthropic Claude 3.5 Sonnet or OpenAI GPT-4o-mini for generating outreach briefing kits and performing complex alignment reasoning.

## Rationale
Python is non-negotiable for the backend due to the heavy reliance on NLP and data pipelines. React provides the most robust ecosystem for the dashboard MVP. Using pgvector avoids the complexity of standing up a separate vector database (like Pinecone) for an MVP.

## What NOT to use
- **Heavy Web Scrapers (Puppeteer/Selenium)**: Avoid for YouTube initially. Rely on the API and transcript libraries to prevent IP bans and reduce infrastructure complexity.
- **Dedicated Vector DBs (Pinecone/Weaviate)**: Overkill for MVP. Use Postgres with `pgvector` to keep the architecture simple.
