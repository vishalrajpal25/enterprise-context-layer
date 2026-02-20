"""Tests for observability (logging, metrics)."""

import pytest

from ecp.observability import get_logger, metrics, setup_logging
from ecp.observability.logging import bind_request_context, unbind_request_context


def test_setup_logging():
    """Test that logging setup doesn't crash."""
    setup_logging(log_level="DEBUG", json_logs=False)
    logger = get_logger(__name__)
    assert logger is not None


def test_get_logger():
    """Test getting a logger instance."""
    setup_logging(log_level="INFO", json_logs=False)
    logger = get_logger("test_module")
    assert logger is not None

    # Test logging (should not crash)
    logger.info("test_message", key="value")
    logger.debug("debug_message")
    logger.warning("warning_message")


def test_bind_request_context():
    """Test binding and unbinding request context."""
    setup_logging(log_level="INFO", json_logs=False)
    logger = get_logger(__name__)

    bind_request_context(request_id="req_123", user_id="u_456")
    logger.info("with_context")

    unbind_request_context()
    logger.info("without_context")


def test_metrics_exist():
    """Test that all expected metrics exist."""
    assert metrics.resolve_requests_total is not None
    assert metrics.resolve_duration_seconds is not None
    assert metrics.execute_requests_total is not None
    assert metrics.execute_duration_seconds is not None
    assert metrics.store_query_duration_seconds is not None
    assert metrics.policy_decisions_total is not None


def test_metrics_record():
    """Test recording metrics doesn't crash."""
    metrics.record_resolve(status="success", duration=0.5, confidence=0.92)
    metrics.record_execute(status="success", duration=1.0)
    metrics.record_store_query(store="graph", duration=0.1)
    metrics.record_policy_decision(decision="allow", duration=0.01)
    metrics.record_validation_failure(rule="test_rule")
    metrics.record_error(error_type="TestError", component="test")
