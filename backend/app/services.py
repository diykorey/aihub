"""Service layer — business logic, keeps routes thin.

Stories 4 & 5: list_insights, get_insight.
Story 15 (digest): get_digest.
"""

from __future__ import annotations

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Insight, Tag, WeeklyDigest

_VALID_STATUSES = {"draft", "published", "review_failed"}


def list_insights(db: Session, *, offset: int = 0, limit: int = 20) -> list[Insight]:
    """Return published insights ordered newest first, with pagination."""
    return list(
        db.scalars(
            select(Insight)
            .where(Insight.status == "published")
            .order_by(Insight.year.desc(), Insight.week.desc())
            .offset(offset)
            .limit(limit)
        ).all()
    )


def get_insight(db: Session, insight_id: int) -> Insight:
    """Return a single insight by ID or raise 404."""
    insight = db.get(Insight, insight_id)
    if not insight:
        raise HTTPException(status_code=404, detail=f"Insight {insight_id} not found")
    return insight


def get_digest(db: Session, year: int, week: int) -> WeeklyDigest:
    """Return weekly digest with its insights or raise 404."""
    digest = db.scalars(
        select(WeeklyDigest).where(
            WeeklyDigest.year == year,
            WeeklyDigest.week == week,
        )
    ).first()
    if not digest:
        raise HTTPException(status_code=404, detail=f"Digest for {year}/W{week:02d} not found")
    return digest


def get_or_create_digest(db: Session, year: int, week: int) -> WeeklyDigest:
    """Return existing digest for the given year/week or create one."""
    digest = db.scalars(
        select(WeeklyDigest).where(
            WeeklyDigest.year == year,
            WeeklyDigest.week == week,
        )
    ).first()
    if not digest:
        digest = WeeklyDigest(year=year, week=week)
        db.add(digest)
        db.flush()
    return digest


def update_insight_status(db: Session, insight_id: int, status: str) -> Insight:
    """Transition an insight to a new status (e.g. draft → published)."""
    if status not in _VALID_STATUSES:
        valid = ", ".join(sorted(_VALID_STATUSES))
        raise HTTPException(
            status_code=400,
            detail=f"Invalid status '{status}'. Must be one of: {valid}",
        )
    insight = db.get(Insight, insight_id)
    if not insight:
        raise HTTPException(status_code=404, detail=f"Insight {insight_id} not found")
    insight.status = status
    if status == "published" and not insight.digest_id:
        digest = get_or_create_digest(db, insight.year, insight.week)
        insight.digest_id = digest.id
    db.flush()
    return insight


def list_tags(db: Session) -> list[Tag]:
    """Return all tags ordered alphabetically."""
    return list(db.scalars(select(Tag).order_by(Tag.name)).all())


def run_pipeline(db: Session, source_text: str) -> Insight:
    """Run the full agent pipeline on source_text and return a draft Insight.

    The orchestrator coordinates all agents sequentially (supervisor pattern),
    logs every run to agent_runs, and flushes the Insight — the caller's
    session commit persists everything together.
    """
    from app.agents.orchestrator import InsightOrchestrator

    return InsightOrchestrator(db).run(source_text)
