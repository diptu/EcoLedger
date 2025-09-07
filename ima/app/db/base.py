"""
File : app/db/base.py
SQLAlchemy base class for declarative models.
"""

from sqlalchemy.orm import DeclarativeBase  # type: ignore


# pylint: disable=too-few-public-methods
class Base(DeclarativeBase):
    """Base class for all SQLAlchemy ORM models."""

    # No methods or attributes required.
