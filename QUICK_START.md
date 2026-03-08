# Quick Start Guide

Get the Influencer Discovery Engine running in 5 minutes!

## TL;DR - Copy & Paste Commands

### Terminal 1: Start Backend
```bash
python -m venv venv
source venv/bin/activate  # or: venv\Scripts\activate on Windows
pip install -r requirements.txt
cp .env.example .env.local
# Edit .env.local with your API keys (GEMINI_API_KEY, YOUTUBE_API_KEY)
python -m uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000
```

### Terminal 2: Start Frontend
```bash
npm install
# Make sure .env.local has: NEXT_PUBLIC_API_URL=http://localhost:8000
npm run dev
```

### Open Browser
```
Frontend: http://localhost:3000
Backend Docs: http://localhost:8000/docs
```

## Step-by-Step

### Step 1: Backend
Your backend must be running first. If it's already running, skip to Step 2.

```bash
# Create virtual environment
python -m venv venv

# Activate it
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Create environment file
cp .env.example .env.local
```

**Edit `.env.local`** and add your API keys:
```
GEMINI_API_KEY=your_key_here
YOUTUBE_API_KEY=your_key_here
```

**Start the server**:
```bash
python -m uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Step 2: Frontend

Open a **new terminal** and run:

```bash
# Install dependencies
npm install

# Check .env.local exists with:
# NEXT_PUBLIC_API_URL=http://localhost:8000

# Start development server
npm run dev
```

You should see:
```
> Local:        http://localhost:3000
```

### Step 3: Open in Browser

1. Go to http://localhost:3000
2. Click "Start Discovering" or search for any creator
3. You should see results!

## What You Just Built

✅ **React Frontend** - Modern, responsive UI with:
- Animated hero with WebGL shader effects
- Smart search with multi-platform filtering
- Trending creators discovery
- Detailed creator profiles
- Anime-style animated navbar with mascot

✅ **FastAPI Backend** - Powerful backend with:
- Multi-source creator search
- Real-time analytics
- Advanced filtering
- Creator ranking and scoring

✅ **Full Integration** - Everything works together:
- Live API communication
- Error handling and loading states
- Responsive design (mobile, tablet, desktop)

## File Structure You Need to Know

```
📁 Project Root
├── 📁 src/api/              ← Backend code
│   └── main.py             ← Start backend from here
├── 📁 app/                 ← Frontend pages
│   ├── page.tsx            ← Home page
│   └── search/page.tsx     ← Search page
├── 📁 components/          ← React components
│   ├── creator-card.tsx
│   └── search-bar.tsx
├── 📁 lib/                 ← Utilities
│   ├── api.ts              ← API client (calls backend)
│   └── hooks.ts            ← React hooks
├── package.json            ← Frontend dependencies
├── .env.local              ← Your API keys
└── requirements.txt        ← Backend dependencies
```

## Key Files to Understand

### Frontend Configuration
- **`.env.local`** - Environment variables
  ```
  NEXT_PUBLIC_API_URL=http://localhost:8000
  ```

- **`lib/api.ts`** - How frontend talks to backend
  ```typescript
  export const searchCreators = async (params) => {
    return apiClient.post('/search', params)
  }
  ```

- **`components/creator-card.tsx`** - Displays a creator
- **`app/search/page.tsx`** - Search page

### Backend Endpoints (Used by Frontend)

| Method | Path | Purpose |
|--------|------|---------|
| POST | `/search` | Search for creators |
| GET | `/creators/trending` | Get trending creators |
| GET | `/creators/{id}` | Get creator details |
| GET | `/creators/by-niche` | Get creators by category |

## Testing

### Test Backend
```bash
curl http://localhost:8000/health
```
Should return: `200 OK`

### Test Frontend
Visit: http://localhost:3000

### Test API Integration
1. Go to http://localhost:3000/search
2. Search for "fitness" or any term
3. Should show results from backend

## Common Issues

### Backend won't start
```bash
# Make sure virtual env is activated
source venv/bin/activate
# Make sure dependencies are installed
pip install -r requirements.txt
# Try different port if 8000 is taken
python -m uvicorn src.api.main:app --port 8001
```

### Frontend won't connect to backend
```bash
# Check .env.local
cat .env.local
# Should have: NEXT_PUBLIC_API_URL=http://localhost:8000

