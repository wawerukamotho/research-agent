from fastapi import FastAPI
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from prometheus_client import start_http_server

from scaffold.config import settings


def setup_observability(app: FastAPI):
    # Set up OpenTelemetry
    resource = Resource(attributes={SERVICE_NAME: settings.app_name})
    provider = TracerProvider(resource=resource)

    # Only export traces if endpoint is provided
    if settings.otel_exporter_otlp_endpoint:
        processor = BatchSpanProcessor(
            OTLPSpanExporter(endpoint=settings.otel_exporter_otlp_endpoint)
        )
        provider.add_span_processor(processor)

    trace.set_tracer_provider(provider)

    # Instrument FastAPI
    FastAPIInstrumentor.instrument_app(app)

    # Start Prometheus metrics server
    start_http_server(settings.prometheus_port)
