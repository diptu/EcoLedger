# locust/config.py
import os


class Settings:
    """Config for Locust load tests."""

    # Target host (your IMA service)
    HOST: str = os.getenv("TARGET_HOST", "http://localhost:8000")

    # Credentials (use test users only!)
    USERNAME: str = os.getenv("LOCUST_USER", "perf_user")
    PASSWORD: str = os.getenv("LOCUST_PASS", "perf_pass")

    # Prometheus exporter port
    PROM_PORT: int = int(os.getenv("PROM_PORT", "8000"))


settings = Settings()
