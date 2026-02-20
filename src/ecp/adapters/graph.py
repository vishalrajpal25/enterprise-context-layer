"""Neo4j graph store adapter with retry protection."""

from typing import Any

from neo4j import AsyncGraphDatabase
from neo4j.exceptions import ServiceUnavailable, SessionExpired

from ecp.adapters.base import GraphStore
from ecp.config import settings
from ecp.observability import get_logger, metrics
from ecp.resilience import with_retry
from ecp.resilience.degradation import DegradationMode, registry_only_fallback
from ecp.resilience.exceptions import StoreConnectionError

logger = get_logger(__name__)


class Neo4jGraphStore(GraphStore):
    """Neo4j graph store with resilience patterns.

    Features:
    - Automatic retry on transient failures
    - Connection error handling
    - Graceful degradation with registry-only fallback
    """

    def __init__(
        self,
        uri: str | None = None,
        user: str | None = None,
        password: str | None = None,
    ) -> None:
        self._uri = uri or settings.neo4j_uri
        self._user = user or settings.neo4j_user
        self._password = password or settings.neo4j_password
        self._driver = AsyncGraphDatabase.driver(self._uri, auth=(self._user, self._password))

    async def close(self) -> None:
        await self._driver.close()

    @with_retry(max_attempts=3, store_name="neo4j")
    async def get_metric_by_id(self, metric_id: str) -> dict[str, Any] | None:
        """Get metric by ID with retry protection.

        Args:
            metric_id: Metric identifier

        Returns:
            Metric data or None if not found

        Raises:
            StoreConnectionError: If cannot connect to Neo4j
        """
        try:
            async with self._driver.session() as session:
                result = await session.run(
                    "MATCH (m:Metric {id: $id}) RETURN m",
                    id=metric_id,
                )
                record = await result.single()
                if not record or not record["m"]:
                    return None
                node = record["m"]
                keys = getattr(node, "keys", None)
                if keys:
                    return {k: node[k] for k in keys()}
                return {"id": metric_id}
        except (ServiceUnavailable, SessionExpired) as e:
            logger.error("neo4j_connection_error", metric_id=metric_id, error=str(e))
            raise StoreConnectionError("neo4j", str(e)) from e

    @with_retry(max_attempts=3, store_name="neo4j")
    async def resolve_region(self, region_code: str, context: str | None) -> dict[str, Any] | None:
        """Resolve region code to countries with retry protection.

        Args:
            region_code: Region code to resolve
            context: Context for resolution (e.g., "finance")

        Returns:
            Region data with countries or None if not found

        Raises:
            StoreConnectionError: If cannot connect to Neo4j
        """
        try:
            async with self._driver.session() as session:
                ctx = context or "finance"
                result = await session.run(
                    """
                    MATCH (r:Region {code: $code})-[:HAS_VARIATION {context: $ctx}]->(v:Variation)
                    RETURN v.countries AS countries
                    """,
                    code=region_code,
                    ctx=ctx,
                )
                record = await result.single()
                if not record:
                    return None
                return {"region_code": region_code, "context": ctx, "countries": record.get("countries") or []}
        except (ServiceUnavailable, SessionExpired) as e:
            logger.error("neo4j_connection_error", region_code=region_code, error=str(e))
            raise StoreConnectionError("neo4j", str(e)) from e

    @with_retry(max_attempts=3, store_name="neo4j")
    async def get_lineage(self, target: str, depth: int = 3) -> dict[str, Any]:
        """Get data lineage for a target asset with retry protection.

        Args:
            target: Target asset ID
            depth: Maximum depth to traverse (unused currently)

        Returns:
            Lineage graph with nodes and edges

        Raises:
            StoreConnectionError: If cannot connect to Neo4j
        """
        try:
            async with self._driver.session() as session:
                result = await session.run(
                    """
                    MATCH path = (m {id: $target})-[:COMPUTED_FROM|TRANSFORMS_FROM*1..5]-(other)
                    RETURN path LIMIT 50
                    """,
                    target=target,
                )
                nodes, edges = [], []
                async for record in result:
                    path = record.get("path")
                    if path:
                        for node in path.nodes:
                            nodes.append({"id": node.element_id, "labels": list(node.labels)})
                        for rel in path.relationships:
                            edges.append({"source": rel.start_node.element_id, "target": rel.end_node.element_id})
                return {"target": target, "nodes": nodes[:20], "edges": edges[:30]}
        except (ServiceUnavailable, SessionExpired) as e:
            logger.error("neo4j_connection_error", target=target, error=str(e))
            raise StoreConnectionError("neo4j", str(e)) from e

    @with_retry(max_attempts=3, store_name="neo4j")
    async def list_metrics_for_dimension(self, dimension: str, domain: str | None, certification_tier: int | None) -> list[dict[str, Any]]:
        """List metrics that use a specific dimension with retry protection.

        Args:
            dimension: Dimension name
            domain: Domain filter (unused currently)
            certification_tier: Filter by certification tier

        Returns:
            List of metrics using the dimension

        Raises:
            StoreConnectionError: If cannot connect to Neo4j
        """
        try:
            async with self._driver.session() as session:
                q = """
                    MATCH (m:Metric)-[:USES_DIMENSION]->(d:Dimension {name: $dim})
                    RETURN m.id AS id, m.name AS name, m.certification_tier AS certification_tier
                """
                params: dict[str, Any] = {"dim": dimension}
                result = await session.run(q, **params)
                rows = []
                async for record in result:
                    rows.append({"id": record["id"], "name": record["name"], "certification_tier": record.get("certification_tier")})
                if certification_tier is not None:
                    rows = [r for r in rows if (r.get("certification_tier") or 4) <= certification_tier]
                return rows
        except (ServiceUnavailable, SessionExpired) as e:
            logger.error("neo4j_connection_error", dimension=dimension, error=str(e))
            raise StoreConnectionError("neo4j", str(e)) from e

    async def health(self) -> bool:
        """Check if Neo4j is healthy.

        Returns:
            True if healthy, False otherwise
        """
        try:
            await self._driver.verify_connectivity()
            return True
        except Exception as e:
            logger.debug("neo4j_health_check_failed", error=str(e))
            return False
