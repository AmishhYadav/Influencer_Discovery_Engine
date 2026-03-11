# Influent: Influencer Discovery Engine – Technical Documentation

## 1. Executive Summary
**Influent** is a specialized AI-powered discovery engine and intelligence platform designed for advocacy organizations. Its mission is to identify highly credible, professionally established influencers (doctors, scientists, environmental experts, chefs) whose content naturally aligns with specific values (e.g., plant-based health, sustainability) without selecting for polarizing or explicitly activist personas.

By analyzing rich multi-modal signals—starting with YouTube transcripts—Influent scores creators based on thematic alignment and generates actionable outreach "Playbooks" for human coordinators.

---

## 2. Core Philosophy & Value Proposition
### Soft Activism vs. Polarizing Activism
The core innovation of Influent is its ability to detect **"Soft Activism."** Traditional influencer tools often surface the most vocal or polarizing voices. Influent’s analysis engine is tuned to:
1.  **Surfaces Experts**: Prioritize individuals whose primary identity is expertise (MDs, researchers, master practitioners).
2.  **Values Natural Alignment**: Identify content where advocacy-aligned themes appear organically as part of professional practice.
3.  **Active De-prioritization**: Filter out aggressive, protest-oriented, or highly polarizing language to ensure outreach targets voices that carry mainstream institutional credibility.

---

## 3. System Architecture
Influent is built as a modular, event-driven-ready system using a **Python + React** stack.

### Layered Architecture
1.  **Ingestion Service (Python)**:
    - **YouTube Connector**: Fetches channel metadata (Subscribers, Engagement) and Video Transcripts via `youtube-transcript-api`.
    - **Cleanup Pipeline**: Strips sponsor reads, filler content, and auto-generated noise to prepare data for the LLM.
2.  **Analysis Engine (Python/LLM)**:
    - **Alignment Scoring**: Uses Gemini 2.5 Flash to evaluate content against specific campaign topics.
    - **Vector search**: Semantic embeddings are stored to allow finding creators who "talk like" a specific advocate.
3.  **Core Data API (FastAPI)**:
    - Provides a unified REST interface for the search dashboard.
    - Manages the state of "Briefings" (outreach playbooks).
4.  **Frontend Dashboard (React)**:
    - A premium, glassmorphic UI for discovery and filtering.
    - Features real-time search, comparison metrics, and an integrated briefing viewer.

---

## 4. Technical Stack
| Component | Technology | Rationale |
|-----------|------------|-----------|
| **Backend** | FastAPI (Python) | High-performance API with async support and native AI/NLP libraries. |
| **Frontend** | React + Vite | Industry standard for rich dashboards with fast refresh cycles. |
| **Database** | PostgreSQL / SQLite | Relational storage for creators and content; pgvector for semantic search. |
| **AI/LLM** | Google Gemini 2.5 | State-of-the-art reasoning for alignment scoring and briefing generation. |
| **Styling** | Vanilla CSS / Framer Motion | Maximum control over premium animations and layouts. |

---

## 5. Data Model
Influent uses a platform-agnostic schema to allow future expansion beyond YouTube:
- **`Creator`**: Unified record for an influencer (name, bio, reach metrics, composite scores).
- **`ContentItem`**: Generic container for blog posts, video transcripts, or papers.
- **`Briefing`**: Stores the generated AI playbooks and their generation status.

---

## 6. Product Roadmap
The project is organized into 5 primary execution phases:
1.  **Phase 1: Ingestion** — Proof of concept for reliable transcript and metadata collection. [COMPLETED]
2.  **Phase 2: Analysis Engine** — Development of the "Soft Activism" scoring logic. [COMPLETED]
3.  **Phase 3: Core Data API** — Development of unified storage and retrieval layers. [COMPLETED]
4.  **Phase 4: Frontend Dashboard** — Implementation of the discovery UI. [COMPLETED]
5.  **Phase 5: Briefing Generator** — Integration of the automated outreach playbook module. [COMPLETED]
6.  **Phase 6 (Post-MVP)** — Expansion to Blog, Twitter, and Academic platforms. [IN-PROGRESS]

---

## 7. Operational Workflows
### Campaign Discovery Workflow
1.  **Thematic Search**: Coordinator enters a topic (e.g., "cellular agriculture").
2.  **Scored Results**: System returns ranked creators with a breakdown of Credibility, Reach, and Alignment.
3.  **Evidence Review**: Coordinator reviews extracted quotes that justified why the creator was ranked highly.
4.  **Playbook Generation**: Click "Generate Briefing" to create a bespoke outreach kit containing suggested talking points and mission relevance.

---

## 8. Anti-Goals & Constraints
- **No Automated Outreach**: We do not build "spam bots." The tool empowers coordinators, not replaces them.
- **Privacy-First**: We only index public-facing content.
- **Non-Polarizing focus**: The tool is specifically built to avoid surfacing the "Twitter bubble" in favor of real-world credible professionals.
