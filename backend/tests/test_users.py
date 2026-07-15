"""Tests for User model — role field (Ticket 3a)."""

from __future__ import annotations

import pytest
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.db import Base
from app.models import USER_ROLES, User

_engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
_TestingSessionLocal = sessionmaker(bind=_engine, autocommit=False, autoflush=False)


def setup_function() -> None:
    Base.metadata.drop_all(bind=_engine)
    Base.metadata.create_all(bind=_engine)


def test_user_role_defaults_to_reader() -> None:
    # given
    db = _TestingSessionLocal()
    try:
        user = User(email="a@example.com")
        db.add(user)
        db.commit()
        db.refresh(user)

        # then
        assert user.role == "reader"
        assert user.is_active is True
        assert user.id is not None
        assert user.created_at is not None
    finally:
        db.close()


@pytest.mark.parametrize("role", USER_ROLES)
def test_user_accepts_each_valid_role(role: str) -> None:
    # given
    db = _TestingSessionLocal()
    try:
        user = User(email=f"{role}@example.com", name=role.title(), role=role)
        db.add(user)
        db.commit()
        db.refresh(user)

        # then
        assert user.role == role
    finally:
        db.close()


def test_user_email_is_unique() -> None:
    # given
    db = _TestingSessionLocal()
    try:
        db.add(User(email="dup@example.com"))
        db.commit()

        # when
        db.add(User(email="dup@example.com"))

        # then
        with pytest.raises(IntegrityError):
            db.commit()

        db.rollback()
    finally:
        db.close()


def test_user_rejects_invalid_role() -> None:
    # given
    db = _TestingSessionLocal()
    try:
        db.add(User(email="bad@example.com", role="superadmin"))

        # then
        with pytest.raises(IntegrityError):
            db.commit()

        db.rollback()
    finally:
        db.close()
