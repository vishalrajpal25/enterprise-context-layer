"""Prometheus metrics for monitoring system health and performance.

This module defines all metrics collected by the ECP platform.
Metrics are exposed at /metrics endpoint for Prometheus scraping.

Metric Categories:
- Request metrics: Total requests, latency, error rates
- Store metrics: Query latency per store, error rates
- Resolution metrics: Confidence scores, disambiguation rates
- Policy metrics: Authorization decisions
"""

from typing import Any

from prometheus_client import Counter, Histogram, Summary


class Metrics:
    """Container for all ECP metrics."""

    def __init__(self) -> None:
        # Request metrics
        self.resolve_requests_total = Counter(
            "ecp_resolve_requests_total",
            "Total number of resolve requests",
            ["status"],  # labels: success, access_denied, error
        )

        self.resolve_duration_seconds = Histogram(
            "ecp_resolve_duration_seconds",
            "Resolution request duration in seconds",
            buckets=[0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0],
        )

        self.execute_requests_total = Counter(
            "ecp_execute_requests_total",
            "Total number of execute requests",
            ["status"],  # labels: success, not_found, error
        )

        self.execute_duration_seconds = Histogram(
            "ecp_execute_duration_seconds",
            "Execute request duration in seconds",
            buckets=[0.1, 0.5, 1.0, 2.0, 5.0, 10.0, 30.0],
        )

        # Store query metrics
        self.store_query_duration_seconds = Histogram(
            "ecp_store_query_duration_seconds",
            "Store query duration in seconds",
            ["store"],  # labels: graph, vector, registry, semantic, policy
            buckets=[0.01, 0.05, 0.1, 0.25, 0.5, 1.0, 2.0],
        )

        self.store_query_errors_total = Counter(
            "ecp_store_query_errors_total",
            "Total number of store query errors",
            ["store", "error_type"],
        )

        # Resolution quality metrics
        self.resolution_confidence = Summary(
            "ecp_resolution_confidence",
            "Confidence score of resolutions",
        )

        self.disambiguation_required_total = Counter(
            "ecp_disambiguation_required_total",
            "Total number of queries requiring disambiguation",
        )

        self.validation_failures_total = Counter(
            "ecp_validation_failures_total",
            "Total number of validation failures",
            ["rule"],
        )

        # Policy metrics
        self.policy_decisions_total = Counter(
            "ecp_policy_decisions_total",
            "Total number of policy decisions",
            ["decision"],  # labels: allow, deny
        )

        self.policy_evaluation_duration_seconds = Histogram(
            "ecp_policy_evaluation_duration_seconds",
            "Policy evaluation duration in seconds",
            buckets=[0.001, 0.005, 0.01, 0.025, 0.05, 0.1],
        )

        # Error metrics
        self.errors_total = Counter(
            "ecp_errors_total",
            "Total number of errors",
            ["error_type", "component"],
        )

    def record_resolve(self, status: str, duration: float, confidence: float | None = None) -> None:
        """Record resolve request metrics.

        Args:
            status: Request status (success, access_denied, error)
            duration: Request duration in seconds
            confidence: Resolution confidence score (0-1)
        """
        self.resolve_requests_total.labels(status=status).inc()
        self.resolve_duration_seconds.observe(duration)
        if confidence is not None:
            self.resolution_confidence.observe(confidence)

    def record_execute(self, status: str, duration: float) -> None:
        """Record execute request metrics.

        Args:
            status: Request status (success, not_found, error)
            duration: Request duration in seconds
        """
        self.execute_requests_total.labels(status=status).inc()
        self.execute_duration_seconds.observe(duration)

    def record_store_query(self, store: str, duration: float, error: str | None = None) -> None:
        """Record store query metrics.

        Args:
            store: Store name (graph, vector, registry, semantic, policy)
            duration: Query duration in seconds
            error: Error type if query failed
        """
        self.store_query_duration_seconds.labels(store=store).observe(duration)
        if error:
            self.store_query_errors_total.labels(store=store, error_type=error).inc()

    def record_policy_decision(self, decision: str, duration: float) -> None:
        """Record policy decision metrics.

        Args:
            decision: Decision result (allow, deny)
            duration: Evaluation duration in seconds
        """
        self.policy_decisions_total.labels(decision=decision).inc()
        self.policy_evaluation_duration_seconds.observe(duration)

    def record_validation_failure(self, rule: str) -> None:
        """Record validation failure.

        Args:
            rule: Validation rule that failed
        """
        self.validation_failures_total.labels(rule=rule).inc()

    def record_error(self, error_type: str, component: str) -> None:
        """Record error occurrence.

        Args:
            error_type: Type of error
            component: Component where error occurred
        """
        self.errors_total.labels(error_type=error_type, component=component).inc()


# Global metrics instance
metrics = Metrics()
