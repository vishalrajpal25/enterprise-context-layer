"""MCP Server - five tools delegating to ECP REST API."""

import os
from typing import Any

import httpx

try:
    from mcp.server.mcpserver import MCPServer
    mcp = MCPServer("enterprise-context-platform")
    _MCP_AVAILABLE = True
except ImportError:
    mcp = None
    _MCP_AVAILABLE = False

API_BASE = os.environ.get("ECP_API_URL", "http://localhost:8000")


def _post(path: str, json: dict[str, Any]) -> dict[str, Any]:
    with httpx.Client(timeout=30.0) as client:
        r = client.post(f"{API_BASE}{path}", json=json)
        r.raise_for_status()
        return r.json()


def _get(path: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
    with httpx.Client(timeout=30.0) as client:
        r = client.get(f"{API_BASE}{path}", params=params or {})
        r.raise_for_status()
        return r.json()


if _MCP_AVAILABLE and mcp is not None:

    @mcp.tool()
    def resolve_business_concept(concept: str, user_context: dict[str, Any] | None = None) -> dict[str, Any]:
        """Resolve a business concept (metric, dimension, entity) to its canonical definition and execution plan."""
        return _post("/api/v1/resolve", {"concept": concept, "user_context": user_context or {}})

    @mcp.tool()
    def execute_metric_query(resolution_id: str, parameters: dict[str, Any] | None = None) -> dict[str, Any]:
        """Execute a metric query using a previously resolved execution plan. Returns results with full provenance."""
        return _post("/api/v1/execute", {"resolution_id": resolution_id, "parameters": parameters or {}})

    @mcp.tool()
    def query_glossary(query: str, domain: str | None = None) -> dict[str, Any]:
        """Search the business glossary for term definitions."""
        return _get("/api/v1/glossary", {"query": query, "domain": domain})

    @mcp.tool()
    def get_lineage(target: str, depth: int = 3) -> dict[str, Any]:
        """Get data lineage for a metric or table."""
        return _get("/api/v1/lineage", {"target": target, "depth": depth})

    @mcp.tool()
    def list_available_metrics(
        dimension: str | None = None,
        domain: str | None = None,
        certification_tier: int | None = None,
    ) -> dict[str, Any]:
        """List metrics available for a given dimension or domain."""
        params: dict[str, Any] = {}
        if dimension:
            params["dimension"] = dimension
        if domain:
            params["domain"] = domain
        if certification_tier is not None:
            params["certification_tier"] = certification_tier
        return _get("/api/v1/metrics", params)


def run_mcp() -> None:
    """Run MCP server (stdio)."""
    if not _MCP_AVAILABLE or mcp is None:
        raise RuntimeError("MCP not available; install mcp package.")
    mcp.run()


if __name__ == "__main__":
    run_mcp()
