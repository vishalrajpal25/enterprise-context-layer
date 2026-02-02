"""Abstract interfaces for store adapters - swap and mock in tests."""

from abc import ABC, abstractmethod
from typing import Any


class GraphStore(ABC):
    """Knowledge graph - entities, metrics, lineage."""

    @abstractmethod
    async def get_metric_by_id(self, metric_id: str) -> dict[str, Any] | None:
        """Return metric node and refs or None."""
        ...

    @abstractmethod
    async def resolve_region(self, region_code: str, context: str | None) -> dict[str, Any] | None:
        """Resolve region (e.g. APAC) to variation (countries list)."""
        ...

    @abstractmethod
    async def get_lineage(self, target: str, depth: int = 3) -> dict[str, Any]:
        """Return lineage graph (nodes, edges) for metric or table."""
        ...

    @abstractmethod
    async def list_metrics_for_dimension(self, dimension: str, domain: str | None, certification_tier: int | None) -> list[dict[str, Any]]:
        """List metrics that have the given dimension."""
        ...

    @abstractmethod
    async def health(self) -> bool:
        """Health check."""
        ...


class VectorStore(ABC):
    """Semantic index - glossary and tribal knowledge search."""

    @abstractmethod
    async def search(self, query_text: str, type_filter: str | None = None, top_k: int = 5) -> list[dict[str, Any]]:
        """Semantic search; return list of {id, type, content_text, metadata, score}."""
        ...

    @abstractmethod
    async def health(self) -> bool:
        """Health check."""
        ...


class AssetRegistry(ABC):
    """Structured artifact storage - glossary, contracts, tribal knowledge."""

    @abstractmethod
    async def get_asset(self, asset_id: str) -> dict[str, Any] | None:
        """Return asset by id (content + metadata) or None."""
        ...

    @abstractmethod
    async def get_assets_by_type(self, asset_type: str, limit: int = 100) -> list[dict[str, Any]]:
        """Return assets of given type."""
        ...

    @abstractmethod
    async def search_glossary(self, query: str, domain: str | None = None, limit: int = 10) -> list[dict[str, Any]]:
        """Search glossary terms (e.g. by canonical_name or definition)."""
        ...

    @abstractmethod
    async def health(self) -> bool:
        """Health check."""
        ...


class SemanticLayerClient(ABC):
    """Executable metric queries - Cube/dbt semantic layer."""

    @abstractmethod
    async def execute_query(self, measure: str, dimensions: list[str], filters: dict[str, Any]) -> dict[str, Any]:
        """Run metric query; return {data, annotation}."""
        ...

    @abstractmethod
    async def health(self) -> bool:
        """Health check."""
        ...


class PolicyEngine(ABC):
    """Runtime policy evaluation - access control."""

    @abstractmethod
    async def evaluate(self, user: dict[str, Any], action: str, data_product: dict[str, Any]) -> dict[str, Any]:
        """Evaluate policy; return {allow: bool, ...}."""
        ...

    @abstractmethod
    async def health(self) -> bool:
        """Health check."""
        ...
