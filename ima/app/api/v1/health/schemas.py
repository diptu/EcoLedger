"""
# File: app/api/v1/health/schemas.py
Schemas for Health API endpoints.

Uses the standardized ResponseModel structure from app.core.response.
"""

from typing import Any, Dict, Optional

from pydantic import BaseModel, Field


class HealthCheckResponse(BaseModel):
    """Standardized response schema for health endpoints."""

    code: int = Field(..., description="HTTP status code")
    status: str = Field(..., description="Overall health status, e.g., 'ok' or 'fail'")
    message: str = Field(..., description="Human-readable message")
    timestamp: str = Field(
        default_factory=lambda: __import__("datetime").datetime.utcnow().isoformat()
        + "Z",
        description="UTC timestamp of the response",
    )
    data: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Main payload data, e.g., {'status': 'ok', 'details': {...}}",
    )
    details: Optional[Dict[str, Any]] = Field(
        default=None, description="Additional details, if any"
    )
