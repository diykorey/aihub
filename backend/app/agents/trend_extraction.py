"""Trend Extraction Agent — Story 12.

Reads raw source text and writes `title` + `summary` into the context.
When OPENAI_API_KEY is set, calls the LLM with a structured JSON prompt.
Without the key, injects realistic stub data so the rest of the pipeline works.
"""

from __future__ import annotations

import json

from app.agents.base import AgentContext, AgentResult, BaseAgent
from app.agents.llm import chat_complete, is_configured

_SYSTEM = (
    "You are an AI trend analyst. Extract the key AI development from the provided text. "
    "Respond with a JSON object only — no markdown, no explanation. "
    'Schema: {"title": "<max 100 chars>", "summary": "<max 300 chars>"}'
)

_STUB_TITLE = "AI Language Models Achieve New Reasoning Benchmark"
_STUB_SUMMARY = (
    "Latest research demonstrates significant improvements in multi-step reasoning "
    "and problem-solving capabilities, outperforming previous state-of-the-art models "
    "on standard academic benchmarks."
)


class TrendExtractionAgent(BaseAgent):
    name = "trend_extraction"

    def run(self, context: AgentContext) -> AgentResult:
        if not is_configured():
            context.title = _STUB_TITLE
            context.summary = _STUB_SUMMARY
            return self._ok({"title": context.title, "summary": context.summary})

        prompt = f"Extract the AI trend from this source text:\n\n{context.source_text}"
        raw = chat_complete(prompt, _SYSTEM)

        try:
            data = json.loads(raw)
            context.title = str(data.get("title", "")).strip()
            context.summary = str(data.get("summary", "")).strip()
            return self._ok({"title": context.title, "summary": context.summary})
        except json.JSONDecodeError:
            return self._fail(f"JSON parse error — raw response: {raw[:300]}")
