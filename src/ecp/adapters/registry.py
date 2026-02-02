"""PostgreSQL Asset Registry adapter."""

from typing import Any

import asyncpg

from ecp.adapters.base import AssetRegistry
from ecp.config import settings


class PostgresAssetRegistry(AssetRegistry):
    def __init__(self, database_url: str | None = None) -> None:
        url = database_url or settings.sync_registry_url
        if "+asyncpg" in url:
            url = url.replace("postgresql+asyncpg", "postgresql")
        self._url = url
        self._pool: asyncpg.Pool | None = None

    async def _get_pool(self) -> asyncpg.Pool:
        if self._pool is None:
            self._pool = await asyncpg.create_pool(self._url, min_size=1, max_size=5)
        return self._pool

    async def close(self) -> None:
        if self._pool:
            await self._pool.close()
            self._pool = None

    async def get_asset(self, asset_id: str) -> dict[str, Any] | None:
        pool = await self._get_pool()
        async with pool.acquire() as conn:
            row = await conn.fetchrow(
                "SELECT id, type, content, metadata FROM assets WHERE id = $1",
                asset_id,
            )
            if not row:
                return None
            return {
                "id": row["id"],
                "type": row["type"],
                "content": dict(row["content"]) if row["content"] else {},
                "metadata": dict(row["metadata"]) if row["metadata"] else {},
            }

    async def get_assets_by_type(self, asset_type: str, limit: int = 100) -> list[dict[str, Any]]:
        pool = await self._get_pool()
        async with pool.acquire() as conn:
            rows = await conn.fetch(
                "SELECT id, type, content, metadata FROM assets WHERE type = $1 ORDER BY id LIMIT $2",
                asset_type,
                limit,
            )
            return [
                {
                    "id": r["id"],
                    "type": r["type"],
                    "content": dict(r["content"]) if r["content"] else {},
                    "metadata": dict(r["metadata"]) if r["metadata"] else {},
                }
                for r in rows
            ]

    async def search_glossary(self, query: str, domain: str | None = None, limit: int = 10) -> list[dict[str, Any]]:
        pool = await self._get_pool()
        async with pool.acquire() as conn:
            if domain:
                rows = await conn.fetch(
                    """
                    SELECT id, type, content, metadata FROM assets
                    WHERE type = 'glossary_term' AND (metadata->>'domain') = $1
                    AND (content->>'canonical_name' ILIKE $2 OR content->>'definition' ILIKE $2)
                    ORDER BY id LIMIT $3
                    """,
                    domain,
                    f"%{query}%",
                    limit,
                )
            else:
                rows = await conn.fetch(
                    """
                    SELECT id, type, content, metadata FROM assets
                    WHERE type = 'glossary_term'
                    AND (content->>'canonical_name' ILIKE $1 OR content->>'definition' ILIKE $1)
                    ORDER BY id LIMIT $2
                    """,
                    f"%{query}%",
                    limit,
                )
            return [
                {
                    "id": r["id"],
                    "type": r["type"],
                    "content": dict(r["content"]) if r["content"] else {},
                    "metadata": dict(r["metadata"]) if r["metadata"] else {},
                }
                for r in rows
            ]

    async def health(self) -> bool:
        try:
            pool = await self._get_pool()
            async with pool.acquire() as conn:
                await conn.fetchval("SELECT 1")
            return True
        except Exception:
            return False
