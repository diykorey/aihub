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
import time
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

    def __init__(self, db: Session) -> None:
        self.db = db
        self._pipeline: tuple[BaseAgent, ...] = (
            TrendExtractionAgent(),
            ReasoningAgent(),
            ExampleGeneratorAgent(),
            DebateGeneratorAgent(),
            ReviewAgent(),
        )

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def run(self, source_text: str) -> Insight:
        """Execute the full pipeline and return a persisted Insight.

        Status is set to 'draft' if the review agent passes, 'review_failed' otherwise.
        """
        context = AgentContext(source_text=source_text)
        run_logs: list[tuple[AgentResult, float]] = []

        for agent in self._pipeline:
            t0 = time.monotonic()
            try:
                result = agent.run(context)
            except Exception as exc:
                result = AgentResult(
                    agent_name=agent.name, success=False, output={}, error=str(exc)
                )
            duration_s = time.monotonic() - t0
            run_logs.append((result, duration_s))

        year, week = _current_week()
        status = "draft" if context.review_passed else "review_failed"
        insight = Insight(
            title=context.title or "Untitled Insight",
            summary=context.summary or "",
            reasoning=context.reasoning or None,
            examples=context.examples or None,
            perspectives=context.perspectives or None,
            week=week,
            year=year,
            status=status,
        )
        self.db.add(insight)
        self.db.flush()  # get insight.id

        for result, duration_s in run_logs:
            self.db.add(
                AgentRun(
                    insight_id=insight.id,
                    agent_name=result.agent_name,
                    model=os.getenv("LLM_MODEL", "stub"),
                    output=json.dumps(result.output),
                    success=result.success,
                    error=result.error,
                    duration_s=round(duration_s, 3),
                )
            )

        self.db.flush()
        return insight
