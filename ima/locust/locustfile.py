from locust import events
from prometheus_client import start_http_server, Summary, Counter
from config import settings

# Import scenarios
from scenarios.health_flow import HealthFlow

# Prometheus metrics
REQUEST_LATENCY = Summary(
    "locust_request_latency_ms", "Request latency in ms", ["method", "name", "status"]
)
REQUEST_COUNT = Counter(
    "locust_requests_total", "Total locust requests", ["method", "name", "status"]
)


@events.test_start.add_listener
def on_test_start(environment, **kwargs):
    start_http_server(settings.PROM_PORT)


@events.request.add_listener
def on_request(request_type, name, response_time, response_length, exception, **kwargs):
    status = "failure" if exception else "success"
    REQUEST_COUNT.labels(request_type, name, status).inc()
    REQUEST_LATENCY.labels(request_type, name, status).observe(response_time)
