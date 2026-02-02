"""Cube semantic layer client."""

from typing import Any

import httpx

from ecp.adapters.base import SemanticLayerClient
from ecp.config import settings


class CubeClient(SemanticLayerClient):
    def __init__(self, base_url: str | None = None, token: str | None = None) -> None:
        self._base_url = (base_url or settings.cube_api_url).rstrip("/")
        self._token = token or settings.cube_api_token

    def _headers(self) -> dict[str, str]:
        h: dict[str, str] = {"Content-Type": "application/json"}
        if self._token:
            h["Authorization"] = self._token
        return h

    async def execute_query(self, measure: str, dimensions: list[str], filters: dict[str, Any]) -> dict[str, Any]:
        # Cube load API: /load with query
        measures = [measure] if isinstance(measure, str) else measure
        query: dict[str, Any] = {
            "measures": measures,
            "dimensions": dimensions,
            "timeDimensions": [],
        }
        if filters:
            query["filters"] = [
                {"member": k, "operator": "equals", "values": v if isinstance(v, list) else [v]}
                for k, v in filters.items()
            ]
        async with httpx.AsyncClient(timeout=30.0) as client:
            r = await client.post(
                f"{self._base_url}/load",
                json={"query": query},
                headers=self._headers(),
            )
            r.raise_for_status()
            return r.json()

    async def health(self) -> bool:
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                r = await client.get(f"{self._base_url.replace('/v1', '')}/readyz", headers=self._headers())
                return r.status_code == 200
        except Exception:
            return False
