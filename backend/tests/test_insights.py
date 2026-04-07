"""Integration tests for insights and digest endpoints — Stories 4 & 5."""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.db import Base, get_db
from app.main import app
from app.models import Insight, WeeklyDigest

# ---------------------------------------------------------------------------
# In-memory SQLite test DB — StaticPool keeps one connection so tables
# created in fixtures are visible to every session in the same test.
# ---------------------------------------------------------------------------

_engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
_TestingSessionLocal = sessionmaker(bind=_engine, autocommit=False, autoflush=False)


def override_get_db():
    db = _TestingSessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture(autouse=True)
def reset_db():
    """Recreate schema and seed minimal data before each test."""
    Base.metadata.drop_all(bind=_engine)
    Base.metadata.create_all(bind=_engine)

    db = _TestingSessionLocal()
    digest = WeeklyDigest(year=2026, week=11)
    db.add(digest)
    db.flush()

    db.add_all(
        [
            Insight(
                id=1,
                title="Test Insight One",
                summary="Summary one",
                reasoning="Reasoning one",
                week=11,
                year=2026,
                status="published",
                digest_id=digest.id,
            ),
            Insight(
                id=2,
                title="Test Insight Two",
                summary="Summary two",
                week=11,
                year=2026,
                status="published",
                digest_id=digest.id,
            ),
            Insight(
                id=3,
                title="Draft Insight",
                summary="Should not appear in list",
                week=11,
                year=2026,
                status="draft",
            ),
        ]
    )
    db.commit()
    db.close()
    yield


# ---------------------------------------------------------------------------
# GET /insights
# ---------------------------------------------------------------------------


def test_list_insights_returns_published_only() -> None:
    response = client.get("/insights")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    titles = {item["title"] for item in data}
    assert "Draft Insight" not in titles


def test_list_insights_shape() -> None:
    response = client.get("/insights")
    item = response.json()[0]
    assert {"id", "title", "summary", "week", "year", "status"}.issubset(item.keys())


# ---------------------------------------------------------------------------
# GET /insights/{id}
# ---------------------------------------------------------------------------


def test_get_insight_by_id() -> None:
    response = client.get("/insights/1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["title"] == "Test Insight One"
    assert data["reasoning"] == "Reasoning one"


def test_get_insight_not_found() -> None:
    response = client.get("/insights/999")
    assert response.status_code == 404


def test_get_draft_insight_still_accessible_by_id() -> None:
    """Direct ID lookup returns any status; list filters to published only."""
    response = client.get("/insights/3")
    assert response.status_code == 200
    assert response.json()["status"] == "draft"


# ---------------------------------------------------------------------------
# GET /digest/{year}/{week}
# ---------------------------------------------------------------------------


def test_get_digest() -> None:
    response = client.get("/digest/2026/11")
    assert response.status_code == 200
    data = response.json()
    assert data["year"] == 2026
    assert data["week"] == 11
    assert len(data["insights"]) == 2


def test_get_digest_not_found() -> None:
    response = client.get("/digest/2026/99")
    assert response.status_code == 404


# ---------------------------------------------------------------------------
# GET /insights — pagination
# ---------------------------------------------------------------------------


def test_list_insights_with_limit() -> None:
    response = client.get("/insights?limit=1")
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_list_insights_with_offset() -> None:
    response = client.get("/insights?offset=1&limit=10")
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_list_insights_offset_beyond_results() -> None:
    response = client.get("/insights?offset=100")
    assert response.status_code == 200
    assert len(response.json()) == 0


# ---------------------------------------------------------------------------
# PATCH /insights/{id}/status
# ---------------------------------------------------------------------------


def test_publish_draft_insight() -> None:
    # given
    response = client.get("/insights/3")
    assert response.json()["status"] == "draft"

    # when
    response = client.patch("/insights/3/status", json={"status": "published"})

    # then
    assert response.status_code == 200
    assert response.json()["status"] == "published"


def test_publish_auto_assigns_digest() -> None:
    # when
    response = client.patch("/insights/3/status", json={"status": "published"})

    # then
    data = response.json()
    assert data["status"] == "published"
    digest_resp = client.get(f"/digest/{data['year']}/{data['week']}")
    assert digest_resp.status_code == 200


def test_update_status_invalid() -> None:
    response = client.patch("/insights/1/status", json={"status": "bogus"})
    assert response.status_code == 400


def test_update_status_not_found() -> None:
    response = client.patch("/insights/999/status", json={"status": "published"})
    assert response.status_code == 404
