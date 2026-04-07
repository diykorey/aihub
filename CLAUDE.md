# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

AI Hub is an AI-generated insight magazine platform. The backend ingests source text, runs it through a multi-agent LLM pipeline, and produces structured "insights" grouped into weekly digests.

## Build & Development Commands

All commands run from the `backend/` directory:

```bash
uv sync --group dev          # install dependencies (creates .venv)
cp .env.example .env         # first-time setup — edit API keys as needed
uv run uvicorn app.main:app --reload   # dev server on :8000
uv run python scripts/seed.py          # seed SQLite with sample data
```

### Testing & Quality

```bash
uv run pytest                  # run all tests
uv run pytest tests/test_health.py           # single test file
uv run pytest -k test_get_insight_by_id      # single test by name
uv run ruff check .            # lint
uv run ruff format .           # format
uv run ty check app/           # type-check
```

## Architecture

### Request Flow

```
FastAPI routes (main.py) → services.py → models.py / agents/orchestrator.py
```

- **`main.py`** — app factory, lifespan (auto-creates tables), CORS, all route definitions
- **`services.py`** — business logic layer; routes stay thin
- **`db.py`** — SQLAlchemy engine, `SessionLocal`, `get_db` dependency (commits on success, rolls back on error)
- **`models.py`** — ORM: `Source`, `Insight`, `WeeklyDigest`, `AgentRun`
- **`schemas.py`** — Pydantic response/request models (`from_attributes = True`)

### Agent Pipeline (supervisor pattern)

`POST /generate-insight` triggers `InsightOrchestrator.run()` which executes agents sequentially through a shared `AgentContext` dataclass:

```
TrendExtractionAgent → ReasoningAgent → ExampleGeneratorAgent
    → DebateGeneratorAgent → ReviewAgent → persist Insight (status=draft)
```

Each agent:
- Extends `BaseAgent` (`agents/base.py`), implements `run(context) -> AgentResult`
- Reads from and mutates the shared `AgentContext`
- Falls back to realistic stub data when LLM credentials are missing (no API key needed for dev/test)
- Every run is logged to the `agent_runs` table

### LLM Integration

`agents/llm.py` provides `chat_complete()` — a provider-agnostic wrapper using official SDKs (OpenAI for OpenAI+Grok, Anthropic, Google GenAI). Configured via env vars (`LLM_PROVIDER`, `LLM_MODEL`, provider API keys). SDKs are lazily imported inside each provider function.

### Database

SQLite by default (`aihub.db`); swap to PostgreSQL by changing `DATABASE_URL` in `.env`. Tables auto-created on startup via `Base.metadata.create_all` (no Alembic yet).

### Testing Patterns

- Tests use an in-memory SQLite with `StaticPool` and FastAPI dependency overrides (`app.dependency_overrides[get_db]`)
- Agent tests run without API keys using the built-in stub mode
- `reset_db` fixture recreates schema and seeds minimal data before each test
