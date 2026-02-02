"""Neo4j graph store adapter."""

from typing import Any

from neo4j import AsyncGraphDatabase

from ecp.adapters.base import GraphStore
from ecp.config import settings


class Neo4jGraphStore(GraphStore):
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

    async def get_metric_by_id(self, metric_id: str) -> dict[str, Any] | None:
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

    async def resolve_region(self, region_code: str, context: str | None) -> dict[str, Any] | None:
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

    async def get_lineage(self, target: str, depth: int = 3) -> dict[str, Any]:
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

    async def list_metrics_for_dimension(self, dimension: str, domain: str | None, certification_tier: int | None) -> list[dict[str, Any]]:
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

    async def health(self) -> bool:
        try:
            await self._driver.verify_connectivity()
            return True
        except Exception:
            return False
