"""
Integration test for the /health endpoint of the API.
Ensures server, database, and Redis are reported as OK.
"""

from unittest.mock import AsyncMock, MagicMock, patch

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_all_ok():
    """Test that /health endpoint returns OK for server, database, and Redis."""

    # Mock AsyncSessionLocal as async context manager
    mock_session = AsyncMock()
    mock_session.__aenter__.return_value.execute = AsyncMock(return_value=None)
    mock_session.__aexit__.return_value = AsyncMock(return_value=None)

    async_session_local_mock = MagicMock(return_value=mock_session)

    # Patch database session and Redis client
    with (
        patch("app.db.session.AsyncSessionLocal", new=async_session_local_mock),
        patch(
            "app.core.redis_cache.redis_client.ping", new=AsyncMock(return_value=True)
        ),
    ):
        response = client.get("/api/v1/health/")

    assert response.status_code == 200

    body = response.json()
    data = body.get("data", {})
    details = data.get("details", {})

    assert data.get("status") == "ok"
    assert details.get("server") == "ok"
    assert details.get("database") == "ok"
    assert details.get("redis") == "ok"
