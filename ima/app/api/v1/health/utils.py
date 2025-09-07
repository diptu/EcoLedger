"""
# File : app / api / v1 / health / utils.py
Health check utilities for FastAPI services.

Provides a standardized async helper for performing health checks on
dependencies (database, cache, external APIs). Responses use the project's
core ResponseModel to ensure consistent JSON structure across APIs.
"""

from typing import Awaitable, Callable, Dict, Optional

from fastapi import status


async def check_health(
    service_name: str,
    check_fn: Callable[[], Awaitable[bool]],
    details_key: Optional[str] = None,
) -> Dict[str, object]:
    """
    Perform a standardized health check for a service.

    Returns a dictionary compatible with FastAPI response models.
    """
    try:
        healthy = await check_fn()
        status_val = "ok" if healthy else "fail"
        details: Optional[Dict[str, str]] = (
            {details_key: status_val} if details_key else None
        )

        return {
            "code": status.HTTP_200_OK,
            "status": "success",
            "message": (
                f"{service_name} health check passed"
                if healthy
                else f"{service_name} health check failed"
            ),
            "data": {"status": status_val, "details": details},
            "details": None,
        }
    except Exception as exc:  # pylint: disable=broad-except
        details = {details_key: "fail"} if details_key else None
        return {
            "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "status": "error",
            "message": f"{service_name} health check failed",
            "data": None,
            "details": {"error": str(exc), "details": details},
        }
