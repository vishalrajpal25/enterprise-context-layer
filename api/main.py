"""FastAPI app - REST API for resolve, execute, glossary, lineage, metrics, health."""

from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from ecp.adapters.graph import Neo4jGraphStore
from ecp.adapters.policy import OPAEngine
from ecp.adapters.registry import PostgresAssetRegistry
from ecp.adapters.semantic import CubeClient
from ecp.adapters.vector import PgVectorStore
from ecp.domain.models import ExecuteRequest, ResolveRequest, UserContext
from ecp.orchestrator import ResolutionOrchestrator


def _create_orchestrator() -> ResolutionOrchestrator:
    graph = Neo4jGraphStore()
    vector = PgVectorStore()
    registry = PostgresAssetRegistry()
    semantic = CubeClient()
    policy = OPAEngine()
    return ResolutionOrchestrator(
        graph=graph,
        vector=vector,
        registry=registry,
        semantic=semantic,
        policy=policy,
    )


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.orchestrator = _create_orchestrator()
    yield
    # Optional: close adapters if they have close()


app = FastAPI(
    title="Enterprise Context Platform API",
    description="Semantic resolution and execution for agentic data access",
    version="1.0.0",
    lifespan=lifespan,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/api/v1/resolve", response_model=dict)
async def resolve(body: dict[str, Any]) -> dict:
    """Resolve a business concept to canonical definition and execution plan."""
    concept = body.get("concept")
    if not concept:
        raise HTTPException(status_code=400, detail="concept is required")
    user_ctx = body.get("user_context")
    request = ResolveRequest(
        concept=concept,
        user_context=UserContext(**user_ctx) if user_ctx else None,
    )
    orch = app.state.orchestrator
    response = await orch.resolve(request)
    return response.model_dump()


@app.post("/api/v1/execute", response_model=dict)
async def execute(body: dict[str, Any]) -> dict:
    """Execute a previously resolved metric query."""
    resolution_id = body.get("resolution_id")
    if not resolution_id:
        raise HTTPException(status_code=400, detail="resolution_id is required")
    params = body.get("parameters") or {}
    orch = app.state.orchestrator
    result = await orch.execute(resolution_id, params)
    return result


@app.get("/api/v1/glossary", response_model=dict)
async def query_glossary(query: str, domain: str | None = None) -> dict:
    """Search the business glossary for term definitions."""
    orch = app.state.orchestrator
    registry = orch._registry
    terms = await registry.search_glossary(query, domain=domain, limit=10)
    return {
        "terms": [
            {
                "id": t["id"],
                "canonical_name": (t.get("content") or {}).get("canonical_name"),
                "definition": (t.get("content") or {}).get("definition"),
                "domain": (t.get("metadata") or {}).get("domain"),
            }
            for t in terms
        ],
        "total": len(terms),
    }


@app.get("/api/v1/lineage", response_model=dict)
async def get_lineage(target: str, depth: int = 3) -> dict:
    """Get data lineage for a metric or table."""
    orch = app.state.orchestrator
    graph = orch._graph
    result = await graph.get_lineage(target, depth=depth)
    return result


@app.get("/api/v1/metrics", response_model=dict)
async def list_available_metrics(
    dimension: str | None = None,
    domain: str | None = None,
    certification_tier: int | None = None,
) -> dict:
    """List metrics available for a given dimension or domain."""
    orch = app.state.orchestrator
    graph = orch._graph
    dim = dimension or "region"
    metrics = await graph.list_metrics_for_dimension(dim, domain=domain, certification_tier=certification_tier)
    return {"metrics": metrics, "total": len(metrics)}


@app.get("/api/v1/health", response_model=dict)
async def health() -> dict:
    """Health check - report status of stores."""
    orch = app.state.orchestrator
    stores: dict[str, bool] = {}
    try:
        stores["graph"] = await orch._graph.health()
    except Exception:
        stores["graph"] = False
    try:
        stores["vector"] = await orch._vector.health()
    except Exception:
        stores["vector"] = False
    try:
        stores["registry"] = await orch._registry.health()
    except Exception:
        stores["registry"] = False
    try:
        stores["semantic"] = await orch._semantic.health()
    except Exception:
        stores["semantic"] = False
    try:
        stores["policy"] = await orch._policy.health()
    except Exception:
        stores["policy"] = False
    status = "ok" if all(stores.values()) else "degraded"
    return {"status": status, "stores": stores}
