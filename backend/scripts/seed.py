"""Seed script — populates SQLite with sample data for development.

Usage:
    uv run python scripts/seed.py
"""

from __future__ import annotations

import sys
from pathlib import Path

# Allow running from repo root or backend/
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.db import Base, SessionLocal, engine
from app.models import Insight, Source, WeeklyDigest


def seed() -> None:
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        if db.query(Insight).count() > 0:
            print("Database already seeded — skipping.")
            return

        # --- Weekly digest ------------------------------------------------
        digest = WeeklyDigest(year=2026, week=11)
        db.add(digest)
        db.flush()  # get digest.id before referencing it

        # --- Insights -----------------------------------------------------
        insights = [
            Insight(
                title="GPT-5 reasoning surpasses PhD-level benchmarks",
                summary=(
                    "OpenAI's GPT-5 achieves state-of-the-art results on GPQA and MATH, "
                    "outperforming human experts in several science domains."
                ),
                reasoning=(
                    "The model uses extended chain-of-thought with self-verification loops. "
                    "Key improvement is the ability to detect and correct its own reasoning errors."
                ),
                week=11,
                year=2026,
                status="published",
                digest_id=digest.id,
            ),
            Insight(
                title="Anthropic releases Constitutional AI v2",
                summary=(
                    "New alignment technique trains models to self-critique responses "
                    "against a written constitution, reducing harmful outputs by 40%."
                ),
                reasoning=(
                    "Constitutional AI v2 adds a multi-stage revision loop where the model "
                    "rewrites its own answers when they violate defined principles."
                ),
                week=11,
                year=2026,
                status="published",
                digest_id=digest.id,
            ),
            Insight(
                title="Open-source LLMs close the gap with proprietary models",
                summary=(
                    "Llama 4 and Mistral Large 3 achieve 90%+ of GPT-4 performance on "
                    "standard benchmarks while running on consumer hardware."
                ),
                reasoning=(
                    "Advances in quantisation (GGUF Q4_K_M) and speculative decoding "
                    "allow 70B models to run at acceptable speeds on 24 GB VRAM."
                ),
                week=10,
                year=2026,
                status="published",
            ),
        ]
        db.add_all(insights)

        # --- Sources ------------------------------------------------------
        sources = [
            Source(
                url="https://openai.com/research/gpt-5",
                source_type="blog",
                provider="OpenAI",
            ),
            Source(
                url="https://arxiv.org/abs/2412.00001",
                source_type="paper",
                provider="arXiv",
            ),
            Source(
                url="https://github.com/facebookresearch/llama",
                source_type="github",
                provider="Meta",
            ),
        ]
        db.add_all(sources)

        db.commit()
        print(f"Seeded {len(insights)} insights, 1 digest, {len(sources)} sources.")

    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed()
