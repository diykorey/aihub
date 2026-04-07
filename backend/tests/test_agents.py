"""Agent unit tests — run without an API key using stub mode."""

from __future__ import annotations

from app.agents.base import AgentContext
from app.agents.debate_generator import DebateGeneratorAgent
from app.agents.example_generator import ExampleGeneratorAgent
from app.agents.reasoning import ReasoningAgent
from app.agents.review import ReviewAgent
from app.agents.trend_extraction import TrendExtractionAgent


def _ctx(text: str = "OpenAI released GPT-5 with improved reasoning.") -> AgentContext:
    return AgentContext(source_text=text)


# ---------------------------------------------------------------------------
# TrendExtractionAgent
# ---------------------------------------------------------------------------


def test_trend_extraction_stub_populates_title_and_summary() -> None:
    ctx = _ctx()
    result = TrendExtractionAgent().run(ctx)
    assert result.success
    assert len(ctx.title) >= 10
    assert len(ctx.summary) >= 20


# ---------------------------------------------------------------------------
# ReasoningAgent
# ---------------------------------------------------------------------------


def test_reasoning_stub_populates_reasoning() -> None:
    ctx = _ctx()
    ctx.title = "GPT-5 released"
    ctx.summary = "OpenAI released GPT-5."
    result = ReasoningAgent().run(ctx)
    assert result.success
    assert len(ctx.reasoning) >= 100


# ---------------------------------------------------------------------------
# ExampleGeneratorAgent
# ---------------------------------------------------------------------------


def test_example_generator_returns_three_examples() -> None:
    ctx = _ctx()
    ctx.title = "GPT-5 released"
    ctx.summary = "OpenAI released GPT-5."
    result = ExampleGeneratorAgent().run(ctx)
    assert result.success
    assert len(ctx.examples) == 3


# ---------------------------------------------------------------------------
# DebateGeneratorAgent
# ---------------------------------------------------------------------------


def test_debate_generator_returns_four_perspectives() -> None:
    ctx = _ctx()
    ctx.title = "GPT-5 released"
    ctx.summary = "OpenAI released GPT-5."
    result = DebateGeneratorAgent().run(ctx)
    assert result.success
    assert len(ctx.perspectives) == 4
    assert "GPT (OpenAI)" in ctx.perspectives


# ---------------------------------------------------------------------------
# ReviewAgent
# ---------------------------------------------------------------------------


def test_review_passes_complete_context() -> None:
    ctx = _ctx()
    ctx.title = "GPT-5 released by OpenAI"
    ctx.summary = "OpenAI released GPT-5 with significantly improved reasoning. " * 3
    ctx.reasoning = "This matters because it raises the capability bar. " * 5
    result = ReviewAgent().run(ctx)
    assert result.success
    assert ctx.review_passed is True


def test_review_fails_on_empty_title() -> None:
    ctx = _ctx()
    ctx.title = "Hi"
    ctx.summary = "Short."
    ctx.reasoning = ""
    result = ReviewAgent().run(ctx)
    assert result.success  # agent ran without exception
    assert ctx.review_passed is False  # but quality gate failed


# ---------------------------------------------------------------------------
# Full pipeline via orchestrator (no DB — unit-level)
# ---------------------------------------------------------------------------


def test_all_agents_run_sequentially_on_stub() -> None:
    """Smoke test: every agent runs without raising, context is fully populated."""
    from app.agents.debate_generator import DebateGeneratorAgent
    from app.agents.example_generator import ExampleGeneratorAgent
    from app.agents.reasoning import ReasoningAgent
    from app.agents.review import ReviewAgent
    from app.agents.trend_extraction import TrendExtractionAgent

    agents = [
        TrendExtractionAgent(),
        ReasoningAgent(),
        ExampleGeneratorAgent(),
        DebateGeneratorAgent(),
        ReviewAgent(),
    ]
    ctx = AgentContext(source_text="OpenAI released GPT-5 with improved reasoning.")

    for agent in agents:
        result = agent.run(ctx)
        assert result.agent_name == agent.name

    assert ctx.title
    assert ctx.summary
    assert ctx.reasoning
    assert ctx.examples
    assert ctx.perspectives
