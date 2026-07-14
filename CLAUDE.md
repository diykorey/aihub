# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

AIHub is an AI-driven intelligence magazine about AI. The backend is a FastAPI Python app that ingests source text, runs it through a multi-agent LLM pipeline, and produces structured "insights" grouped into weekly digests.

End-to-end flow: source signals → agent pipeline → structured insights → REST API → SvelteKit pages.

## Repository Reality

- `backend/` is implemented (FastAPI app, SQLAlchemy models, agents, tests).
- `frontend/` is not yet present — treat it as planned work.
- Treat runtime behavior in `backend/app/` and `backend/tests/` as source of truth; use `docs/` for MVP scope/roadmap.
- `docs/backlog/ai_hub_startup_backlog.md` defines MVP story order and acceptance criteria — prefer that over inventing scope.

## Build & Development Commands

All commands run from the `backend/` directory:

```bash
uv sync --group dev                    # Install all dependencies (creates .venv)
cp .env.example .env                   # First-time setup — edit API keys as needed
uv run uvicorn app.main:app --reload   # Dev server on http://localhost:8000 (verify /docs + /health)
uv run python scripts/seed.py          # Seed SQLite with sample data
```

### Testing & Quality

```bash
uv run pytest                                        # Run all tests
uv run pytest tests/test_health.py                   # Single test file
uv run pytest tests/test_agents.py -k "test_trend"   # Single test by name
uv run ruff check .                                  # Lint
uv run ruff format .                                 # Auto-format
uv run ty check app/                                 # Type check (strict)
```

No API keys needed for local dev — agents fall back to stub mode when credentials are missing.

## Architecture

### Request Flow

```
FastAPI routes (main.py) → services.py → models.py / agents/orchestrator.py
```

Keep service boundaries simple: thin routes, logic in `services.py`.

### Backend Layers (`backend/app/`)

- **main.py** — app factory, lifespan (auto-creates tables), CORS, all route definitions
- **services.py** — business logic / query layer; routes stay thin
- **db.py** — SQLAlchemy engine, `SessionLocal`, `get_db` dependency (commits on success, rolls back on error)
- **models.py** — SQLAlchemy 2.0 ORM: `User`, `Source`, `Tag`, `Player`, `Insight`, `WeeklyDigest`, `AgentRun`
- **schemas.py** — Pydantic request/response models (`from_attributes = True` for ORM mapping)

### REST Endpoints

- `GET /health` — liveness
- `GET /insights` — paginated list
- `GET /insights/{id}` — single insight
- `GET /digest/{year}/{week}` — weekly digest with insights
- `POST /generate-insight` — admin: runs the orchestrator pipeline on provided source text, returns a draft insight
- `PATCH /insights/{id}/status` — admin: transition status (e.g. draft → published; auto-assigns to week's digest)

### Agent Pipeline (`backend/app/agents/`)

`POST /generate-insight` triggers `InsightOrchestrator.run()`, which executes agents sequentially through a shared `AgentContext` dataclass:

1. **TrendExtractionAgent** — Extracts title + summary from source text
2. **ReasoningAgent** — Writes analysis of why it matters
3. **ExampleGeneratorAgent** — Generates 3 practical use cases
4. **DebateGeneratorAgent** — Generates 4 AI ecosystem perspectives
5. **ReviewAgent** — Quality gate (structural checks + LLM review)

Key abstractions:
- `BaseAgent` in `agents/base.py` with `run(context: AgentContext) -> AgentResult`
- Agents mutate the shared `AgentContext` in-place; downstream agents build on prior results
- `AgentResult` is JSON-serializable with success flag + error message; every run is logged to the `agent_runs` table
- Non-fatal agent failures don't stop the pipeline (orchestrator catches exceptions per-agent)
- Insight is persisted with `status='draft'` when review passes, `'review_failed'` otherwise
- Agents fall back to stub outputs when LLM credentials are not configured

### LLM Integration

`agents/llm.py` provides `chat_complete()` — a provider-agnostic wrapper using official SDKs (OpenAI SDK for OpenAI and Grok, Anthropic, Google GenAI). SDKs are lazily imported inside each provider function. Configured via env vars (`LLM_PROVIDER`, `LLM_MODEL`, provider API keys). When credentials are missing, returns a stub marker string so local dev/tests continue without secrets.

### Database

SQLite by default (`aihub.db`); swap to PostgreSQL by changing `DATABASE_URL` in `.env`. Tables auto-created on startup via `Base.metadata.create_all` (no Alembic yet).

### Testing (`backend/tests/`)

- Endpoint tests use in-memory SQLite with `StaticPool` and FastAPI `app.dependency_overrides[get_db]` (see `test_insights.py`)
- `reset_db` fixture recreates schema and seeds minimal data before each test
- Agent tests run in stub mode (no API keys) via direct agent calls
- `TestClient` for endpoint tests, direct agent calls for unit tests

## Configuration

Environment variables (see `backend/.env.example`):
- `DATABASE_URL` — Default `sqlite:///./aihub.db`
- `LLM_PROVIDER` — `openai|anthropic|gemini|grok`
- `LLM_MODEL` — Provider-specific model name
- Provider API keys: `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, `GEMINI_API_KEY`, `XAI_API_KEY`

## Code Conventions

- Python 3.12, managed with `uv`
- Ruff: 100-char line length, PEP 8
- SQLAlchemy 2.0 `mapped_column` + `select()` style (not legacy Query API)
- FastAPI dependency injection via `Depends(get_db)`

## Frontend (Planned)

Not yet implemented. Planned stack and conventions (from `docs/ai_hub_frontend_setup_simple.md`):

- **Stack:** SvelteKit + TypeScript + Tailwind CSS, package manager `pnpm`
- **Minimal libs:** `lucide-svelte`, `date-fns`
- **Routing:** `/`, `/insights/[id]`, `/digest/[year]/[week]`
- **API layer:** `src/lib/api/client.ts` with tiny wrappers (`insights.ts`, `digests.ts`)
- **Components:** build small and focused first (`InsightCard`, `ReasoningBlock`, `SourcesBlock`, `DebateBlock`)
- **Mocks:** use `src/lib/mocks` before the backend is wired up, then replace with API calls
- **Local run:** `pnpm install` then `pnpm dev`

Frontend depends first on the `/insights`, `/insights/{id}`, and `/digest/{year}/{week}` contracts.

## Implementation Sequencing

Backlog implementation order (see `docs/backlog/ai_hub_dev_tickets.md`):

1. Backend core
2. Frontend foundation
3. Agents
4. Source ingestion
5. Admin / monitoring

Post-MVP items (forecasting, broader ops) are documented but should not block MVP delivery.

## Documentation

- `docs/ai_hub_backend_setup_simple.md` — backend MVP setup guide
- `docs/ai_hub_frontend_setup_simple.md` — frontend MVP setup guide
- `docs/ai_hub_mindmap_improved.md` — product intent / mindmap
- `docs/backlog/` — story backlog with acceptance criteria
