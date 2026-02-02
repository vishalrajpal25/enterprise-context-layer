# ECP Observability

## Logging

- **Structured logging:** Use `structlog` (or stdlib `logging` with JSON formatter) for request-scoped logs.
- **Request ID:** Generate a `request_id` (e.g. UUID) per resolve/execute and include it in all log lines and optional response headers.
- **Log levels:** DEBUG for store queries and DAG steps in development; INFO for resolve/execute summary; WARNING for policy deny and validation failures.

## Metrics (Recommended)

- **Resolution latency:** Histogram of time from resolve request to response (p50, p95, p99).
- **Execute latency:** Histogram of execute request to response.
- **Store latency:** Per-store (graph, vector, registry, semantic, policy) query latency.
- **Error counts:** Counters by error type (e.g. policy_denied, resolution_not_found, store_error).
- **Throughput:** Resolve and execute request rate.

Export via Prometheus endpoint (e.g. `/metrics`) or push to Datadog/New Relic.

## Tracing (Optional)

- **OpenTelemetry:** Instrument resolve/execute with spans; child spans for each store call and DAG stage.
- **Propagation:** Use W3C tracecontext so downstream services (e.g. Cube, OPA) can join the trace.

## Health

- **`GET /api/v1/health`:** Returns status of each store (graph, vector, registry, semantic, policy). Use for readiness probes.
