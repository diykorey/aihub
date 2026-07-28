# AIHub Documentation

Documentation for **AIHub**, an AI-driven intelligence magazine about AI. Start with the
[Overview](overview.md) for the big picture, then dive into the section you need.

> This directory mirrors the project's [GitHub wiki](../wiki/) — the pages here are the
> in-repo source of truth; the `wiki/` folder holds the wiki-sync copies.

## Start here

| Article | What it covers |
|---------|----------------|
| [Overview](overview.md) | What AIHub is, architecture, tech stack, and the phase roadmap |
| [Glossary](glossary.md) | Definitions of domain, agent-pipeline, and tooling terms |

## Guides

Practical setup and how-to articles.

| Article | What it covers |
|---------|----------------|
| [Backend Setup](guides/backend-setup.md) | Backend MVP setup guide |
| [Frontend Setup](guides/frontend-setup.md) | Frontend MVP setup guide (planned stack) |

## Phases

Implementation records, one per delivered phase.

| Article | Status |
|---------|--------|
| [Phase 1 — Backend Core](phases/phase-1-backend-core.md) | ✅ Complete |

## Product

Product intent and planning material.

| Article | What it covers |
|---------|----------------|
| [Mindmap](product/mindmap.md) | Product intent / mindmap |

## Backlog

Story backlog with acceptance criteria — the source of scope and sequencing.

| Article | What it covers |
|---------|----------------|
| [Epics](backlog/epics.md) | Product features grouped by epic |
| [Dev Tickets](backlog/dev-tickets.md) | ~92 concrete development tickets + suggested order |
| [Startup Backlog](backlog/startup-backlog.md) | User stories, acceptance criteria, estimates, dependencies |

## Directory map

```
docs/
├── README.md              This index
├── overview.md            Project overview
├── glossary.md            Term definitions
├── guides/                Setup & how-to guides
│   ├── backend-setup.md
│   └── frontend-setup.md
├── phases/                Per-phase implementation records
│   └── phase-1-backend-core.md
├── product/               Product intent
│   └── mindmap.md
└── backlog/               Stories, epics, tickets
    ├── epics.md
    ├── dev-tickets.md
    └── startup-backlog.md
```
