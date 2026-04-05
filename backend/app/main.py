from __future__ import annotations

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app import models, schemas, services
from app.db import Base, engine, get_db

# ---------------------------------------------------------------------------
# Lifespan
# ---------------------------------------------------------------------------


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:  # noqa: ARG001
    """Create all tables on startup (SQLite; replace with Alembic when needed)."""
    Base.metadata.create_all(bind=engine)
    yield


# ---------------------------------------------------------------------------
# App
# ---------------------------------------------------------------------------

app = FastAPI(
    title="AI Hub API",
    description="AI-generated insight magazine backend.",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------------------------
# Schemas (inline — kept here so /health stays self-contained)
# ---------------------------------------------------------------------------


class HealthResponse(BaseModel):
    status: str


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------


@app.get("/health", response_model=HealthResponse, tags=["meta"])
def health() -> HealthResponse:
    """Liveness probe — returns {status: ok}."""
    return HealthResponse(status="ok")


@app.get("/insights", response_model=list[schemas.InsightOut], tags=["insights"])
def list_insights(db: Session = Depends(get_db)) -> list[models.Insight]:
    """Return all published insights, newest first."""
    return services.list_insights(db)


@app.get("/insights/{insight_id}", response_model=schemas.InsightOut, tags=["insights"])
def get_insight(insight_id: int, db: Session = Depends(get_db)) -> models.Insight:
    """Return a single insight by ID."""
    return services.get_insight(db, insight_id)


@app.get("/digest/{year}/{week}", response_model=schemas.DigestOut, tags=["digest"])
def get_digest(year: int, week: int, db: Session = Depends(get_db)) -> models.WeeklyDigest:
    """Return a weekly digest with its insights."""
    return services.get_digest(db, year, week)


@app.post(
    "/generate-insight",
    response_model=schemas.InsightOut,
    status_code=201,
    tags=["admin"],
)
def generate_insight(
    request: schemas.GenerateInsightRequest,
    db: Session = Depends(get_db),
) -> models.Insight:
    """Manually trigger the agent pipeline on provided source text.

    Returns a draft Insight (status='draft') — publish it via the admin flow.
    """
    return services.run_pipeline(db, request.source_text)
