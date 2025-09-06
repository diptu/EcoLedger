"""
Entry point for the IMA FastAPI service.

This module starts the FastAPI app using uvicorn. Host and port can be
configured via the HOST and PORT environment variables.
"""

import os
import uvicorn
from app.main import app


def get_env_var(name: str, default: str) -> str:
    """Retrieve environment variable or return default."""
    return os.getenv(name, default)


if __name__ == "__main__":
    host: str = get_env_var("HOST", "127.0.0.1")
    port: int = int(get_env_var("PORT", "8000"))

    uvicorn.run(
        app,
        host=host,
        port=port,
        reload=True,
    )
