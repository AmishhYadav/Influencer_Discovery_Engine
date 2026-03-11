# Influent: Influencer Discovery Engine 🚀

A professional-grade engine for discovering, scoring, and analyzing influencers across multiple platforms. Influent leverages Gemini AI to provide dynamic alignment scoring and personalized engagement playbooks.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg)]()
[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)]()
[![Stars](https://img.shields.io/github/stars/AmishhYadav/Influencer_Discovery_Engine?style=social)](https://github.com/AmishhYadav/Influencer_Discovery_Engine)
[![Issues](https://img.shields.io/github/issues/AmishhYadav/Influencer_Discovery_Engine)](https://github.com/AmishhYadav/Influencer_Discovery_Engine/issues)

---

## 📍 Table of Contents

- [Project Overview](#-project-overview)
- [Key Features](#-key-features)
- [Tech Stack](#-tech-stack)
- [Architecture](#-architecture)
- [Installation](#-installation)
- [Usage](#-usage)
- [Project Structure](#-project-structure)
- [Configuration](#-configuration)
- [Roadmap](#-roadmap)
- [Contributing](#-contributing)
- [License](#-license)
- [Author](#-author)

---

## 🔍 Project Overview

Finding the right creator for a campaign is often manual and slow. **Influent** solves this by unifying data from YouTube, blogs, social media (Twitter/Instagram), and academic registries into a single scorable platform. 

The engine doesn't just look at follower counts—it analyzes actual content (transcripts, posts, abstracts) using LLMs to calculate a real-time **Alignment Score** against your specific campaign goals.

---

## ✨ Key Features

- **Unified Multi-Source Search**: Discover creators across YouTube, Twitter, Instagram, Blogs, and Academic sources in one interface.
- **Dynamic AI Scoring**: Real-time evaluation of *Credibility*, *Engagement*, *Reach*, and *Alignment* scores.
- **Live Content Ingestion**: Automatically fetches latest YouTube transcripts and blog content for fresh analysis.
- **AI Strategy Briefings**: One-click generation of professional outreach "Playbooks" tailored to your campaign context.
- **Comparison Engine**: Side-by-side analytics for shortlisted creators to find the perfect fit.
- **High-Performance Caching**: Intelligent read-through caching for sub-second search results on known entities.

---

## 💻 Tech Stack

### Backend
- **Framework**: [FastAPI](https://fastapi.tiangolo.com/) (Python 3.10+)
- **ORM**: [SQLAlchemy](https://www.sqlalchemy.org/)
- **Database**: PostgreSQL (Production) / SQLite (Local)
- **Task Queue**: FastAPI BackgroundTasks

### AI / Data
- **LLM**: [Google Gemini API](https://ai.google.dev/) (Flash 2.5)
- **Ingestion**: YouTube Data API v3, YouTube Transcript API
- **NLP**: Custom scoring algorithms based on vector similarity and semantic analysis.

### Frontend
- **Framework**: [React](https://reactjs.org/) with [Vite](https://vitejs.dev/)
- **Styling**: Vanilla CSS / Tailwind (Optional)
- **Icons/Animations**: [Lucide React](https://lucide.dev/), [Framer Motion](https://www.framer.com/motion/)
- **Routing**: React Router v6

---

## 🏗️ Architecture

Influent follows a modular **Service-Oriented Architecture**:

1. **Ingestion Layer**: Connectors for various APIs (YouTube, Twitter Scrapers, Academic crawlers).
2. **Analysis Layer (AI Engine)**: Process raw text through Gemini to extract semantic meaning and alignment quotes.
3. **Data Layer**: Unified model that normalizes diverse platform data into a standard `Creator` and `ContentItem` schema.
4. **API Layer**: REST endpoints for search, analytics detail, and async briefing generation.

---

## ⚙️ Installation

### Prerequisites
- Python 3.10+
- Node.js 18+
- [Gemini API Key](https://aistudio.google.com/)
- [YouTube API Key](https://console.cloud.google.com/)

### 1. Clone the Repository
```bash
git clone https://github.com/AmishhYadav/Influencer_Discovery_Engine.git
cd Influencer_Discovery_Engine
```

### 2. Backend Setup
```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
touch .env
```
*Add your API keys to the `.env` file (see [Configuration](#-configuration)).*

### 3. Frontend Setup
```bash
cd frontend
npm install
```

---

## 🚀 Usage

### Start the Backend
```bash
# From the project root
uvicorn src.api.main:app --reload --port 8000
```

### Start the Frontend
```bash
# In another terminal instance
cd frontend
npm run dev
```

Visit `http://localhost:5173` to launch the dashboard.

---

## 📂 Project Structure

```text
Influencer_Discovery_Engine/
├── src/
│   ├── api/                # FastAPI routers and schemas
│   ├── ingestion/          # Platform-specific connectors (YT, Blog, etc.)
│   ├── analysis/           # AI scoring and NLP logic
│   └── db/                 # Models and DAOs
├── frontend/
│   ├── src/
│   │   ├── pages/         # Search, Analytics, Briefings dashboards
│   │   ├── components/    # Reusable UI elements
│   │   └── api/           # Frontend API client
├── scripts/                # Utility scripts (ingestion, migrations)
├── tests/                  # Unit and integration tests
└── .env.example            # Environment template
```

---

## 🛠️ Configuration

The following environment variables are required in your `.env` file:

| Variable | Description |
|----------|-------------|
| `YOUTUBE_API_KEY` | Google Cloud API key for YouTube Data V3. |
| `GEMINI_API_KEY` | Google AI Studio key for LLM analysis. |
| `DATABASE_URL` | SQLAlchemy connection string (Default: `sqlite:///./engine.db`). |
| `VITE_API_BASE_URL` | Frontend URL for the backend API. |

---

## 📸 Screenshots / Demo

*(Coming Soon)* - Integration images of the Discovery Dashboard and AI Briefing sections.

---

## 🗺️ Roadmap

- [ ] **Advanced Filtering**: Filter by location, language, and audience age brackets.
- [ ] **CRM Integration**: Export leads directly to HubSpot or Salesforce.
- [ ] **X (Twitter) & Instagram API**: Official LinkedIn/X integration for premium reach.
- [ ] **Campaign Management**: Track historical outreach success per creator.
- [ ] **Social Listening**: Real-time alerts for creators mentioning specific keywords.

---

## 🤝 Contributing

We welcome contributions! 

1. Fork the Project.
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`).
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`).
4. Push to the Branch (`git push origin feature/AmazingFeature`).
5. Open a Pull Request.

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

---

## 👤 Author

**Amish Yadav**
- GitHub: [@AmishhYadav](https://github.com/AmishhYadav)
- Project: [Influencer Discovery Engine](https://github.com/AmishhYadav/Influencer_Discovery_Engine)

---

## 🎁 Acknowledgments

- [Google DeepMind](https://deepmind.google/) for the Gemini API.
- The open-source community for the excellent React-FastAPI ecosystem.
