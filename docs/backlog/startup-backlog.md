
# AI Hub – Startup-Style Development Backlog
User Stories • Acceptance Criteria • Estimates • Dependencies • AI Implementation Prompts

This backlog is optimized for **AI-assisted development**.  
Stories are intentionally **small, clear, and implementable by coding agents**.

Estimates use **Story Points (SP)** roughly aligned with startup teams:
1 SP ≈ very small task
2 SP ≈ small
3 SP ≈ medium
5 SP ≈ complex

---

# EPIC 1 — Backend Foundation

## Story 1 — Create FastAPI Project
User Story:
As a developer, I want a minimal FastAPI backend so that the platform can expose APIs.

Acceptance Criteria:
- FastAPI project created
- `/health` endpoint exists
- Server runs locally

Estimate:
1 SP

Dependencies:
None

AI Prompt:
Create a minimal FastAPI application with a `/health` endpoint returning `{status:"ok"}` and runnable via `uvicorn`.

---

## Story 2 — Setup PostgreSQL Connection
User Story:
As a developer, I want the backend connected to PostgreSQL so that data can be stored.

Acceptance Criteria:
- SQLAlchemy configured
- DB connection works
- Session factory created

Estimate:
2 SP

Dependencies:
Story 1

AI Prompt:
Implement a database module using SQLAlchemy with PostgreSQL providing `engine`, `SessionLocal`, and `Base`.

---

## Story 3 — Create Core Models
User Story:
As a developer, I want core database models so that insights and sources can be stored.

Acceptance Criteria:
Models exist:
- `Source` — represents an external URL collected as a raw signal for insight generation.
- `Insight` — represents a fully structured AI-generated article produced by the agent pipeline.
- `WeeklyDigest` — groups insights by ISO calendar week for chronological browsing.
- `AgentRun` — records every agent execution for auditing and debugging.
- `User` — represents a registered user with a role controlling platform access.
- `Tag` — categorises insights by topic for filtering and navigation.
- `Player` — represents a major AI ecosystem company for the company-lens browsing experience.

Estimate:
3 SP

Dependencies:
Story 2

AI Prompt:
Create SQLAlchemy models for Source, Insight, and WeeklyDigest with basic fields.

---

## Story 4 — Implement Insights API
User Story:
As a user, I want to view insights so that I can read AI intelligence.

Acceptance Criteria:
Endpoint:
`GET /insights`

Returns list of insights.

Estimate:
2 SP

Dependencies:
Story 3

AI Prompt:
Create `/insights` endpoint returning all Insight records.

---

## Story 5 — Implement Insight Detail API
User Story:
As a user, I want to open an insight page so that I can see detailed analysis.

Acceptance Criteria:
Endpoint:
`GET /insights/{id}`

Estimate:
2 SP

Dependencies:
Story 4

AI Prompt:
Create endpoint returning a single Insight by ID.

---

# EPIC 2 — Frontend Foundation

## Story 6 — Create SvelteKit Project
User Story:
As a developer, I want a frontend project so that users can access the platform.

Acceptance Criteria:
- SvelteKit project created
- dev server runs

Estimate:
1 SP

Dependencies:
None

AI Prompt:
Create SvelteKit project using TypeScript and ensure it runs with `pnpm dev`.

---

## Story 7 — Add Tailwind
User Story:
As a developer, I want Tailwind CSS so UI can be built quickly.

Acceptance Criteria:
- Tailwind installed
- styles applied

Estimate:
1 SP

Dependencies:
Story 6

AI Prompt:
Install and configure Tailwind CSS in the SvelteKit project.

---

## Story 8 — Create Base Layout
User Story:
As a user, I want consistent navigation so that I can explore the site.

Acceptance Criteria:
Layout includes header and navigation.

Estimate:
2 SP

Dependencies:
Story 7

AI Prompt:
Create base layout component with header and navigation.

---

# EPIC 3 — Insight UI

