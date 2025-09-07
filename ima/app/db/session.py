"""
File : app / db / session.py
Async SQLAlchemy session for PostgreSQL using asyncpg.

Provides an async engine, session factory, and a dependency generator
with error handling for FastAPI endpoints.
"""

from collections.abc import AsyncGenerator

from app.core.config import settings
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    create_async_engine)

# Async engine for PostgreSQL/NeonDB
engine = create_async_engine(
    settings.database.uri,
    echo=True,
    connect_args={"ssl": "require"},
)

# Async session factory with proper typing
AsyncSessionLocal: async_sessionmaker[AsyncSession] = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Yield an async database session.

    Raises
    ------
    HTTPException
        If the database session could not be created.
    """
    try:
        async with AsyncSessionLocal() as session:
            yield session
    except Exception as exc:
        # Optional: add logging here
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database connection error: {exc}",
        ) from exc
