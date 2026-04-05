"""Insight Orchestrator — supervisor pattern.

Runs agents sequentially, logs every run to agent_runs, then persists the
resulting Insight to the database.

Pipeline order (matches backlog Stories 12–17):
  TrendExtractionAgent → ReasoningAgent → ExampleGeneratorAgent
      → DebateGeneratorAgent → ReviewAgent → persist Insight
"""

from __future__ import annotations

import json
import os
from datetime import UTC, datetime

from sqlalchemy.orm import Session

from app.agents.base import AgentContext, AgentResult, BaseAgent
from app.agents.debate_generator import DebateGeneratorAgent
from app.agents.example_generator import ExampleGeneratorAgent
from app.agents.reasoning import ReasoningAgent
from app.agents.review import ReviewAgent
from app.agents.trend_extraction import TrendExtractionAgent
from app.models import AgentRun, Insight


def _current_week() -> tuple[int, int]:
    now = datetime.now(UTC)
    iso = now.isocalendar()
    return iso.year, iso.week


class InsightOrchestrator:
    """Supervisor-pattern orchestrator.

    Each agent writes into a shared AgentContext.  The orchestrator logs every
    AgentResult to agent_runs and links them to the created Insight once it is
    flushed.
    """

    _pipeline: list[BaseAgent] = [
        TrendExtractionAgent(),
        ReasoningAgent(),
        ExampleGeneratorAgent(),
        DebateGeneratorAgent(),
        ReviewAgent(),
    ]

    def __init__(self, db: Session) -> None:
        self.db = db

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def run(self, source_text: str) -> Insight:
        """Execute the full pipeline and return a persisted Insight (status=draft)."""
        context = AgentContext(source_text=source_text)
        run_logs: list[AgentResult] = []

        for agent in self._pipeline:
            result = agent.run(context)
            run_logs.append(result)
            # Non-fatal: log failure but continue so downstream agents can
            # fill in what they can with partial context.

        year, week = _current_week()
        insight = Insight(
            title=context.title or "Untitled Insight",
            summary=context.summary or "",
            reasoning=context.reasoning or None,
            examples=json.dumps(context.examples) if context.examples else None,
            perspectives=json.dumps(context.perspectives) if context.perspectives else None,
            week=week,
            year=year,
            status="draft",  # requires admin review before publishing
        )
        self.db.add(insight)
        self.db.flush()  # get insight.id

        for result in run_logs:
            self.db.add(
                AgentRun(
                    insight_id=insight.id,
                    agent_name=result.agent_name,
                    model=os.getenv("LLM_MODEL", "stub"),
                    output=json.dumps(result.output),
                    success=result.success,
                    error=result.error,
                )
            )

        self.db.flush()
        return insight
