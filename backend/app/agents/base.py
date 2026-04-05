"""Agent protocol, shared context and result types.

Every agent in the pipeline accepts an AgentContext (mutates it in-place)
and returns an AgentResult for logging.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class AgentContext:
    """Accumulated state passed through the pipeline.

    Each agent reads what it needs and writes its output back into the same
    context so downstream agents can build on prior results.
    """

    source_text: str
    # populated by TrendExtractionAgent
    title: str = ""
    summary: str = ""
    # populated by ReasoningAgent
    reasoning: str = ""
    # populated by ExampleGeneratorAgent
    examples: list[str] = field(default_factory=list)
    # populated by DebateGeneratorAgent  {"GPT-4": "...", "Gemini": "...", ...}
    perspectives: dict[str, str] = field(default_factory=dict)
    # populated by ReviewAgent
    review_passed: bool = False
    review_notes: str = ""
    # arbitrary extra data agents may attach
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class AgentResult:
    """Returned by every agent — logged to agent_runs table."""

    agent_name: str
    success: bool
    output: dict[str, Any]
    error: str | None = None


class BaseAgent:
    """Minimal base class all agents extend."""

    name: str = "base"

    def run(self, context: AgentContext) -> AgentResult:
        raise NotImplementedError

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _ok(self, output: dict[str, Any]) -> AgentResult:
        return AgentResult(agent_name=self.name, success=True, output=output)

    def _fail(self, error: str) -> AgentResult:
        return AgentResult(agent_name=self.name, success=False, output={}, error=error)
