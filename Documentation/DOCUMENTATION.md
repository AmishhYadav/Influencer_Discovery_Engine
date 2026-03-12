# Influencer Discovery Engine — Technical Documentation

## 1. Executive Summary

**Influencer Discovery Engine** is an AI-powered platform built for advocacy organizations to discover highly credible, professionally established creators — doctors, scientists, environmental experts, chefs — whose content naturally aligns with specific values (e.g., plant-based health, sustainability) without selecting for polarizing or explicitly activist personas.

The platform searches across **five platforms** (YouTube, Twitter/X, Instagram, Blogs, and Academic databases), scores creators using a **4-dimensional composite scoring engine**, and generates AI-powered engagement playbooks using Google Gemini.

> **Core Innovation:** The engine detects **"Soft Activism"** — content where advocacy-aligned themes appear organically as part of professional practice — rather than surfacing vocal or polarizing voices.

---

## 2. Core Philosophy & Value Proposition

### Soft Activism vs. Polarizing Activism

Traditional influencer tools surface the most vocal or polarizing voices. This platform's analysis engine is tuned differently:

| Principle | Description |
|-----------|-------------|
| **Surface Experts** | Prioritize individuals whose primary identity is expertise (MDs, researchers, master practitioners) |
| **Value Natural Alignment** | Identify content where advocacy themes appear organically as part of professional practice |
| **De-prioritize Polarization** | Filter out aggressive, protest-oriented, or polarizing language. Target voices with mainstream institutional credibility |
| **Privacy-First** | Only index public-facing content. No authenticated scraping or private data |
| **No Automated Outreach** | The tool empowers human coordinators, not replaces them |

---

## 3. Development Phases

The project was built incrementally across 6 phases, each adding a complete subsystem:

### Phase 1: Ingestion Layer ✅

**Goal:** Build reliable data collection pipelines for YouTube.

**What was built:**
- `src/ingestion/youtube_api.py` — YouTube Data API v3 integration for channel metadata (subscribers, video count) and video listing
- `src/ingestion/transcripts.py` — YouTube transcript extraction via `youtube-transcript-api`
- `src/ingestion/cleaner.py` — Text normalization pipeline that strips sponsor reads, filler content, and auto-generated noise

**Key decisions:**
- Used `youtube-transcript-api` for transcript extraction (no API key required for transcripts)
- Stored raw transcripts as JSON arrays of `{text, start, duration}` segments for timestamp-level analysis
- Built a cleanup pipeline to prepare text for LLM scoring

---

### Phase 2: Analysis Engine ✅

**Goal:** Develop the "Soft Activism" scoring logic using AI.

**What was built:**
- `src/analysis/nlp.py` — Gemini-powered alignment scoring and text embedding generation
  - `score_text_content()` — Sends content to Gemini 2.5 Flash with a structured prompt that evaluates alignment against a target topic (0–100 scale)
  - `generate_embeddings()` — Generates 1536-dimensional embeddings using Gemini's `text-embedding-004` model
  - `score_alignment()` — Special YouTube transcript alignment scoring with evidence quote extraction
- `src/analysis/scoring.py` — 4-dimensional composite scoring engine
  - Credibility, Engagement, Reach, Alignment scores (0–100 each)
  - Platform-specific weight profiles
  - Log-scaled metrics with configurable thresholds
- `src/analysis/chunker.py` — Transcript text chunking for embedding generation (splits on sentence boundaries, ~500 word chunks)

**Key decisions:**
- Chose Gemini 2.5 Flash for alignment scoring (fast, cost-effective, strong reasoning)
- Designed platform-agnostic scoring with platform-specific weight adjustments
- Alignment score heavily weighted (40–50%) because it's the core differentiator

---

### Phase 3: Core Data API ✅

**Goal:** Build a unified REST API and persistent storage.

