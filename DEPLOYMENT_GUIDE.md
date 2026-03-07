# Deployment Guide - Influencer Discovery Engine

## Overview

This project is a full-stack application with:
- **Backend**: Python FastAPI REST API (`src/api/main.py`)
- **Frontend**: Next.js 15 React application (`frontend/`)

## Deployment Options

### Option 1: Vercel (Recommended for Frontend)

The current setup is optimized for deploying the **Next.js frontend** on Vercel.

#### Steps:

1. **Connect GitHub Repository**
   - Go to [vercel.com](https://vercel.com)
   - Import your GitHub repository
   - Select `react-frontend-setup` branch

2. **Configure Environment Variables**
   - In Vercel Settings → Environment Variables
   - Add: `NEXT_PUBLIC_API_URL` → Your backend API URL (e.g., `https://api.example.com` or `http://localhost:8000` for local dev)

3. **Deploy**
   - Vercel will automatically build and deploy the frontend
   - The `vercel.json` file handles the Next.js configuration

#### Important Notes:

- The frontend will be deployed at your Vercel domain
- The backend needs to be deployed separately (see Option 2)
- CORS is already configured in the backend for any origin (`allow_origins=["*"]`)

### Option 2: Backend Deployment (FastAPI)

The backend can be deployed to various platforms:

#### **A. Heroku**

```bash
# Create Procfile
echo "web: uvicorn app:app --host 0.0.0.0 --port \$PORT" > Procfile

# Create runtime.txt
echo "python-3.11.0" > runtime.txt

# Deploy
heroku create your-app-name
git push heroku main
```

#### **B. Railway**

1. Connect GitHub repo to Railway
2. Select the root directory
3. Set `PYTHON_VERSION=3.11`
4. Railway auto-detects `pyproject.toml`
5. Set PORT environment variable to `8000`

#### **C. PythonAnywhere**

1. Upload code to PythonAnywhere
2. Configure WSGI: `app:app` from `app.py`
3. Set Python version to 3.11

#### **D. AWS/DigitalOcean/Render**

- Use the `app.py` entry point
- Ensure `PYTHONUNBUFFERED=1` is set
- Start command: `uvicorn app:app --host 0.0.0.0 --port 8000`

### Option 3: Full Stack on Single Platform

#### **Option 3a: Vercel with Serverless Backend**

Create `api/app.py`:
```python
from src.api.main import app
```

Then update `vercel.json` to include Python functions.

#### **Option 3b: Railway (Recommended)**

Railway handles both Node.js and Python in a single project:

1. Connect GitHub to Railway
2. Add build command: `npm install && cd frontend && npm install`
3. Start command: `npm run dev` (uses concurrently)
4. Railway detects both frontend and backend

## Local Development

### Prerequisites

```bash
- Node.js 18+ and npm
- Python 3.11+
- pip or uv package manager
```

### Setup

#### Backend

```bash
# Install dependencies
pip install -r requirements.txt
# or using uv:
uv venv
uv pip install -r requirements.txt

# Run backend
python -m uvicorn app:app --reload --port 8000
# Backend will be available at http://localhost:8000
```

#### Frontend

```bash
cd frontend

# Install dependencies
npm install

# Run frontend
npm run dev
# Frontend will be available at http://localhost:3000
```

#### Both Together

```bash
# From root directory
npm run dev
# This runs both backend and frontend concurrently
```

## Environment Variables

### Frontend (`frontend/.env.local`)

```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

For production on Vercel:
- Set `NEXT_PUBLIC_API_URL` to your deployed backend URL
- Example: `https://api.example.com`

### Backend (`src/` or root)

- No additional env vars needed for MVP
- CORS is open for all origins
- Database and API keys can be added as needed

## API Base URLs

### Development
- Frontend: `http://localhost:3000`
- Backend: `http://localhost:8000`
- API Docs: `http://localhost:8000/docs`

### Production (Vercel + Backend Service)

If backend is deployed at `https://api.example.com`:
- Frontend: `https://your-vercel-domain.com`
- Backend: `https://api.example.com`
- API Docs: `https://api.example.com/docs`

Set `NEXT_PUBLIC_API_URL=https://api.example.com` in Vercel environment variables.

## Troubleshooting

### Frontend deployment fails
- Check `vercel.json` is present
- Ensure `buildCommand` points to `cd frontend && npm run build`
- Check all dependencies are installed (no missing packages)

### API calls fail on production
- Verify `NEXT_PUBLIC_API_URL` is set correctly
- Check backend CORS configuration
- Verify backend URL is accessible from frontend domain

### Build errors
- Clear `.next` folder: `rm -rf frontend/.next`
- Reinstall dependencies: `rm -rf node_modules && npm install`
- Check Node/Python versions match requirements

## File Structure Summary

```
/
├── app.py                    # FastAPI entry point for Vercel
├── pyproject.toml           # Python dependencies & config
├── package.json             # Root package.json for monorepo
├── vercel.json              # Vercel configuration
├── src/                     # Backend code
│   ├── api/
│   │   ├── main.py          # FastAPI app definition
│   │   ├── routers/         # API endpoints
│   │   └── schemas.py       # Pydantic models
│   └── ...
├── frontend/                # Next.js application
│   ├── app/                 # Next.js App Router pages
│   ├── components/          # React components
│   ├── hooks/               # Custom React hooks (useApi)
│   ├── lib/                 # Utilities & types
│   └── package.json         # Frontend dependencies
└── ...
```

## Next Steps

1. **Local Testing**: Follow "Local Development" section
2. **Backend Deployment**: Choose deployment platform from Option 2
3. **Frontend Deployment**: Deploy to Vercel using the frontend branch
4. **Update Frontend Config**: Set `NEXT_PUBLIC_API_URL` to backend URL
5. **Test**: Verify API calls work from production frontend

## Support

For deployment-specific issues:
- **Vercel**: https://vercel.com/help
- **FastAPI**: https://fastapi.tiangolo.com/
- **Next.js**: https://nextjs.org/docs
