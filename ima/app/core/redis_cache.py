"""
Redis cache client for IMA service using asyncio Redis.

Provides a singleton async Redis client instance with optional connection
health check.
"""

from __future__ import annotations

import redis.asyncio as redis
from app.core.config import settings

# Singleton async Redis client
redis_client: redis.Redis = redis.Redis(
    host=settings.redis.host,
    port=settings.redis.port,
    password=settings.redis.password,
    db=settings.redis.db,
    decode_responses=True,
)
