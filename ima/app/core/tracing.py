# core/tracing.py
from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter

from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor
from opentelemetry.instrumentation.logging import LoggingInstrumentor


def init_tracing(service_name: str = "ima-service", otlp_endpoint: str | None = None):
    resource = Resource.create({"service.name": service_name})
    provider = TracerProvider(resource=resource)
    trace.set_tracer_provider(provider)

    # Export to OTLP if endpoint is given, otherwise just log to console
    if otlp_endpoint:
        otlp_exporter = OTLPSpanExporter(endpoint=otlp_endpoint)
        provider.add_span_processor(BatchSpanProcessor(otlp_exporter))
    else:
        console_exporter = ConsoleSpanExporter()
        provider.add_span_processor(BatchSpanProcessor(console_exporter))

    # Attach trace/span IDs to logs
    LoggingInstrumentor().instrument(set_logging_format=True)

    return provider


def instrument_fastapi(app, tracer_provider=None):
    FastAPIInstrumentor.instrument_app(app, tracer_provider=tracer_provider)


def instrument_sqlalchemy(engine):
    SQLAlchemyInstrumentor().instrument(
        engine=engine if not hasattr(engine, "sync_engine") else engine.sync_engine
    )
