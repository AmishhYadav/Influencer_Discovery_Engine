# Setup Guide - Influencer Discovery Engine

Complete setup instructions for both the FastAPI backend and React frontend.

## Prerequisites

- **Node.js**: 18.17 or higher
- **Python**: 3.9 or higher
- **Package Manager**: npm, yarn, pnpm, or bun
- **Git**: For version control

## Quick Start (5 minutes)

### 1. Backend Setup

```bash
# Navigate to project root
cd /path/to/influencer_discovery_engine

# Create Python virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env.local
# Edit .env.local with your API keys (GEMINI_API_KEY, YOUTUBE_API_KEY)

# Start FastAPI server
python -m uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000
```

Backend will be available at: `http://localhost:8000`

API Documentation: `http://localhost:8000/docs` (Swagger UI)

### 2. Frontend Setup

```bash
# In a new terminal, navigate to project root
cd /path/to/influencer_discovery_engine

# Install Node dependencies
npm install
# or: yarn install, pnpm install, bun install

# Set up environment variables
cp .env.example .env.local
# Ensure NEXT_PUBLIC_API_URL=http://localhost:8000

# Start development server
npm run dev
# or: yarn dev, pnpm dev, bun dev
```

Frontend will be available at: `http://localhost:3000`

## Detailed Setup Instructions

### Backend Setup

#### Step 1: Create Virtual Environment

```bash
python -m venv venv
```

#### Step 2: Activate Virtual Environment

**Windows**:
```bash
venv\Scripts\activate
```

**macOS/Linux**:
```bash
source venv/bin/activate
```

#### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

#### Step 4: Configure Environment Variables

Create a `.env.local` file in the project root:

```bash
cp .env.example .env.local
```

Edit `.env.local` and add your API keys:

```
GEMINI_API_KEY=your_gemini_api_key_here
YOUTUBE_API_KEY=your_youtube_api_key_here
DATABASE_URL=postgresql+asyncpg://user:pass@localhost:5432/influencer_discovery
```

#### Step 5: Run Database Migrations (if applicable)

```bash
# If using Alembic for migrations
alembic upgrade head
```

#### Step 6: Start the FastAPI Server

```bash
python -m uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000
```

**Verify backend is running**:
- Open browser: http://localhost:8000/docs
- You should see Swagger UI with API documentation

### Frontend Setup

#### Step 1: Install Node Dependencies

```bash
npm install
```

If you prefer other package managers:
- Yarn: `yarn install`
- pnpm: `pnpm install`
- Bun: `bun install`

#### Step 2: Configure Environment Variables

Create `.env.local`:

```bash
# This file may already exist, but check/update it
NEXT_PUBLIC_API_URL=http://localhost:8000
```

**Important**: The `NEXT_PUBLIC_` prefix makes this variable accessible in the browser.

#### Step 3: Start Development Server

```bash
npm run dev
```

**Verify frontend is running**:
- Open browser: http://localhost:3000
- You should see the home page with the animated hero

#### Step 4: Test API Integration

1. Go to http://localhost:3000
2. Click "Start Discovering" or navigate to /search
3. Enter a search query (e.g., "fitness")
4. You should see results from the backend

## Project Structure

```
influencer_discovery_engine/
├── src/
│   └── api/
│       ├── main.py              # FastAPI app entry point
│       ├── schemas.py           # Pydantic models
│       ├── routers/
│       │   └── search.py        # Search endpoints
│       └── services/            # Business logic
│
├── app/                         # Next.js app directory
│   ├── layout.tsx
│   ├── page.tsx                 # Home page
│   ├── globals.css
│   ├── search/
│   ├── trending/
│   ├── about/
│   └── creators/
│
├── components/                  # React components
│   ├── ui/                      # Custom UI components
│   ├── creator-card.tsx
│   └── search-bar.tsx
│
├── lib/                         # Utilities and hooks
│   ├── api.ts                   # API client
│   ├── hooks.ts                 # Custom hooks
│   └── utils.ts
│
├── package.json
├── tsconfig.json
├── tailwind.config.ts
├── next.config.js
└── .env.example
```

## Port Configuration

