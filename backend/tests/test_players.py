"""Tests for Player model and GET /players endpoint (Tickets 8 & 14)."""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.db import Base, get_db
from app.main import app
from app.models import Insight, Player

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


def test_player_creation() -> None:
    # given
    db = _TestingSessionLocal()
    try:
        player = Player(name="Anthropic")

        # when
        db.add(player)
        db.commit()
        db.refresh(player)

        # then
        assert player.id is not None
        assert player.name == "Anthropic"
    finally:
        db.close()


def test_player_insight_association() -> None:
    # given
    db = _TestingSessionLocal()
    try:
        player = Player(name="OpenAI")
        insight = Insight(
            title="GPT-5 Launch",
            summary="OpenAI launches GPT-5",
            week=15,
            year=2026,
            status="published",
        )
        # when
        insight.players.append(player)
        db.add(insight)
        db.commit()
        db.refresh(player)
        db.refresh(insight)

        # then
        assert player in insight.players
        assert insight in player.insights
    finally:
        db.close()


def test_player_name_is_unique() -> None:
    # given
    db = _TestingSessionLocal()
    try:
        db.add(Player(name="Anthropic"))
        db.commit()

        # when
        db.add(Player(name="Anthropic"))

        # then
        with pytest.raises(IntegrityError):
            db.commit()

        db.rollback()
    finally:
        db.close()


# ---------------------------------------------------------------------------
# GET /players
# ---------------------------------------------------------------------------


def test_list_players_empty() -> None:
    # when
    response = client.get("/players")

    # then
    assert response.status_code == 200
    assert response.json() == []


def test_list_players_returns_all() -> None:
    # given
    db = _TestingSessionLocal()
    try:
        db.add_all([Player(name="OpenAI"), Player(name="Anthropic"), Player(name="Google")])
        db.commit()
    finally:
        db.close()

    # when
    response = client.get("/players")

    # then
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3
    names = [p["name"] for p in data]
    assert names == ["Anthropic", "Google", "OpenAI"]  # alphabetical order


def test_list_players_shape() -> None:
    # given
    db = _TestingSessionLocal()
    try:
        db.add(Player(name="xAI"))
        db.commit()
    finally:
        db.close()

    # when
    response = client.get("/players")

    # then
    item = response.json()[0]
    assert set(item.keys()) == {"id", "name"}