# If backend is on different port:
# NEXT_PUBLIC_API_URL=http://localhost:8001

# Restart frontend
npm run dev
```

### "npm: command not found"
You need to install Node.js: https://nodejs.org/

### "python: command not found"
You need to install Python: https://www.python.org/

## What to Try Next

### 1. Search For Creators
- Go to http://localhost:3000
- Click "Start Discovering"
- Try searching: "fitness", "fashion", "tech", etc.
- Use filters to refine results

### 2. View Creator Profiles
- Click on any creator card
- See detailed stats and analytics
- Check top performing content

### 3. Explore Trending
- Click "Trending" in navbar
- See most popular creators right now

### 4. Read Documentation
- **Frontend**: `FRONTEND_README.md`
- **API**: `API_INTEGRATION.md`
- **Setup**: `SETUP.md`

## Production Deployment

### Frontend
```bash
npm run build
npm run start
# or deploy to Vercel with: vercel
```

### Backend
```bash
# Remove --reload flag
python -m uvicorn src.api.main:app --host 0.0.0.0 --port 8000
# Deploy to: Heroku, AWS, DigitalOcean, etc.
```

## Getting Help

1. **Check logs** - Look at terminal output for errors
2. **Browser console** - Press F12, check Console tab
3. **API docs** - Visit http://localhost:8000/docs
4. **Read docs** - Check `SETUP.md` troubleshooting section

## Key Features Built

### Home Page (`/`)
- Animated WebGL hero
- Trust badges
- Feature showcase
- CTA buttons

### Search Page (`/search`)
- Real-time search
- Multi-platform filtering
- Advanced filters (niche, followers, engagement)
- Results pagination
- Creator cards

### Trending Page (`/trending`)
- Real-time trending creators
- Rankings (#1, #2, #3)
- Same creator cards as search

### Creator Detail (`/creators/{id}`)
- Full creator profile
- Analytics dashboard
- Follower counts
- Engagement rates
- Top content breakdown

### Navigation
- Anime-styled navbar
- Animated mascot character
- Responsive mobile menu
- Smooth transitions

## Architecture Overview

```
User Opens http://localhost:3000
    ↓
React Frontend (Next.js)
    ├── Home Page (Hero + Features)
    ├── Search Page (Input → API Call → Results)
    ├── Trending Page (Fetch trending → Display)
    └── Creator Detail (Fetch details → Display)
    ↓
Axios API Client (lib/api.ts)
    ↓
FastAPI Backend (http://localhost:8000)
    ├── /search endpoint
    ├── /creators/trending
    ├── /creators/{id}
    └── /creators/by-niche
    ↓
Returns JSON Data
    ↓
Frontend Displays Results
```

## Next Steps

1. ✅ Get both running (5 min)
2. 📖 Read `FRONTEND_README.md` for component details
3. 📚 Read `API_INTEGRATION.md` for API details
4. 🔧 Customize colors in `app/globals.css`
5. 🎨 Modify components in `components/`
6. 🚀 Deploy to production

## Environment Variables Needed

### For Backend (.env.local)
```
GEMINI_API_KEY=your_key
YOUTUBE_API_KEY=your_key
```

### For Frontend (.env.local)
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Useful Commands

```bash
# Backend
python -m venv venv          # Create virtual env
source venv/bin/activate     # Activate venv
pip install -r requirements.txt  # Install deps
python -m uvicorn src.api.main:app --reload  # Run dev

# Frontend
npm install                  # Install dependencies
npm run dev                 # Run dev server
npm run build               # Build for production
npm run start               # Run production build
npm run lint                # Check code quality
```

## Troubleshooting Checklist

- [ ] Backend running on http://localhost:8000
- [ ] Frontend running on http://localhost:3000
- [ ] `.env.local` has `NEXT_PUBLIC_API_URL=http://localhost:8000`
- [ ] Backend `.env.local` has API keys
- [ ] No port conflicts (8000 or 3000 in use)
- [ ] Python virtual env activated
- [ ] Node modules installed (`npm install`)

## You're All Set! 🚀

Go to http://localhost:3000 and start discovering influencers!

Need help? Check the detailed docs:
- `SETUP.md` - Complete setup guide
- `FRONTEND_README.md` - Frontend details
- `API_INTEGRATION.md` - API documentation