## Story 9 — Insight Card Component
User Story:
As a user, I want to see insights summarized so that I can quickly browse.

Acceptance Criteria:
Card displays title, summary, tags.

Estimate:
2 SP

Dependencies:
Story 8

AI Prompt:
Create InsightCard component displaying insight preview.

---

## Story 10 — Insight List Page
User Story:
As a user, I want to browse insights so that I can explore AI trends.

Acceptance Criteria:
Homepage displays insight cards.

Estimate:
2 SP

Dependencies:
Story 9

AI Prompt:
Create homepage that fetches `/insights` and renders InsightCard components.

---

## Story 11 — Insight Detail Page
User Story:
As a user, I want to read a full insight article.

Acceptance Criteria:
Page `/insights/[id]` displays reasoning, examples, sources.

Estimate:
3 SP

Dependencies:
Story 10

AI Prompt:
Create dynamic SvelteKit page `/insights/[id]` fetching insight from API.

---

# EPIC 4 — AI Insight Generation

## Story 12 — Trend Extraction Agent
User Story:
As the system, I want to detect AI developments from sources.

Acceptance Criteria:
Agent outputs title and summary.

Estimate:
3 SP

Dependencies:
Story 3

AI Prompt:
Create LLM function extracting a trend title and summary from provided text.

---

## Story 13 — Reasoning Agent
User Story:
As a reader, I want to understand why a development matters.

Acceptance Criteria:
Agent outputs reasoning text.

Estimate:
3 SP

Dependencies:
Story 12

AI Prompt:
Generate reasoning explaining the importance of an AI development.

---

## Story 14 — Example Generator Agent
User Story:
As a user, I want examples so I can apply AI trends.

Acceptance Criteria:
Agent returns 2–3 practical examples.

Estimate:
3 SP

Dependencies:
Story 13

AI Prompt:
Generate real-world examples applying the AI development.

---

# EPIC 5 — Weekly Digest

## Story 15 — Weekly Digest API
User Story:
As a user, I want AI developments grouped weekly.

Acceptance Criteria:
Endpoint `/digest/{year}/{week}` returns insights.

Estimate:
3 SP

Dependencies:
Story 4

AI Prompt:
Create service grouping insights by week.

---

## Story 16 — Weekly Digest Page
User Story:
As a user, I want to browse weekly summaries.

Acceptance Criteria:
Page `/digest/[year]/[week]` displays insights.

Estimate:
3 SP

Dependencies:
Story 15

AI Prompt:
Create SvelteKit page displaying weekly digest insights.

---

# EPIC 6 — AI Debate System

## Story 17 — Model Perspectives
User Story:
As a reader, I want to see different AI interpretations.

Acceptance Criteria:
Perspectives generated for GPT, Gemini, Grok.

Estimate:
3 SP

Dependencies:
Story 13

AI Prompt:
Generate multiple AI model perspectives on a trend.

---

## Story 18 — Debate UI
User Story:
As a reader, I want to compare AI opinions visually.

Acceptance Criteria:
UI component showing perspectives side-by-side.

Estimate:
3 SP

Dependencies:
Story 17

AI Prompt:
Create DebateBlock component showing multiple perspectives.

---

# EPIC 7 — Tagging

## Story 19 — Tag Model
User Story:
As a user, I want insights categorized.

Acceptance Criteria:
Tag table exists and linked to Insight.

Estimate:
2 SP

Dependencies:
Story 3

AI Prompt:
Create Tag model with many-to-many relation to Insight.

---

## Story 20 — Tag Page
User Story:
As a user, I want to explore insights by topic.

Acceptance Criteria:
Route `/tags/[tag]` filters insights.

Estimate:
2 SP

Dependencies:
Story 19

AI Prompt:
Create page displaying insights filtered by tag.

---

# EPIC 8 — Admin Tools

## Story 21 — Admin Insight Review
User Story:
As an admin, I want to review AI-generated insights.

Acceptance Criteria:
Admin page listing insights.

Estimate:
3 SP

