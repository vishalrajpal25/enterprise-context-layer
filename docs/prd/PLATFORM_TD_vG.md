# Cogentiq Studio: Technical Implementation Specification

**Target Audience:** Senior Engineering / AI Coding Assistants
**Goal:** Scaffold a production-ready, domain-agnostic Logic Control Plane.

---

# 1. SYSTEM ARCHITECTURE & TECH STACK

## 1.1 Core Stack
* **Language:** Python 3.11+ (Strict Typing with `mypy`).
* **API Framework:** FastAPI (Async/Await).
* **ORM/Database:** SQLAlchemy 2.0 (Async) + Alembic (Migrations).
* **Graph DB:** Neo4j 5.x (using `neo4j-driver`).
* **Task Queue:** Celery + Redis (for Ingestion/Drift jobs).
* **Logic Engine:** Google CEL (`cel-python`) for high-performance constraint evaluation.
* **LLM Interface:** `litellm` (Abstraction layer for OpenAI/Azure/Bedrock).

## 1.2 Microservices Architecture
1.  **`cogentiq-api`**: Stateless REST API for runtime decisions and management.
2.  **`cogentiq-worker`**: Background worker for heavy lifting (Harvester, Drift Monitor).
3.  **`cogentiq-brain`**: Library code shared between API/Worker containing the Router & Semantic Logic.

---

# 2. DIRECTORY STRUCTURE

