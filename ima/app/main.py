"""
FastAPI entrypoint for the IMA Service.

Defines the main FastAPI app instance and root health-check endpoint.
"""

from fastapi import FastAPI

app = FastAPI(
    title="IMA Service",
    description="Permission-based auth service with role management.",
    version="0.1.0",
)


@app.get("/")
async def read_root() -> dict[str, str]:
    """
    Root endpoint for health check.

    Returns a simple JSON message confirming the service is running.
    """
    return {"message": "Hello World!"}