Dependencies:
Story 10

AI Prompt:
Create simple admin page listing insights and status.

---

## Story 22 — Manual Insight Generation
User Story:
As an admin, I want to trigger AI insight generation.

Acceptance Criteria:
Endpoint `POST /generate-insight`.

Estimate:
3 SP

Dependencies:
Story 12

AI Prompt:
Create endpoint running trend extraction and reasoning agents.

---

# EPIC 9 — Monitoring

## Story 23 — Agent Logs
User Story:
As a developer, I want to inspect AI runs.

Acceptance Criteria:
Agent run data stored in DB.

Estimate:
3 SP

Dependencies:
Story 12

AI Prompt:
Create `agent_runs` table storing model, prompt, and output.

---

# EPIC 10 — Future Intelligence

## Story 24 — Trend Forecasting
User Story:
As a reader, I want predictions about AI developments.

Acceptance Criteria:
Forecast field added to insights.

Estimate:
5 SP

Dependencies:
Story 13

AI Prompt:
Generate forecast describing potential impact of AI trend.

---

# EPIC 11 — Access & Engagement

## Story 25 — Smart/Dumb Generation Mode
User Story:
As an admin, I want to switch between smart and dumb generation mode so that I can balance quality and cost.

Acceptance Criteria:
- System supports `smart` and `dumb` generation modes.
- Mode is passed to insight generation flow.
- Active mode is stored with generated insight metadata.

Estimate:
3 SP

Dependencies:
Story 22

AI Prompt:
Add generation mode support (`smart`/`dumb`) to pipeline entrypoint and persist selected mode on generated insight metadata.

---

## Story 26 — Role-Based Access (Reader / Subscriber / Admin)
User Story:
As a product owner, I want role-based permissions so users get the right capabilities.

Acceptance Criteria:
- Roles exist: reader, subscriber, admin.
- Reader can view insights and comments.
- Subscriber can view insights and create comments.
- Admin can manage insights, comments, and generation settings.

Estimate:
5 SP

Dependencies:
Story 4

AI Prompt:
Introduce role model and authorization checks for reader/subscriber/admin permissions on content, comments, and admin endpoints.

---

## Story 27 — Admin Article Editing
User Story:
As an admin, I want to edit generated articles so I can improve quality before publishing.

Acceptance Criteria:
- Admin can update title, summary, reasoning, examples, and perspectives.
- Edit endpoint validates payload and stores last-updated timestamp.
- Non-admin roles cannot edit articles.

Estimate:
3 SP

Dependencies:
Story 21

AI Prompt:
Create admin-only insight update endpoint and UI form to edit generated article fields.

---

## Story 28 — Insight Comments for Subscriber/Admin
User Story:
As a subscriber or admin, I want to leave comments on insights so that discussion can happen around each article.

Acceptance Criteria:
- Comments can be listed per insight.
- Subscriber and admin can create comments.
- Reader cannot create comments.

Estimate:
3 SP

Dependencies:
Story 26

AI Prompt:
Add comments model, comments API, and insight detail UI block with role-checked comment submission.

---

## Story 29 — Email Subscription
User Story:
As a reader, I want to subscribe by email so I can receive weekly AI Hub updates.

Acceptance Criteria:
- User can subscribe with email.
- User can unsubscribe.
- Weekly digest email includes links to latest insights.

Estimate:
3 SP

Dependencies:
Story 15

AI Prompt:
Create email subscription flow with subscribe/unsubscribe endpoints and weekly digest email job.

---

## Story 30 — Article Search
User Story:
As a user, I want to search articles so I can quickly find relevant insights.

Acceptance Criteria:
- Search supports title and summary.
- Results are sorted by relevance and recency.
- Empty query returns latest insights.

Estimate:
3 SP

Dependencies:
Story 4

AI Prompt:
Add query search to insights listing and frontend search UI with debounced input.

---

## Story 31 — Advanced Filters
User Story:
As a user, I want to filter insights by model, topic, timeframe, and content type.

