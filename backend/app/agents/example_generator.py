"""Example Generator Agent — Story 14.

Reads `title` + `summary` from context, writes 3 practical usage examples
into `context.examples` covering solo entrepreneurs, developers, and enterprises.
"""

from __future__ import annotations

import json

from app.agents.base import AgentContext, AgentResult, BaseAgent
from app.agents.llm import chat_complete, is_configured

_SYSTEM = (
    "You are a practical AI application consultant. "
    "Given an AI development, generate exactly 3 real-world usage examples. "
    "One for solo entrepreneurs, one for developers, one for enterprises. "
    "Respond with a JSON array of 3 strings only — no markdown, no explanation. "
    'Example: ["Solo: ...", "Dev: ...", "Enterprise: ..."]'
)

_STUB_EXAMPLES = [
    (
        "Solo entrepreneur: Use the improved reasoning capability to build a personal "
        "AI research assistant that synthesises multiple sources and flags contradictions "
        "without manual review."
    ),
    (
        "Developer: Integrate the model into a code-review pipeline that not only spots "
        "bugs but explains the multi-step logic errors causing them, reducing back-and-forth "
        "with junior engineers."
    ),
    (
        "Enterprise: Deploy in a compliance workflow where the model evaluates contract "
        "clauses against regulatory requirements and provides a structured risk assessment "
        "with cited precedents."
    ),
]


class ExampleGeneratorAgent(BaseAgent):
    name = "example_generator"

    def run(self, context: AgentContext) -> AgentResult:
        if not is_configured():
            context.examples = _STUB_EXAMPLES
            return self._ok({"examples": context.examples})

        prompt = (
            f"AI Development: {context.title}\n\n"
            f"Summary: {context.summary}\n\n"
            "Generate 3 practical usage examples."
        )
        raw = chat_complete(prompt, _SYSTEM)

        try:
            data = json.loads(raw)
            if isinstance(data, list):
                context.examples = [str(item) for item in data[:3]]
                return self._ok({"examples": context.examples})
            return self._fail(f"Expected JSON array, got: {raw[:200]}")
        except json.JSONDecodeError:
            return self._fail(f"JSON parse error — raw response: {raw[:300]}")
