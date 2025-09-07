"""
File: app/utils/response.py
Standardized JSON response helpers and models for API endpoints.
"""

from datetime import datetime
from typing import Any, Literal, Optional

from fastapi import status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field


class ResponseModel(BaseModel):
    """Schema for standardized API responses."""

    code: int = Field(..., description="HTTP status code")
    status: Literal["success", "error"] = Field(..., description="Response status")
    message: str = Field(..., description="Human-readable message")
    timestamp: str = Field(
        default_factory=lambda: datetime.utcnow().isoformat() + "Z",
        description="Response UTC timestamp",
    )
    data: Optional[Any] = Field(None, description="Main payload data")
    details: Optional[Any] = Field(None, description="Additional error details, if any")


def _build_response(
    code: int,
    status_type: Literal["success", "error"],
    message: str,
    data: Optional[Any] = None,
    details: Optional[Any] = None,
) -> JSONResponse:
    """
    Internal helper to build a standardized JSON response.
    """
    payload = ResponseModel(
        code=code,
        status=status_type,
        message=message,
        data=data,
        details=details,
    )
    return JSONResponse(status_code=code, content=payload.model_dump())


def success_response(data: Any = None, message: str = "Success") -> JSONResponse:
    """
    Return a standard success JSON response.
    """
    return _build_response(
        code=status.HTTP_200_OK,
        status_type="success",
        message=message,
        data=data,
    )


def error_response(
    message: str,
    code: int = status.HTTP_400_BAD_REQUEST,
    details: Optional[Any] = None,
) -> JSONResponse:
    """
    Return a standard error JSON response.
    """
    return _build_response(
        code=code,
        status_type="error",
        message=message,
        details=details,
    )
