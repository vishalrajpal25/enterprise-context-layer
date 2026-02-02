"""E2E tests - run against local API with synthetic data (optional)."""

import os
import pytest

import httpx

BASE_URL = os.environ.get("ECP_E2E_URL", "http://localhost:8000")
SKIP_E2E = os.environ.get("SKIP_E2E", "1")  # Set SKIP_E2E=0 to run E2E when API is up


@pytest.mark.skipif(SKIP_E2E == "1", reason="E2E skipped by default; set SKIP_E2E=0 and run API")
@pytest.mark.asyncio
async def test_e2e_resolve_and_execute() -> None:
    async with httpx.AsyncClient(timeout=30.0, base_url=BASE_URL) as client:
        r = await client.post(
            "/api/v1/resolve",
            json={
                "concept": "APAC revenue last quarter",
                "user_context": {"department": "finance", "role": "analyst"},
            },
        )
        assert r.status_code == 200
        data = r.json()
        assert "resolution_id" in data
        assert data.get("status") in ("complete", "access_denied")
        if data.get("status") != "complete":
            return
        resolution_id = data["resolution_id"]
        r2 = await client.post("/api/v1/execute", json={"resolution_id": resolution_id})
        assert r2.status_code == 200
        exec_data = r2.json()
        assert "results" in exec_data
        assert "provenance" in exec_data


@pytest.mark.skipif(SKIP_E2E == "1", reason="E2E skipped by default")
@pytest.mark.asyncio
async def test_e2e_glossary_lineage_metrics() -> None:
    async with httpx.AsyncClient(timeout=10.0, base_url=BASE_URL) as client:
        r = await client.get("/api/v1/glossary", params={"query": "revenue"})
        assert r.status_code == 200
        assert "terms" in r.json()
        r = await client.get("/api/v1/lineage", params={"target": "net_revenue"})
        assert r.status_code == 200
        assert "target" in r.json()
        r = await client.get("/api/v1/metrics", params={"dimension": "region"})
        assert r.status_code == 200
        assert "metrics" in r.json()
