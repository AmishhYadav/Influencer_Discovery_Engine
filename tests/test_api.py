"""Tests for the FastAPI app — health check, creators, and briefings endpoints."""

import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from src.db.models import Base, create_tables
from src.db.dao import upsert_channel, create_briefing, update_briefing
from src.api.main import app
from src.api.deps import get_db


# ── Test Database Fixture ────────────────────────────────────────────────

@pytest.fixture
def test_db(tmp_path):
    """Create a temporary SQLite database with test data."""
    db_url = f"sqlite:///{tmp_path}/api_test.db"
    engine = create_engine(db_url, echo=False)
    create_tables(engine)
    TestSession = sessionmaker(bind=engine)

    with TestSession() as session:
        # Seed channels
        upsert_channel(session, {
            "channel_id": "UC_high",
            "title": "High Alignment Channel",
            "description": "Very aligned",
            "subscriber_count": 100000,
            "video_count": 200,
        })
        upsert_channel(session, {
            "channel_id": "UC_low",
            "title": "Low Alignment Channel",
            "description": "Not aligned",
            "subscriber_count": 5000,
            "video_count": 20,
        })
        session.commit()

        # Set alignment scores directly
        ch_high = session.get(
            __import__("src.db.models", fromlist=["Channel"]).Channel, "UC_high"
        )
        ch_high.alignment_score = 85
        ch_high.alignment_quotes = [{"text": "Great quote", "timestamp": "1:23"}]

        ch_low = session.get(
            __import__("src.db.models", fromlist=["Channel"]).Channel, "UC_low"
        )
        ch_low.alignment_score = 25

        # Create a completed briefing
        briefing = create_briefing(session, "UC_high")
        update_briefing(session, briefing.id, "# Briefing\nContent", "completed")
        session.commit()

        briefing_id = briefing.id

    # Override get_db dependency
    def override_get_db():
        s = TestSession()
        try:
            yield s
        finally:
            s.close()

    app.dependency_overrides[get_db] = override_get_db
    yield {"db_url": db_url, "briefing_id": briefing_id}
    app.dependency_overrides.clear()


@pytest.fixture
def client(test_db):
    return TestClient(app)


# ── Health Check ─────────────────────────────────────────────────────────

class TestHealthCheck:
    def test_health_returns_ok(self, client):
        resp = client.get("/health")
        assert resp.status_code == 200
        assert resp.json() == {"status": "ok"}


# ── Creators Endpoints ───────────────────────────────────────────────────

class TestCreatorsEndpoints:
    def test_list_creators_returns_all(self, client):
        resp = client.get("/api/creators")
        assert resp.status_code == 200
        data = resp.json()
        assert data["total"] == 2
        assert len(data["creators"]) == 2
        # Should be sorted by score desc
        assert data["creators"][0]["alignment_score"] == 85
        assert data["creators"][1]["alignment_score"] == 25

    def test_list_creators_with_min_score(self, client):
        resp = client.get("/api/creators?min_score=50")
        assert resp.status_code == 200
        data = resp.json()
        assert data["total"] == 1
        assert data["creators"][0]["id"] == "UC_high"

    def test_list_creators_pagination(self, client):
        resp = client.get("/api/creators?limit=1&offset=0")
        data = resp.json()
        assert len(data["creators"]) == 1
        assert data["total"] == 2
        assert data["limit"] == 1
        assert data["offset"] == 0

    def test_get_creator_detail(self, client):
        resp = client.get("/api/creators/UC_high")
        assert resp.status_code == 200
        data = resp.json()
        assert data["id"] == "UC_high"
        assert data["alignment_score"] == 85
        assert len(data["alignment_quotes"]) == 1

    def test_get_creator_not_found(self, client):
        resp = client.get("/api/creators/UC_nonexistent")
        assert resp.status_code == 404


# ── Briefings Endpoints ──────────────────────────────────────────────────

class TestBriefingsEndpoints:
    def test_get_briefing(self, client, test_db):
        briefing_id = test_db["briefing_id"]
        resp = client.get(f"/api/briefings/{briefing_id}")
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "completed"
        assert "Briefing" in data["content"]

    def test_get_briefing_not_found(self, client):
        resp = client.get("/api/briefings/nonexistent")
        assert resp.status_code == 404

    @patch("src.api.routers.briefings.generate_briefing_task")
    def test_trigger_briefing_accepted(self, mock_task, client):
        resp = client.post(
            "/api/briefings/generate",
            json={"channel_id": "UC_high"},
        )
        assert resp.status_code == 202
        data = resp.json()
        assert data["status"] == "accepted"
        assert "briefing_id" in data

    def test_trigger_briefing_channel_not_found(self, client):
        resp = client.post(
            "/api/briefings/generate",
            json={"channel_id": "UC_nonexistent"},
        )
        assert resp.status_code == 404
