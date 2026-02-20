"""Resilience module - retry logic, circuit breakers, graceful degradation."""

from ecp.resilience.circuit_breaker import (
    CircuitBreakerManager,
    is_circuit_open,
    wait_for_circuit_recovery,
    with_circuit_breaker,
)
from ecp.resilience.degradation import DegradationMode
from ecp.resilience.exceptions import (
    AuthorizationError,
    ECPError,
    ResolutionError,
    StoreError,
    ValidationError,
)
from ecp.resilience.retry import retry_on_transient_error, with_retry

__all__ = [
    "ECPError",
    "StoreError",
    "ResolutionError",
    "ValidationError",
    "AuthorizationError",
    "retry_on_transient_error",
    "with_retry",
    "CircuitBreakerManager",
    "with_circuit_breaker",
    "is_circuit_open",
    "wait_for_circuit_recovery",
    "DegradationMode",
]
