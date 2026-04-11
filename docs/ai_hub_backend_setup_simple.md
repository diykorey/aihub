# AI Hub Backend Setup (Ultra-Simple Version for AI Development)

## Goal

Create a **minimal backend** that AI agents can extend quickly and safely.

Priorities:

- fast development
- low complexity
- clear structure
- minimal dependencies

Avoid unnecessary infrastructure in the beginning.

---

# Stack (Minimal)

Use this stack unless there is a hard blocker:

- **Python 3.12**
- **FastAPI**
- **SQLAlchemy**
- **SQLite** (default via `DATABASE_URL`; swap to PostgreSQL by changing the URL)
- **uv** (dependency management)

Add only later if needed:

- Alembic
- Redis
- Celery
- Docker

Start simple.

---

# Step 1 — Create the Project

Create a new Python project.

Suggested structure:

```text
backend/
  app/
    main.py
    db.py
    models.py
    schemas.py
    services.py
    agents/
      base.py
      orchestrator.py
      trend_extraction.py
      reasoning.py
      example_generator.py
      debate_generator.py
      review.py
      llm.py
  scripts/
    seed.py
  tests/
  pyproject.toml
  .env
  .env.example
```

Install dependencies:

```bash
uv sync --group dev
```

Copy environment template:

```bash
cp .env.example .env
```

Run the app:

```bash
uv run uvicorn app.main:app --reload
```

Verify:

```text
http://localhost:8000/docs
```

---

# Step 2 — Basic FastAPI App

Create minimal API.

`app/main.py`

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}
```

Purpose:

- verify API works
- verify local environment

---

# Step 3 — Database Connection

Create a simple database connection in:

`app/db.py`

Example:

```python
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./aihub.db")

_connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(DATABASE_URL, connect_args=_connect_args)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

class Base(DeclarativeBase):
    pass
```

Default is SQLite (`aihub.db` in project root).  
To switch to PostgreSQL set `DATABASE_URL=postgresql://user:pass@localhost/aihub` in `.env`.

---

# Step 4 — Models

Create models in `app/models.py`.

## User

Represents a registered platform user and controls what actions they are allowed to perform based on their role.

Fields:

- id
- email
- role (`reader`, `subscriber`, `admin`)
- created_at

## Source

Represents a single external signal (URL) collected from the web that the agent pipeline uses as raw input to generate insights.

Fields:

- id
- url
- source_type (`github`, `blog`, `paper`)
- provider
- published_at
- trust_score (float, default `0.5`, range `0.0`–`1.0`)

## Insight

Represents a fully structured AI-generated article, including the reasoning, usage examples, and multi-model debate perspectives produced by the agent pipeline.

Fields:

- id
- title
- summary
- reasoning
- examples (JSON string — list of strings)
- perspectives (JSON string — dict of model→text)
- week
- year
- status (`draft`, `published`)
- digest_id (FK → WeeklyDigest)

## WeeklyDigest

Groups a set of insights published within the same ISO calendar week so users can browse the platform chronologically.

Fields:

- id
- year
- week

## Tag

Categorises insights by topic so users can filter and navigate content by subject area (e.g. "LLM models", "AI agents").

Fields:

- id
- name

## Player

Represents a major AI ecosystem company (e.g. OpenAI, Anthropic) so insights and debate perspectives can be browsed through a company lens.

Fields:

- id
- name
- description

## AgentRun

Records the inputs, outputs, and success/failure of every individual agent execution, providing a full audit trail for each insight generated.

Fields:

- id
- agent_name
- model
- output (JSON string)
- success
- error
- created_at
- insight_id (FK → Insight)

---

# Step 5 — Schemas

Create simple Pydantic schemas in:

`app/schemas.py`

Example:

```python
from pydantic import BaseModel

class InsightOut(BaseModel):
    id: int
    title: str
    summary: str
    week: int
    year: int
```

Use schemas for API responses.

Do not over-design them early.

---

# Step 6 — Services

Put business logic into:

`app/services.py`

Example functions:

- `list_insights()`
- `get_insight()`
- `list_digest()`

Routes should stay thin.

---

# Step 7 — Core Endpoints

Implement these first:

- `GET /health`
- `GET /insights`
- `GET /insights/{id}`
- `GET /digest/{year}/{week}`

This is enough to unblock frontend work.

Avoid complex filters at the beginning.

---

# Step 8 — Create Sample Data

Add a seed script to populate the database for local development.

Seed script location:

```text
scripts/seed.py
```

Run it with:

```bash
uv run python scripts/seed.py
```

Seed should include:

- a few published insights
- one weekly digest
- a few sources (with `trust_score` set)

If the database is already seeded the script should skip safely.

---

# Step 9 — Agent Pipeline

Agent pipeline lives in `app/agents/`.

Implemented agents (supervisor pattern via `orchestrator.py`):

- `trend_extraction.py` — extracts title + summary
- `reasoning.py` — explains why the development matters
- `example_generator.py` — generates 3 real-world usage examples
- `debate_generator.py` — generates 4 AI ecosystem perspectives
- `review.py` — quality gate (structural checks + optional LLM review)

LLM client in `app/agents/llm.py` supports:

- `openai`, `anthropic`, `gemini`, `grok` — configured via `LLM_PROVIDER` + `LLM_MODEL` in `.env`
- Falls back to **stub output** automatically when no API key is set — pipeline always runs locally

Pipeline is triggered via `POST /generate-insight`.  
Every agent run is logged to the `agent_runs` table.

---

# Step 10 — Keep Heavy Work Simple

At the beginning, do NOT add Celery or Redis.

Use one of these:

- manual trigger endpoint
- direct service call
- FastAPI background task if really needed

Only add real queue/workers later.

---

# Step 11 — Suggested Next Evolution

When the backend starts growing, add in this order:

1. Alembic
2. review tables
3. model perspectives
4. filters
5. Redis + Celery
6. Docker

This keeps complexity under control.

---

# Step 12 — Definition of Done

Backend setup is complete when:

- API runs locally (`uv run uvicorn app.main:app --reload`)
- Database connects (SQLite default; PostgreSQL via `DATABASE_URL`)
- All models exist: `User`, `Source`, `Insight`, `WeeklyDigest`, `AgentRun`
- Tables are created on startup
- `GET /health` returns `{"status": "ok"}`
- `GET /insights` returns published insights
- `GET /insights/{id}` returns single insight or 404
- `GET /digest/{year}/{week}` returns digest with insights or 404
- `POST /generate-insight` runs agent pipeline and returns draft insight
- Seed data loads via `uv run python scripts/seed.py`
- Agent pipeline runs in stub mode without an API key
- All tests pass: `uv run pytest`

---

# Final Rule

Always prefer:

- simpler code
- fewer files
- fewer dependencies
- direct logic first

Do not over-engineer the backend in MVP.
