"""Reasoning Agent — Story 13.

Reads `title` + `summary` from context, writes `reasoning` explaining
why the development matters — ecosystem implications, strategic significance,
adoption trends.
"""

from __future__ import annotations

from app.agents.base import AgentContext, AgentResult, BaseAgent
from app.agents.llm import chat_complete, is_configured

_SYSTEM = (
    "You are a senior AI industry analyst. "
    "Given an AI development, explain in 2–4 paragraphs WHY it matters: "
    "its ecosystem implications, technological significance, and adoption trends. "
    "Write directly — no headers, no bullet points."
)

_STUB_REASONING = (
    "This development marks a significant step forward in the broader AI ecosystem. "
    "By pushing the boundaries of reasoning capability, it expands the set of tasks "
    "that language models can reliably handle, opening the door to new enterprise "
    "applications in legal, medical, and scientific domains.\n\n"
    "From a competitive standpoint, improvements in benchmark performance typically "
    "accelerate adoption cycles as organizations benchmark their own workflows and "
    "identify automation opportunities. The resulting pressure on competing labs "
    "will likely compress the timeline for the next generation of capability jumps.\n\n"
    "For developers, the practical implication is that prompt engineering strategies "
    "optimised for weaker models may need revisiting — more complex, multi-step "
    "instructions become viable, which reduces the need for fine-tuning on simple tasks."
)


class ReasoningAgent(BaseAgent):
    name = "reasoning"

    def run(self, context: AgentContext) -> AgentResult:
        if not is_configured():
            context.reasoning = _STUB_REASONING
            return self._ok({"reasoning": context.reasoning})

        prompt = (
            f"AI Development: {context.title}\n\n"
            f"Summary: {context.summary}\n\n"
            "Explain why this development matters."
        )
        context.reasoning = chat_complete(prompt, _SYSTEM)
        return self._ok({"reasoning": context.reasoning})
