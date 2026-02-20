"""Graceful degradation strategies for service failures.

This module provides fallback strategies when external services fail,
ensuring the platform can continue operating in a degraded mode rather
than completely failing.

Degradation Strategies:
- Vector store down → keyword-based search fallback
- Policy engine down → fail-secure (deny by default)
- Semantic layer down → return cached/approximate results
- Graph store down → use limited registry data

Key Features:
- Automatic fallback detection
- Degraded mode indicators in responses
- Metrics tracking for degraded states
- Configurable fail-secure vs fail-open policies
"""

from typing import Any

from ecp.observability import get_logger, metrics

logger = get_logger(__name__)


class DegradationMode:
    """Tracks which services are in degraded mode."""

    _degraded_services: set[str] = set()

    @classmethod
    def mark_degraded(cls, service_name: str, reason: str) -> None:
        """Mark a service as degraded.

        Args:
            service_name: Name of the service (e.g., "vector_store", "policy_engine")
            reason: Why the service is degraded
        """
        if service_name not in cls._degraded_services:
            cls._degraded_services.add(service_name)
            logger.warning(
                "service_degraded",
                service=service_name,
                reason=reason,
                message=f"{service_name} entering degraded mode: {reason}",
            )
            metrics.record_error(
                error_type="service_degraded",
                component=service_name,
            )

    @classmethod
    def mark_recovered(cls, service_name: str) -> None:
        """Mark a service as recovered.

        Args:
            service_name: Name of the service
        """
        if service_name in cls._degraded_services:
            cls._degraded_services.remove(service_name)
            logger.info(
                "service_recovered",
                service=service_name,
                message=f"{service_name} recovered from degraded mode",
            )

    @classmethod
    def is_degraded(cls, service_name: str) -> bool:
        """Check if a service is degraded.

        Args:
            service_name: Name of the service

        Returns:
            True if service is degraded, False otherwise
        """
        return service_name in cls._degraded_services

    @classmethod
    def get_degraded_services(cls) -> list[str]:
        """Get list of all degraded services.

        Returns:
            List of degraded service names
        """
        return list(cls._degraded_services)

    @classmethod
    def reset(cls) -> None:
        """Reset degradation state (useful for testing)."""
        cls._degraded_services.clear()


def keyword_search_fallback(query: str, top_k: int = 3) -> list[dict[str, Any]]:
    """Fallback keyword search when vector store is unavailable.

    This is a simple keyword-based search that can work without embeddings.
    In production, this could query a simpler index or cache.

    Args:
        query: Search query
        top_k: Number of results to return

    Returns:
        List of search results (may be empty or lower quality)
    """
    logger.warning(
        "keyword_search_fallback_used",
        query=query,
        top_k=top_k,
        message="Vector store unavailable, using keyword fallback",
    )

    metrics.record_error(
        error_type="fallback_keyword_search",
        component="vector_store",
    )

    # In production, this would query a simpler backing store
    # For now, return empty results with degraded indicator
    return []


def cached_policy_fallback(
    user: dict[str, Any],
    action: str,
    data_product: dict[str, Any],
    default_allow: bool = False,
) -> dict[str, Any]:
    """Fallback policy evaluation when OPA is unavailable.

    Implements fail-secure by default: when policy engine is down,
    deny access unless explicitly configured otherwise.

    Args:
        user: User context
        action: Action being attempted
        data_product: Data product being accessed
        default_allow: If True, allow access when policy engine down (DANGEROUS)

    Returns:
        Policy decision (always deny by default for safety)
    """
    logger.warning(
        "policy_fallback_used",
        user_role=user.get("role"),
        action=action,
        data_product_id=data_product.get("id"),
        default_allow=default_allow,
        message="Policy engine unavailable, using fail-secure fallback",
    )

    metrics.record_error(
        error_type="fallback_policy_deny",
        component="policy_engine",
    )

    # Fail-secure: deny by default
    allowed = default_allow

    return {
        "allowed": allowed,
        "reason": "policy_engine_unavailable_fail_secure" if not allowed else "policy_engine_unavailable_default_allow",
        "degraded": True,
    }


def approximate_results_fallback(
    measure: str,
    dimensions: list[str],
    filters: dict[str, Any],
) -> dict[str, Any]:
    """Fallback for semantic layer when Cube API is unavailable.

    Returns approximate or cached results when the semantic layer is down.

    Args:
        measure: Measure being queried
        dimensions: Dimensions for the query
        filters: Query filters

    Returns:
        Approximate results with degraded indicator
    """
    logger.warning(
        "semantic_layer_fallback_used",
        measure=measure,
        dimensions=dimensions,
        message="Semantic layer unavailable, using fallback",
    )

    metrics.record_error(
        error_type="fallback_semantic_layer",
        component="semantic_layer",
    )

    # In production, could return:
    # - Cached results from last successful query
    # - Approximate values from data warehouse
    # - Historical data
    return {
        "data": [],
        "degraded": True,
        "reason": "semantic_layer_unavailable",
        "message": "Semantic layer is temporarily unavailable. Results may be incomplete.",
    }


def registry_only_fallback(region_code: str, context: str | None) -> dict[str, Any] | None:
    """Fallback for graph store when Neo4j is unavailable.

    Uses only registry data without graph relationships.

    Args:
        region_code: Region code to resolve
        context: Context for resolution

    Returns:
        Limited resolution using only registry data
    """
    logger.warning(
        "graph_store_fallback_used",
        region_code=region_code,
        context=context,
        message="Graph store unavailable, using registry-only fallback",
    )

    metrics.record_error(
        error_type="fallback_graph_store",
        component="graph_store",
    )

    # In production, would query asset registry for basic info
    # without full graph traversal capabilities
    return None
