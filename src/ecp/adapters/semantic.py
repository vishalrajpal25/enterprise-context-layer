"""Cube semantic layer client with retry and circuit breaker protection."""

from typing import Any

import httpx
from pybreaker import CircuitBreakerError

from ecp.adapters.base import SemanticLayerClient
from ecp.config import settings
from ecp.observability import get_logger, metrics
from ecp.resilience import with_circuit_breaker, with_retry
from ecp.resilience.degradation import DegradationMode, approximate_results_fallback
from ecp.resilience.exceptions import StoreConnectionError, StoreTimeoutError

logger = get_logger(__name__)


class CubeClient(SemanticLayerClient):
    """Cube semantic layer client with resilience patterns.

    Features:
    - Automatic retry on transient failures
    - Circuit breaker to prevent cascading failures
    - Graceful degradation with fallback results
    """

    def __init__(self, base_url: str | None = None, token: str | None = None) -> None:
        self._base_url = (base_url or settings.cube_api_url).rstrip("/")
        self._token = token or settings.cube_api_token

    def _headers(self) -> dict[str, str]:
        h: dict[str, str] = {"Content-Type": "application/json"}
        if self._token:
            h["Authorization"] = self._token
        return h

    @with_retry(max_attempts=3, store_name="cube_api")
    async def _execute_query_with_retry(
        self,
        query: dict[str, Any],
    ) -> dict[str, Any]:
        """Execute query with retry logic (internal method).

        Args:
            query: Cube query object

        Returns:
            Query results

        Raises:
            StoreConnectionError: If cannot connect to Cube
            StoreTimeoutError: If query times out
        """
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                r = await client.post(
                    f"{self._base_url}/load",
                    json={"query": query},
                    headers=self._headers(),
                )
                r.raise_for_status()
                return r.json()
        except httpx.ConnectError as e:
            raise StoreConnectionError("cube_api", str(e)) from e
        except httpx.TimeoutException as e:
            raise StoreTimeoutError("cube_api", "execute_query", 30.0) from e
        except httpx.HTTPStatusError as e:
            # Don't retry 4xx errors
            if 400 <= e.response.status_code < 500:
                logger.error(
                    "cube_query_client_error",
                    status_code=e.response.status_code,
                    error=str(e),
                )
                raise
            # 5xx errors will be retried
            raise StoreConnectionError("cube_api", f"HTTP {e.response.status_code}") from e

    async def execute_query(
        self,
        measure: str,
        dimensions: list[str],
        filters: dict[str, Any],
    ) -> dict[str, Any]:
        """Execute a query against Cube semantic layer.

        Includes retry logic, circuit breaker, and graceful degradation.

        Args:
            measure: Measure(s) to query
            dimensions: Dimensions for the query
            filters: Query filters

        Returns:
            Query results or fallback results if Cube is unavailable
        """
        measures = [measure] if isinstance(measure, str) else measure
        query: dict[str, Any] = {
            "measures": measures,
            "dimensions": dimensions,
            "timeDimensions": [],
        }
        if filters:
            query["filters"] = [
                {"member": k, "operator": "equals", "values": v if isinstance(v, list) else [v]}
                for k, v in filters.items()
            ]

        try:
            # Execute with circuit breaker protection
            async with with_circuit_breaker(
                "cube_api",
                failure_threshold=5,
                recovery_timeout=60,
            ):
                result = await self._execute_query_with_retry(query)

                # Mark as recovered if it was degraded
                if DegradationMode.is_degraded("cube_api"):
                    DegradationMode.mark_recovered("cube_api")

                return result

        except CircuitBreakerError:
            # Circuit is open, use fallback immediately
            logger.warning(
                "cube_circuit_breaker_open",
                message="Cube API circuit breaker is open, using fallback",
            )
            DegradationMode.mark_degraded("cube_api", "circuit_breaker_open")
            return approximate_results_fallback(measure, dimensions, filters)

        except Exception as e:
            # Other errors: log, mark degraded, use fallback
            logger.error(
                "cube_query_failed",
                error=str(e),
                error_type=type(e).__name__,
                message="Cube query failed, using fallback",
            )
            DegradationMode.mark_degraded("cube_api", str(e))
            metrics.record_error(error_type=type(e).__name__, component="cube_api")
            return approximate_results_fallback(measure, dimensions, filters)

    async def health(self) -> bool:
        """Check if Cube API is healthy.

        Returns:
            True if healthy, False otherwise
        """
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                r = await client.get(
                    f"{self._base_url.replace('/v1', '')}/readyz",
                    headers=self._headers(),
                )
                return r.status_code == 200
        except Exception as e:
            logger.debug("cube_health_check_failed", error=str(e))
            return False
