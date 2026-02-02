"""Unit tests for Resolution Orchestrator with mocked adapters."""

import pytest

from ecp.domain.models import ResolveRequest, UserContext
from ecp.orchestrator import ResolutionOrchestrator


@pytest.mark.asyncio
async def test_resolve_returns_resolution_id_and_plan(
    orchestrator: ResolutionOrchestrator,
    resolve_request: ResolveRequest,
) -> None:
    response = await orchestrator.resolve(resolve_request)
    assert response.resolution_id
    assert response.status == "complete"
    assert response.execution_plan is not None
    assert response.execution_plan.plan_type == "metric_query"
    assert len(response.execution_plan.queries) >= 1
    assert response.resolved_concepts.get("metric") or response.resolved_concepts.get("region")
    assert response.confidence_score > 0


@pytest.mark.asyncio
async def test_resolve_denied_when_policy_denies(
    mock_graph: object,
    mock_vector: object,
    mock_registry: object,
    mock_semantic: object,
    resolve_request: ResolveRequest,
) -> None:
    from unittest.mock import AsyncMock
    from ecp.adapters.base import PolicyEngine
    deny_policy = AsyncMock(spec=PolicyEngine)
    deny_policy.evaluate.return_value = {"allow": False}
    deny_policy.health.return_value = True
    orch = ResolutionOrchestrator(
        graph=mock_graph,
        vector=mock_vector,
        registry=mock_registry,
        semantic=mock_semantic,
        policy=deny_policy,
    )
    response = await orch.resolve(resolve_request)
    assert response.status == "access_denied"
    assert response.warnings


@pytest.mark.asyncio
async def test_execute_after_resolve(
    orchestrator: ResolutionOrchestrator,
    resolve_request: ResolveRequest,
) -> None:
    resolve_response = await orchestrator.resolve(resolve_request)
    assert resolve_response.status == "complete"
    result = await orchestrator.execute(resolve_response.resolution_id, {})
    assert "results" in result
    assert result["confidence_score"] > 0


@pytest.mark.asyncio
async def test_execute_unknown_resolution_id_returns_warning(
    orchestrator: ResolutionOrchestrator,
) -> None:
    result = await orchestrator.execute("unknown-id", {})
    assert result["warnings"]
    assert "not found" in str(result["warnings"]).lower() or "expired" in str(result["warnings"]).lower()
