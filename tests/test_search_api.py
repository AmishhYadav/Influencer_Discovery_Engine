"""Tests for the search API router and multi-source endpoints."""

import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

import os
os.environ["DATABASE_URL"] = "sqlite:///:memory:"

from src.db.models import Base, create_tables
from src.db.dao import upsert_creator, upsert_content_item, update_creator_scores
from src.api.main import app
from src.api.deps import get_db


# ── Test Database Fixture ────────────────────────────────────────────────

@pytest.fixture
def test_db(tmp_path):
    """Create a temporary SQLite database with multi-source test data."""
    db_url = f"sqlite:///{tmp_path}/search_test.db"
    engine = create_engine(db_url, echo=False)
    create_tables(engine)
    TestSession = sessionmaker(bind=engine)

    with TestSession() as session:
        # Seed creators from different platforms
        creator1 = upsert_creator(session, {
            "name": "Dr. Plant-Based",
            "platform": "blog",
            "platform_id": "https://plantbased.blog",
            "profile_url": "https://plantbased.blog",
            "bio": "Nutrition researcher",
            "follower_count": 10000,
        })
        update_creator_scores(
            session, creator1.id,
            credibility_score=80.0,
            engagement_score=60.0,
            reach_score=40.0,
            alignment_score=85.0,
            composite_score=72.0,
        )
        upsert_content_item(session, {
            "creator_id": creator1.id,
            "source_type": "blog_post",
            "title": "Health Benefits of Plant-Based Diets",
            "text_content": "A deep dive into nutrition science...",
            "url": "https://plantbased.blog/health-benefits",
            "published_at": "2024-01-15",
        })

        creator2 = upsert_creator(session, {
            "name": "Prof. Environmental",
            "platform": "academic",
            "platform_id": "s2-99999",
            "bio": "Environmental science professor",
            "follower_count": 0,
        })
        update_creator_scores(
            session, creator2.id,
            credibility_score=90.0,
            engagement_score=70.0,
            reach_score=10.0,
            alignment_score=75.0,
            composite_score=68.0,
        )

        creator3 = upsert_creator(session, {
            "name": "Chef Green",
            "platform": "twitter",
            "platform_id": "chefgreen",
            "profile_url": "https://twitter.com/chefgreen",
            "bio": "Plant-based chef and food TV host",
            "follower_count": 50000,
        })
        update_creator_scores(
            session, creator3.id,
            credibility_score=50.0,
            engagement_score=80.0,
            reach_score=60.0,
            alignment_score=65.0,
            composite_score=63.0,
        )

        session.commit()

    def override_get_db():
        s = TestSession()
        try:
            yield s
        finally:
            s.close()

    app.dependency_overrides[get_db] = override_get_db
    yield {"db_url": db_url}
    app.dependency_overrides.clear()


@pytest.fixture
def client(test_db):
    return TestClient(app)


# ── Creator List Endpoint Tests ──────────────────────────────────────────

class TestMultiCreatorList:
    def test_list_all_creators(self, client):
        resp = client.get("/api/search/creators")
        assert resp.status_code == 200
        data = resp.json()
        assert data["total"] == 3
        # Should be sorted by composite_score desc
        scores = [c["composite_score"] for c in data["creators"]]
        assert scores == sorted(scores, reverse=True)

    def test_filter_by_platform(self, client):
        resp = client.get("/api/search/creators?platform=blog")
        data = resp.json()
        assert data["total"] == 1
        assert data["creators"][0]["platform"] == "blog"

    def test_filter_by_min_score(self, client):
        resp = client.get("/api/search/creators?min_score=70")
        data = resp.json()
        assert data["total"] == 1
        assert data["creators"][0]["composite_score"] >= 70

    def test_pagination(self, client):
        resp = client.get("/api/search/creators?limit=1&offset=0")
        data = resp.json()
        assert len(data["creators"]) == 1
        assert data["total"] == 3


class TestMultiCreatorDetail:
    def test_get_creator_detail(self, client, test_db):
        # First get the list to find an ID
        resp = client.get("/api/search/creators")
        creator_id = resp.json()["creators"][0]["id"]

        resp = client.get(f"/api/search/creators/{creator_id}")
        assert resp.status_code == 200
        data = resp.json()
        assert "scores" in data
        assert "content_items" in data
        assert data["scores"]["credibility_score"] > 0

    def test_creator_not_found(self, client):
        resp = client.get("/api/search/creators/nonexistent")
        assert resp.status_code == 404


# ── Search Endpoint Tests ────────────────────────────────────────────────

class TestSearchEndpoint:
    @patch("src.api.routers.search._ingest_academic_results")
    def test_search_academic(self, mock_ingest, client, test_db):
        # Mock returns empty (no actual API calls in tests)
        mock_ingest.return_value = []

        resp = client.post(
            "/api/search",
            json={
                "query": "plant-based nutrition",
                "sources": ["academic"],
                "max_results": 5,
            },
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["query"] == "plant-based nutrition"
        assert "academic" in data["sources"]

    def test_search_with_invalid_request(self, client, test_db):
        resp = client.post("/api/search", json={})
        assert resp.status_code == 422  # Validation error for missing query
