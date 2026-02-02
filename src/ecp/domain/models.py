"""Domain models - request/response and resolution DAG."""

from typing import Any

from pydantic import BaseModel, Field


class UserContext(BaseModel):
    user_id: str | None = None
    department: str | None = None
    role: str | None = None
    allowed_regions: list[str] | None = None


class ResolveRequest(BaseModel):
    concept: str
    user_context: UserContext | None = None


class ExecutionPlan(BaseModel):
    plan_type: str = "metric_query"
    queries: list[dict[str, Any]] = Field(default_factory=list)
    computation: dict[str, str] | None = None


class ResolveResponse(BaseModel):
    resolution_id: str
    status: str = "complete"
    execution_plan: ExecutionPlan | None = None
    resolved_concepts: dict[str, Any] = Field(default_factory=dict)
    confidence_score: float = 0.0
    provenance: dict[str, Any] = Field(default_factory=dict)
    warnings: list[dict[str, Any]] = Field(default_factory=list)


class ExecuteRequest(BaseModel):
    resolution_id: str
    parameters: dict[str, Any] | None = None


class ExecuteResponse(BaseModel):
    results: dict[str, Any] = Field(default_factory=dict)
    provenance: dict[str, Any] = Field(default_factory=dict)
    confidence_score: float = 0.0
    warnings: list[dict[str, Any]] = Field(default_factory=list)


class DAGNode(BaseModel):
    id: str
    type: str
    status: str = "pending"
    depends_on: list[str] = Field(default_factory=list)
    output: dict[str, Any] | None = None


class ResolutionDAG(BaseModel):
    query_id: str
    user_context: dict[str, Any] = Field(default_factory=dict)
    original_query: str = ""
    nodes: list[DAGNode] = Field(default_factory=list)
