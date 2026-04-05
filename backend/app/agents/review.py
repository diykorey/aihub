"""Review Agent — Story 23 prerequisite.

Performs a quality gate on the accumulated context before the insight is
persisted.  Checks that minimum content is present and, when the LLM is
configured, asks the model to rate overall quality.
"""

from __future__ import annotations

from app.agents.base import AgentContext, AgentResult, BaseAgent
from app.agents.llm import chat_complete, is_configured

_SYSTEM = (
    "You are a senior editorial reviewer for an AI intelligence magazine. "
    "Review the insight draft below and decide whether it meets publication quality. "
    "Reply with exactly two lines:\n"
    "Line 1: PASS or FAIL\n"
    "Line 2: One sentence of constructive feedback."
)

_MIN_TITLE_LEN = 10
_MIN_SUMMARY_LEN = 50
_MIN_REASONING_LEN = 100


class ReviewAgent(BaseAgent):
    name = "review"

    def run(self, context: AgentContext) -> AgentResult:
        # ------------------------------------------------------------------
        # Structural checks (always run, no LLM required)
        # ------------------------------------------------------------------
        issues: list[str] = []
        if len(context.title) < _MIN_TITLE_LEN:
            issues.append(f"Title too short ({len(context.title)} chars, min {_MIN_TITLE_LEN})")
        if len(context.summary) < _MIN_SUMMARY_LEN:
            issues.append(
                f"Summary too short ({len(context.summary)} chars, min {_MIN_SUMMARY_LEN})"
            )
        if len(context.reasoning) < _MIN_REASONING_LEN:
            issues.append(
                f"Reasoning too short ({len(context.reasoning)} chars, min {_MIN_REASONING_LEN})"
            )

        if issues:
            context.review_passed = False
            context.review_notes = "; ".join(issues)
            return self._ok({"passed": False, "notes": context.review_notes})

        # ------------------------------------------------------------------
        # LLM quality check (only when API key is available)
        # ------------------------------------------------------------------
        if not is_configured():
            context.review_passed = True
            context.review_notes = "Structural checks passed. LLM review skipped (no API key)."
            return self._ok({"passed": True, "notes": context.review_notes})

        prompt = (
            f"Title: {context.title}\n\n"
            f"Summary: {context.summary}\n\n"
            f"Reasoning: {context.reasoning}\n\n"
            f"Examples: {'; '.join(context.examples)}\n\n"
            "Review this insight draft."
        )
        reply = chat_complete(prompt, _SYSTEM).strip()
        first_line = reply.splitlines()[0].strip().upper() if reply else "FAIL"
        notes = reply.splitlines()[1].strip() if len(reply.splitlines()) > 1 else reply

        context.review_passed = first_line == "PASS"
        context.review_notes = notes
        return self._ok({"passed": context.review_passed, "notes": context.review_notes})
