"""Debate Generator Agent — Story 17.

Generates perspectives on the AI development from the viewpoint of four
major AI ecosystems: GPT (OpenAI), Gemini (Google), Claude (Anthropic),
Grok (xAI). Writes into `context.perspectives`.
"""

from __future__ import annotations

import json

from app.agents.base import AgentContext, AgentResult, BaseAgent
from app.agents.llm import chat_complete, is_configured

_PLAYERS = ["GPT (OpenAI)", "Gemini (Google)", "Claude (Anthropic)", "Grok (xAI)"]

_SYSTEM = (
    "You are a multi-perspective AI analyst. "
    "Given an AI development, write a short paragraph (3–5 sentences) from the strategic "
    "point of view of each of these AI ecosystem players: "
    + ", ".join(_PLAYERS)
    + ". Consider advantages, risks, and competitive implications for each. "
    "Respond with a JSON object only. "
    'Schema: {"GPT (OpenAI)": "...", "Gemini (Google)": "...",'
    ' "Claude (Anthropic)": "...", "Grok (xAI)": "..."}'
)

_STUB_PERSPECTIVES: dict[str, str] = {
    "GPT (OpenAI)": (
        "This development directly validates OpenAI's multi-year investment in scaling "
        "transformer architectures. As the benchmark setter, OpenAI benefits from raising "
        "the bar — competitors must spend significantly to match, while OpenAI retains "
        "the integration advantage through the existing API ecosystem and enterprise contracts."
    ),
    "Gemini (Google)": (
        "Google's deep infrastructure advantage means Gemini can leverage the same "
        "architectural insight at lower marginal cost via TPUs. The key risk is perception: "
        "public benchmarks favour OpenAI's narrative, so Google must demonstrate real-world "
        "productivity gains rather than competing solely on academic scores."
    ),
    "Claude (Anthropic)": (
        "Anthropic's Constitutional AI alignment work could differentiate Anthropic in "
        "regulated industries where reasoning accuracy must be auditable. This development "
        "raises the bar for safety-conscious reasoning — an area where Anthropic has invested "
        "heavily and where a capability gap would undermine its core positioning."
    ),
    "Grok (xAI)": (
        "xAI's real-time data advantage through X/Twitter remains its primary differentiator. "
        "Improved reasoning capability in competitor models narrows the gap in factual accuracy, "
        "making Grok's timeliness advantage more critical. Expect xAI to emphasise speed and "
        "recency over benchmark performance in its next positioning cycle."
    ),
}


class DebateGeneratorAgent(BaseAgent):
    name = "debate_generator"

    def run(self, context: AgentContext) -> AgentResult:
        if not is_configured():
            context.perspectives = _STUB_PERSPECTIVES
            return self._ok({"perspectives": context.perspectives})

        prompt = (
            f"AI Development: {context.title}\n\n"
            f"Summary: {context.summary}\n\n"
            "Generate perspectives from each AI ecosystem player."
        )
        raw = chat_complete(prompt, _SYSTEM)

        try:
            data = json.loads(raw)
            if isinstance(data, dict):
                context.perspectives = {str(k): str(v) for k, v in data.items()}
                return self._ok({"perspectives": context.perspectives})
            return self._fail(f"Expected JSON object, got: {raw[:200]}")
        except json.JSONDecodeError:
            return self._fail(f"JSON parse error — raw response: {raw[:300]}")
