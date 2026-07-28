# Phase 1 — Core Platform (Backend)

Phase 1 delivers the **core backend API**: the FastAPI skeleton, database layer,
all persistence models, and the read/admin endpoints the frontend and agent pipeline
build on. It corresponds to **Epic 1 — Core Platform** in the backlog (Tickets 1–14
plus 3a and 6a).

**Status: ✅ Complete** — 42 passing tests, clean `ruff` / `ty` checks.

---

## Data models (`app/models.py`)

SQLAlchemy 2.0 ORM, using `mapped_column` and typed `Mapped[...]` annotations.

| Model | Table | Purpose | Ticket |
|-------|-------|---------|--------|
| `User` | `users` | Registered user; `role` gates permitted actions | 3a |
| `Source` | `sources` | External URL collected as raw signal input | 4 |
| `Tag` | `tags` | Topic categorisation for insights | 7 |
| `Player` | `players` | Major AI ecosystem company (e.g. OpenAI, Anthropic) | 8 |
| `Insight` | `insights` | Fully structured AI-generated article | 5 |
| `WeeklyDigest` | `weekly_digests` | Groups insights by ISO calendar week | 6 |
| `AgentRun` | `agent_runs` | Audit record of every agent execution | 6a |

Association tables `insight_tags` and `insight_players` provide many-to-many links
between insights and their tags / players.

### `User` model (Ticket 3a)

The most recent Phase 1 addition, which closed the epic.

| Field | Type | Notes |
|-------|------|-------|
| `id` | int | Primary key |
| `email` | str(320) | Unique, indexed |
| `name` | str(200) \| null | Optional display name |
| `role` | str(20) | `reader` \| `subscriber` \| `admin`, default `reader` |
| `is_active` | bool | Default `True` |
| `created_at` | datetime | UTC, set on insert |

- Roles are constrained at the database level by a `ck_users_role` CHECK constraint.
- The valid set is exported as `USER_ROLES = ("reader", "subscriber", "admin")` for
  reuse by the later role-gating epic (Tickets 61–62).
- Role semantics: **reader** browses published content; **subscriber** unlocks
  subscriber features; **admin** manages insights and runs the agent pipeline.

---

## REST endpoints

Defined in `app/main.py`, with logic delegated to `app/services.py`.

| Method | Path | Description | Ticket |
|--------|------|-------------|--------|
| `GET` | `/health` | Liveness probe | 9 |
| `GET` | `/insights` | Paginated list of published insights (newest first) | 10 |
| `GET` | `/insights/{id}` | Single insight by ID (404 if missing) | 11 |
| `GET` | `/digest/{year}/{week}` | Weekly digest with its insights | 12 |
| `GET` | `/tags` | All tags, alphabetical | 13 |
| `GET` | `/players` | All players, alphabetical | 14 |
| `POST` | `/generate-insight` | **Admin:** run the agent pipeline on source text → draft insight | 60 |
| `PATCH` | `/insights/{id}/status` | **Admin:** transition status (e.g. draft → published) | 56 |

`PATCH /insights/{id}/status` validates against `{draft, published, review_failed}` and,
when publishing, auto-assigns the insight to its ISO week's digest (creating the digest
if needed).

---

## Supporting infrastructure

- **App factory & lifespan** (`main.py`) — tables auto-created on startup via
  `Base.metadata.create_all` (no Alembic yet); permissive CORS for local dev.
- **DB layer** (`db.py`) — SQLAlchemy engine, `SessionLocal`, and a `get_db` FastAPI
  dependency that commits on success and rolls back on error.
- **Schemas** (`schemas.py`) — Pydantic response models (`InsightOut`, `DigestOut`,
  `TagOut`, `PlayerOut`, `AgentRunOut`) and request models
  (`GenerateInsightRequest`, `UpdateInsightStatusRequest`), all `from_attributes = True`.
- **Seed script** (`scripts/seed.py`) — populates SQLite with sample users (one per
  role), insights, a digest, and sources for local development.
- **CI & tooling** — GitHub Actions workflow, Docker + docker-compose, `ruff`, `ty`.

---

## Testing (`backend/tests/`)

- Endpoint tests use in-memory SQLite with `StaticPool` and FastAPI
  `app.dependency_overrides[get_db]`.
- A `reset_db` fixture recreates the schema and seeds minimal data before each test.
- Model tests exercise defaults, constraints (uniqueness, role CHECK), and associations.
- Agent tests run in stub mode (no API keys) via direct agent calls.

Current suite: **42 tests passing**, including model coverage for `User`, `Source`,
`Tag`, `Player`, and full endpoint coverage for insights, tags, and players.

---

## What Phase 1 intentionally leaves for later

- **Role enforcement** — the `User.role` field exists, but middleware/dependency gates
  that enforce it live in Phase 6 (Tickets 61–62).
- **Source ingestion endpoints & collectors** — Phase 4.
- **Frontend** — Phase 2.
- **Specialised agents** (real-life usage, player lens, consensus) — remainder of Phase 3.

See the [Overview](../overview.md) for the full phase roadmap and the
[Glossary](../glossary.md) for term definitions.
