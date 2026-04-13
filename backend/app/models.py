"""SQLAlchemy ORM models — Story 3 + agent logging.

Tables: sources, insights, weekly_digests, agent_runs.
"""

from __future__ import annotations

from datetime import UTC, datetime

from sqlalchemy import (
    JSON,
    Boolean,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Table,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base


class Source(Base):
    __tablename__ = "sources"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    url: Mapped[str] = mapped_column(String(500), unique=True, index=True)
    source_type: Mapped[str] = mapped_column(String(50))  # e.g. "github", "blog", "paper"
    provider: Mapped[str] = mapped_column(String(100))
    published_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    trust_score: Mapped[float] = mapped_column(Float, default=0.5)


insight_tags = Table(
    "insight_tags",
    Base.metadata,
    Column("insight_id", Integer, ForeignKey("insights.id"), primary_key=True),
    Column("tag_id", Integer, ForeignKey("tags.id"), primary_key=True),
)


class Tag(Base):
    __tablename__ = "tags"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, index=True)

    insights: Mapped[list[Insight]] = relationship(
        "Insight", secondary=insight_tags, back_populates="tags"
    )


insight_players = Table(
    "insight_players",
    Base.metadata,
    Column("insight_id", Integer, ForeignKey("insights.id"), primary_key=True),
    Column("player_id", Integer, ForeignKey("players.id"), primary_key=True),
)


class Player(Base):
    __tablename__ = "players"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(200), unique=True, index=True)

    insights: Mapped[list[Insight]] = relationship(
        "Insight", secondary=insight_players, back_populates="players"
    )


class Insight(Base):
    __tablename__ = "insights"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(500))
    summary: Mapped[str] = mapped_column(Text)
    reasoning: Mapped[str | None] = mapped_column(Text, nullable=True)
    examples: Mapped[list | None] = mapped_column(JSON, nullable=True)
    perspectives: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    week: Mapped[int] = mapped_column(Integer, index=True)
    year: Mapped[int] = mapped_column(Integer, index=True)
    status: Mapped[str] = mapped_column(String(50), default="published")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(tz=UTC))
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(tz=UTC), onupdate=lambda: datetime.now(tz=UTC)
    )

    digest_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("weekly_digests.id"), nullable=True
    )
    digest: Mapped[WeeklyDigest | None] = relationship("WeeklyDigest", back_populates="insights")
    agent_runs: Mapped[list[AgentRun]] = relationship("AgentRun", back_populates="insight")
    tags: Mapped[list[Tag]] = relationship("Tag", secondary=insight_tags, back_populates="insights")
    players: Mapped[list[Player]] = relationship(
        "Player", secondary=insight_players, back_populates="insights"
    )


class WeeklyDigest(Base):
    __tablename__ = "weekly_digests"
    __table_args__ = (UniqueConstraint("year", "week", name="uq_digest_year_week"),)

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
    duration_s: Mapped[float | None] = mapped_column(Float, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(tz=UTC))

    insight_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("insights.id"), nullable=True, index=True
    )
    insight: Mapped[Insight | None] = relationship("Insight", back_populates="agent_runs")
