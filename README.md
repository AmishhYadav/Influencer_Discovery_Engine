<div align="center">

# 🔍 Influencer Discovery Engine

**An AI-powered platform for discovering, analyzing, and ranking social media influencers using advanced NLP and multi-platform data aggregation.**

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Next.js](https://img.shields.io/badge/Next.js-14-black?logo=next.js&logoColor=white)](https://nextjs.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

[Features](#-features) · [Architecture](#-architecture) · [Getting Started](#-getting-started) · [API Reference](#-api-reference) · [Contributing](#-contributing)

</div>

---

## 📋 Table of Contents

- [Features](#-features)
- [Architecture](#-architecture)
- [Tech Stack](#-tech-stack)
- [Getting Started](#-getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Environment Variables](#environment-variables)
  - [Running the Application](#running-the-application)
- [Project Structure](#-project-structure)
- [API Reference](#-api-reference)
- [How It Works](#-how-it-works)
- [Contributing](#-contributing)
- [License](#-license)

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🤖 **AI-Powered Analysis** | Leverages NLP (SpaCy, NLTK) for content analysis, sentiment scoring, and topic extraction |
| 🌐 **Multi-Platform Support** | Aggregates data from YouTube, Instagram, Twitter/X, and more via RapidAPI |
| 📊 **Smart Ranking** | Composite scoring algorithm combining engagement rate, reach, relevance, and authenticity |
| 🔎 **Natural Language Search** | Search for influencers using plain English queries (e.g., *"tech reviewers with 100k+ followers"*) |
| 📈 **Real-Time Analytics** | Live engagement metrics, audience demographics, and growth trends |
| 🏷️ **Niche Classification** | Automatic categorization into niches like Tech, Fashion, Fitness, Gaming, etc. |
| ⚡ **Caching Layer** | Redis-backed caching for fast repeated queries and rate-limit management |
| 🎨 **Modern Dashboard** | Responsive Next.js frontend with interactive charts and filtering |

---

## 🏗 Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Next.js Frontend                     │
│              (Dashboard · Search · Analytics)           │
└──────────────────────┬──────────────────────────────────┘
                       │ REST API
┌──────────────────────▼──────────────────────────────────┐
│                   FastAPI Backend                        │
│  ┌─────────────┐ ┌──────────────┐ ┌──────────────────┐ │
│  │  API Router  │ │  NLP Engine  │ │  Ranking Engine  │ │
│  │  & Endpoints │ │ (SpaCy/NLTK) │ │ (Scoring Logic)  │ │
│  └──────┬──────┘ └──────┬───────┘ └────────┬─────────┘ │
│         │               │                  │            │
│  ┌──────▼───────────────▼──────────────────▼─────────┐  │
│  │              Data Aggregation Layer               │  │
│  │    (YouTube · Instagram · Twitter · RapidAPI)     │  │
│  └───────────────────────┬───────────────────────────┘  │
│                          │                              │
│  ┌───────────────────────▼───────────────────────────┐  │
│  │          Cache Layer (Redis / In-Memory)          │  │
│  └───────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

---

## 🛠 Tech Stack

### Backend
- **Framework:** FastAPI (Python 3.8+)
- **NLP:** SpaCy, NLTK, TextBlob
- **Data Fetching:** HTTPX, RapidAPI integrations
- **Caching:** Redis (optional, falls back to in-memory)
- **Validation:** Pydantic v2

### Frontend
- **Framework:** Next.js 14 (React 18)
- **Styling:** Tailwind CSS
- **Charts:** Recharts
- **HTTP Client:** Axios
- **Language:** TypeScript

### DevOps & Tooling
- **Containerization:** Docker & Docker Compose
- **Testing:** Pytest
- **Linting:** ESLint, Prettier

---

## 🚀 Getting Started

### Prerequisites

- **Python** 3.8+
- **Node.js** 18+
- **npm** or **yarn**
- **Redis** (optional — the app falls back to in-memory caching)
- API keys from [RapidAPI](https://rapidapi.com/) for social media data

### Installation

```bash
# Clone the repository
git clone https://github.com/your-username/Influencer_Discovery_Engine.git
cd Influencer_Discovery_Engine
```

#### Backend Setup

```bash
cd backend

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Download NLP models
python -m spacy download en_core_web_sm
python -m nltk.downloader punkt vader_lexicon stopwords
```

#### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install
```

### Environment Variables

Create a `.env` file in the `backend/` directory:

```env
# API Keys
RAPID_API_KEY=your_rapidapi_key_here

# YouTube (optional — direct API)
YOUTUBE_API_KEY=your_youtube_api_key_here

# Redis (optional)
REDIS_URL=redis://localhost:6379/0

# Server
HOST=0.0.0.0
PORT=8000
DEBUG=true
```

Create a `.env.local` file in the `frontend/` directory:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Running the Application

#### Option 1: Docker Compose (Recommended)

```bash
docker-compose up --build
```

The frontend will be available at `http://localhost:3000` and the API at `http://localhost:8000`.

#### Option 2: Manual

**Terminal 1 — Backend:**
```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 — Frontend:**
```bash
cd frontend
npm run dev
```

---

## 📁 Project Structure

```
Influencer_Discovery_Engine/
├── backend/
│   ├── app/
│   │   ├── main.py                 # FastAPI application entry point
│   │   ├── config.py               # Configuration & environment settings
│   │   ├── api/
│   │   │   └── routes/
│   │   │       ├── influencer_routes.py  # Influencer search & detail endpoints
│   │   │       └── analytics_routes.py   # Analytics & trending endpoints
│   │   ├── models/
│   │   │   └── influencer.py       # Pydantic data models
│   │   ├── services/
│   │   │   ├── data_aggregator.py  # Multi-platform data fetching
│   │   │   ├── youtube_service.py  # YouTube API integration
│   │   │   ├── instagram_service.py# Instagram data service
│   │   │   ├── twitter_service.py  # Twitter/X data service
│   │   │   ├── nlp_analyzer.py     # NLP content & sentiment analysis
│   │   │   ├── ranking_engine.py   # Influencer scoring & ranking
│   │   │   └── cache_service.py    # Redis / in-memory caching
│   │   └── utils/
│   │       ├── helpers.py          # Shared utility functions
│   │       └── rate_limiter.py     # API rate-limit handling
│   ├── tests/                      # Pytest test suite
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── app/                    # Next.js App Router pages
│   │   ├── components/             # Reusable UI components
│   │   ├── services/               # API client services
│   │   ├── types/                  # TypeScript type definitions
│   │   └── utils/                  # Frontend utilities
│   ├── public/                     # Static assets
│   ├── package.json
│   ├── tailwind.config.ts
│   ├── tsconfig.json
│   └── Dockerfile
├── docker-compose.yml
├── .gitignore
├── LICENSE
└── README.md
```

---

## 📡 API Reference

### Base URL

```
http://localhost:8000/api
```

### Endpoints

#### Search Influencers

```http
GET /api/influencers/search?query={query}&platform={platform}&niche={niche}&limit={limit}
```

| Parameter  | Type     | Default | Description                          |
|------------|----------|---------|--------------------------------------|
| `query`    | `string` | —       | Natural language search query        |
| `platform` | `string` | `all`   | Filter by platform (`youtube`, `instagram`, `twitter`) |
| `niche`    | `string` | `all`   | Filter by niche (`tech`, `fashion`, `fitness`, etc.)   |
| `limit`    | `int`    | `20`    | Number of results to return          |

**Response:**
```json
{
  "results": [
    {
      "id": "abc123",
      "name": "Jane Doe",
      "platform": "youtube",
      "niche": "technology",
      "followers": 250000,
      "engagement_rate": 4.8,
      "relevance_score": 92.5,
      "avatar_url": "https://...",
      "profile_url": "https://youtube.com/..."
    }
  ],
  "total": 1,
  "query_analysis": {
    "keywords": ["tech", "reviewer"],
    "sentiment": "neutral",
    "intent": "discovery"
  }
}
```

#### Get Influencer Details

```http
GET /api/influencers/{influencer_id}
```

#### Get Trending Influencers

```http
GET /api/analytics/trending?platform={platform}&timeframe={timeframe}
```

#### Get Niche Overview

```http
GET /api/analytics/niches
```

> 📖 **Interactive API Docs:** Visit `http://localhost:8000/docs` for the full Swagger UI.

---

## ⚙️ How It Works

1. **Query Parsing** — The NLP engine parses the user's search query to extract keywords, intent, filters, and semantic meaning using SpaCy and NLTK.

2. **Data Aggregation** — The platform fetches influencer data from multiple social media APIs concurrently via HTTPX async requests through RapidAPI.

3. **Content Analysis** — Each influencer's recent content is analyzed for:
   - **Sentiment** (positive/negative/neutral)
   - **Topic relevance** (keyword & semantic matching)
   - **Engagement authenticity** (bot detection heuristics)

4. **Scoring & Ranking** — A composite score is computed:
   ```
   Score = w₁·EngagementRate + w₂·RelevanceScore + w₃·AuthenticityScore + w₄·GrowthRate
   ```
   Weights are dynamically adjusted based on the query context.

5. **Results Delivery** — Ranked results are returned with rich metadata, cached for subsequent requests, and rendered on the Next.js dashboard.

---

## 🧪 Running Tests

```bash
cd backend
pytest tests/ -v --tb=short
```

```bash
cd frontend
npm run test
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

**Built with ❤️ using FastAPI & Next.js**

[⬆ Back to Top](#-influencer-discovery-engine)

</div>
