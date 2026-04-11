# AI Hub – Product Features (Grouped by Epics)

This document defines the **feature set for AI Hub**, organized into **Epics**.  
The structure is optimized for **AI-assisted development** and can be used to generate tickets in Jira/Linear/GitHub Issues.

Each Epic contains a list of **Features** that can later be converted into **User Stories or Tasks**.

---

# Epic 1 — Core Content Platform

Purpose: provide the core functionality of the AI Hub magazine.

## Features

### Insight Articles
Display AI-generated insights explaining AI developments.

Capabilities:
- show insight title
- show summary
- show reasoning
- show tags
- show related AI players

---

### Insight Detail Page

Dedicated page for each insight.

Sections:
- summary
- reasoning
- real-life usage
- examples
- sources
- AI debate
- major player lens

---

### Weekly Digest

Group insights by week.

Capabilities:
- view insights for a specific week
- chronological navigation
- highlight most important insights

Route example:

```
/digest/{year}/{week}
```

---

### Home Page

Entry point to platform.

Content:
- latest insights
- latest weekly digest
- trending topics

---

# Epic 2 — Insight Intelligence

Purpose: transform raw AI news into structured intelligence.

## Features

### AI Reasoning

Explain **why a development matters**.

Examples:
- technology implications
- ecosystem impact
- adoption trends

---

### Real-life Usage

Show how developments can be applied in practice.

Categories:
- solo entrepreneur
- developers
- SMB
- enterprise

---

### Example Generation

Provide practical examples.

Examples:
- automation workflow
- AI product usage
- development workflow improvement

---

### Source Tracking

Attach sources used to generate insight.

Sources may include:

- official AI company pages
- research papers
- GitHub repositories
- social media posts

Primary/trusted source examples:

- https://www.ycombinator.com/
- https://openai.com/
- https://www.anthropic.com/
- https://ai.google/

Trusted-source policy (scoring + ranking use):

- Each source is assigned a `trust_score` from `0.0` to `1.0`.
- Default score for new/unclassified sources: `0.5`.
- Trusted domains start at `0.8` to `1.0`; unknown or low-confidence domains are `0.0` to `0.4`.
- Insight candidate ranking uses `trust_score` as a multiplier/weight so higher-trust sources are prioritized when signals conflict.
- Final ranking blends trust with existing factors (recency, novelty, ecosystem impact), so trust boosts quality but does not fully override relevance.

---

# Epic 3 — AI Debate System

Purpose: show **different AI perspectives** on the same topic.

## Features

### Model Perspectives

Display interpretation from different AI models.

Examples:
- ChatGPT perspective
- Gemini perspective
- Grok perspective

---

### Pros and Cons

Highlight disagreements between models.

Sections:
- pros
- risks
- disagreements

---

### Debate View

Visual interface showing differences between models.

User can switch between:
- model opinions
- combined summary

---

# Epic 4 — AI Player Ecosystem

Purpose: help users understand how trends relate to major AI companies.

## Features

### Major Player Lens

Explain relevance to major players.

Players:

- OpenAI
- Gemini
- Anthropic
- Grok

Example questions:
- which company benefits
- which ecosystem this affects

---

### Player Pages

Dedicated page per AI player.

Route example:

```
/players/{player}
```

Content:
- insights related to that player
- ecosystem developments

---

# Epic 5 — Tagging and Navigation

Purpose: make content discoverable.

## Features

### Tag System

Assign tags to insights.

Example tags:

- AI agents
- LLM models
- AI coding
- multimodal AI
- enterprise AI

---

### Tag Pages

View insights grouped by tag.

Route example:

```
/tags/{tag}
```

---

### Filters

Filter insights by:

- tag
- AI player
- timeframe
- model
- content type

---

### Article Search

Find insights quickly with keyword search.

Capabilities:

- search by title
- search by summary
- search by full article text

---

# Epic 6 — Agent Intelligence Pipeline

Purpose: automate content creation using AI agents.

## Features

### Source Collection

Collect signals from:

- AI company announcements
- research releases
- GitHub projects (first-class source lane)
- social media

GitHub source scope:

- repositories
- release notes
- project READMEs

---

### Trend Extraction

Identify trends from collected signals.

Output:

- trend title
- summary
- category

---

### Insight Generation

Generate structured insight article.

Sections produced:

- summary
- reasoning
- examples
- usage

---

### Agent Review

Insights reviewed by additional agents to ensure quality.

Review checks:

- hallucinations
- missing evidence
- unclear reasoning

---

### Consensus Generation

Final agent synthesizes review results and produces final article.

---

# Epic 7 — Weekly Intelligence Digest

Purpose: summarize developments over time.

## Features

### Digest Generation

Automatically generate weekly digest.

Includes:

- top insights
- major trends
- notable debates

---

### Digest Ranking

Rank insights by:

- importance
- novelty
- ecosystem impact

---

### Archive

Access historical digests.

Example:

```
/digest/2026/12
```

---

# Epic 8 — Admin & Operations

Purpose: manage system operations.

## Features

