# AI Hub — Backend

Minimal FastAPI backend for the AI Hub insight magazine platform.

## Stack

- Python 3.12
- FastAPI
- PostgreSQL + SQLAlchemy (Story 2+)
- `uv` for dependency management

## Quick start

```bash
# 1. Install dependencies (creates .venv automatically)
uv sync --group dev

# 2. Copy environment template
cp .env.example .env   # edit DATABASE_URL for Story 2+

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
    main.py        # FastAPI app, lifespan, routes
    db.py          # SQLAlchemy engine + session (Story 2)
    models.py      # ORM models: Source, Insight, WeeklyDigest (Story 3)
    schemas.py     # Pydantic response schemas (Story 3-5)
    services.py    # Business logic, keeps routes thin (Story 4-5)
    agents/        # Agent stubs — trend extraction, reasoning, etc. (Story 9+)
  tests/
    test_health.py
  pyproject.toml
  .env.example
```

## Implemented stories

| Story                                 | Status     | Notes                          |
|---------------------------------------|------------|--------------------------------|
| Story 1 — FastAPI project + `/health` | ✅ Done     |                                |
| Story 2 — PostgreSQL connection       | 🔲 Next    | needs `DATABASE_URL` in `.env` |
| Story 3 — Core models                 | 🔲 Pending |                                |
| Story 4 — `GET /insights`             | 🔲 Pending |                                |
| Story 5 — `GET /insights/{id}`        | 🔲 Pending |                                |

