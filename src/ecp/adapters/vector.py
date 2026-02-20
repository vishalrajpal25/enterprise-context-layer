"""pgvector store adapter with retry protection - semantic search over glossary and tribal knowledge."""

import asyncio
from typing import Any

import asyncpg

from ecp.adapters.base import VectorStore
from ecp.config import settings
from ecp.observability import get_logger
from ecp.resilience import with_retry
from ecp.resilience.degradation import DegradationMode, keyword_search_fallback
from ecp.resilience.exceptions import StoreConnectionError, StoreTimeoutError

logger = get_logger(__name__)


class PgVectorStore(VectorStore):
    """pgvector store with resilience patterns.

    Features:
    - Automatic retry on transient failures
    - Connection pooling
    - Graceful degradation with keyword fallback
    """

    def __init__(self, connection_string: str | None = None) -> None:
        self._conn_str = connection_string or settings.pgvector_connection_string
        self._pool: asyncpg.Pool | None = None

    async def _get_pool(self) -> asyncpg.Pool:
        if self._pool is None:
            try:
                self._pool = await asyncpg.create_pool(
                    self._conn_str,
                    min_size=1,
                    max_size=5,
                    timeout=10.0,
                )
            except Exception as e:
                logger.error("pgvector_pool_creation_failed", error=str(e))
                raise StoreConnectionError("pgvector", str(e)) from e
        return self._pool

    async def close(self) -> None:
        if self._pool:
            await self._pool.close()
            self._pool = None

    @with_retry(max_attempts=3, store_name="pgvector")
    async def search(
        self,
        query_text: str,
        type_filter: str | None = None,
        top_k: int = 5,
    ) -> list[dict[str, Any]]:
        """Search for similar embeddings with retry protection.

        Args:
            query_text: Query text
            type_filter: Optional type filter (e.g., "glossary_term")
            top_k: Number of results to return

        Returns:
            List of search results with scores

        Raises:
            StoreConnectionError: If cannot connect to pgvector
            StoreTimeoutError: If query times out
        """
        try:
            pool = await self._get_pool()
            # Simple text match for demo (no embedding of query_text)
            # In production: use query embedding and similarity search
            async with pool.acquire(timeout=5.0) as conn:
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
                    rows = await conn.fetch(
                        "SELECT id, type, content_text, metadata FROM embeddings LIMIT $1",
                        top_k,
                    )

                # Mark as recovered if it was degraded
                if DegradationMode.is_degraded("pgvector"):
                    DegradationMode.mark_recovered("pgvector")

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
        except asyncpg.PostgresConnectionError as e:
            logger.error("pgvector_connection_error", error=str(e))
            raise StoreConnectionError("pgvector", str(e)) from e
        except asyncio.TimeoutError as e:
            logger.error("pgvector_timeout", error=str(e))
            raise StoreTimeoutError("pgvector", "search", 5.0) from e
        except Exception as e:
            # Other errors - mark degraded and use fallback
            logger.error(
                "pgvector_search_failed",
                query=query_text,
                error=str(e),
                error_type=type(e).__name__,
            )
            DegradationMode.mark_degraded("pgvector", str(e))
            # Use keyword fallback
            return keyword_search_fallback(query_text, top_k)

    async def health(self) -> bool:
        """Check if pgvector is healthy.

        Returns:
            True if healthy, False otherwise
        """
        try:
            pool = await self._get_pool()
            async with pool.acquire(timeout=2.0) as conn:
                await conn.fetchval("SELECT 1")
            return True
        except Exception as e:
            logger.debug("pgvector_health_check_failed", error=str(e))
            return False
