"""Resolution Orchestrator - coordinates parse, plan, resolve, execute, validate, assemble."""

import uuid
from typing import Any

from ecp.adapters.base import (
    AssetRegistry,
    GraphStore,
    PolicyEngine,
    SemanticLayerClient,
    VectorStore,
)
from ecp.domain.models import (
    DAGNode,
    ExecutionPlan,
    ResolveRequest,
    ResolveResponse,
    ResolutionDAG,
    UserContext,
)


class ResolutionOrchestrator:
    """Orchestrates resolution from natural language concept to execution plan and execution to results."""

    def __init__(
        self,
        graph: GraphStore,
        vector: VectorStore,
        registry: AssetRegistry,
        semantic: SemanticLayerClient,
        policy: PolicyEngine,
    ) -> None:
        self._graph = graph
        self._vector = vector
        self._registry = registry
        self._semantic = semantic
        self._policy = policy
        self._resolution_cache: dict[str, dict[str, Any]] = {}

    async def resolve(self, request: ResolveRequest) -> ResolveResponse:
        """Resolve a business concept to canonical definition and execution plan."""
        query_id = str(uuid.uuid4())
        user_ctx = (request.user_context or UserContext()).model_dump(exclude_none=True)
        dag = ResolutionDAG(query_id=query_id, user_context=user_ctx, original_query=request.concept, nodes=[])

        # 1. Parse intent (simple: extract metric and dimension keywords)
        parse_node = DAGNode(id="parse_intent", type="parse", status="complete", output=_parse_intent(request.concept))
        dag.nodes.append(parse_node)

        # 2. Resolve concepts: metric (vector + graph), region (graph), time (registry)
        resolved: dict[str, Any] = {}
        # Metric: semantic search then graph
        vector_hits = await self._vector.search(request.concept, type_filter="glossary_term", top_k=3)
        metric_id = "net_revenue"
        if vector_hits:
            first = vector_hits[0]
            resolved["metric"] = {"id": first.get("metadata", {}).get("term", "net_revenue"), "source": "vector"}
            metric_id = resolved["metric"].get("id") or "net_revenue"
        graph_metric = await self._graph.get_metric_by_id(metric_id)
        if graph_metric:
            resolved["metric"] = resolved.get("metric") or {}
            resolved["metric"]["semantic_layer_ref"] = graph_metric.get("semantic_layer_ref", "Revenue.netRevenue")

        resolve_metric_node = DAGNode(
            id="resolve_metric",
            type="resolve_concept",
            status="complete",
            depends_on=["parse_intent"],
            output={"resolved": resolved.get("metric"), "stores_queried": ["vector", "graph"]},
        )
        dag.nodes.append(resolve_metric_node)

        # Region: default APAC for demo
        region_code = "APAC"
        region_ctx = user_ctx.get("department") or "finance"
        region_data = await self._graph.resolve_region(region_code, region_ctx)
        resolved["region"] = region_data or {"region_code": region_code, "countries": ["JP", "KR", "SG", "HK", "TW", "AU", "NZ", "IN", "CN"]}
        resolve_region_node = DAGNode(
            id="resolve_region",
            type="resolve_concept",
            status="complete",
            depends_on=["parse_intent"],
            output={"resolved": resolved["region"]},
        )
        dag.nodes.append(resolve_region_node)

        # Time: calendar from registry
        cal = await self._registry.get_asset("ar_cal_001")
        time_resolved = {"fiscal_period": "Q3-2024", "start_date": "2024-10-01", "end_date": "2024-12-31"}
        if cal and cal.get("content"):
            time_resolved["calendar_type"] = cal["content"].get("calendar_type", "fiscal")
        resolved["time"] = time_resolved
        resolve_time_node = DAGNode(
            id="resolve_time",
            type="resolve_concept",
            status="complete",
            depends_on=["parse_intent"],
            output={"resolved": resolved["time"]},
        )
        dag.nodes.append(resolve_time_node)

        # 3. Build execution plan
        semantic_ref = (resolved.get("metric") or {}).get("semantic_layer_ref") or "Revenue.netRevenue"
        measure = "Revenue.netRevenue" if "Revenue" in semantic_ref else "netRevenue"
        filters: dict[str, Any] = {
            "Revenue.fiscalPeriod": resolved["time"].get("fiscal_period", "Q3-2024"),
        }
        if resolved.get("region", {}).get("countries"):
            filters["Revenue.region"] = resolved["region"]["countries"]
        elif resolved.get("region", {}).get("region_code"):
            filters["Revenue.region"] = [resolved["region"]["region_code"]]

        execution_plan = ExecutionPlan(
            plan_type="metric_query",
            queries=[
                {
                    "id": "actual_revenue",
                    "measure": measure,
                    "dimensions": ["Revenue.region", "Revenue.fiscalPeriod"],
                    "filters": filters,
                }
            ],
        )
        plan_node = DAGNode(
            id="build_plan",
            type="plan",
            status="complete",
            depends_on=["resolve_metric", "resolve_region", "resolve_time"],
            output={"execution_plan": execution_plan.model_dump()},
        )
        dag.nodes.append(plan_node)

        # 4. Authorize
        data_product = {"certification_tier": 1}
        policy_result = await self._policy.evaluate(
            {"role": user_ctx.get("role") or "analyst"},
            "query",
            data_product,
        )
        allowed = policy_result.get("allow", False)
        auth_node = DAGNode(
            id="authorize",
            type="authorize",
            status="complete",
            depends_on=["build_plan"],
            output={"allowed": allowed, "policy_result": policy_result},
        )
        dag.nodes.append(auth_node)

        if not allowed:
            return ResolveResponse(
                resolution_id=query_id,
                status="access_denied",
                resolved_concepts=resolved,
                confidence_score=0.0,
                provenance={"dag": dag.model_dump(), "reason": "Policy denied"},
                warnings=[{"type": "access_denied", "message": "Policy evaluation denied access"}],
            )

        # Cache resolution for execute
        self._resolution_cache[query_id] = {
            "execution_plan": execution_plan,
            "resolved_concepts": resolved,
            "user_context": user_ctx,
        }

        return ResolveResponse(
            resolution_id=query_id,
            status="complete",
            execution_plan=execution_plan,
            resolved_concepts=resolved,
            confidence_score=0.92,
            provenance={"dag": dag.model_dump()},
            warnings=[],
        )

    async def execute(self, resolution_id: str, parameters: dict[str, Any] | None = None) -> dict[str, Any]:
        """Execute a previously resolved query; return results and provenance."""
        cached = self._resolution_cache.get(resolution_id)
        if not cached:
            return {
                "results": {},
                "provenance": {},
                "confidence_score": 0.0,
                "warnings": [{"type": "not_found", "message": f"Resolution {resolution_id} not found or expired"}],
            }
        plan = cached["execution_plan"]
        resolved = cached["resolved_concepts"]
        params = parameters or {}

        # Run semantic layer query
        queries = plan.queries or []
        results: dict[str, Any] = {}
        for q in queries:
            measure = q.get("measure", "Revenue.netRevenue")
            dimensions = q.get("dimensions", ["Revenue.region", "Revenue.fiscalPeriod"])
            filters = {**q.get("filters", {}), **params}
            try:
                data = await self._semantic.execute_query(measure, dimensions, filters)
                results[q.get("id", "default")] = data
            except Exception as e:
                results[q.get("id", "default")] = {"error": str(e), "data": []}

        return {
            "results": results,
            "provenance": {"resolution_id": resolution_id, "resolved_concepts": resolved},
            "confidence_score": 0.92,
            "warnings": [],
        }


def _parse_intent(concept: str) -> dict[str, Any]:
    """Simple intent parser - extract keywords for metric, dimension, time."""
    concept_lower = concept.lower()
    out: dict[str, Any] = {"concepts": [], "raw": concept}
    if "revenue" in concept_lower:
        out["concepts"].append({"type": "metric", "raw": "revenue", "confidence": 0.95})
    if "apac" in concept_lower or "asia" in concept_lower:
        out["concepts"].append({"type": "dimension_filter", "raw": "APAC", "dimension": "region", "confidence": 0.98})
    if "quarter" in concept_lower or "last quarter" in concept_lower:
        out["concepts"].append({"type": "time_filter", "raw": "last quarter", "confidence": 0.92})
    return out
