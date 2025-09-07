"""
FastAPI entrypoint for the IMA Service.
"""

from app.api.v1 import api_v1_router
from fastapi import FastAPI

app = FastAPI(
    title="IMA Service",
    description="Permission-based auth service with role management.",
    version="0.1.0",
)

# Include API v1 routers
app.include_router(api_v1_router, prefix="/api/v1")
