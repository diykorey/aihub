# AI Hub — Backend

Minimal FastAPI backend for the AI Hub insight magazine platform.

## Stack

- Python 3.12
- FastAPI
- SQLite (MVP default) / PostgreSQL via `DATABASE_URL`
- SQLAlchemy (ORM + session management)
- `uv` for dependency management
- LLM SDKs: OpenAI (+ Grok/xAI via compatible API), Anthropic, Google GenAI

## Quick start

```bash
# 1. Install dependencies (creates .venv automatically)
uv sync --group dev

# 2. Copy environment template
cp .env.example .env   # optionally edit DATABASE_URL, LLM keys

# 3. Run the dev server
uv run uvicorn app.main:app --reload
```

Verify at <http://localhost:8000/health> — should return `{"status":"ok"}`.  
Interactive docs (Swagger): <http://localhost:8000/docs>  
Read-only docs (ReDoc): <http://localhost:8000/redoc>

## Development commands

```bash
uv run pytest            # run tests
uv run ruff check .      # lint
uv run ruff format .     # format
uv run ty check app/     # type-check
```

## Project structure

```
backend/
  app/
    main.py           # FastAPI app, lifespan, routes
    db.py             # SQLAlchemy engine + session
    models.py         # ORM models: Source, Insight, WeeklyDigest, AgentRun
    schemas.py        # Pydantic request/response schemas
    services.py       # Business logic layer (keeps routes thin)
    agents/
      base.py         # BaseAgent, AgentContext (shared pipeline state), AgentResult
      llm.py          # Provider-agnostic LLM client (OpenAI, Anthropic, Google GenAI SDKs)
      orchestrator.py # Supervisor-pattern pipeline coordinator
      trend_extraction.py
      reasoning.py
      example_generator.py
      debate_generator.py
      review.py
  tests/
    test_health.py
    test_insights.py
    test_agents.py
  scripts/
    seed.py           # Populates SQLite with sample data
  pyproject.toml
  .env.example
```

## Agent pipeline

`POST /generate-insight` triggers the supervisor-pattern orchestrator, which runs agents sequentially through a shared `AgentContext`:

```
TrendExtractionAgent → ReasoningAgent → ExampleGeneratorAgent
    → DebateGeneratorAgent → ReviewAgent → persist Insight
```

- Each agent falls back to realistic stub data when LLM credentials are missing, so the full pipeline works locally without API keys
- Agents are isolated: if one raises an unhandled exception, it is logged as a failure and the pipeline continues
- Each agent run records execution duration (`duration_s`) for performance profiling
- ReviewAgent result determines insight status: `draft` (passed) or `review_failed`

### LLM provider configuration

Set in `.env` (see `.env.example`):
- `LLM_PROVIDER` — `openai` | `anthropic` | `gemini` | `grok`
- `LLM_MODEL` — model name (defaults per provider if unset)
- Provider-specific API key (`OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, etc.)

Each provider uses its official SDK (OpenAI, Anthropic, Google GenAI). Grok/xAI is OpenAI-compatible and uses the OpenAI SDK with a custom `base_url`. Default model is `gpt-5-nano` (cheapest option).

## Implemented stories

| Story                                 | Status     | Notes                              |
|---------------------------------------|------------|------------------------------------|
| Story 1 — FastAPI project + `/health` | ✅ Done     |                                    |
| Story 2 — Database connection         | ✅ Done     | SQLite default, PostgreSQL-ready   |
| Story 3 — Core models                 | ✅ Done     | Source, Insight, WeeklyDigest, AgentRun |
| Story 4 — `GET /insights`             | ✅ Done     | paginated, filters to `published`  |
| Story 5 — `GET /insights/{id}`        | ✅ Done     |                                    |
| Status management — `PATCH /insights/{id}/status` | ✅ Done | draft → published with auto-digest |
| Story 12 — Trend Extraction Agent     | ✅ Done     | stub + LLM mode                   |
| Story 13 — Reasoning Agent            | ✅ Done     | stub + LLM mode                   |
| Story 14 — Example Generator Agent    | ✅ Done     | stub + LLM mode                   |
| Story 15 — Weekly Digest endpoint     | ✅ Done     | `GET /digest/{year}/{week}`        |
| Story 17 — Debate Generator Agent     | ✅ Done     | 4 AI ecosystem perspectives        |
| Story 23 — Agent run logging + Review | ✅ Done     | `agent_runs` table, ReviewAgent    |

## Known gaps & future work

### LLM integration
- **No streaming** — `POST /generate-insight` blocks synchronously for 5+ sequential LLM calls with no progress feedback
- **No token/cost tracking** — SDK responses contain usage metadata but it's not yet captured or stored
- **No rate limiting** — nothing prevents concurrent `/generate-insight` calls from exhausting API quotas

### Data & persistence
- **No database migrations** — tables auto-created via `create_all`; no Alembic setup for schema evolution
- **`Source` model unused** — defined and seeded but no endpoint or service references it; placeholder for a future ingestion pipeline

### API & product surface
- **No frontend** — API-only; no consumer UI exists yet
- **No authentication** — all endpoints are public, including `POST /generate-insight` and `PATCH /insights/{id}/status`
- **No agent run log endpoint** — `agent_runs` are stored but not queryable via API

### Operational readiness
- **No structured logging** — uses default Python logging; no request tracing or correlation IDs

