"""Circuit breaker pattern for external service calls.

Circuit breakers prevent cascading failures by temporarily blocking calls
to services that are failing, giving them time to recover.

States:
- CLOSED: Normal operation, requests pass through
- OPEN: Service is failing, requests are blocked immediately
- HALF_OPEN: Testing if service has recovered

Key Features:
- Automatic state transitions based on failure rates
- Configurable failure thresholds
- Recovery timeout
- Metrics and logging integration

Usage:
    from ecp.resilience import CircuitBreakerManager

    breaker = CircuitBreakerManager.get_breaker("cube_api")

    async with breaker:
        result = await call_external_service()
"""

import asyncio
from contextlib import asynccontextmanager
from typing import Any, AsyncIterator

from pybreaker import CircuitBreaker, CircuitBreakerError, CircuitBreakerState

from ecp.observability import get_logger, metrics

logger = get_logger(__name__)


class CircuitBreakerManager:
    """Manages circuit breakers for external services.

    Singleton pattern to ensure only one breaker per service.
    """

    _breakers: dict[str, CircuitBreaker] = {}

    @classmethod
    def get_breaker(
        cls,
        name: str,
        failure_threshold: int = 5,
        recovery_timeout: int = 60,
        expected_exception: type[Exception] = Exception,
    ) -> CircuitBreaker:
        """Get or create a circuit breaker for a service.

        Args:
            name: Unique name for the service (e.g., "cube_api", "opa_policy")
            failure_threshold: Number of failures before opening circuit
            recovery_timeout: Seconds to wait before attempting recovery
            expected_exception: Exception type that triggers the breaker

        Returns:
            CircuitBreaker instance
        """
        if name not in cls._breakers:
            logger.info(
                "circuit_breaker_created",
                name=name,
                failure_threshold=failure_threshold,
                recovery_timeout=recovery_timeout,
            )

            breaker = CircuitBreaker(
                fail_max=failure_threshold,
                reset_timeout=recovery_timeout,
                exclude=[
                    # Don't trip breaker on these exceptions
                    ValueError,
                    TypeError,
                    KeyError,
                ],
                listeners=[
                    CircuitBreakerListener(name),
                ],
                name=name,
            )

            cls._breakers[name] = breaker

        return cls._breakers[name]

    @classmethod
    def reset_all(cls) -> None:
        """Reset all circuit breakers (useful for testing)."""
        for breaker in cls._breakers.values():
            breaker.reset()
        logger.info("all_circuit_breakers_reset")


class CircuitBreakerListener:
    """Listener for circuit breaker state changes.

    Records metrics and logs when breaker state changes.
    """

    def __init__(self, name: str) -> None:
        self.name = name

    def state_change(self, breaker: CircuitBreaker, old_state: CircuitBreakerState, new_state: CircuitBreakerState) -> None:
        """Called when circuit breaker state changes."""
        logger.warning(
            "circuit_breaker_state_changed",
            breaker_name=self.name,
            old_state=old_state.name,
            new_state=new_state.name,
            failure_count=breaker.fail_counter,
        )

        # Record metric
        metrics.record_error(
            error_type=f"circuit_breaker_{new_state.name.lower()}",
            component=self.name,
        )

    def before_call(self, breaker: CircuitBreaker, func: Any, *args: Any, **kwargs: Any) -> None:
        """Called before attempting to call the protected function."""
        pass

    def success(self, breaker: CircuitBreaker) -> None:
        """Called when call succeeds."""
        pass

    def failure(self, breaker: CircuitBreaker, exception: Exception) -> None:
        """Called when call fails."""
        logger.debug(
            "circuit_breaker_failure",
            breaker_name=self.name,
            failure_count=breaker.fail_counter,
            failure_threshold=breaker.fail_max,
            error=str(exception),
        )


@asynccontextmanager
async def with_circuit_breaker(name: str, **breaker_kwargs: Any) -> AsyncIterator[None]:
    """Context manager for circuit breaker protection.

    Args:
        name: Service name for the circuit breaker
        **breaker_kwargs: Additional arguments for get_breaker()

    Raises:
        CircuitBreakerError: If circuit is open
        Original exception: If call fails but circuit is closed

    Example:
        async with with_circuit_breaker("cube_api"):
            result = await cube_client.query(...)
    """
    breaker = CircuitBreakerManager.get_breaker(name, **breaker_kwargs)

    try:
        # Check if circuit is open
        if breaker.current_state == CircuitBreakerState.STATE_OPEN:
            logger.warning(
                "circuit_breaker_open_request_blocked",
                breaker_name=name,
                message="Circuit breaker is OPEN, request blocked",
            )
            raise CircuitBreakerError(breaker)

        # Allow call through
        yield

        # Mark success
        breaker.call_succeeded()

    except CircuitBreakerError:
        # Circuit is open, don't count as failure
        raise

    except Exception as e:
        # Call failed, record failure
        breaker.call_failed()

        logger.error(
            "circuit_breaker_call_failed",
            breaker_name=name,
            error=str(e),
            error_type=type(e).__name__,
            failure_count=breaker.fail_counter,
            state=breaker.current_state.name,
        )

        raise


def is_circuit_open(name: str) -> bool:
    """Check if a circuit breaker is open.

    Args:
        name: Service name

    Returns:
        True if circuit is open, False otherwise
    """
    if name not in CircuitBreakerManager._breakers:
        return False

    breaker = CircuitBreakerManager._breakers[name]
    return breaker.current_state == CircuitBreakerState.STATE_OPEN


async def wait_for_circuit_recovery(name: str, max_wait: float = 120.0) -> bool:
    """Wait for a circuit breaker to recover.

    Args:
        name: Service name
        max_wait: Maximum time to wait in seconds

    Returns:
        True if circuit recovered, False if timeout
    """
    start = asyncio.get_event_loop().time()

    while asyncio.get_event_loop().time() - start < max_wait:
        if not is_circuit_open(name):
            logger.info(
                "circuit_breaker_recovered",
                breaker_name=name,
                wait_time=asyncio.get_event_loop().time() - start,
            )
            return True

        await asyncio.sleep(1.0)

    logger.warning(
        "circuit_breaker_recovery_timeout",
        breaker_name=name,
        max_wait=max_wait,
    )
    return False