```text
/cogentiq-platform
├── /app
│   ├── /api              # API Routes (v1)
│   │   ├── /runtime      # /decide endpoints
│   │   ├── /ontology     # CRUD for definitions
│   │   └── /harvest      # Ingestion triggers
│   ├── /core             # Config, Security, Logging
│   ├── /db               # Database setup
│   │   ├── /models       # SQLAlchemy models (Postgres)
│   │   └── /graph        # Neo4j Cypher queries
│   ├── /engine           # THE BRAIN (Logic Layer)
│   │   ├── router.py     # Neuro-Symbolic Router
│   │   ├── semantic.py   # Metric Compilation Logic
│   │   ├── constraints.py# CEL Evaluation
│   │   └── context.py    # Session/Entity Resolution
│   ├── /adapters         # MCP Implementation
│   │   ├── base.py       # Interface Definition
│   │   ├── snowflake.py
│   │   └── databricks.py
│   └── main.py           # App Entrypoint
├── /worker               # Celery Workers
│   ├── tasks.py          # Task definitions
│   └── harvester.py      # Ingestion Logic
├── /tests                # Pytest Suite
├── /alembic              # DB Migrations
├── docker-compose.yml
└── requirements.txt
3. DATABASE SCHEMA SPECIFICATION (PostgreSQL)
Use this schema to generate SQLAlchemy models.

SQL

-- Multi-tenancy Root
CREATE TABLE tenants (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    config JSONB DEFAULT '{}', -- Feature flags
    created_at TIMESTAMP DEFAULT NOW()
);

-- Domain Intelligence (Ontology)
CREATE TABLE ontology_classes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID REFERENCES tenants(id),
    namespace VARCHAR(255) NOT NULL, -- e.g., 'cogentiq.finance'
    name VARCHAR(255) NOT NULL,
    definition JSONB NOT NULL, -- { "attributes": [...], "relations": [...] }
    version VARCHAR(50) NOT NULL,
    status VARCHAR(20) DEFAULT 'draft', -- 'draft', 'published', 'deprecated'
    UNIQUE(tenant_id, namespace, name, version)
);

-- Semantic Catalog (Metrics)
CREATE TABLE metrics (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID REFERENCES tenants(id),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    formula TEXT NOT NULL, -- Jinja2 template: "{{gross_sales}} - {{discounts}}"
    dimensions JSONB, -- List of compatible dimension IDs
    data_source_uri VARCHAR(500), -- "snowflake://db/schema/table"
    constraints JSONB, -- List of CEL expressions
    version VARCHAR(50),
    UNIQUE(tenant_id, name, version)
);

-- Governance (Schema Drift)
CREATE TABLE drift_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    metric_id UUID REFERENCES metrics(id),
    check_timestamp TIMESTAMP DEFAULT NOW(),
    status VARCHAR(20), -- 'PASS', 'FAIL'
    error_details TEXT
);

-- Lineage & Audit
CREATE TABLE lineage_records (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID REFERENCES tenants(id),
    trace_id VARCHAR(255),
    input_query TEXT,
    router_decision VARCHAR(50), -- 'SYMBOLIC', 'NEURAL'
    metric_used_id UUID,
    output_snapshot JSONB, -- Store small results only
    execution_time_ms INTEGER
);
4. CORE MODULE IMPLEMENTATION DETAILS
4.1 The Neuro-Symbolic Router (app/engine/router.py)
Algorithm:

Extract Intent: Use a fast LLM (GPT-3.5-Turbo/Haiku) to extract entities and intent from the query.

Graph Lookup: Query Neo4j to see if extracted entities map to known Ontology Classes or Metrics.

Score Confidence:

If Mapping_Confidence > 0.8 AND Metric_Exists -> SYMBOLIC Path.

If Mapping_Confidence < 0.5 -> NEURAL Path (RAG).

Else -> AMBIGUOUS Path (Trigger clarification).

Python

# Pseudo-code for Router Logic
async def route_query(query: str, tenant_id: str) -> RoutingDecision:
    intent = await llm.extract_intent(query)
    
    # Check Graph for Entity Matches
    matches = await graph_service.match_entities(intent.entities, tenant_id)
    
    # Calculate coverage
    matched_count = len([m for m in matches if m.score > 0.8])
    coverage = matched_count / len(intent.entities) if intent.entities else 0

    if coverage >= 0.8 and intent.type == "CALCULATION":
        return RoutingDecision(path=PathType.SYMBOLIC, plan=...)
    elif coverage < 0.4:
        return RoutingDecision(path=PathType.NEURAL, plan=...)
    else:
        return RoutingDecision(path=PathType.AMBIGUOUS, plan=...)
4.2 The Semantic Compiler (app/engine/semantic.py)
Responsibility: Convert a Metric Definition into executable SQL.

Input: Metric ID (net_revenue), Filters (quarter='Q3').

Process:

Fetch Metric definition from DB.

Resolve dependencies (if formula uses other metrics, resolve recursively).

Inject into Jinja2 SQL template based on Adapter Dialect (Snowflake vs Databricks).

Apply RLS filters (Row Level Security).

4.3 The Harvester Worker (worker/harvester.py)
Responsibility: Ingest legacy schemas.

Dependency: sqlglot (for SQL parsing).

Workflow:

Connect: Use MCP adapter credentials.

Scan: Query INFORMATION_SCHEMA.

Profile: Execute lightweight agg queries (COUNT DISTINCT, MIN/MAX) to understand column data shapes.

Infer: Send Schema + Profile Stats to LLM to generate OntologyClass candidates.

Persist: Save to DB with status='draft'.

5. API SPECIFICATION (OpenAPI)
5.1 Runtime API (POST /v1/runtime/decide)
Request:

JSON

{
  "tenant_id": "uuid",
  "session_id": "uuid",
  "query": "What is the Net Revenue for Q3?",
  "user_context": { "role": "analyst", "region": "US-East" }
}
Response (Symbolic Path):

JSON

{
  "path": "SYMBOLIC",
  "decision_id": "uuid",
  "actions": [
    {
      "tool": "execute_sql",
      "args": {
        "sql": "SELECT SUM(amount) ...",
        "connection_id": "snowflake_prod"
      }
    }
  ],
  "reasoning": "Mapped 'Net Revenue' to metric 'finance.net_rev_v2'."
}
6. DEVELOPER EXPERIENCE (CLI)
The CLI interacts with the API to manage the lifecycle.

cogentiq init: Create a local cogentiq.yaml config.

cogentiq pull: Fetch ontology definitions to local YAML files.

cogentiq push: Upload local YAML changes to the platform (Draft mode).

cogentiq test: Run a suite of regression questions against the current logic.

7. CODING GUIDELINES FOR AI ASSISTANT
Type Safety: All function signatures must be fully typed. Use pydantic for all data transfer objects.

Async First: All I/O bound operations (DB, LLM, External API) must be async.

Error Handling: Use custom exception classes mapped to HTTP status codes. Never leak stack traces in API responses.

Configuration: Use pydantic-settings to manage environment variables (.env).

Testing: Every module requires a corresponding pytest file in /tests. Use testcontainers for DB/Graph integration tests.