
# AI Hub – Development Tickets (~92) 
Derived from Product Epics

This document converts the feature epics into **concrete development tickets** suitable for Jira, Linear, or GitHub Issues.

Tickets are grouped by **Epic** matching `ai_hub_features_epics.md`.

The list is optimized for **fast AI-assisted development** and incremental delivery.

---

# Epic 1 — Core Platform (Backend)

### Ticket 1
Create FastAPI project skeleton

### Ticket 2
Configure database connection (SQLite default; PostgreSQL-ready via `DATABASE_URL`)

### Ticket 3
Implement SQLAlchemy base models

### Ticket 3a
Create `User` database model with `role` field (`reader`, `subscriber`, `admin`) — represents a registered user and controls what actions they are allowed to perform.

### Ticket 4
Create `Source` database model with `trust_score` field (`0.0`–`1.0`, default `0.5`) — represents an external URL collected as raw signal input for the agent pipeline.

### Ticket 5
Create `Insight` database model — represents a fully structured AI-generated article including reasoning, examples, and multi-model debate perspectives.

### Ticket 6
Create `WeeklyDigest` database model — groups insights by ISO calendar week so users can browse the platform chronologically.

### Ticket 6a
Create `AgentRun` database model (agent name, model, output, success, error, insight FK) — records every agent execution to provide a full audit trail for each generated insight.

### Ticket 7
Create `Tag` model — categorises insights by topic so users can filter and navigate content by subject area.

### Ticket 8
Create `Player` model — represents a major AI ecosystem company (e.g. OpenAI, Anthropic) so insights can be browsed and filtered through a company lens.

### Ticket 9
Implement `/health` endpoint

### Ticket 10
Implement `/insights` endpoint

### Ticket 11
Implement `/insights/{id}` endpoint

### Ticket 12
Implement `/digest/{year}/{week}` endpoint

### Ticket 13
Implement `/tags` endpoint

### Ticket 14
Implement `/players` endpoint

---

# Epic 2 — Backend Services

### Ticket 15
Create insights service layer

### Ticket 16
Implement insight creation logic

### Ticket 17
Implement insight retrieval logic

### Ticket 18
Implement digest generation service

### Ticket 19
Implement tagging service

### Ticket 20
Implement player association service

---

# Epic 3 — AI Agent Pipeline

### Ticket 21
Create `agents/` project folder

### Ticket 22
Create trend extraction agent

### Ticket 23
Create reasoning agent

### Ticket 24
Create example generation agent

### Ticket 25
Create real-life usage agent

### Ticket 26
Create debate generation agent

### Ticket 27
Create player lens agent

### Ticket 28
Create review agent

### Ticket 29
Create consensus agent

### Ticket 30
Implement agent orchestration service

---

# Epic 4 — Source Intelligence

### Ticket 31
Implement source ingestion model

### Ticket 32
Create endpoint to add sources

### Ticket 33
Implement source deduplication

### Ticket 34
Create GitHub source collector _(superseded by Ticket 83 — preserved for traceability)_

### Ticket 35
Create official pages source collector

### Ticket 36
Create social media signal collector

### Ticket 36a
Seed trusted source registry with initial domains (`ycombinator.com`, `openai.com`, `anthropic.com`, `ai.google/`)

### Ticket 36b
Apply `trust_score` weighting in digest ranking algorithm

### Ticket 82
Create trusted source registry model + admin CRUD (seed with `ycombinator.com`)

### Ticket 83
Implement GitHub-first source ingestion (repo, owner, release/README metadata) — supersedes Ticket 34

---

# Epic 5 — Weekly Digest System

### Ticket 37
Implement digest ranking algorithm

### Ticket 38
Generate weekly digest automatically

### Ticket 39
Store digest summaries

### Ticket 40
Expose digest via API

---

# Epic 6 — Frontend Foundation

### Ticket 41
Create SvelteKit project

### Ticket 42
Add Tailwind CSS

### Ticket 43
Create base layout

### Ticket 44
Create top navigation component

### Ticket 45
Create `InsightCard` component

---

# Epic 7 — Frontend Pages

