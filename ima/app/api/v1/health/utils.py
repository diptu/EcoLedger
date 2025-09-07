"""
# File : app / api / v1 / health / utils.py
Health check utilities for FastAPI services.

Provides a standardized async helper for performing health checks on
dependencies (database, cache, external APIs). Responses use the project's
core ResponseModel to ensure consistent JSON structure across APIs.
"""

from typing import Awaitable, Callable, Optional

from fastapi import status

from app.core.response import ResponseModel, error_response, success_response


async def check_health(
    service_name: str,
    check_fn: Callable[[], Awaitable[bool]],
    details_key: Optional[str] = None,
) -> ResponseModel:
    """
    Perform a standardized health check for a service.

    Parameters
    ----------
    service_name : str
        Name of the service being checked.
    check_fn : Callable[[], Awaitable[bool]]
        Async function returning True if healthy, False otherwise.
    details_key : Optional[str], default=None
        Key for embedding check details in the response.

    Returns
    -------
    ResponseModel
        Standardized API response indicating service health.
    """
    try:
        healthy = await check_fn()
        status_val = "ok" if healthy else "fail"
        details = {details_key: status_val} if details_key else None

        message = (
            f"{service_name} health check passed"
            if healthy
            else f"{service_name} health check failed"
        )

        return success_response(
            data={"status": status_val, "details": details}, message=message
        )
    except Exception as exc:  # pylint: disable=broad-except
        details = {details_key: "fail"} if details_key else None
        return error_response(
            code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message=f"{service_name} health check failed",
            details={"error": str(exc), "details": details},
        )
