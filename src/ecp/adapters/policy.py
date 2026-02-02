"""OPA policy engine adapter."""

from typing import Any

import httpx

from ecp.adapters.base import PolicyEngine
from ecp.config import settings


class OPAEngine(PolicyEngine):
    def __init__(self, base_url: str | None = None, policy_path: str | None = None) -> None:
        self._base_url = (base_url or settings.opa_url).rstrip("/")
        self._policy_path = policy_path or settings.opa_policy_path

    async def evaluate(self, user: dict[str, Any], action: str, data_product: dict[str, Any]) -> dict[str, Any]:
        path = self._policy_path.replace(".", "/")
        input_doc = {"user": user, "action": action, "data_product": data_product}
        async with httpx.AsyncClient(timeout=10.0) as client:
            r = await client.post(
                f"{self._base_url}/data/{path}",
                json={"input": input_doc},
            )
            r.raise_for_status()
            data = r.json()
            return data.get("result", data)

    async def health(self) -> bool:
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                r = await client.get(f"{self._base_url.replace('/v1', '')}/health")
                return r.status_code == 200
        except Exception:
            return False
