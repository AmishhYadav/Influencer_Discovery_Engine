"""Database session dependency for FastAPI."""

import os
from typing import Generator

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from src.db.models import create_tables

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///influencer_discovery.db")

engine = create_engine(DATABASE_URL, echo=False)
create_tables(engine)

SessionLocal = sessionmaker(bind=engine)


def get_db() -> Generator[Session, None, None]:
    """Yield a database session, auto-closing on exit."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
