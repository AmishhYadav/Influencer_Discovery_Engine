# Influent: Non-Activist Influencer Discovery Engine 🌿

**Influent** is an AI-powered discovery engine built for advocacy organizations to identify highly credible, naturally aligned creative voices (like doctors, scientists, and chefs) using existing content signals—**without selecting for polarizing activism.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg)]()
[![Development Phase](https://img.shields.io/badge/phase-1_%E2%80%93_Ingestion-blue.svg)]()

---

## 📍 Table of Contents

- [What This Is](#-what-this-is)
- [Core Value](#-core-value)
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

---

## 🔍 What This Is

Influent helps advocacy outreach teams identify influencers whose public content already aligns with core organizational values (e.g., plant-based health, sustainability, or ethical food systems). Unlike traditional tools that search for hashtags, Influent uses Gemini-powered semantic analysis to find professionals whose primary identity is expertise, not activism.

---

## 💡 Core Value

> **"Identify highly credible, naturally aligned creative voices using existing content signals without selecting for polarizing activism."**

The system actively deprioritizes polarizing messaging in favor of "soft activism" and natural alignment, making outreach more effective and credible for mainstream audiences.

---

## ✨ Key Features

- **Semantic Alignment Engine**: Uses Gemini AI to analyze YouTube transcripts and identify deep thematic alignment beyond simple keywords.
- **Multi-Source discovery**: Unified database handling YouTube, Blog authors, Academic researchers, and Social Media profiles.
- **Credibility Scoring**: Complex algorithm that ranks candidates based on professional authority (e.g., Doctors, Chefs, Scientists) and audience engagement.
- **AI Strategy Briefings**: Generates "Outreach Playbooks" for human coordinators, providing specific content citations and suggested talking points.
- **Comparison Analytics**: Side-by-side score breakdowns for shortlisted creators.

---

## 💻 Tech Stack

### Core Engine
- **Backend API**: [FastAPI](https://fastapi.tiangolo.com/) (Python 3.10+)
- **Analysis Logic**: [Google Gemini API](https://ai.google.dev/) (Flash 2.5) for semantic scoring and summarization.
- **Database**: PostgreSQL with `pgvector` compatibility (supported via local SQLAlchemy/SQLite fallback).
- **Ingestion**: `youtube-transcript-api` and Google Search integration.

### Frontend Dashboard
- **Framework**: [React](https://reactjs.org/) + [Vite](https://vitejs.dev/)
- **UI System**: Framer Motion for animations & Lucide icons.
- **API Integration**: Custom Type-safe client for unified search and briefing polling.

---

## ⚙️ Installation

### 1. Clone & Setup
```bash
git clone https://github.com/AmishhYadav/Influencer_Discovery_Engine.git
cd Influencer_Discovery_Engine
```

### 2. Backend Installation
```bash
# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Frontend Installation
```bash
cd frontend
npm install
```

---

## 🚀 Usage

### 1. Configure Environment
Create a `.env` file in the root directory:
```env
YOUTUBE_API_KEY=your_key_here
GEMINI_API_KEY=your_key_here
DATABASE_URL=sqlite:///./engine.db
```

### 2. Run the Engine
```bash
# Terminal 1: Backend
uvicorn src.api.main:app --reload

# Terminal 2: Frontend
cd frontend
npm run dev
```

---

## 📂 Project Structure

```text
Influencer_Discovery_Engine/
├── .planning/          # Vision, Requirements, and Phase Tracking
├── src/
│   ├── api/            # FastAPI Routers & Pydantic Schemas
│   ├── ingestion/      # YouTube Metadata & Transcript Fetchers
│   ├── analysis/       # Scoring & NLP Logic (Gemini Integrated)
│   └── db/             # Unified Creator & Content Models
└── frontend/           # React Search & Analytics Dashboards
```

---

## 🗺️ Roadmap

- [x] **Phase 1: Ingestion** (YouTube Transcript Pipeline)
- [x] **Phase 2: Analysis Engine** (Semantic Alignment Scoring)
- [x] **Phase 3: Core Data API** (Unified Creator Schema)
- [x] **Phase 4: Frontend Dashboard** (Search & Analytics)
- [x] **Phase 5: Briefing Generator** (Playbook Strategy AI)
- [ ] **Phase 6: Advanced Source Expansion** (Official X/LinkedIn integration)

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

---

## 👤 Author

**Amish Yadav**
- Project Repository: [Influencer Discovery Engine](https://github.com/AmishhYadav/Influencer_Discovery_Engine)
- Reference Documents: [.planning/PROJECT.md](file://./.planning/PROJECT.md)