### Ticket 46
Create homepage

### Ticket 47
Create insight detail page

### Ticket 48
Create weekly digest page

### Ticket 49
Create tag page

### Ticket 50
Create player page

---

# Epic 8 — Frontend Data Layer

### Ticket 51
Create API client wrapper

### Ticket 52
Implement insights fetcher

### Ticket 53
Implement digest fetcher

### Ticket 54
Implement tag fetcher

### Ticket 55
Implement player fetcher

---

# Epic 9 — Admin & Monitoring

### Ticket 56
Create admin insight review endpoint

### Ticket 57
Create agent job monitor endpoint

### Ticket 58
Create admin dashboard page

### Ticket 59
Display agent execution logs

### Ticket 60
Create manual "generate insight" trigger endpoint (`POST /generate-insight` — already implemented)

---

# Epic 9b — Data & API Layer (New Endpoints)

### Ticket 60a
Add `POST /subscribe` and `DELETE /subscribe` email subscription endpoints

### Ticket 60b
Add `POST /insights/{id}/debate` and `GET /insights/{id}/debate` subscriber debate session endpoints

### Ticket 60c
Add `GET /users/me/billing` billing summary endpoint

### Ticket 60d
Add `GET /articles/drafts` and `POST /articles/drafts` subscriber article draft endpoints

### Ticket 60e
Add `POST /articles/drafts/{id}/feedback` AI feedback on subscriber draft endpoint

---

# Epic 10 — Access & Engagement

### Ticket 61
Enforce `User` model role gates on endpoints (`reader`, `subscriber`, `admin`) — depends on Ticket 3a

### Ticket 62
Implement role-aware auth middleware/dependencies

### Ticket 63
Add smart/dumb generation mode config (`LLM tier` profile)

### Ticket 64
Allow mode selection in manual insight generation flow

### Ticket 65
Create admin endpoint to edit article content

### Ticket 66
Create admin UI form for editing insight content

### Ticket 67
Create comments model and migration

### Ticket 68
Implement comments API + insight comments UI (subscriber/admin write)

---

# Epic 11 — Subscription, Discovery & Subscriber Intelligence

### Ticket 69
Create email subscription model and subscribe/unsubscribe endpoints

### Ticket 70
Implement weekly digest email delivery job

### Ticket 71
Add article search support in `/insights` (title/summary/text)

### Ticket 72
Add combined filters in `/insights` (`model`, `topic`, `timeframe`, `content_type`)

### Ticket 73
Create frontend search bar + filter panel with URL-synced state

### Ticket 74
Create subscriber article draft model + submission endpoint

### Ticket 75
Create admin moderation endpoint for subscriber articles (approve/reject)

### Ticket 76
Implement subscriber AI debate sessions (multi-turn) for insights

### Ticket 77
Create AI feedback endpoint for subscriber article drafts

---

# Epic 12 — Usage & Billing

### Ticket 78
Track per-user AI usage metrics (requests, tokens, model tier, topic sessions)

### Ticket 79
Calculate periodic expense reports per user and per feature

### Ticket 80
Implement subscriber charging logic (quota + overage pricing)

### Ticket 81
Create billing summary endpoint + frontend billing page

---

# Suggested Development Order

Recommended implementation phases:

Phase 1
- Tickets 1–14 + Tickets 3a, 6a (core backend API including `User` and `AgentRun` models)

Phase 2
- Tickets 41–50 (frontend UI)

Phase 3
- Tickets 21–30 (AI agents)

Phase 4
- Tickets 31–40 + Tickets 36a, 36b, 82, 83 (source ingestion + trust registry + GitHub lane)

Phase 5
- Tickets 51–60 + Tickets 60a–60e (admin + monitoring + new API endpoints)

Phase 6
- Tickets 61–68 (roles + modes + editing + comments)

Phase 7
- Tickets 69–77 (subscription + search + filters + subscriber intelligence)

Phase 8
- Tickets 78–81 (usage metering + billing)


---

# Notes

These tickets are intentionally small so that:
- AI agents can implement them safely
- development progress is visible quickly
- features can be tested incrementally
