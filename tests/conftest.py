"""Pytest fixtures - mock adapters and orchestrator."""

from typing import Any
from unittest.mock import AsyncMock

import pytest

from ecp.adapters.base import (
    AssetRegistry,
    GraphStore,
    PolicyEngine,
    SemanticLayerClient,
    VectorStore,
)
from ecp.adapters.graph import Neo4jGraphStore
from ecp.adapters.policy import OPAEngine
from ecp.adapters.registry import PostgresAssetRegistry
from ecp.adapters.semantic import CubeClient
from ecp.adapters.vector import PgVectorStore
from ecp.domain.models import ResolveRequest, UserContext
from ecp.orchestrator import ResolutionOrchestrator


@pytest.fixture
def mock_graph() -> GraphStore:
    m = AsyncMock(spec=GraphStore)
    m.get_metric_by_id.return_value = {
        "id": "net_revenue",
        "semantic_layer_ref": "Revenue.netRevenue",
    }
    m.resolve_region.return_value = {"region_code": "APAC", "countries": ["JP", "KR", "SG"]}
    m.get_lineage.return_value = {"target": "net_revenue", "nodes": [], "edges": []}
    m.list_metrics_for_dimension.return_value = [{"id": "net_revenue", "name": "Net Revenue"}]
    m.health.return_value = True
    return m


@pytest.fixture
def mock_vector() -> VectorStore:
    m = AsyncMock(spec=VectorStore)
    m.search.return_value = [
        {"id": "vec_g_001", "type": "glossary_term", "metadata": {"term": "net_revenue"}, "score": 0.9},
    ]
    m.health.return_value = True
    return m


@pytest.fixture
def mock_registry() -> AssetRegistry:
    m = AsyncMock(spec=AssetRegistry)
    m.get_asset.return_value = {
        "id": "ar_cal_001",
        "content": {"calendar_type": "fiscal", "quarters": {"Q3": [10, 11, 12]}},
    }
    m.get_assets_by_type.return_value = []
    m.search_glossary.return_value = [{"id": "ar_g_003", "content": {"canonical_name": "net_revenue"}}]
    m.health.return_value = True
    return m


@pytest.fixture
def mock_semantic() -> SemanticLayerClient:
    m = AsyncMock(spec=SemanticLayerClient)
    m.execute_query.return_value = {"data": [{"Revenue.netRevenue": 142300000}], "annotation": {}}
    m.health.return_value = True
    return m


@pytest.fixture
def mock_policy() -> PolicyEngine:
    m = AsyncMock(spec=PolicyEngine)
    m.evaluate.return_value = {"allow": True}
    m.health.return_value = True
    return m


@pytest.fixture
def orchestrator(
    mock_graph: GraphStore,
    mock_vector: VectorStore,
    mock_registry: AssetRegistry,
    mock_semantic: SemanticLayerClient,
    mock_policy: PolicyEngine,
) -> ResolutionOrchestrator:
    return ResolutionOrchestrator(
        graph=mock_graph,
        vector=mock_vector,
        registry=mock_registry,
        semantic=mock_semantic,
        policy=mock_policy,
    )


@pytest.fixture
def resolve_request() -> ResolveRequest:
    return ResolveRequest(
        concept="APAC revenue last quarter",
        user_context=UserContext(department="finance", role="analyst"),
    )