**What was built:**
- `src/api/main.py` — FastAPI application entry point with CORS middleware, router wiring, and startup migrations
- `src/api/schemas.py` — Pydantic v2 request/response models (`SearchRequest`, `SearchResponse`, `CreatorSummary`, `BriefingResponse`)
- `src/api/deps.py` — Dependency injection for database sessions
- `src/api/routers/search.py` — Multi-platform search endpoint with platform-specific ingestors
- `src/api/routers/creators.py` — Creator listing and detail endpoints with pagination
- `src/api/routers/briefings.py` — Briefing generation trigger and polling endpoints
- `src/db/models.py` — SQLAlchemy 2.0 models for all entities
- `src/db/dao.py` — Data access objects with upsert logic for creators, content items, briefings, and score updates

**Key decisions:**
- Used PostgreSQL with pgvector extension for vector similarity search
- Startup migration to fix FK constraints (briefings: `channels` → `creators`)
- Idempotent migrations that run on every startup (safe to repeat)
- SQLAlchemy 2.0 with `declarative_base` pattern

---

### Phase 4: Frontend Dashboard ✅

**Goal:** Build a premium, data-rich discovery interface.

**What was built:**
- `frontend/src/pages/LandingPage.tsx` — Hero landing page with WebGL animated light rays (via custom `LightRays` component), glassmorphic UI elements, and animated entry
- `frontend/src/pages/SearchDashboard.tsx` — Multi-platform search interface
  - Platform multi-select filter (YouTube, Twitter, Instagram, Blog, Academic)
  - Real-time search with loading states
  - Database-first results with "Refresh with Live Search" button
  - Creator card grid with platform-aware metrics
- `frontend/src/pages/AnalyticsDashboard.tsx` — Individual creator analytics with score breakdown and content feed
- `frontend/src/pages/BriefingsDashboard.tsx` — AI briefing viewer with full Markdown rendering (`react-markdown`) and custom styled components for tables, blockquotes, lists, code
- `frontend/src/components/CreatorCard.tsx` — Platform-aware creator cards showing Subscribers (YouTube), Followers (Twitter/IG), Research Relevance (Academic), or Content Alignment (Blog)
- `frontend/src/components/DashboardLayout.tsx` — Shared layout with sidebar navigation
- `frontend/src/components/LightRays.tsx` — Custom WebGL shader-based animated background effect
- `frontend/src/api/client.ts` — Typed API client with all endpoint methods

**Tech stack:**
- React 18 + TypeScript + Vite 7
- Tailwind CSS v4
- Framer Motion for page transitions
- Lucide React for icons
- react-markdown for briefing rendering

