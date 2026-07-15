# AIHub Wiki

**AIHub** is an AI-driven intelligence magazine *about* AI. It ingests raw source
signals (articles, papers, GitHub releases), runs them through a multi-agent LLM
pipeline, and produces structured **insights** grouped into weekly digests that are
served over a REST API and (planned) SvelteKit frontend.

> **End-to-end flow:** source signals → agent pipeline → structured insights → REST API → SvelteKit pages

## What it does

- **Ingests** external signals as `Source` records with a `trust_score`.
- **Generates** insights via a sequential agent pipeline (trend extraction → reasoning →
  examples → debate → review), with every agent run audited in the database.
- **Organises** insights into ISO-week `WeeklyDigest` groups and by `Tag` and `Player`
  (AI ecosystem company) lenses.
- **Serves** everything through a thin FastAPI REST layer.

## Architecture at a glance

```
FastAPI routes (main.py) → services.py → models.py / agents/orchestrator.py
```

| Layer | File | Responsibility |
|-------|------|----------------|
| Routes | `app/main.py` | App factory, lifespan (auto-creates tables), CORS, endpoints |
| Services | `app/services.py` | Business logic / query layer (routes stay thin) |
| Data | `app/models.py` | SQLAlchemy 2.0 ORM models |
| Contracts | `app/schemas.py` | Pydantic request/response models |
| DB | `app/db.py` | Engine, `SessionLocal`, `get_db` dependency |
| Agents | `app/agents/` | Multi-agent insight pipeline + LLM wrapper |

## Tech stack

- **Language:** Python 3.12, managed with `uv`
- **Web:** FastAPI + Uvicorn
- **ORM:** SQLAlchemy 2.0 (`mapped_column` + `select()` style)
- **Validation:** Pydantic (`from_attributes = True` for ORM mapping)
- **Database:** SQLite by default (`aihub.db`); PostgreSQL-ready via `DATABASE_URL`
- **LLM providers:** OpenAI, Anthropic, Google GenAI, Grok — pluggable, with stub
  fallback when no API keys are configured
- **Quality:** `ruff` (lint + format), `ty` (strict type check), `pytest`

## Repository layout

- `backend/` — implemented (FastAPI app, models, agents, tests)
- `frontend/` — planned (SvelteKit + TypeScript + Tailwind)
- `docs/` — MVP setup guides, product mindmap, and the story backlog
- `docs/backlog/` — epics, ~92 dev tickets, and acceptance criteria

## Getting started

All commands run from `backend/`:

```bash
uv sync --group dev                    # Install dependencies (creates .venv)
cp .env.example .env                   # First-time setup — edit API keys as needed
uv run uvicorn app.main:app --reload   # Dev server → http://localhost:8000 (/docs + /health)
uv run python scripts/seed.py          # Seed SQLite with sample data
uv run pytest                          # Run the test suite
```

No API keys are needed for local dev — agents fall back to stub mode when
credentials are missing.

## Development phases

The backlog is delivered in 8 phases (see `docs/backlog/ai_hub_dev_tickets.md`):

| Phase | Scope | Status |
|-------|-------|--------|
| **1 — Core backend** | FastAPI skeleton, DB, models, core endpoints | ✅ Complete |
| 2 — Frontend UI | SvelteKit pages & components | ⬜ Not started |
| 3 — AI agents | Full agent pipeline | 🟡 Core done |
| 4 — Source ingestion | Collectors, trust registry | ⬜ Not started |
| 5–8 — Admin, roles, subscriptions, billing | Post-MVP | ⬜ Not started |

See **[[Phase 1 Backend Core|Phase-1-Backend-Core]]** for the detailed record of what
Phase 1 delivered, and the **[[Glossary]]** for definitions of the domain terms used
throughout the project.
