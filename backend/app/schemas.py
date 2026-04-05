"""Pydantic response schemas — Stories 4, 5 & agent pipeline."""

from __future__ import annotations

from pydantic import BaseModel


class InsightOut(BaseModel):
    id: int
    title: str
    summary: str
    reasoning: str | None = None
    examples: str | None = None  # JSON string — frontend parses
    perspectives: str | None = None  # JSON string — frontend parses
    week: int
    year: int
    status: str

    model_config = {"from_attributes": True}


class DigestOut(BaseModel):
    id: int
    year: int
    week: int
    insights: list[InsightOut] = []

    model_config = {"from_attributes": True}


# ---------------------------------------------------------------------------
# Agent pipeline
# ---------------------------------------------------------------------------


class GenerateInsightRequest(BaseModel):
    source_text: str


class AgentRunOut(BaseModel):
    id: int
    agent_name: str
    model: str | None = None
    success: bool
    error: str | None = None

    model_config = {"from_attributes": True}
