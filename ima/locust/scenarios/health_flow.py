from locust import HttpUser, task, between


class HealthFlow(HttpUser):
    """Simple health check scenario for the IMA service."""

    wait_time = between(1, 2)

    @task
    def health_check(self):
        """Call /health endpoint."""
        r = self.client.get("/api/v1/health", name="GET /api/v1/health")
        if r.status_code != 200:
            r.failure(f"Health check failed {r.status_code}")
