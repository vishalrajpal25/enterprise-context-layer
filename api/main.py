"""FastAPI app - REST API for resolve, execute, glossary, lineage, metrics, health."""

import time
from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, PlainTextResponse
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest

from ecp.adapters.graph import Neo4jGraphStore
from ecp.adapters.policy import OPAEngine
from ecp.adapters.registry import PostgresAssetRegistry
from ecp.adapters.semantic import CubeClient
from ecp.adapters.vector import PgVectorStore
from ecp.config import settings
from ecp.domain.models import ExecuteRequest, ResolveRequest, UserContext
from ecp.observability import get_logger, metrics, setup_logging
from ecp.observability.middleware import ObservabilityMiddleware
from ecp.orchestrator import ResolutionOrchestrator
from ecp.resilience import DegradationMode, ECPError

# Initialize logging
setup_logging(log_level=settings.log_level, json_logs=(settings.env != "local"))
logger = get_logger(__name__)


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
    logger.info("application_startup", env=settings.env)
    app.state.orchestrator = _create_orchestrator()
    yield
    logger.info("application_shutdown")
    # Optional: close adapters if they have close()


app = FastAPI(
    title="Enterprise Context Platform API",
    description="Semantic resolution and execution for agentic data access",
    version="1.0.0",
    lifespan=lifespan,
)


# RFC 7807 Problem Details error handler
@app.exception_handler(ECPError)
async def ecp_error_handler(request: Request, exc: ECPError) -> JSONResponse:
    """Handle ECPError exceptions with RFC 7807 Problem Details format.

    Returns errors in the standard format:
    {
        "type": "https://api.example.com/errors/{error_code}",
        "title": "Human-readable title",
        "status": 500,
        "detail": "Detailed error message",
        "instance": "/api/v1/resolve",
        "errors": {...additional details...}
    }
    """
    logger.error(
        "ecp_error_occurred",
        error_code=exc.error_code,
        error=exc.message,
        http_status=exc.http_status,
        path=str(request.url.path),
        details=exc.details,
    )

    # Record error metric
    metrics.record_error(
        error_type=exc.error_code,
        component="api",
    )

    # Check if services are degraded
    degraded_services = DegradationMode.get_degraded_services()

    # Build RFC 7807 Problem Details response
    problem = {
        "type": f"https://api.enterprise-context.com/errors/{exc.error_code}",
        "title": exc.error_code.replace("_", " ").title(),
        "status": exc.http_status,
        "detail": exc.message,
        "instance": str(request.url.path),
    }

    # Add additional details if present
    if exc.details:
        problem["errors"] = exc.details

    # Add degradation notice if services are degraded
    if degraded_services:
        problem["degraded_services"] = degraded_services
        problem["degradation_notice"] = "Some services are experiencing issues. Results may be incomplete."

    return JSONResponse(
        status_code=exc.http_status,
        content=problem,
        headers={"Content-Type": "application/problem+json"},
    )


# Middleware - order matters (last added = first executed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(ObservabilityMiddleware)


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

    logger.info("resolve_request", concept=concept, user_context=user_ctx)

    start_time = time.time()
    orch = app.state.orchestrator

    try:
        response = await orch.resolve(request)
        duration = time.time() - start_time

        # Record metrics
        metrics.record_resolve(
            status=response.status,
            duration=duration,
            confidence=response.confidence_score,
        )

        logger.info(
            "resolve_completed",
            resolution_id=response.resolution_id,
            status=response.status,
            confidence=response.confidence_score,
            duration_seconds=duration,
        )

        return response.model_dump()

    except Exception as e:
        duration = time.time() - start_time
        metrics.record_resolve(status="error", duration=duration)
        logger.error("resolve_failed", error=str(e), error_type=type(e).__name__, exc_info=True)
        raise


@app.post("/api/v1/execute", response_model=dict)
async def execute(body: dict[str, Any]) -> dict:
    """Execute a previously resolved metric query."""
    resolution_id = body.get("resolution_id")
    if not resolution_id:
        raise HTTPException(status_code=400, detail="resolution_id is required")

    params = body.get("parameters") or {}
    logger.info("execute_request", resolution_id=resolution_id, parameters=params)

    start_time = time.time()
    orch = app.state.orchestrator

    try:
        result = await orch.execute(resolution_id, params)
        duration = time.time() - start_time

        # Determine status from result
        status = "not_found" if result.get("warnings") else "success"
        metrics.record_execute(status=status, duration=duration)

        logger.info(
            "execute_completed",
            resolution_id=resolution_id,
            status=status,
            duration_seconds=duration,
        )

        return result

    except Exception as e:
        duration = time.time() - start_time
        metrics.record_execute(status="error", duration=duration)
        logger.error("execute_failed", error=str(e), error_type=type(e).__name__, exc_info=True)
        raise


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
    except Exception as e:
        stores["graph"] = False
        logger.warning("health_check_failed", store="graph", error=str(e))

    try:
        stores["vector"] = await orch._vector.health()
    except Exception as e:
        stores["vector"] = False
        logger.warning("health_check_failed", store="vector", error=str(e))

    try:
        stores["registry"] = await orch._registry.health()
    except Exception as e:
        stores["registry"] = False
        logger.warning("health_check_failed", store="registry", error=str(e))

    try:
        stores["semantic"] = await orch._semantic.health()
    except Exception as e:
        stores["semantic"] = False
        logger.warning("health_check_failed", store="semantic", error=str(e))

    try:
        stores["policy"] = await orch._policy.health()
    except Exception as e:
        stores["policy"] = False
        logger.warning("health_check_failed", store="policy", error=str(e))

    status = "ok" if all(stores.values()) else "degraded"
    return {"status": status, "stores": stores}


@app.get("/metrics")
async def prometheus_metrics() -> PlainTextResponse:
    """Prometheus metrics endpoint.

    Returns metrics in Prometheus text format for scraping.
    """
    return PlainTextResponse(
        generate_latest(),
        media_type=CONTENT_TYPE_LATEST,
    )
