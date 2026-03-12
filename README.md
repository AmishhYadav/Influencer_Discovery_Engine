<div align="center">

# 🔍 Influencer Discovery Engine

**An AI-powered platform that discovers, scores, and profiles content creators across YouTube, Twitter/X, Instagram, Blogs, and Academia — built for advocacy organizations seeking credible, naturally-aligned voices.**

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110%2B-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-18-61DAFB?logo=react&logoColor=black)](https://react.dev)
[![Vite](https://img.shields.io/badge/Vite-7-646CFF?logo=vite&logoColor=white)](https://vite.dev)
[![Gemini](https://img.shields.io/badge/Google_Gemini-2.5-4285F4?logo=google&logoColor=white)](https://ai.google.dev)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-316192?logo=postgresql&logoColor=white)](https://www.postgresql.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

[Features](#-features) · [Architecture](#-system-architecture) · [Quick Start](#-quick-start) · [API Reference](#-api-reference) · [Documentation](#-documentation)

</div>

---

## 📋 Table of Contents

- [Features](#-features)
- [System Architecture](#-system-architecture)
- [Data Flow](#-data-flow)
- [Scoring Engine](#-scoring-engine)
- [Tech Stack](#-tech-stack)
- [Quick Start](#-quick-start)
  - [Prerequisites](#prerequisites)
  - [Backend Setup](#backend-setup)
  - [Frontend Setup](#frontend-setup)
  - [Environment Variables](#environment-variables)
- [Project Structure](#-project-structure)
- [API Reference](#-api-reference)
- [How It Works](#-how-it-works)
- [Documentation](#-documentation)
- [Contributing](#-contributing)
- [License](#-license)

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🎯 **Multi-Platform Discovery** | Search creators across YouTube, Twitter/X, Instagram, Blogs, and Academic databases in one unified query |
| 🧠 **AI Alignment Scoring** | Google Gemini-powered analysis evaluates content alignment against campaign topics with a 0–100 score |
| 📊 **4-Dimensional Scoring** | Composite scores computed from Credibility, Engagement, Reach, and Alignment — with platform-specific weights |
| 🗃️ **Database-First Search** | Results are cached in PostgreSQL. Subsequent searches return instant results with a one-click live refresh option |
| 📝 **AI Briefing Generator** | One-click generation of executive-level engagement playbooks with talking points, evidence, and outreach strategy |
| 🔍 **Web Discovery** | Keyword queries automatically discover relevant blog URLs, Twitter handles, and Instagram profiles via Google Search |
| 🌐 **Keyword → Handle Resolution** | Type "nature" instead of "@NatGeo" — the engine finds relevant profiles across all platforms |
| 🎨 **Premium Dashboard** | Glassmorphic dark-themed UI with animated light rays, real-time search, and Markdown-rendered briefings |

---

## 🏗 System Architecture

```
┌───────────────────────────────────────────────────────┐
│             Frontend  (React + Vite)                  │
│   Landing Page · Search · Analytics · Briefings       │
└───────────────────────────┬───────────────────────────┘
                            │
                       REST API
                            │
┌───────────────────────────▼───────────────────────────┐
│                                                       │
│                   FastAPI Backend                     │
│                                                       │
│  Routers:                                             │
│    Search · Creators · Briefings · Background Tasks   │
│                                                       │
│  Ingestion Layer:                                     │
│    YouTube API · Twitter · Instagram                  │
│    Blog Scraper · Academic · Web Discovery            │
│                                                       │
│  Analysis Engine:                                     │
│    Gemini LLM Scoring · Composite Scorer              │
│    Text Chunker · Embeddings (1536-dim)               │
│                                                       │
└───────────────────────────┬───────────────────────────┘
                            │
              ┌─────────────▼──────────────┐
              │  PostgreSQL  +  pgvector   │
              │  Creators · Content · AI   │
              └────────────────────────────┘
```

---

## 🔄 Data Flow

```mermaid
sequenceDiagram
    participant U as 👤 User
    participant FE as 🖥️ Frontend
    participant API as ⚡ API
    participant DB as 💾 Database
    participant ING as 📥 Ingestors
    participant AI as 🧠 Gemini AI

    U->>FE: Search "nature"
    FE->>API: POST /api/search
    API->>DB: Check for cached results (≥3?)

    alt Database has ≥3 results
        DB-->>API: Cached creators
        API-->>FE: Results (from_cache: true)
        FE-->>U: Show results + "Refresh" button
    else Not enough cached results
        API->>ING: Discover & scrape platforms
        ING->>AI: Score content alignment
        AI-->>ING: alignment_score (0-100)
        ING->>DB: Persist creators + scores
        DB-->>API: New creators
        API-->>FE: Results (from_cache: false)
        FE-->>U: Show results
    end

    U->>FE: Click "Generate Briefing"
    FE->>API: POST /api/briefings/generate
    API->>AI: Generate engagement playbook
    AI-->>API: Markdown briefing
    API->>DB: Save briefing
    FE->>API: Poll GET /api/briefings/{id}
    API-->>FE: Completed briefing
    FE-->>U: Rendered Markdown briefing
```

---

## 📐 Scoring Engine

Creators are evaluated across **4 dimensions**, each scored 0–100, then combined using **platform-specific weights**:

```
Composite = w₁·Credibility + w₂·Engagement + w₃·Reach + w₄·Alignment
```

### Platform Weight Profiles

| Dimension | YouTube | Twitter / IG | Academic | Blog |
|-----------|---------|-------------|----------|------|
| **Credibility** | 25% | 20% | 35% | 30% |
| **Engagement** | 20% | 25% | 20% | 15% |
| **Reach** | 15% | 15% | 5% | 5% |
| **Alignment** | 40% | 40% | 40% | 50% |

### Score Breakdown

```mermaid
graph LR
    subgraph Credibility["🛡️ Credibility (0-100)"]
        BIO[Professional Keywords]
        VER[Verification Status]
        HI[h-index / Citations]
    end

    subgraph Engagement["💬 Engagement (0-100)"]
        ER[Interaction Rate]
        CIT[Citation Impact]
    end

    subgraph Reach["📡 Reach (0-100)"]
        FOL[Log-Scaled Followers]
        BASE[Platform Baseline]
    end

    subgraph Alignment["🎯 Alignment (0-100)"]
        LLM[Gemini LLM Judge]
        QUO[Evidence Quotes]
    end

    Credibility --> COMP[Composite Score]
    Engagement --> COMP
    Reach --> COMP
    Alignment --> COMP
```

| Metric | How It's Calculated |
|--------|-------------------|
| **Credibility** | Professional keywords in bio (Dr., PhD, etc.), verification status, h-index, citation count |
| **Engagement** | Social: (likes + comments + shares) / views. Academic: log-scaled citation count |
| **Reach** | Log₁₀ scaled follower count. Academic/Blog get a 40-point baseline |
| **Alignment** | Gemini LLM evaluates content against the campaign topic. Penalizes polarizing language |

---

## 🛠 Tech Stack

### Backend
| Component | Technology |
|-----------|-----------|
| **Framework** | FastAPI (Python 3.9+) |
| **AI / LLM** | Google Gemini 2.5 Flash |
| **Embeddings** | Gemini Text Embedding 004 (1536-dim) |
| **Database** | PostgreSQL + pgvector |
| **ORM** | SQLAlchemy 2.0 |
| **Web Scraping** | httpx + BeautifulSoup4 + feedparser |
| **Validation** | Pydantic v2 |

### Frontend
| Component | Technology |
|-----------|-----------|
| **Framework** | React 18 + TypeScript |
| **Build Tool** | Vite 7 |
| **Styling** | Tailwind CSS v4 |
| **Animations** | Framer Motion |
| **Markdown** | react-markdown |
| **Icons** | Lucide React |

---

## 🚀 Quick Start

### Prerequisites

- **Python** 3.9+
- **Node.js** 18+
- **PostgreSQL** 15+ (with pgvector extension)
- **Google API Keys** (Gemini + YouTube Data API v3)

### Backend Setup

```bash
# Clone the repository
git clone https://github.com/AmishhYadav/Influencer_Discovery_Engine.git
cd Influencer_Discovery_Engine

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install
```

### Environment Variables

Create a `.env` file in the project root:

```env
# Required
GEMINI_API_KEY=your_gemini_api_key
YOUTUBE_API_KEY=your_youtube_data_api_v3_key
DATABASE_URL=postgresql://user:pass@localhost:5432/influencer_db

# Optional — enables Google Custom Search for better blog/social discovery
GOOGLE_CSE_API_KEY=your_google_cse_key
GOOGLE_CSE_ID=your_custom_search_engine_id
```

### Running the Application

**Terminal 1 — Backend:**
```bash
source .venv/bin/activate
uvicorn src.api.main:app --reload --port 8000
```

**Terminal 2 — Frontend:**
```bash
cd frontend
npm run dev
```

| Service | URL |
|---------|-----|
| **Frontend** | http://localhost:5173 |
| **API** | http://localhost:8000 |
| **API Docs** | http://localhost:8000/docs |

---

## 📁 Project Structure

```
Influencer_Discovery_Engine/
├── src/
│   ├── api/                          # FastAPI application
│   │   ├── main.py                   # App entry point + startup migrations
│   │   ├── schemas.py                # Pydantic request/response models
│   │   ├── deps.py                   # Dependency injection (DB session)
│   │   ├── tasks.py                  # Background tasks (briefing generation)
│   │   └── routers/
│   │       ├── search.py             # Multi-platform search endpoint
│   │       ├── creators.py           # Creator CRUD + listing
│   │       └── briefings.py          # Briefing generation + retrieval
│   │
│   ├── ingestion/                    # Data collection modules
│   │   ├── youtube_api.py            # YouTube Data API v3 integration
│   │   ├── transcripts.py            # YouTube transcript extraction
│   │   ├── social_media.py           # Twitter (Nitter) & Instagram scraper
│   │   ├── blog_scraper.py           # Blog RSS/HTML discovery + extraction
│   │   ├── academic.py               # Semantic Scholar + OpenAlex integration
│   │   ├── web_discovery.py          # Google Search → URL/handle resolver
│   │   └── cleaner.py                # Text normalization pipeline
│   │
│   ├── analysis/                     # AI scoring & NLP
│   │   ├── nlp.py                    # Gemini embeddings + LLM alignment judge
│   │   ├── scoring.py                # 4-dimensional composite scoring engine
│   │   └── chunker.py                # Transcript text chunking
│   │
│   └── db/                           # Database layer
│       ├── models.py                 # SQLAlchemy models (Creator, ContentItem, Briefing)
│       └── dao.py                    # Data access objects (CRUD operations)
│
├── frontend/
│   └── src/
│       ├── api/
│       │   └── client.ts             # Typed API client
│       ├── pages/
│       │   ├── LandingPage.tsx        # Hero landing page
│       │   ├── SearchDashboard.tsx     # Multi-platform search interface
│       │   ├── AnalyticsDashboard.tsx  # Creator detail & scoring breakdown
│       │   └── BriefingsDashboard.tsx  # AI briefing viewer (Markdown)
│       └── components/
│           ├── CreatorCard.tsx         # Platform-aware creator cards
│           ├── DashboardLayout.tsx     # Shared layout wrapper
│           └── LightRays.tsx           # WebGL animated background
│
├── docs/
│   └── DOCUMENTATION.md              # Detailed technical documentation
├── tests/                            # Pytest test suite
├── requirements.txt                  # Python dependencies
└── README.md
```

---

## 📡 API Reference

### Base URL: `http://localhost:8000/api`

### Search Creators

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

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `query` | `string` | — | Keyword, handle (@user), or URL |
| `platforms` | `string[]` | all | Filter by platforms |
| `max_results` | `int` | `10` | Results per platform |
| `force_live` | `bool` | `false` | Skip DB cache, force live search |

**Response:**
```json
{
  "creators": [
    {
      "id": "uuid",
      "name": "Nature Lens",
      "platform": "youtube",
      "follower_count": 125000,
      "composite_score": 78.5,
      "alignment_score": 85.0,
      "credibility_score": 42.0,
      "profile_url": "https://youtube.com/..."
    }
  ],
  "total": 5,
  "from_cache": true
}
```

### Generate Briefing

```http
POST /api/briefings/generate
Content-Type: application/json

{
  "creator_id": "uuid",
  "campaign_context": "Plant-based nutrition campaign"
}
```

### Get Briefing Status

```http
GET /api/briefings/{briefing_id}
```

### List Creators

```http
GET /api/creators?platform=youtube&min_score=50&limit=20&offset=0
```

> 📖 **Interactive API Docs:** Visit `http://localhost:8000/docs` for the full Swagger UI.

---

## ⚙️ How It Works

### Campaign Discovery Workflow

```mermaid
graph TD
    A["🔍 1. User enters search query"] --> B{DB has ≥3 results?}
    B -->|Yes| C["⚡ Instant results from database"]
    B -->|No| D["🌐 2. Web Discovery"]
    D --> E["📥 3. Platform Ingestors scrape data"]
    E --> F["🧠 4. Gemini scores content alignment"]
    F --> G["💾 5. Results saved to PostgreSQL"]
    G --> H["📊 6. Composite scores computed"]
    H --> I["🖥️ 7. Results displayed with scores"]
    C --> I
    I --> J{User clicks Generate Briefing?}
    J -->|Yes| K["📝 8. Gemini generates playbook"]
    K --> L["✅ 9. Rendered Markdown briefing"]
    J -->|No| M["🔄 User can force live refresh"]
    M --> D
```

### Step-by-Step

1. **Query Parsing** — The system determines if the input is a keyword, handle, or URL and routes to the correct ingestors.

2. **Web Discovery** — For keyword queries, Google Search discovers relevant blog URLs, Twitter handles, and Instagram profiles automatically.

3. **Platform Ingestion** — Each platform module fetches creator metadata and content:
   - **YouTube**: Channel data via API + transcripts via `youtube-transcript-api`
   - **Twitter**: Profile scraping via Nitter public proxies
   - **Instagram**: Public profile meta tag extraction
   - **Blog**: RSS feed discovery + HTML article extraction
   - **Academic**: Semantic Scholar + OpenAlex paper search

4. **AI Content Scoring** — Gemini 2.5 Flash evaluates scraped content against the campaign topic, producing an alignment score (0–100) with evidence quotes. The system penalizes polarizing or activist language.

5. **Composite Scoring** — Each creator gets a 4-dimensional score with platform-specific weight profiles. Academic creators aren't penalized for having no followers.

6. **Database Persistence** — All live data is stored permanently. Subsequent identical searches return instant database results.

7. **Briefing Generation** — One-click AI playbooks include Creator Snapshot, Mission Alignment, Credibility Assessment, Evidence Quotes, and Outreach Strategy.

---

## 📖 Documentation

For in-depth technical documentation, including the project's core philosophy of **"Soft Activism"** detection and the complete product roadmap, see:

→ [`docs/DOCUMENTATION.md`](docs/DOCUMENTATION.md)

---

## 🧪 Running Tests

```bash
source .venv/bin/activate
pytest tests/ -v --tb=short
```

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### Development Guidelines

- Follow [PEP 8](https://pep8.org/) for Python code
- Use TypeScript strict mode for frontend code
- Write tests for new features
- Update documentation for API changes

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

<div align="center">

**Built with ❤️ using FastAPI, React, and Google Gemini**

[⬆ Back to Top](#-influencer-discovery-engine)

</div>
