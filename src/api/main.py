"""FastAPI application — Influencer Discovery Engine API."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.routers import creators, briefings, search

app = FastAPI(
    title="Influencer Discovery Engine",
    description="API for discovering and analyzing influencers aligned with advocacy topics.",
    version="0.3.0",
)

# CORS — open for MVP
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Wire routers
app.include_router(creators.router)
app.include_router(briefings.router)
app.include_router(search.router)


@app.get("/health", tags=["system"])
def health_check():
    """Simple health check endpoint."""
    return {"status": "ok"}
