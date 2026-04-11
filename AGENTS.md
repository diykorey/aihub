# AGENTS.md

## Repository reality first
- `backend/` is implemented (FastAPI app, SQLAlchemy models, agents, tests); `frontend/` is currently empty.
- Treat backend runtime behavior in `backend/app/` + `backend/tests/` as source of truth; use `docs/ai_hub_backend_setup_simple.md` and `docs/ai_hub_frontend_setup_simple.md` for MVP scope/roadmap.
- `docs/backlog/ai_hub_startup_backlog.md` defines MVP story order and acceptance criteria; prefer that over inventing scope.

## Big picture architecture (MVP)
- Product intent: AI-generated "insight magazine" (`docs/ai_hub_mindmap_improved.md`).
- End-to-end flow: source signals -> agent pipeline -> structured insights -> REST API -> SvelteKit pages.
- Backend responsibilities: source collection, agent execution, structured persistence, REST endpoints.
- Frontend responsibilities: browse insights, open detail pages, view weekly digest, later tags/players.
- Keep service boundaries simple: thin routes, logic in services (`app/services.py` in backend setup doc).

## Backend conventions to follow
- Preferred stack: Python + FastAPI + SQLAlchemy; default DB is SQLite via `DATABASE_URL` in `backend/.env.example` (PostgreSQL-ready by URL swap).
- Suggested backend layout (from docs): `app/main.py`, `app/db.py`, `app/models.py`, `app/schemas.py`, `app/services.py`, `app/agents/`.
- Core models in code: `Source`, `Insight`, `WeeklyDigest`, `AgentRun`.
- Core initial endpoints (MVP unblockers):
  - `GET /health`
  - `GET /insights`
  - `GET /insights/{id}`
  - `GET /digest/{year}/{week}`
- Implemented admin endpoint: `POST /generate-insight` (runs orchestrator pipeline and returns draft insight).
- Add seed data early (`scripts/seed.py`) so frontend can integrate before agent pipeline is complete.

## Frontend conventions to follow
- Preferred stack: SvelteKit + TypeScript + Tailwind + `pnpm`; minimal libs (`lucide-svelte`, `date-fns`).
- Suggested routing structure includes `/`, `/insights/[id]`, `/digest/[year]/[week]`.
- Suggested API layer: `src/lib/api/client.ts` with tiny wrappers (`insights.ts`, `digests.ts`).
- Build small, focused components first (`InsightCard`, `ReasoningBlock`, `SourcesBlock`, `DebateBlock`).
- Use mock data in `src/lib/mocks` before backend is ready; replace with API calls later.

## Critical workflows (documented commands)
- Backend local run: `cd backend && uv sync --group dev && uv run uvicorn app.main:app --reload` and verify `/docs` + `/health`.
- Backend tests/tooling: `cd backend && uv run pytest`, `uv run ruff check .`, `uv run ruff format .`, `uv run ty check app/`.
- Seed local data: `cd backend && uv run python scripts/seed.py`.
- Frontend local run (planned): `pnpm install` then `pnpm dev`.
- Dependency install examples from docs:
  - Backend: `uv sync --group dev`
  - Frontend: `pnpm add lucide-svelte date-fns`

## Integration points and sequencing
- Frontend depends first on `/insights`, `/insights/{id}`, `/digest/{year}/{week}` contracts.
- Agent pipeline is implemented in `app/agents/` with supervisor orchestration in `app/agents/orchestrator.py` and run logs in `agent_runs`; agents fall back to stub outputs when LLM credentials are not configured.
- Backlog implementation order is explicit: Backend core -> Frontend foundation -> Agents -> Source ingestion -> Admin/monitoring (`docs/backlog/ai_hub_dev_tickets.md`).
- Post-MVP items (forecasting, broader ops) are documented but should not block MVP delivery.

