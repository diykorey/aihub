"""SQLAlchemy ORM models — Story 3 + agent logging.

Tables: sources, insights, weekly_digests, agent_runs.
"""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base


class Source(Base):
    __tablename__ = "sources"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    url: Mapped[str] = mapped_column(String(500), unique=True, index=True)
    source_type: Mapped[str] = mapped_column(String(50))  # e.g. "github", "blog", "paper"
    provider: Mapped[str] = mapped_column(String(100))
    published_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)


class Insight(Base):
    __tablename__ = "insights"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(500))
    summary: Mapped[str] = mapped_column(Text)
    reasoning: Mapped[str | None] = mapped_column(Text, nullable=True)
    # JSON-encoded list[str] — populated by ExampleGeneratorAgent
    examples: Mapped[str | None] = mapped_column(Text, nullable=True)
    # JSON-encoded dict[str, str] — populated by DebateGeneratorAgent
    perspectives: Mapped[str | None] = mapped_column(Text, nullable=True)
    week: Mapped[int] = mapped_column(Integer, index=True)
    year: Mapped[int] = mapped_column(Integer, index=True)
    status: Mapped[str] = mapped_column(String(50), default="published")

    digest_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("weekly_digests.id"), nullable=True
    )
    digest: Mapped[WeeklyDigest | None] = relationship("WeeklyDigest", back_populates="insights")
    agent_runs: Mapped[list[AgentRun]] = relationship("AgentRun", back_populates="insight")


class WeeklyDigest(Base):
    __tablename__ = "weekly_digests"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    year: Mapped[int] = mapped_column(Integer, index=True)
    week: Mapped[int] = mapped_column(Integer, index=True)

    insights: Mapped[list[Insight]] = relationship(
        "Insight", back_populates="digest", lazy="select"
    )


class AgentRun(Base):
    """Records every agent execution for debugging and auditing — Story 23."""

    __tablename__ = "agent_runs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    agent_name: Mapped[str] = mapped_column(String(100), index=True)
    model: Mapped[str | None] = mapped_column(String(100), nullable=True)
    output: Mapped[str | None] = mapped_column(Text, nullable=True)  # JSON string
    success: Mapped[bool] = mapped_column(Boolean, default=True)
    error: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.utcnow())

    insight_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("insights.id"), nullable=True, index=True
    )
    insight: Mapped[Insight | None] = relationship("Insight", back_populates="agent_runs")
