"""OPA policy engine adapter with retry and circuit breaker protection."""

from typing import Any

import httpx
from pybreaker import CircuitBreakerError

from ecp.adapters.base import PolicyEngine
from ecp.config import settings
from ecp.observability import get_logger, metrics
from ecp.resilience import with_circuit_breaker, with_retry
from ecp.resilience.degradation import DegradationMode, cached_policy_fallback
from ecp.resilience.exceptions import StoreConnectionError, StoreTimeoutError

logger = get_logger(__name__)


class OPAEngine(PolicyEngine):
    """OPA policy engine with resilience patterns.

    Features:
    - Automatic retry on transient failures
    - Circuit breaker to prevent cascading failures
    - Fail-secure: deny access when OPA is unavailable
    """

    def __init__(
        self,
        base_url: str | None = None,
        policy_path: str | None = None,
        fail_open: bool = False,
    ) -> None:
        self._base_url = (base_url or settings.opa_url).rstrip("/")
        self._policy_path = policy_path or settings.opa_policy_path
        # fail_open=True allows access when OPA is down (DANGEROUS, only for dev)
        self._fail_open = fail_open

    @with_retry(max_attempts=3, store_name="opa")
    async def _evaluate_with_retry(
        self,
        input_doc: dict[str, Any],
    ) -> dict[str, Any]:
        """Evaluate policy with retry logic (internal method).

        Args:
            input_doc: OPA input document

        Returns:
            Policy decision

        Raises:
            StoreConnectionError: If cannot connect to OPA
            StoreTimeoutError: If evaluation times out
        """
        try:
            path = self._policy_path.replace(".", "/")
            async with httpx.AsyncClient(timeout=10.0) as client:
                r = await client.post(
                    f"{self._base_url}/data/{path}",
                    json={"input": input_doc},
                )
                r.raise_for_status()
                data = r.json()
                return data.get("result", data)
        except httpx.ConnectError as e:
            raise StoreConnectionError("opa", str(e)) from e
        except httpx.TimeoutException as e:
            raise StoreTimeoutError("opa", "evaluate", 10.0) from e
        except httpx.HTTPStatusError as e:
            # Don't retry 4xx errors
            if 400 <= e.response.status_code < 500:
                logger.error(
                    "opa_client_error",
                    status_code=e.response.status_code,
                    error=str(e),
                )
                raise
            # 5xx errors will be retried
            raise StoreConnectionError("opa", f"HTTP {e.response.status_code}") from e

    async def evaluate(
        self,
        user: dict[str, Any],
        action: str,
        data_product: dict[str, Any],
    ) -> dict[str, Any]:
        """Evaluate policy for user action on data product.

        Includes retry logic, circuit breaker, and fail-secure fallback.

        CRITICAL: When OPA is unavailable, this fails SECURE by default
        (denies access) unless fail_open=True was set in constructor.

        Args:
            user: User context
            action: Action being attempted
            data_product: Data product being accessed

        Returns:
            Policy decision with 'allowed' boolean
        """
        input_doc = {
            "user": user,
            "action": action,
            "data_product": data_product,
        }

        try:
            # Execute with circuit breaker protection
            async with with_circuit_breaker(
                "opa",
                failure_threshold=5,
                recovery_timeout=60,
            ):
                result = await self._evaluate_with_retry(input_doc)

                # Mark as recovered if it was degraded
                if DegradationMode.is_degraded("opa"):
                    DegradationMode.mark_recovered("opa")

                return result

        except CircuitBreakerError:
            # Circuit is open, use fail-secure fallback
            logger.warning(
                "opa_circuit_breaker_open",
                user_role=user.get("role"),
                action=action,
                fail_open=self._fail_open,
                message="OPA circuit breaker is open, using fail-secure fallback",
            )
            DegradationMode.mark_degraded("opa", "circuit_breaker_open")
            return cached_policy_fallback(user, action, data_product, default_allow=self._fail_open)

        except Exception as e:
            # Other errors: log, mark degraded, use fail-secure fallback
            logger.error(
                "opa_evaluation_failed",
                user_role=user.get("role"),
                action=action,
                error=str(e),
                error_type=type(e).__name__,
                fail_open=self._fail_open,
                message="OPA evaluation failed, using fail-secure fallback",
            )
            DegradationMode.mark_degraded("opa", str(e))
            metrics.record_error(error_type=type(e).__name__, component="opa")
            return cached_policy_fallback(user, action, data_product, default_allow=self._fail_open)

    async def health(self) -> bool:
        """Check if OPA is healthy.

        Returns:
            True if healthy, False otherwise
        """
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                r = await client.get(f"{self._base_url.replace('/v1', '')}/health")
                return r.status_code == 200
        except Exception as e:
            logger.debug("opa_health_check_failed", error=str(e))
            return False
