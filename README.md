# AI Hub

AI-powered insight magazine platform that ingests source material, runs it through a multi-agent LLM pipeline, and produces structured weekly digests of AI industry developments.

## Repository structure

```
backend/    FastAPI backend — API, agent pipeline, data layer
docs/       Documentation — overview, guides, phases, glossary, backlog (start at docs/README.md)
wiki/       GitHub wiki mirror of docs/
```

Full documentation lives in [docs/](docs/README.md).

## Quick start

```bash
cd backend
uv sync --group dev
cp .env.example .env
uv run uvicorn app.main:app --reload
```

API available at http://localhost:8000 — see [backend/README.md](backend/README.md) for full documentation.

## Docker

```bash
cp backend/.env.example backend/.env
docker compose up --build
```

## How it works

Source text is submitted via `POST /generate-insight` and processed through a sequential agent pipeline:

1. **Trend Extraction** — identifies the key AI development (title + summary)
2. **Reasoning** — explains why the development matters
3. **Example Generator** — produces practical usage examples for different audiences
4. **Debate Generator** — generates perspectives from four AI ecosystem players (OpenAI, Google, Anthropic, xAI)
5. **Review** — quality gate that validates the output before persistence

Each agent supports multiple LLM providers (OpenAI, Anthropic, Gemini, Grok) and falls back to stub data when no API key is configured, so the full pipeline works locally without credentials.

Insights are created as drafts and can be published via `PATCH /insights/{id}/status`, which auto-assigns them to their weekly digest.

## License

GPL-3.0 — see [LICENSE](LICENSE).
