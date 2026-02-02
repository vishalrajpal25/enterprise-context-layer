"""Contract tests - API response shape matches OpenAPI/expectations."""

from unittest.mock import AsyncMock, patch

import pytest
from fastapi.testclient import TestClient

from api.main import app
from ecp.adapters.base import AssetRegistry, GraphStore, PolicyEngine, SemanticLayerClient, VectorStore


@pytest.fixture
def mock_stores():
    graph = AsyncMock(spec=GraphStore)
    graph.get_metric_by_id.return_value = {"id": "net_revenue", "semantic_layer_ref": "Revenue.netRevenue"}
    graph.resolve_region.return_value = {"region_code": "APAC", "countries": ["JP", "KR", "SG"]}
    graph.get_lineage.return_value = {"target": "net_revenue", "nodes": [], "edges": []}
    graph.list_metrics_for_dimension.return_value = [{"id": "net_revenue", "name": "Net Revenue"}]
    graph.health.return_value = True

    vector = AsyncMock(spec=VectorStore)
    vector.search.return_value = [{"id": "vec_g_001", "type": "glossary_term", "metadata": {"term": "net_revenue"}}]
    vector.health.return_value = True

    registry = AsyncMock(spec=AssetRegistry)
    registry.get_asset.return_value = {"id": "ar_cal_001", "content": {"calendar_type": "fiscal"}}
    registry.search_glossary.return_value = [{"id": "ar_g_001", "content": {"canonical_name": "revenue"}, "metadata": {}}]
    registry.health.return_value = True

    semantic = AsyncMock(spec=SemanticLayerClient)
    semantic.execute_query.return_value = {"data": [{"Revenue.netRevenue": 142300000}]}
    semantic.health.return_value = True

    policy = AsyncMock(spec=PolicyEngine)
    policy.evaluate.return_value = {"allow": True}
    policy.health.return_value = True

    return {"graph": graph, "vector": vector, "registry": registry, "semantic": semantic, "policy": policy}


@pytest.fixture
def client(mock_stores):
    with patch("api.main._create_orchestrator") as m:
        from ecp.orchestrator import ResolutionOrchestrator
        orch = ResolutionOrchestrator(
            graph=mock_stores["graph"],
            vector=mock_stores["vector"],
            registry=mock_stores["registry"],
            semantic=mock_stores["semantic"],
            policy=mock_stores["policy"],
        )
        m.return_value = orch
        with TestClient(app) as c:
            yield c


def test_resolve_contract(client: TestClient) -> None:
    r = client.post(
        "/api/v1/resolve",
        json={"concept": "APAC revenue last quarter", "user_context": {"department": "finance"}},
    )
    assert r.status_code == 200
    data = r.json()
    assert "resolution_id" in data
    assert "status" in data
    assert data.get("status") in ("complete", "access_denied")
    if data["status"] == "complete":
        assert "execution_plan" in data
        assert "resolved_concepts" in data
        assert "confidence_score" in data


def test_execute_contract(client: TestClient) -> None:
    resolve_r = client.post(
        "/api/v1/resolve",
        json={"concept": "APAC revenue last quarter"},
    )
    assert resolve_r.status_code == 200
    resolution_id = resolve_r.json().get("resolution_id")
    if not resolution_id or resolve_r.json().get("status") != "complete":
        return
    r = client.post("/api/v1/execute", json={"resolution_id": resolution_id})
    assert r.status_code == 200
    data = r.json()
    assert "results" in data
    assert "provenance" in data
    assert "confidence_score" in data


def test_glossary_contract(client: TestClient) -> None:
    r = client.get("/api/v1/glossary", params={"query": "revenue"})
    assert r.status_code == 200
    data = r.json()
    assert "terms" in data
    assert "total" in data
    assert isinstance(data["terms"], list)


def test_lineage_contract(client: TestClient) -> None:
    r = client.get("/api/v1/lineage", params={"target": "net_revenue"})
    assert r.status_code == 200
    data = r.json()
    assert "target" in data
    assert "nodes" in data
    assert "edges" in data


def test_metrics_contract(client: TestClient) -> None:
    r = client.get("/api/v1/metrics", params={"dimension": "region"})
    assert r.status_code == 200
    data = r.json()
    assert "metrics" in data
    assert "total" in data


def test_health_contract(client: TestClient) -> None:
    r = client.get("/api/v1/health")
    assert r.status_code == 200
    data = r.json()
    assert "status" in data
    assert "stores" in data
