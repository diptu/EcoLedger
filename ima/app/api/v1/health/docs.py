"""
File : app / api / v1 / health / docs.py
OpenAPI documentation metadata for health endpoints.
"""

SERVER_HEALTH_DOCS = {
    "summary": "Server Health Check",
    "description": "Check if the API server is running and reachable.",
}

DATABASE_HEALTH_DOCS = {
    "summary": "Database Health Check",
    "description": "Check connectivity to the PostgreSQL database.",
}

REDIS_HEALTH_DOCS = {
    "summary": "Redis Health Check",
    "description": "Check connectivity to the Redis cache.",
}

FULL_HEALTH_DOCS = {
    "summary": "Full System Health Check",
    "description": "Run combined health checks for server, database, and Redis.",
}
