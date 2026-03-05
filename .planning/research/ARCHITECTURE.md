# ARCHITECTURE: Influencer Discovery Engine

## Component Boundaries

1.  **Data Ingestion Service (Python)**
    *   Job: Fetch data from YouTube (API + Transcripts).
    *   Outputs: Raw text and metadata stored in the database.
2.  **Analysis & Alignment Engine (Python)**
    *   Job: Processes transcripts using NLP/Embeddings to generate alignment scores. Detects topics and filters out explicit activism.
    *   Outputs: Scores, categorized topics, and justification data to the database.
3.  **Core API (FastAPI)**
    *   Job: Serves dashboard requests (search, filter, view creator profiles).
    *   Job: Triggers the LLM module to generate briefing kits on demand.
4.  **Frontend Dashboard (React)**
    *   Job: Display data, rank influencers, trigger and display briefing kits.

## Data Flow
1.  **Ingestion**: User submits a seed keyword or channel → Ingestion Service fetches YouTube transcripts & stats → Saves to PostgreSQL.
2.  **Analysis**: Analysis Engine reads raw transcripts → Embeds text / prompts LLM for thematic evaluation → Saves scores and semantic vectors to PostgreSQL (`pgvector`).
3.  **Discovery**: Coordinator opens React Dashboard → Core API queries PostgreSQL for top-ranked creators → React displays results.
4.  **Briefing**: Coordinator clicks "Generate Briefing" → Core API calls LLM with creator context → LLM returns formatted bulleted briefing → Saved to DB and displayed in React.

## Suggested Build Order
1.  **Ingestion Service**: Prove you can reliably get YouTube transcripts.
2.  **Analysis Engine**: Prove the "soft activism / alignment" scoring works on real data. (Core risk).
3.  **Core API + Database**: Hook up the data storage.
4.  **Frontend Dashboard**: Build the UI.
5.  **Briefing Generator**: Add the final AI output step.
