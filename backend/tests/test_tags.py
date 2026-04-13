"""Tests for Tag model and GET /tags endpoint (Tickets 7 & 13)."""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.db import Base, get_db
from app.main import app
from app.models import Insight, Tag

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


client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_db():
    app.dependency_overrides[get_db] = override_get_db
    Base.metadata.drop_all(bind=_engine)
    Base.metadata.create_all(bind=_engine)
    yield
    app.dependency_overrides.pop(get_db, None)


def test_tag_creation() -> None:
    # given
    db = _TestingSessionLocal()
    try:
        tag = Tag(name="LLM")

        # when
        db.add(tag)
        db.commit()
        db.refresh(tag)

        # then
        assert tag.id is not None
        assert tag.name == "LLM"
    finally:
        db.close()


def test_tag_insight_association() -> None:
    # given
    db = _TestingSessionLocal()
    try:
        tag = Tag(name="Robotics")
        insight = Insight(
            title="Robot Arms",
            summary="New robot arms",
            week=15,
            year=2026,
            status="published",
        )
        insight.tags.append(tag)
        db.add(insight)
        db.commit()
        db.refresh(tag)
        db.refresh(insight)

        # then
        assert tag in insight.tags
        assert insight in tag.insights
    finally:
        db.close()


def test_tag_name_is_unique() -> None:
    # given
    db = _TestingSessionLocal()
    try:
        db.add(Tag(name="LLM"))
        db.commit()

        # when
        db.add(Tag(name="LLM"))

        # then
        with pytest.raises(IntegrityError):
            db.commit()

        db.rollback()
    finally:
        db.close()


# ---------------------------------------------------------------------------
# GET /tags
# ---------------------------------------------------------------------------


def test_list_tags_empty() -> None:
    # when
    response = client.get("/tags")

    # then
    assert response.status_code == 200
    assert response.json() == []


def test_list_tags_returns_all() -> None:
    # given
    db = _TestingSessionLocal()
    try:
        db.add_all([Tag(name="LLM"), Tag(name="Robotics"), Tag(name="Ethics")])
        db.commit()
    finally:
        db.close()

    # when
    response = client.get("/tags")

    # then
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3
    names = [t["name"] for t in data]
    assert names == ["Ethics", "LLM", "Robotics"]  # alphabetical order


def test_list_tags_shape() -> None:
    # given
    db = _TestingSessionLocal()
    try:
        db.add(Tag(name="Vision"))
        db.commit()
    finally:
        db.close()

    # when
    response = client.get("/tags")

    # then
    item = response.json()[0]
    assert set(item.keys()) == {"id", "name"}