Default ports:
- **Backend**: `8000` (http://localhost:8000)
- **Frontend**: `3000` (http://localhost:3000)

To change ports:

**Backend**:
```bash
python -m uvicorn src.api.main:app --port 8001
```

**Frontend**:
```bash
npm run dev -- -p 3001
```

## Troubleshooting

### Backend Issues

#### "Module not found" error
```bash
# Ensure you're in the virtual environment
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate     # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

#### Port 8000 already in use
```bash
# Find and kill process using port 8000
# Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# macOS/Linux:
lsof -i :8000
kill -9 <PID>

# Or use a different port:
python -m uvicorn src.api.main:app --port 8001
```

#### CORS errors
Ensure the frontend URL is added to CORS allowed origins in backend settings.

### Frontend Issues

#### "API connection refused"
1. Verify backend is running: `http://localhost:8000/docs`
2. Check `.env.local` has correct `NEXT_PUBLIC_API_URL`
3. Try restarting frontend: `npm run dev`

#### "Cannot find module" error
```bash
# Clear node_modules and reinstall
rm -rf node_modules
npm install
npm run dev
```

#### Port 3000 already in use
```bash
# Use different port
npm run dev -- -p 3001
```

## Development Workflow

### Making Changes

**Backend**:
1. Edit files in `src/`
2. Server will auto-reload (with `--reload` flag)
3. Test using Swagger UI: http://localhost:8000/docs

**Frontend**:
1. Edit files in `app/` or `components/`
2. Hot Module Replacement (HMR) will auto-update browser
3. Check browser console for errors

### Running Tests

**Backend**:
```bash
pytest
```

**Frontend**:
```bash
npm run test
```

### Building for Production

**Backend**:
```bash
# Remove --reload flag for production
python -m uvicorn src.api.main:app --host 0.0.0.0 --port 8000
```

**Frontend**:
```bash
npm run build
npm run start
```

## Environment Variables Reference

### Backend (.env or .env.local)

| Variable | Required | Description | Example |
|----------|----------|-------------|---------|
| `GEMINI_API_KEY` | Yes | Google Gemini API key | `AIza...` |
| `YOUTUBE_API_KEY` | Yes | YouTube Data API key | `AIza...` |
| `DATABASE_URL` | No | PostgreSQL connection string | `postgresql+asyncpg://...` |

### Frontend (.env.local)

| Variable | Required | Description | Example |
|----------|----------|-------------|---------|
| `NEXT_PUBLIC_API_URL` | Yes | FastAPI backend URL | `http://localhost:8000` |

## Health Check

### Backend Health Check
```bash
curl http://localhost:8000/health
```

Should return `200 OK`

### Frontend Health Check
```bash
curl http://localhost:3000
```

Should return HTML content

## Getting API Keys

### Gemini API Key
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Click "Create API Key"
3. Copy the key to `.env.local`

### YouTube API Key
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create new project
3. Enable YouTube Data API v3
4. Create API key
5. Copy to `.env.local`

## Next Steps

1. **Explore API Documentation**: Visit http://localhost:8000/docs
2. **Try the UI**: Visit http://localhost:3000
3. **Read Documentation**: Check `FRONTEND_README.md` and `API_INTEGRATION.md`
4. **Configure Database**: Set up PostgreSQL if needed
5. **Deploy**: Follow deployment guides for your hosting platform

## Support

For issues:
1. Check error messages in terminal
2. Review logs in browser DevTools (F12)
3. Refer to troubleshooting sections in README files
4. Check API documentation at `/docs`

## Performance Tips

### Backend
- Use connection pooling for database
- Implement caching for frequently accessed data
- Monitor API response times

### Frontend
- Enable production builds: `npm run build`
- Use image optimization
- Monitor bundle size: `npm run build -- --analyze`

## Security Checklist

- [ ] Never commit `.env.local` files
- [ ] Use environment variables for sensitive data
- [ ] Enable HTTPS in production
- [ ] Configure CORS properly
- [ ] Validate all user inputs
- [ ] Use secure session management
- [ ] Keep dependencies updated

## Deployment

### Backend Deployment
See backend documentation for deploying to production platforms (Heroku, AWS, etc.)

### Frontend Deployment
```bash
# Build optimized bundle
npm run build

# Deploy to Vercel (recommended for Next.js)
vercel
```

## Additional Resources

- [Next.js Documentation](https://nextjs.org/docs)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
- [TypeScript Documentation](https://www.typescriptlang.org/docs/)
