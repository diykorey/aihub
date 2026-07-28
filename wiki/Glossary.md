# Glossary

Definitions of the domain, architecture, and tooling terms used across AIHub.

## Domain concepts

**Insight**
: A fully structured, AI-generated article — the core content unit of the magazine.
Includes a title, summary, reasoning, examples, and multi-model debate perspectives.
Persisted in the `insights` table with a `status` of `draft`, `published`, or
`review_failed`.

**Source**
: An external URL collected as a raw signal input for the agent pipeline (e.g. a blog
post, paper, or GitHub release). Carries a `trust_score` used to weight its reliability.

**Trust score**
: A `0.0`–`1.0` reliability weight on a `Source` (default `0.5`). Higher-trust sources
are intended to rank more strongly in digest ranking (weighting logic is later-phase).

**Weekly digest**
: A grouping of insights by ISO calendar week (`year` + `week`), letting users browse
content chronologically. One digest per year/week (enforced by a unique constraint).

**Tag**
: A topic label (e.g. "LLM", "Robotics") used to categorise and filter insights.
Many-to-many with insights via the `insight_tags` table.

**Player**
: A major AI ecosystem company (e.g. OpenAI, Anthropic) that insights can be browsed and
filtered by — a "company lens" on the content. Many-to-many with insights via
`insight_players`.

**User**
: A registered user of the platform. Its `role` controls what actions are permitted.

**Role**
: A `User`'s permission level — one of `reader` (browse published content),
`subscriber` (paying user; unlocks subscriber features), or `admin` (manage insights,
run the pipeline). Enforced as a set (`USER_ROLES`) and a DB CHECK constraint.

**Status (insight)**
: The lifecycle state of an insight: `draft` (freshly generated, unpublished),
`published` (live and listed), or `review_failed` (rejected by the review agent).

## Agent pipeline

**Agent**
: A single step in the insight-generation pipeline. Each subclasses `BaseAgent` and
implements `run(context: AgentContext) -> AgentResult`, mutating a shared context so
downstream agents build on prior results.

**Orchestrator**
: `InsightOrchestrator.run()` — coordinates the agents sequentially through a shared
`AgentContext`, logs every run to `agent_runs`, and persists the resulting insight.
Non-fatal agent failures are caught per-agent and don't stop the pipeline.

**AgentContext**
: A shared dataclass passed through the pipeline that agents read from and write to
in-place, carrying the accumulating insight data.

**AgentResult**
: The JSON-serialisable return value of an agent — includes a success flag and error
message. Every result is logged to the `agent_runs` table for auditing.

**AgentRun**
: A database record of a single agent execution (agent name, model, output, success,
error, duration, insight FK) — the audit trail for how an insight was generated.

**TrendExtractionAgent**
: Extracts a title and summary from the raw source text (pipeline step 1).

**ReasoningAgent**
: Writes the analysis of *why* the trend matters (step 2).

**ExampleGeneratorAgent**
: Generates practical use-case examples (step 3).

**DebateGeneratorAgent**
: Generates multiple AI-ecosystem perspectives / debate positions (step 4).

**ReviewAgent**
: Quality gate that runs structural checks plus an LLM review; determines whether the
insight is saved as `draft` or `review_failed` (step 5).

**Stub mode**
: Fallback behaviour when LLM credentials are missing — agents return canned stub
outputs so local dev and tests run without API keys.

## Architecture & tooling

**Service layer**
: `app/services.py` — the business-logic / query layer. Keeps route handlers thin;
routes call services, services touch models.

**Schema (Pydantic)**
: A request/response model in `app/schemas.py`. Response schemas use
`from_attributes = True` to map directly from ORM objects.

**`get_db` dependency**
: The FastAPI dependency (`Depends(get_db)`) that yields a database session, commits on
success, and rolls back on error.

**Lifespan**
: The FastAPI startup/shutdown hook in `main.py`; on startup it auto-creates all tables
via `Base.metadata.create_all`.

**LLM provider**
: A configured large-language-model backend (`openai`, `anthropic`, `gemini`, or `grok`),
selected via the `LLM_PROVIDER` env var and wrapped by `chat_complete()` in
`agents/llm.py`.

**`chat_complete()`**
: The provider-agnostic LLM wrapper. Lazily imports the relevant SDK per provider and
returns a stub marker string when credentials are absent.

**uv**
: The Python package/dependency manager used for the backend (`uv sync`, `uv run`).

**ruff**
: The linter and formatter (100-char line length, PEP 8).

**ty**
: The strict type checker run against `app/`.

**MVP**
: Minimum Viable Product — the initial scoped release defined by the backlog; post-MVP
items (forecasting, broader ops) are documented but do not block delivery.

**ISO week**
: The ISO-8601 calendar week numbering used to key weekly digests (`year` + `week`).

See **[[Home]]** for the project overview and **[[Phase 1 Backend Core|Phase-1-Backend-Core]]**
for the Phase 1 implementation record.