### Insight Management

Admin can:

- review generated insights
- publish/unpublish insights
- edit metadata
- edit article content (title, summary, reasoning, examples, debate blocks)

---

### Role-Based Access

System supports three roles:

- reader (read-only access)
- subscriber (read + comment)
- admin (full editorial and operations access)

Compact permissions matrix (API + UI constraints):

| Capability | Reader | Subscriber | Admin |
| --- | --- | --- | --- |
| View insights/digests/tags/players/search/filter | Yes | Yes | Yes |
| Create comments (`POST /insights/{id}/comments`) | No | Yes | Yes |
| Submit own article draft | No | Yes | Yes |
| Start debate-with-AI session | No | Yes | Yes |
| Request AI feedback on own draft | No | Yes | Yes |
| Edit/publish insight articles | No | No | Yes |
| Manage sources, agent jobs, and generation mode | No | No | Yes |
| View own usage/billing summary | No | Yes | Yes |

---

### Model Quality Mode

Switch generation behavior based on AI model level.

Modes:

- dumb mode (lighter/cheaper model profile)
- smart mode (higher-quality model profile)

Usage:

- generation endpoints can select mode explicitly
- default mode can be configured per environment

---

### Source Monitoring

View collected sources.

Capabilities:

- inspect raw sources
- identify duplicates

---

### Agent Job Monitor

Display running and completed agent jobs.

Information:

- job status
- execution time
- errors

---

# Epic 9 — Data & API Layer

Purpose: expose backend data to frontend.

## Features

### Insights API

Endpoints:

```
GET /insights
GET /insights/{id}
```

---

### Digest API

Endpoints:

```
GET /digest/{year}/{week}
```

---

### Tags API

Endpoints:

```
GET /tags
```

---

### Players API

Endpoints:

```
GET /players
```

---

### Comments API

Endpoints:

```
GET /insights/{id}/comments
POST /insights/{id}/comments
```

Access:

- subscriber, admin: create comments
- reader: view comments only

---

### Subscription API

Endpoints:

```
POST /subscribe
DELETE /subscribe
```

---

### Subscriber Debate API

Endpoints:

```
POST /insights/{id}/debate
GET /insights/{id}/debate
```

Access: subscriber, admin only

---

### Subscriber Articles API

Endpoints:

```
GET /articles/drafts
POST /articles/drafts
POST /articles/drafts/{id}/feedback
```

Access: subscriber, admin only

---

### Billing API

Endpoints:

```
GET /users/me/billing
```

Access: subscriber, admin only

---

# Epic 10 — Future Intelligence Layer (Post-MVP)

Purpose: move from explanation to prediction.

## Features

### Trend Forecasting

Predict impact of AI developments.

---

### Adoption Predictions

Predict:

- enterprise adoption
- developer usage
- startup opportunities

---

### Strategic Analysis

Long-form analysis of AI ecosystem shifts.

---

# Epic 11 — Access & Engagement

Purpose: support role-based collaboration and editorial workflows.

## Features

### Article Editing Workflow

Admin can edit and save article content after AI generation.

---

### Email Subscription

Users can subscribe by email to receive updates.

Capabilities:

- subscribe/unsubscribe
- weekly digest delivery
- product update announcements

---

### Subscriber Article Publishing

Subscribers can submit their own articles.

Capabilities:

- create draft article
- submit for moderation
- publish after admin approval

---

### Subscriber Debate with AI

Subscribers can open a debate session with AI around an insight.

Capabilities:

- ask follow-up questions
- receive model-backed arguments
- keep per-user debate history

---

### AI Feedback on Subscriber Articles

Subscribers can request AI feedback on their own article drafts.

Feedback scope:

- clarity and structure
- reasoning quality
- missing evidence or weak claims

---

### Insight Comments

Subscribers and admins can leave comments on insight detail pages.

Capabilities:

- threaded discussion (basic parent/child support)
- comment timestamp and author role
- moderation by admin

---

# Epic 12 — Usage & Billing

Purpose: track AI usage costs and charge users based on consumed resources.

## Features

### Usage Metering

Track per-user consumption.

Dimensions:

- AI requests
- token usage
- model tier (smart/dumb)
- topic/debate sessions used

---

### Expense Calculation

Calculate internal AI costs from usage data.

Outputs:

- per-user cost breakdown
- per-feature cost breakdown
- billing period totals

---

### User Charging

Charge subscribers based on consumed AI features.

Charging rules can include:

- included quota
- overage pricing
- topic/debate usage-based add-ons

---

# Final Notes

This feature structure allows:

- incremental development
- AI-assisted ticket generation
- clean separation of responsibilities
- MVP-first implementation

Suggested development order:

1. Core Content Platform
2. Insight Intelligence
3. Agent Pipeline
4. Weekly Digest
5. Tagging & Navigation
6. AI Debate
7. Player Ecosystem
8. Admin Tools
9. Access & Engagement
10. Subscription, Discovery & Subscriber Intelligence
11. Usage & Billing
12. Source Trust & GitHub Signals
