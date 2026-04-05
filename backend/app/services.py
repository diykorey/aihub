"""Service layer — business logic, keeps routes thin.

Stories 4 & 5: list_insights, get_insight.
Story 15 (digest): get_digest.
"""

from __future__ import annotations

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Insight, WeeklyDigest


def list_insights(db: Session) -> list[Insight]:
    """Return all published insights ordered newest first."""
    return list(
        db.scalars(
            select(Insight)
            .where(Insight.status == "published")
            .order_by(Insight.year.desc(), Insight.week.desc())
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


def run_pipeline(db: Session, source_text: str) -> Insight:
    """Run the full agent pipeline on source_text and return a draft Insight.

    The orchestrator coordinates all agents sequentially (supervisor pattern),
    logs every run to agent_runs, and flushes the Insight — the caller's
    session commit persists everything together.
    """
    from app.agents.orchestrator import InsightOrchestrator

    return InsightOrchestrator(db).run(source_text)
