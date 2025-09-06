"""Application settings using Pydantic Settings (async-ready)."""

from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseSettings):
    """PostgreSQL async database configuration."""

    uri: str = Field(..., alias="DB_URI")
    pool_min: int = Field(10, alias="DB_POOL_MIN")
    pool_max: int = Field(50, alias="DB_POOL_MAX")
    replica1_host: Optional[str] = Field(None, alias="DB_REPLICA1_HOST")
    replica2_host: Optional[str] = Field(None, alias="DB_REPLICA2_HOST")

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="allow",
    )


class RedisSettings(BaseSettings):
    """Redis configuration."""

    host: str = Field(..., alias="REDIS_HOST")
    port: int = Field(..., alias="REDIS_PORT")
    password: str = Field(..., alias="REDIS_PASSWORD")
    db: int = Field(..., alias="REDIS_DB")
    cache_ttl: int = Field(..., alias="REDIS_CACHE_TTL")

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="allow",
    )


class RateLimitSettings(BaseSettings):
    """Rate limiting configuration."""

    count: int = Field(5, alias="RATE_LIMIT_COUNT")
    window: int = Field(60, alias="RATE_LIMIT_WINDOW")

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="allow",
    )


class Settings(BaseSettings):
    """Main application settings."""

    app_name: str = Field(..., alias="APP_NAME")
    base_url: str = Field(..., alias="BASE_URL")
    env: str = Field(..., alias="ENV")
    debug: bool = Field(..., alias="DEBUG")
    port: int = Field(..., alias="PORT")

    # Nested settings with default factories (no lambda needed)
    database: DatabaseSettings = Field(
        default_factory=DatabaseSettings  # type: ignore[arg-type]
    )
    redis: RedisSettings = Field(
        default_factory=RedisSettings  # type: ignore[arg-type]
    )
    rate_limit: RateLimitSettings = Field(
        default_factory=RateLimitSettings  # type: ignore[arg-type]
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="allow",
    )


# Singleton instance (mypy cannot know env vars at type-check time)
settings = Settings()  # type: ignore[call-arg]
