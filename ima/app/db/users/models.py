"""
FILE : app/db/users/models.py
User model for the application.

Defines database schema for users, including roles, verification, roles,
and timestamps.
"""

import enum
import uuid
from datetime import datetime

from app.db.base import Base
from sqlalchemy import Boolean, DateTime, Enum, String
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column


class UserRole(str, enum.Enum):
    """Enumeration of possible user roles."""

    USER = "user"
    MODERATOR = "moderator"
    ADMIN = "admin"


class User(Base):  # pylint: disable=too-few-public-methods
    """Database model representing a user account."""

    __tablename__ = "users"

    uid: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        unique=True,
        nullable=False,
        default=uuid.uuid4,
        doc="Unique identifier for the user account",
    )
    username: Mapped[str] = mapped_column(String, nullable=False, doc="Unique username")
    first_name: Mapped[str | None] = mapped_column(
        String, nullable=True, doc="First name of the user"
    )
    last_name: Mapped[str | None] = mapped_column(
        String, nullable=True, doc="Last name of the user"
    )
    is_verified: Mapped[bool] = mapped_column(
        Boolean, default=False, doc="Is the user verified?"
    )
    email: Mapped[str] = mapped_column(
        String, unique=True, index=True, nullable=False, doc="Email"
    )
    hashed_password: Mapped[str] = mapped_column(
        String, nullable=False, doc="Hashed password"
    )
    role: Mapped[UserRole] = mapped_column(
        Enum(UserRole), default=UserRole.USER, nullable=False, doc="Role"
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean, default=True, nullable=False, doc="Is active?"
    )
    is_superuser: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False, doc="Is superuser?"
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False, doc="Created timestamp"
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
        doc="Updated timestamp",
    )

    def __repr__(self) -> str:
        """Return a human-readable representation of the user."""
        return f"<User {self.username}>"
