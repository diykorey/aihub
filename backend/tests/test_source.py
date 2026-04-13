"""Tests for Source model — trust_score field (Ticket 4)."""

from __future__ import annotations

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.db import Base
from app.models import Source

_engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
_TestingSessionLocal = sessionmaker(bind=_engine, autocommit=False, autoflush=False)


def setup_function() -> None:
    Base.metadata.drop_all(bind=_engine)
    Base.metadata.create_all(bind=_engine)


def test_source_trust_score_defaults_to_half() -> None:
    # given
    db = _TestingSessionLocal()
    try:
        source = Source(url="https://example.com", source_type="blog", provider="test")
        db.add(source)
        db.commit()
        db.refresh(source)

        # then
        assert source.trust_score == 0.5
    finally:
        db.close()


def test_source_trust_score_custom_value() -> None:
    # given
    db = _TestingSessionLocal()
    try:
        source = Source(
            url="https://example.com/2",
            source_type="paper",
            provider="arxiv",
            trust_score=0.9,
        )
        db.add(source)
        db.commit()
        db.refresh(source)

        # then
        assert source.trust_score == 0.9
    finally:
        db.close()
