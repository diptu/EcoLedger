"""
Application settings using Pydantic BaseSettings (async-ready).

Provides configuration for database, Redis, and application-level settings.
"""

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

    model_config = SettingsConfigDict(env_file=".env", extra="allow")


class RedisSettings(BaseSettings):
    """Redis configuration."""

    host: str = Field(..., alias="REDIS_HOST")
    port: int = Field(..., alias="REDIS_PORT")
    password: str = Field(..., alias="REDIS_PASSWORD")
    db: int = Field(..., alias="REDIS_DB")
    cache_ttl: int = Field(3600, alias="REDIS_CACHE_TTL")  # default 1 hour

    model_config = SettingsConfigDict(env_file=".env", extra="allow")


class RateLimitSettings(BaseSettings):
    """Rate limiting configuration."""

    count: int = Field(5, alias="RATE_LIMIT_COUNT")
    window: int = Field(60, alias="RATE_LIMIT_WINDOW")

    model_config = SettingsConfigDict(env_file=".env", extra="allow")


class SentrySettings(BaseSettings):
    """Sentry error reporting configuration."""

    dsn: Optional[str] = Field(None, alias="SENTRY_DSN")
    environment: str = Field("development", alias="SENTRY_ENVIRONMENT")
    release: Optional[str] = Field(None, alias="SENTRY_RELEASE")
    traces_sample_rate: float = Field(0.1, alias="SENTRY_TRACES_SAMPLE_RATE")
    debug: bool = Field(False, alias="SENTRY_DEBUG")

    model_config = SettingsConfigDict(env_file=".env", extra="allow")


class Settings(BaseSettings):
    """Main application settings."""

    app_name: str = Field(..., alias="APP_NAME")
    base_url: str = Field(..., alias="BASE_URL")
    env: str = Field(..., alias="ENV")
    debug: bool = Field(..., alias="DEBUG")
    port: int = Field(..., alias="PORT")

    database: DatabaseSettings = DatabaseSettings()  # type: ignore[call-arg]
    redis: RedisSettings = RedisSettings()  # type: ignore[call-arg]
    # sentry: SentrySettings = SentrySettings()  # type: ignore[call-arg]
    # jwt: JWTSettings = JWTSettings()  # Uncomment when JWTSettings is defined
    # rate_limit: RateLimitSettings = RateLimitSettings()  # Uncomment if needed

    model_config = SettingsConfigDict(env_file=".env", extra="allow")


# Singleton instance (mypy cannot know env vars at type-check time)
settings: Settings = Settings()  # type: ignore[call-arg]
