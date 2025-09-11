"""
FastAPI entrypoint for the IMA Service.
"""

import os

from app.api.v1 import api_v1_router
from fastapi import FastAPI
from app.core.tracing import init_tracing, instrument_fastapi, instrument_sqlalchemy
from app.db.session import engine


app = FastAPI(
    title="IMA Service",
    description="Permission-based auth service with role management.",
    version="0.1.0",
)

# Include API v1 routers
app.include_router(api_v1_router, prefix="/api/v1")


OTLP_ENDPOINT = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT")  # optional
SERVICE_NAME = os.getenv("OTEL_SERVICE_NAME", "ima-service")

tracer_provider = init_tracing(service_name=SERVICE_NAME, otlp_endpoint=OTLP_ENDPOINT)

instrument_fastapi(app, tracer_provider)
instrument_sqlalchemy(engine)
