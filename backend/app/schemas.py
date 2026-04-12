"""Pydantic response schemas — Stories 4, 5 & agent pipeline."""

from __future__ import annotations

from pydantic import BaseModel


class InsightOut(BaseModel):
    id: int
    title: str
    summary: str
    reasoning: str | None = None
    examples: list[str] | None = None
    perspectives: dict[str, str] | None = None
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


class TagOut(BaseModel):
    id: int
    name: str

    model_config = {"from_attributes": True}


# ---------------------------------------------------------------------------
# Agent pipeline
# ---------------------------------------------------------------------------


class GenerateInsightRequest(BaseModel):
    source_text: str


class UpdateInsightStatusRequest(BaseModel):
    status: str


class AgentRunOut(BaseModel):
    id: int
    agent_name: str
    model: str | None = None
    success: bool
    error: str | None = None
    duration_s: float | None = None

    model_config = {"from_attributes": True}