**Design decisions:**
- Dark mode only (SaaS aesthetic with `#0f172a` base)
- Emerald (#10B981) accent for primary metrics, Indigo/Violet for AI features
- Glassmorphism on floating cards (`bg-white/5 backdrop-blur-xl`)
- Platform-specific metric display (not all platforms have follower counts)

---

### Phase 5: Briefing Generator ✅

**Goal:** AI-powered engagement playbooks generated on demand.

**What was built:**
- `src/api/tasks.py` — Background task runner for briefing generation
  - Triggered via FastAPI `BackgroundTasks`
  - Fetches creator data + content items from DB
  - Constructs a structured prompt with creator intel table and content samples
  - Calls Gemini 2.5 Flash with executive-level system instructions
  - Saves result as Markdown to DB with status tracking

**Briefing structure (AI-generated):**
1. 🎯 **Creator Snapshot** — Executive summary of who they are
2. 🔗 **Mission Alignment** — Why they're a natural campaign fit
3. 📊 **Credibility & Reach Assessment** — Authority signal analysis
4. 💡 **Key Content Themes** — Recurring topics that overlap with advocacy goals
5. 📝 **Evidence & Quotes** — Specific blockquoted citations from content
6. 🤝 **Outreach Strategy** — Actionable conversation openers

**Key decisions:**
- Async generation with status polling (pending → completed/failed)
- Executive-level tone with specific formatting instructions
- Temperature 0.7 for creative but controlled output
- Max 2500 output tokens for comprehensive but focused briefings

---

### Phase 6: Multi-Platform Expansion ✅

**Goal:** Expand beyond YouTube to Twitter, Instagram, Blogs, and Academic databases.

**What was built:**

#### Twitter/X Integration
- `src/ingestion/social_media.py` — Profile scraping via Nitter public proxies (3 instance rotation)
- Extracts: name, bio, follower count, recent tweets
- Falls back to shell profile when all Nitter instances are unavailable
- Parses human-readable counts ("1.2K", "3.5M")

#### Instagram Integration
- `src/ingestion/social_media.py` — Public profile meta tag extraction (OG tags)
- Extracts: name, bio, follower count from `og:title` and `og:description`
- Falls back to shell profile on failure
- Limited to public accounts

#### Blog Discovery & Scraping
- `src/ingestion/blog_scraper.py` — Full blog content pipeline:
  1. RSS/Atom feed discovery via `<link rel="alternate">` tags
  2. Common feed path probing (`/feed`, `/rss`, `/atom.xml`)
  3. HTML link crawling as fallback (looks for `<article>` containers)
  4. Article extraction with main content isolation (`<article>` → `<main>` → largest `<div>`)
  5. Author, date, and title extraction from meta tags

#### Academic Search
- `src/ingestion/academic.py` — Dual-source academic search:
  - **Semantic Scholar API** — Paper search with citation counts, h-index, author metadata
  - **OpenAlex API** — Fallback with works count, citation aggregation, open access URLs
  - Automatic failover between sources (handles 429 rate limiting)
  - Aggregates: h-index, total citations, paper count per author

#### Web Discovery (Keyword → Handle Resolver)
- `src/ingestion/web_discovery.py` — Google Search-based discovery that converts keyword queries into platform-specific URLs/handles:
  - `discover_blog_urls()` — Searches `"{query} blog articles expert"` and extracts unique domains
  - `discover_twitter_handles()` — Searches `"site:twitter.com {query} expert"` and parses handles from URLs
  - `discover_instagram_handles()` — Searches `"site:instagram.com {query} expert"` and parses handles
  - Supports Google Custom Search API (if keys provided) with fallback to HTML scraping
  - Filters out social media, search engines, and aggregator sites from blog results

**Key improvements in this phase:**
- All ingestors now support keyword queries (not just handles/URLs)
- Platform-specific scoring weights (academic/blog don't penalize for zero followers)
- LLM alignment scoring applied to all platforms (not just YouTube)
- Database-first search with ≥3 result threshold before triggering live search
- `force_live` parameter for explicit cache bypass
- All live search data is persisted to PostgreSQL for future queries

---

## 4. System Architecture

```
┌──────────────────────────────────────────────────────────────────────────┐
│                        Frontend (React + Vite)                          │
│          Landing Page · Search · Analytics · Briefings                  │
└─────────────────────────────┬────────────────────────────────────────────┘
                              │ REST API (localhost:8000)
┌─────────────────────────────▼────────────────────────────────────────────┐
│                         FastAPI Backend                                  │
│  ┌──────────────┐   ┌────────────────┐   ┌───────────────────────────┐  │
│  │ Search Router │   │ Creators Router│   │ Briefings Router + Tasks  │  │
│  └──────┬───────┘   └────────┬───────┘   └─────────────┬─────────────┘  │
│         │                    │                          │                │
│  ┌──────▼────────────────────▼──────────────────────────▼─────────────┐  │
│  │                      Ingestion Layer                               │  │
│  │   YouTube API · Twitter · Instagram · Blog · Academic · Discovery  │  │
│  └──────────────────────────┬────────────────────────────────────────┘  │
│                             │                                           │
│  ┌──────────────────────────▼────────────────────────────────────────┐  │
│  │                      Analysis Engine                              │  │
│  │        Gemini LLM Scoring · Composite Scorer · Embeddings         │  │
│  └──────────────────────────┬────────────────────────────────────────┘  │
└─────────────────────────────┼────────────────────────────────────────────┘
                              │
                 ┌────────────▼────────────┐
                 │   PostgreSQL + pgvector  │
                 │  Creators · Content · AI │
                 └─────────────────────────┘
```

---

## 5. Data Model

### Entity Relationship

```
┌─────────────┐       ┌──────────────────┐       ┌────────────────┐
│   Creator    │──1:N──│   ContentItem    │       │    Briefing    │
│             │       │                  │       │                │
│ id (PK)     │       │ id (PK)          │       │ id (PK)        │
│ name        │       │ creator_id (FK)  │       │ creator_id (FK)│
│ platform    │       │ source_type      │       │ content (text) │
│ platform_id │       │ title            │       │ status         │
│ bio         │       │ text_content     │       │ created_at     │
│ follower_ct │       │ url              │       └────────────────┘
│ cred_score  │       │ published_at     │
│ engag_score │       │ engagement_json  │
│ reach_score │       └──────────────────┘
│ align_score │
│ comp_score  │──1:N──── Briefing
└─────────────┘

┌─────────────┐       ┌──────────────────┐       ┌────────────────────┐
│   Channel   │──1:N──│     Video        │──1:N──│  TranscriptChunk   │
│ (YouTube)   │       │                  │       │                    │
│ id (PK)     │       │ id (PK)          │       │ id (PK)            │
│ title       │       │ channel_id (FK)  │       │ video_id (FK)      │
│ description │       │ title            │       │ start_time         │
│ sub_count   │       │ published_at     │       │ end_time           │
│ align_score │       │ transcript (JSON)│       │ text               │
│ align_quotes│       └──────────────────┘       │ embedding (vector) │
└─────────────┘                                  └────────────────────┘
```

### Creator (Platform-Agnostic)
The `Creator` model is the central entity. It stores data from any platform with a unified schema:

| Field | Type | Description |
|-------|------|-------------|
| `id` | UUID (hex) | Auto-generated unique identifier |
| `name` | String | Display name |
| `platform` | String | One of: `youtube`, `twitter`, `instagram`, `blog`, `academic` |
| `platform_id` | String | Channel ID, handle, URL, or author ID |
| `bio` | Text | Profile bio or description |
| `follower_count` | Integer | Subscribers/followers (0 for academic/blog) |
| `credibility_score` | Float | 0–100 credibility rating |
| `engagement_score` | Float | 0–100 engagement rating |
| `reach_score` | Float | 0–100 reach rating |
| `alignment_score` | Float | 0–100 AI alignment rating |
| `composite_score` | Float | Weighted composite of all four |

### ContentItem (Generic Content Container)
Stores any piece of content — blog post, tweet, paper, Instagram post, or YouTube transcript — linked to a Creator:

| Field | Type | Description |
|-------|------|-------------|
| `source_type` | String | `blog_post`, `tweet`, `paper`, `instagram_post`, `twitter_bio` |
| `text_content` | Text | Full text content (up to 10,000 chars) |
| `engagement_metrics` | JSON | Platform-specific metrics (likes, citations, shares) |

### Briefing (AI-Generated Playbook)
Tracks async briefing generation:

| Field | Type | Description |
|-------|------|-------------|
| `creator_id` | FK → Creator | The creator this briefing is for |
| `content` | Text | Generated Markdown briefing |
| `status` | String | `pending` → `completed` or `failed` |

---

## 6. Scoring Engine — Deep Dive

### 6.1 Credibility Score (0–100)

Evaluates professional authority through bio analysis:

```python
# Professional keywords (each adds 8 points, capped at 50)
PROFESSIONAL_KEYWORDS = [
    "dr", "doctor", "phd", "professor", "researcher",
    "scientist", "md", "engineer", "expert", "specialist",
    "chef", "nutritionist", "dietitian", "therapist",
    "journalist", "author", "editor", "correspondent",
]
```

- +8 points per professional keyword found in bio (max 50)
- +20 bonus for verified accounts
- Academic: h-index adds `min(h_index * 2, 40)`, citations add `min(log₁₀(citations) * 10, 30)`

### 6.2 Engagement Score (0–100)

For social platforms:
```
engagement_rate = (likes + comments + shares) / views
engagement_score = min(engagement_rate * 20, 100)
```

For academic: `min(log₁₀(citations + 1) * 25, 100)`

### 6.3 Reach Score (0–100)

Logarithmic scaling to prevent mega-influencers from drowning out smaller experts:
```python
if follower_count > 0:
    reach_score = min(math.log10(follower_count + 1) * 15, 100)
else:
    reach_score = 40.0  # Baseline for academic/blog (no followers)
```

| Followers | Reach Score |
|-----------|-------------|
| 0 (academic/blog) | 40 (baseline) |
| 1,000 | 45 |
| 10,000 | 60 |
| 100,000 | 75 |
| 1,000,000 | 90 |

### 6.4 Alignment Score (0–100)

The most critical dimension. Uses Gemini 2.5 Flash as an LLM judge:

1. Content texts are sent to `score_text_content()` in `nlp.py`
2. Gemini evaluates alignment against the target campaign topic
3. Returns a 0–100 score with evidence quotes
4. Specifically penalizes polarizing, aggressive, or protest-oriented language

### 6.5 Composite Score

```python
composite = (
    weights.credibility * credibility_score +
    weights.engagement * engagement_score +
    weights.reach * reach_score +
    weights.alignment * alignment_score
)
```

### Platform-Specific Weight Profiles

| Platform | Credibility | Engagement | Reach | Alignment |
|----------|------------|------------|-------|-----------|
| YouTube (default) | 25% | 20% | 15% | 40% |
| Twitter / Instagram | 20% | 25% | 15% | 40% |
| Academic | 35% | 20% | 5% | 40% |
| Blog | 30% | 15% | 5% | 50% |

**Rationale:** Academic and blog creators don't have meaningful follower counts, so reach weight is shifted to credibility and alignment. Blog creators get the highest alignment weight (50%) because their long-form content is the richest signal.

---

## 7. Search Pipeline — Deep Dive

### 7.1 Search Flow

```
User Query → Platform Selection → Check Database → Ingest if Needed → Score → Return
```

1. **Input parsing:** Determine if the query is a keyword, handle (`@username`), or URL (`http://...`)
2. **Database check:** Query PostgreSQL for existing creators matching the query. If ≥3 results exist, return them immediately as cached results
3. **Live discovery:** If not enough cached results (or `force_live: true`):
   - For keywords: `web_discovery.py` converts to platform-specific handles/URLs
   - For handles/URLs: Directly scrape the target
4. **Ingestion:** Platform-specific scraper fetches metadata + content
5. **Scoring:** Gemini alignment scoring + composite scoring
6. **Persistence:** Save all data to PostgreSQL for future queries
7. **Response:** Return creators with `from_cache` flag

### 7.2 Web Discovery Pipeline

When a user searches with a keyword (e.g., "nature"):

| Platform | Discovery Query | Extraction |
|----------|----------------|------------|
| Blog | `"nature blog articles expert"` | Extracts unique domains from Google results |
| Twitter | `"site:twitter.com nature expert"` | Parses handles from `twitter.com/{handle}` URLs |
| Instagram | `"site:instagram.com nature expert"` | Parses handles from `instagram.com/{handle}` URLs |
| YouTube | Uses YouTube Data API `search.list` directly | N/A — API is keyword-native |
| Academic | Uses Semantic Scholar/OpenAlex APIs directly | N/A — APIs are keyword-native |

Filtered domains (social media, search engines, Wikipedia, Amazon) are automatically excluded from blog discovery.

### 7.3 Platform Ingestor Details

| Ingestor | Data Source | Content Extracted |
|----------|-----------|-------------------|
| **YouTube** | YouTube Data API v3 | Channel metadata, video transcripts, subscriber counts |
| **Twitter** | Nitter proxies (3-instance rotation) | Name, bio, followers, recent tweets (up to 10) |
| **Instagram** | Public profile OG meta tags | Name, bio, follower count |
| **Blog** | RSS feeds + HTML crawling | Articles with author, title, date, full text (up to 10K chars) |
| **Academic** | Semantic Scholar + OpenAlex | Papers, h-index, citation count, abstracts |

---

## 8. Briefing Generation — Deep Dive

### 8.1 Generation Flow

```
POST /api/briefings/generate
    → Validate creator exists in DB
    → Create Briefing record (status: "pending")
    → Spawn background task
    → Return briefing_id immediately (202 Accepted)

Background Task:
    → Fetch Creator + ContentItems from DB
    → Build prompt with creator intel table + content excerpts
    → Call Gemini 2.5 Flash (2500 max tokens, temp 0.7)
    → Save response as Markdown (status: "completed")
    → On error: save error message (status: "failed")

Frontend:
    → Polls GET /api/briefings/{id} every 3 seconds
    → Shows loading animation during "pending"
    → Renders Markdown on "completed"
    → Shows error message on "failed"
```

### 8.2 Prompt Engineering

The briefing prompt uses a structured template with:
- **Creator Intel table** (Markdown table with name, platform, audience size, alignment score)
- **Content samples** (up to 5 excerpts, each truncated to 300 chars)
- **System instruction** requiring executive-level, polished output
- **Explicit section headings** with emoji markers for visual scanning

### 8.3 Output Quality Controls

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| Temperature | 0.7 | Creative but controlled — avoid hallucination |
| Max tokens | 2500 | Long enough for depth, short enough for focus |
| System instruction | "Executive communications specialist" | Ensures professional, non-AI-sounding tone |
| Content limit | 5 excerpts × 300 chars | Enough context without overwhelming the prompt |

---

## 9. Frontend Architecture

### 9.1 Page Structure

```
App.tsx (Router)
├── / → LandingPage.tsx
│   └── WebGL LightRays + Hero + CTA
├── /dashboard → SearchDashboard.tsx
│   └── Search input + Platform filter + CreatorCard grid
├── /analytics/:id → AnalyticsDashboard.tsx
│   └── Score breakdown + Content feed + Briefing trigger
└── /briefing/:id → BriefingsDashboard.tsx
    └── Polling loop + Markdown renderer
```

### 9.2 Key UI Patterns

| Pattern | Implementation |
|---------|---------------|
| **Database-first indication** | Green banner showing "Showing results from database" with "Refresh with Live Search" button |
| **Platform-aware metrics** | `CreatorCard` shows Subscribers (YouTube), Followers (Twitter/IG), Research Relevance (Academic), Content Alignment (Blog) |
| **Async briefing** | Loading spinner with descriptive text → auto-transitions to rendered Markdown |
| **Markdown rendering** | `react-markdown` with 15 custom component overrides for dark-theme styling (tables, blockquotes, headings, lists, code) |
| **WebGL background** | Custom shader with mouse-following light rays, noise, and distortion parameters |

### 9.3 API Client

`frontend/src/api/client.ts` provides typed methods for all API calls:

| Method | Endpoint | Description |
|--------|----------|-------------|
| `searchCreators(query, platforms, maxResults, forceLive)` | `POST /api/search` | Multi-platform search |
| `getCreators(platform, limit, offset)` | `GET /api/creators` | Paginated listing |
| `getCreator(id)` | `GET /api/creators/{id}` | Creator details |
| `generateBriefing(creatorId, context)` | `POST /api/briefings/generate` | Trigger generation |
| `getBriefingStatus(id)` | `GET /api/briefings/{id}` | Poll for completion |

---

## 10. API Reference

### 10.1 Search

```http
POST /api/search
Content-Type: application/json

{
  "query": "nature",
  "platforms": ["youtube", "twitter", "blog", "academic", "instagram"],
  "max_results": 10,
  "force_live": false
}
```

**Response (200):**
```json
{
  "creators": [
    {
      "id": "a1b2c3...",
      "name": "Nature Lens",
      "platform": "youtube",
      "follower_count": 125000,
      "composite_score": 78.5,
      "alignment_score": 85.0,
      "credibility_score": 42.0,
      "engagement_score": 55.0,
      "reach_score": 76.3,
      "profile_url": "https://youtube.com/..."
    }
  ],
  "total": 5,
  "from_cache": true
}
```

### 10.2 Briefings

```http
POST /api/briefings/generate
Content-Type: application/json

{
  "creator_id": "a1b2c3...",
  "campaign_context": "Plant-based nutrition campaign"
}
```

**Response (202):**
```json
{
  "briefing_id": "d4e5f6..."
}
```

```http
GET /api/briefings/{briefing_id}
```

**Response (200):**
```json
{
  "id": "d4e5f6...",
  "status": "completed",
  "content": "## 🎯 Creator Snapshot\n\nNature Lens is a ...",
  "created_at": "2026-03-12T15:30:00Z"
}
```

### 10.3 Creators

```http
GET /api/creators?platform=youtube&min_score=50&limit=20&offset=0
GET /api/creators/{creator_id}
GET /health
```

> 📖 **Interactive API Docs:** Visit `http://localhost:8000/docs` for the Swagger UI.

---

## 11. Environment & Configuration

### Required Environment Variables

| Variable | Description |
|----------|-------------|
| `GEMINI_API_KEY` | Google Gemini API key for alignment scoring and briefing generation |
| `YOUTUBE_API_KEY` | YouTube Data API v3 key for channel/video search |
| `DATABASE_URL` | PostgreSQL connection string (e.g., `postgresql://user:pass@localhost:5432/influencer_db`) |

### Optional Environment Variables

| Variable | Description |
|----------|-------------|
| `GOOGLE_CSE_API_KEY` | Google Custom Search API key (more reliable blog/social discovery) |
| `GOOGLE_CSE_ID` | Custom Search Engine ID |

### Database Setup

PostgreSQL with pgvector extension:
```sql
CREATE EXTENSION IF NOT EXISTS vector;
```

Tables are auto-created on startup via `Base.metadata.create_all()`. FK migrations run automatically with idempotent `CREATE ... IF NOT EXISTS` patterns.

---

## 12. Dependencies

### Python (`requirements.txt`)

| Category | Packages |
|----------|----------|
| **YouTube & Data** | `google-api-python-client`, `youtube-transcript-api` |
| **Database** | `sqlalchemy`, `asyncpg`, `psycopg2-binary`, `pgvector`, `greenlet` |
| **AI / NLP** | `google-genai`, `pydantic` |
| **API** | `fastapi`, `uvicorn`, `httpx` |
| **Resilience** | `tenacity` |
| **Web Scraping** | `beautifulsoup4`, `lxml`, `feedparser` |
| **CLI** | `typer`, `rich` |
| **Testing** | `pytest`, `pytest-asyncio` |
| **Utilities** | `python-dotenv` |

### Frontend (`package.json`)

React 18, TypeScript, Vite 7, Tailwind CSS v4, Framer Motion, Lucide React, react-markdown, react-router-dom

---

## 13. Known Limitations & Anti-Goals

| Item | Description |
|------|-------------|
| **Semantic Scholar rate limiting** | 429 errors on high-frequency queries. Mitigated by OpenAlex fallback |
| **Instagram scraping** | Limited to public accounts; only extracts meta tags (no post content) |
| **Nitter availability** | Twitter scraping depends on Nitter proxy uptime; falls back to shell profile |
| **Google Search throttling** | Blog/social discovery via Google may be rate-limited; Google CSE API recommended |
| **No automated outreach** | By design — the tool empowers human coordinators, not replaces them |
| **Public content only** | Privacy-first: no authenticated scraping, no private data indexing |
| **No real-time analytics** | Scores are computed at search time, not continuously monitored |

---

## 14. Future Roadmap

- [ ] **TikTok integration** — Scrape public profiles and trending content
- [ ] **LinkedIn integration** — Professional credential verification
- [ ] **Batch processing** — Queue-based ingestion for large-scale campaigns
- [ ] **Comparative dashboards** — Side-by-side creator comparison
- [ ] **Export to CRM** — Integration with HubSpot, Salesforce, etc.
- [ ] **Scheduled re-scoring** — Periodic refresh of alignment scores as content evolves
- [ ] **Team collaboration** — Multi-user workspace with shared briefings and annotations
