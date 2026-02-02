"""pgvector store adapter - semantic search over glossary and tribal knowledge."""

from typing import Any

import asyncpg

from ecp.adapters.base import VectorStore
from ecp.config import settings


class PgVectorStore(VectorStore):
    def __init__(self, connection_string: str | None = None) -> None:
        self._conn_str = connection_string or settings.pgvector_connection_string
        self._pool: asyncpg.Pool | None = None

    async def _get_pool(self) -> asyncpg.Pool:
        if self._pool is None:
            self._pool = await asyncpg.create_pool(self._conn_str, min_size=1, max_size=5)
        return self._pool

    async def close(self) -> None:
        if self._pool:
            await self._pool.close()
            self._pool = None

    async def search(self, query_text: str, type_filter: str | None = None, top_k: int = 5) -> list[dict[str, Any]]:
        pool = await self._get_pool()
        # Simple text match for demo (no embedding of query_text); in prod use query embedding and similarity search.
        # For deterministic demo we return by type_filter or all.
        async with pool.acquire() as conn:
            if type_filter:
                rows = await conn.fetch(
                    "SELECT id, type, content_text, metadata FROM embeddings WHERE type = $1 LIMIT $2",
                    type_filter,
                    top_k,
                )
            else:
                rows = await conn.fetch(
                    "SELECT id, type, content_text, metadata FROM embeddings WHERE content_text ILIKE $1 LIMIT $2",
                    f"%{query_text}%",
                    top_k,
                )
            if not rows and not type_filter:
                rows = await conn.fetch("SELECT id, type, content_text, metadata FROM embeddings LIMIT $1", top_k)
            return [
                {
                    "id": r["id"],
                    "type": r["type"],
                    "content_text": r["content_text"],
                    "metadata": dict(r["metadata"]) if r["metadata"] else {},
                    "score": 0.85,
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
