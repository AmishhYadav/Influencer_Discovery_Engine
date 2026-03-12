"""FastAPI application — Influencer Discovery Engine API."""

import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.routers import creators, briefings, search

logger = logging.getLogger(__name__)

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


@app.on_event("startup")
def run_db_migrations():
    """Run safe, idempotent schema migrations on startup.

    These fix the briefings table FK to point at creators instead of channels.
    The try/except ensures this is safe to run repeatedly.
    """
    from src.api.deps import engine
    from sqlalchemy import text, inspect

    try:
        inspector = inspect(engine)
        fk_constraints = inspector.get_foreign_keys("briefings")

        # Check if the old constraint still exists
        needs_migration = any(
            fk.get("referred_table") == "channels" for fk in fk_constraints
        )

        if needs_migration:
            with engine.begin() as conn:
                # Drop the old FK pointing to channels
                conn.execute(text(
                    "ALTER TABLE briefings DROP CONSTRAINT IF EXISTS briefings_channel_id_fkey;"
                ))
                # Add the correct FK pointing to creators
                conn.execute(text("""
                    ALTER TABLE briefings
                    ADD CONSTRAINT briefings_creator_id_fkey
                    FOREIGN KEY (creator_id) REFERENCES creators (id) ON DELETE CASCADE;
                """))
            logger.info("Migrated briefings FK: channels -> creators")
            print("✅ Migrated briefings FK: channels -> creators")
        else:
            logger.info("Briefings FK migration already applied.")
    except Exception as e:
        # Safe to fail — might be SQLite or constraint already correct
        logger.warning("FK migration skipped: %s", e)
        print(f"FK migration skipped (safe): {e}")


@app.get("/health", tags=["system"])
def health_check():
    """Simple health check endpoint."""
    return {"status": "ok"}