Acceptance Criteria:
- Filters supported: model, topic/tag, timeframe, content type.
- Filters can be combined.
- Filter state is reflected in URL params.

Estimate:
3 SP

Dependencies:
Story 30

AI Prompt:
Extend insights API and list UI to support combined filters for model/topic/timeframe/content_type.

---

## Story 32 — Subscriber Article Submission
User Story:
As a subscriber, I want to submit my own article so that it can be published after review.

Acceptance Criteria:
- Subscriber can create draft article.
- Admin can approve or reject submission.
- Approved article appears in insights feed.

Estimate:
5 SP

Dependencies:
Story 26

AI Prompt:
Add subscriber article submission flow with moderation states: draft, pending_review, approved, rejected.

---

## Story 33 — Subscriber Debate with AI
User Story:
As a subscriber, I want to debate with AI around an insight so I can challenge and refine my understanding.

Acceptance Criteria:
- Subscriber can open a debate session from insight detail page.
- Multi-turn Q&A is supported per session.
- Debate history is saved per user.

Estimate:
5 SP

Dependencies:
Story 26

AI Prompt:
Implement subscriber-only multi-turn AI debate sessions linked to insight and user.

---

## Story 34 — AI Feedback on Subscriber Article
User Story:
As a subscriber, I want AI feedback on my draft article so I can improve it before submission.

Acceptance Criteria:
- Subscriber can request AI feedback on draft article.
- Feedback covers structure, clarity, and reasoning quality.
- Feedback is stored and viewable in draft history.

Estimate:
3 SP

Dependencies:
Story 32

AI Prompt:
Add AI feedback endpoint for subscriber drafts and persist feedback records with timestamps.

---

# EPIC 12 — Usage & Billing

## Story 35 — Usage Costing and Subscriber Charges
User Story:
As a product owner, I want to calculate AI expenses and charge users based on consumed features.

Acceptance Criteria:
- Usage is metered per subscriber (requests/tokens/model tier/topic sessions).
- Monthly cost report is generated per user.
- Charging logic applies included quota + overage.

Estimate:
5 SP

Dependencies:
Story 33

AI Prompt:
Implement usage metering and monthly billing calculation for subscribers based on AI feature consumption.

---

# EPIC 13 — Source Trust & GitHub Signals

## Story 36 — Trusted Source Registry
User Story:
As an admin, I want a list of primary/trusted sources so that generated insights prioritize reliable inputs.

Acceptance Criteria:
- Trusted source registry supports domain-level entries.
- Initial trusted list includes `ycombinator.com`.
- Source ingestion marks whether a source is trusted.

Estimate:
3 SP

Dependencies:
Story 3

AI Prompt:
Add trusted source registry support and mark sources as trusted when provider domain matches configured list.

---

## Story 37 — GitHub as a Source
User Story:
As a user, I want GitHub treated as a source so that insights include code-native AI signals.

Acceptance Criteria:
- GitHub is supported as a first-class `source_type`.
- Ingestion captures repository URL, owner, and repo name.
- GitHub-sourced insights are visible in source metadata.

Estimate:
3 SP

Dependencies:
Story 36

AI Prompt:
Implement GitHub source ingestion as a first-class lane and persist repository metadata on collected sources.

---

# Recommended Implementation Order

Phase 1
Stories 1–5 (Backend)

Phase 2
Stories 6–11 (Frontend)

Phase 3
Stories 12–14 (Agents)

Phase 4
Stories 15–16 (Digest)

Phase 5
Stories 17–20 (Debate + tags)

Phase 6
Stories 21–23 (Admin + monitoring) + Stories 36–37 (trusted sources + GitHub source lane)

Phase 7
Story 24 (Forecasting)

Phase 8
Stories 25–28 (Modes + roles + editing + comments)

Phase 9
Stories 29–34 (subscription + search + filters + subscriber content)

Phase 10
Story 35 (usage + billing)


