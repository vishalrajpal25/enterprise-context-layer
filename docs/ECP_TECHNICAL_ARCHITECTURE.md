# Enterprise Context Platform: Technical Architecture
**Version:** 2.0 | **Audience:** Engineering & Architecture Teams | **Status:** Implementation-Ready

---

## 1. SYSTEM ARCHITECTURE

### 1.1 Component Stack

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        AGENT RUNTIME LAYER                              │
│          (Azure AI Foundry / Vertex AI / Bedrock / Custom)             │
│                   Agent makes tool/function calls                       │
└────────────────────────────┬────────────────────────────────────────────┘
                             │
                             │ MCP / REST / gRPC
                             │
┌────────────────────────────▼────────────────────────────────────────────┐
│                    RESOLUTION ORCHESTRATOR                              │
│                    (Python/FastAPI Service)                             │
│                                                                         │
│  ┌─────────────┐  ┌──────────────┐  ┌──────────────┐  ┌─────────────┐ │
│  │   Parser    │→ │   Resolver   │→ │   Executor   │→ │  Assembler  │ │
│  │  (Intent)   │  │ (Multi-Store)│  │   (Query)    │  │ (Provenance)│ │
│  └─────────────┘  └──────────────┘  └──────────────┘  └─────────────┘ │
│                                                                         │
│  State: Resolution DAG (Redis) | Cache: Query Results (Redis)          │
└─────────────────────────────────────────────────────────────────────────┘
                             │
          ┌──────────────────┼──────────────────┬─────────────────┐
          │                  │                  │                 │
          ▼                  ▼                  ▼                 ▼
┌──────────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│  Knowledge Graph │  │ Vector Store │  │Asset Registry│  │ Semantic     │
│   (Neo4j)        │  │ (Pinecone)   │  │(PostgreSQL)  │  │ Layer        │
│                  │  │              │  │              │  │ (Cube.js)    │
│ • Entities       │  │ • Embeddings │  │ • Glossary   │  │              │
│ • Relationships  │  │ • Semantic   │  │ • Contracts  │  │ • Metrics    │
│ • Lineage DAG    │  │   Search     │  │ • Tribal KB  │  │ • Dimensions │
│ • Ontology       │  │              │  │ • Policies   │  │ • Execution  │
└──────────────────┘  └──────────────┘  └──────────────┘  └──────┬───────┘
          │                  │                  │                 │
          └──────────────────┴──────────────────┴─────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                        PHYSICAL DATA ESTATE                             │
│           Snowflake / Databricks / SQL Server / Oracle / etc.          │
└─────────────────────────────────────────────────────────────────────────┘
```

### 1.2 Technology Stack

| Layer | Component | Technology | Port/Protocol | Purpose |
|-------|-----------|------------|---------------|---------|
| **API Gateway** | Load Balancer | Nginx/Envoy | 443/HTTPS | TLS termination, rate limiting |
| **Orchestration** | Resolution Service | Python 3.11 + FastAPI | 8080/HTTP | Core business logic |
| **Orchestration** | MCP Server | Node.js + MCP SDK | 3000/SSE | Agent integration |
| **Orchestration** | State Store | Redis 7.x | 6379/Redis | Session state, cache |
| **Context** | Knowledge Graph | Neo4j 5.x Enterprise | 7687/Bolt | Relationships, lineage |
| **Context** | Vector Store | Pinecone Serverless | HTTPS/gRPC | Semantic search |
| **Context** | Asset Registry | PostgreSQL 15 | 5432/PostgreSQL | Structured metadata |
| **Compute** | Semantic Layer | Cube.js 0.35+ | 4000/HTTP | Metric execution |
| **Policy** | Authorization | OPA 0.60+ | 8181/HTTP | Policy evaluation |
| **Monitoring** | Observability | Datadog/Prometheus | - | Metrics, traces, logs |

---

## 2. DATA MODELS

### 2.1 Knowledge Graph Schema (Neo4j)

```cypher
// Core entity types
(:Entity {
  id: string,              // e.g., "customer", "product", "region"
  name: string,
  domain: string,          // e.g., "sales", "finance", "operations"
  description: string,
  created_at: datetime,
  updated_at: datetime
})

(:Attribute {
  id: string,              // e.g., "customer.email", "product.sku"
  name: string,
  data_type: string,       // e.g., "string", "integer", "date"
  nullable: boolean,
  pii: boolean
})

(:Metric {
  id: string,              // e.g., "net_revenue", "customer_churn_rate"
  name: string,
  description: string,
  semantic_layer_ref: string,  // e.g., "cube.finance.Revenue.netRevenue"
  asset_registry_id: string,   // Reference to full definition
  certification_tier: integer, // 1-4
  owner: string
})

(:GlossaryTerm {
  id: string,
  canonical_name: string,
  asset_registry_id: string
})

(:Column {
  id: string,              // e.g., "raw.erp.transactions.amount"
  table_id: string,
  name: string,
  data_type: string
})

(:Table {
  id: string,              // e.g., "analytics.finance.fact_revenue"
  schema: string,
  name: string,
  platform: string         // e.g., "snowflake", "databricks"
})

(:TribalKnowledge {
  id: string,
  asset_registry_id: string,
  severity: string         // "high", "medium", "low"
})

// Relationships
(:Entity)-[:HAS_ATTRIBUTE]->(:Attribute)
(:Entity)-[:MAPS_TO {context: string}]->(:Entity)      // Cross-domain mapping
(:Metric)-[:DEFINED_BY]->(:GlossaryTerm)
(:Metric)-[:USES_DIMENSION]->(:Attribute)
(:Metric)-[:COMPUTED_FROM]->(:Column)
(:Metric)-[:HAS_KNOWN_ISSUE]->(:TribalKnowledge)
(:Column)-[:BELONGS_TO]->(:Table)
(:Column)-[:TRANSFORMS_TO {logic: string}]->(:Column)  // Lineage
(:GlossaryTerm)-[:HAS_VARIATION {context: string}]->(:GlossaryTerm)
```

### 2.2 Asset Registry Schema (PostgreSQL)

```sql
-- Main assets table (JSONB for flexibility)
CREATE TABLE assets (
    id VARCHAR(50) PRIMARY KEY,
    type VARCHAR(50) NOT NULL,
    version INTEGER NOT NULL DEFAULT 1,
    content JSONB NOT NULL,
    metadata JSONB,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    created_by VARCHAR(100),
    updated_by VARCHAR(100),
    CONSTRAINT valid_type CHECK (type IN (
        'glossary_term', 'data_contract', 'validation_rule', 
        'tribal_knowledge', 'policy', 'query_template'
    ))
);

CREATE INDEX idx_assets_type ON assets(type);
CREATE INDEX idx_assets_content_gin ON assets USING GIN(content);
CREATE INDEX idx_assets_metadata_gin ON assets USING GIN(metadata);

-- Example: Glossary term structure
{
  "canonical_name": "revenue",
  "display_name": "Revenue",
  "definition": "Income from normal business operations, recognized per ASC 606",
  "variations": [
    {
      "context": "sales",
      "name": "bookings",
      "definition": "Value of signed contracts",
      "formula": "SUM(contract_value)"
    },
    {
      "context": "finance",
      "name": "recognized_revenue",
      "definition": "Revenue recognized per GAAP",
      "formula": "Handled by semantic layer"
    }
  ],
  "synonyms": ["income", "sales", "top line"],
  "acronyms": ["ARR", "MRR"],
  "owner": "finance_operations",
  "last_reviewed": "2025-01-15"
}

-- Example: Tribal knowledge structure
{
  "type": "known_issue",
  "scope": {
    "tables": ["finance.fact_revenue_daily"],
    "dimensions": {
      "region": ["APAC"],
      "fiscal_period": ["2019-Q4"]
    }
  },
  "description": "Q4 2019 APAC data is incomplete due to Oracle→Snowflake migration",
  "reason": "Migration script failed for 2 weeks of data",
  "impact": "Revenue underreported by approximately 15%",
  "workaround": "Use Q4 2018 growth-adjusted estimate for trend analysis",
  "discovered_by": "maria.chen@company.com",
  "discovered_date": "2020-02-14",
  "verified": true,
  "active": true
}

-- Example: Data contract structure
{
  "name": "fact_revenue_daily",
  "owner": {
    "team": "finance_data_engineering",
    "contact": "fin-data@company.com"
  },
  "source": {
    "platform": "snowflake",
    "database": "analytics",
    "schema": "finance",
    "table": "fact_revenue_daily"
  },
  "sla": {
    "freshness_hours": 6,
    "availability_pct": 99.5,
    "completeness_pct": 99.9
  },
  "schema": {
    "columns": [
      {
        "name": "transaction_id",
        "type": "VARCHAR(50)",
        "nullable": false,
        "unique": true,
        "description": "Unique identifier for transaction"
      },
      {
        "name": "amount",
        "type": "DECIMAL(18,2)",
        "nullable": false,
        "description": "Transaction amount in local currency"
      }
    ]
  },
  "quality_rules": [
    {
      "rule": "transaction_id IS NOT NULL AND transaction_id != ''",
      "severity": "critical"
    },
    {
      "rule": "amount >= 0",
      "severity": "warning"
    }
  ]
}

-- Resolution state tracking
CREATE TABLE resolution_sessions (
    query_id VARCHAR(50) PRIMARY KEY,
    user_id VARCHAR(100) NOT NULL,
    user_context JSONB NOT NULL,
    original_query TEXT NOT NULL,
    resolution_dag JSONB NOT NULL,
    status VARCHAR(20) NOT NULL,
    started_at TIMESTAMP DEFAULT NOW(),
    completed_at TIMESTAMP,
    result JSONB,
    CONSTRAINT valid_status CHECK (status IN (
        'parsing', 'resolving', 'planning', 'authorizing', 
        'executing', 'validating', 'complete', 'failed'
    ))
);

CREATE INDEX idx_resolution_user ON resolution_sessions(user_id);
CREATE INDEX idx_resolution_status ON resolution_sessions(status);
CREATE INDEX idx_resolution_started ON resolution_sessions(started_at);
```

### 2.3 Semantic Layer Schema (Cube.js)

```javascript
// schema/Revenue.js
cube('Revenue', {
  sql: `SELECT * FROM analytics.finance.fact_revenue_daily`,
  
  measures: {
    netRevenue: {
      type: 'sum',
      sql: `amount`,
      filters: [
        { sql: `${CUBE}.type = 'recognized'` },
        { sql: `${CUBE}.refunded = false` }
      ],
      meta: {
        certification_tier: 1,
        owner: 'sarah.johnson@company.com',
        definition: 'Recognized revenue per ASC 606 minus refunds',
        asset_registry_id: 'ar_m_001',
        graph_node_id: 'net_revenue'
      }
    },
    
    grossRevenue: {
      type: 'sum',
      sql: `amount`,
      filters: [
        { sql: `${CUBE}.type IN ('recognized', 'invoiced')` }
      ],
      meta: {
        certification_tier: 2,
        owner: 'sales_ops@company.com',
        definition: 'Total invoiced revenue before adjustments'
      }
    }
  },
  
  dimensions: {
    region: {
      type: 'string',
      sql: `region_code`,
      meta: {
        variations: {
          finance: {
            apac: ['JP', 'KR', 'SG', 'HK', 'TW', 'AU', 'NZ', 'IN', 'CN'],
            emea: ['GB', 'DE', 'FR', 'IT', 'ES', 'NL', 'CH', 'SE', 'NO']
          },
          sales: {
            apac: ['JP', 'KR', 'SG', 'HK', 'TW', 'IN', 'CN'],  // excludes ANZ
            emea: ['GB', 'DE', 'FR', 'IT', 'ES', 'NL', 'CH', 'SE', 'NO', 'AE']
          }
        }
      }
    },
    
    fiscalPeriod: {
      type: 'string',
      sql: `fiscal_period`
    },
    
    transactionDate: {
      type: 'time',
      sql: `transaction_date`
    }
  },
  
  preAggregations: {
    revenueByRegionQuarter: {
      measures: [netRevenue],
      dimensions: [region, fiscalPeriod],
      timeDimension: transactionDate,
      granularity: 'quarter',
      refreshKey: {
        every: '6 hour'
      }
    }
  }
});
```

### 2.4 Vector Store Schema (Pinecone)

```python
# Vector index configuration
vector_index = {
    "name": "ecp-context",
    "dimension": 1536,  # OpenAI text-embedding-3-small
    "metric": "cosine",
    "spec": {
        "serverless": {
            "cloud": "aws",
            "region": "us-east-1"
        }
    }
}

# Vector record structure
vector_record = {
    "id": "vec_g_042",
    "values": [0.012, -0.034, ...],  # 1536-dimensional embedding
    "metadata": {
        "type": "glossary_term",
        "term": "revenue",
        "asset_registry_id": "ar_g_042",
        "graph_node_id": "revenue",
        "domain": "finance",
        "contexts": ["sales", "finance", "operations"],
        "text": "Revenue: Income generated from normal business operations..."
    }
}

# Query example
query_result = index.query(
    vector=[...],  # Query embedding
    filter={
        "type": {"$eq": "glossary_term"},
        "domain": {"$eq": "finance"}
    },
    top_k=5,
    include_metadata=True
)
```

---

## 3. API SPECIFICATIONS

### 3.1 REST API (OpenAPI 3.0)

```yaml
openapi: 3.0.0
info:
  title: Enterprise Context Platform API
  version: 2.0.0
  
paths:
  /api/v1/resolve:
    post:
      summary: Resolve a business concept to executable plan
      requestBody:
        content:
          application/json:
            schema:
              type: object
              required: [concept]
              properties:
                concept:
                  type: string
                  example: "APAC revenue last quarter"
                user_context:
                  type: object
                  properties:
                    user_id: {type: string}
                    department: {type: string}
                    role: {type: string}
                    allowed_regions: {type: array, items: {type: string}}
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
                properties:
                  resolution_id: {type: string}
                  status: {type: string, enum: [resolved, disambiguation_required]}
                  execution_plan:
                    type: object
                    properties:
                      semantic_layer_calls: {type: array}
                      computation: {type: object}
                  resolved_concepts:
                    type: object
                  confidence_score: {type: number}
                  warnings: {type: array}
                  provenance:
                    type: object
                    properties:
                      resolution_dag: {type: object}
                      stores_queried: {type: array}
                      definitions_used: {type: object}
  
  /api/v1/execute:
    post:
      summary: Execute a resolved query plan
      requestBody:
        content:
          application/json:
            schema:
              type: object
              required: [resolution_id]
              properties:
                resolution_id: {type: string}
                parameters: {type: object}
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
                properties:
                  results: {type: object}
                  confidence_score: {type: number}
                  warnings: {type: array}
                  provenance:
                    type: object
                    properties:
                      lineage: {type: array}
                      source_systems: {type: array}
                      execution_time_ms: {type: integer}
```

### 3.2 MCP Server Tool Definitions

```typescript
// MCP Server Tools
const tools = [
  {
    name: "resolve_business_concept",
    description: "Resolve business concept to canonical definition and execution plan",
    inputSchema: {
      type: "object",
      properties: {
        concept: {
          type: "string",
          description: "Business concept to resolve (e.g., 'APAC revenue')"
        },
        user_context: {
          type: "object",
          properties: {
            user_id: { type: "string" },
            department: { type: "string" },
            role: { type: "string" }
          }
        }
      },
      required: ["concept"]
    }
  },
  
  {
    name: "execute_metric_query",
    description: "Execute a metric query with full provenance",
    inputSchema: {
      type: "object",
      properties: {
        resolution_id: {
          type: "string",
          description: "ID from previous resolve call"
        },
        parameters: {
          type: "object",
          description: "Runtime parameters (filters, time range)"
        }
      },
      required: ["resolution_id"]
    }
  }
];
```

---

## 4. RESOLUTION ORCHESTRATION FLOW

### 4.1 Detailed Execution Flow

```
User Query: "What was APAC revenue last quarter compared to budget?"
                            │
                            ▼
┌────────────────────────────────────────────────────────────────────┐
│ 1. PARSE INTENT (LLM + Rules)                                     │
│    Extract: metric="revenue", dimension="APAC",                   │
│             time="last quarter", comparison="budget"              │
│    Confidence: 0.92                                               │
└────────────────────┬───────────────────────────────────────────────┘
                     │
                     ▼
┌────────────────────────────────────────────────────────────────────┐
│ 2. RESOLVE CONCEPTS (Parallel Queries)                            │
│                                                                    │
│    2a. Resolve "revenue"                                          │
│        Vector Search → Top matches: [net_revenue (0.85),          │
│                                      gross_revenue (0.70)]        │
│        Graph Query → Find definition → Select net_revenue         │
│                                         (user.dept = finance)     │
│                                                                    │
│    2b. Resolve "APAC"                                             │
│        Graph Query → region_apac entity                           │
│                   → variations: {finance: [JP,KR,...,CN],         │
│                                  sales: [JP,KR,...,CN exc ANZ]}  │
│                   → Select finance variation                      │
│                                                                    │
│    2c. Resolve "last quarter"                                     │
│        Asset Registry → calendar_config                           │
│                      → fiscal_year_start: April                   │
│                      → resolved_period: Q3-2024 (Oct-Dec)         │
│                                                                    │
│    2d. Resolve "budget"                                           │
│        Graph Query → budget_net_revenue metric                    │
│                   → semantic_layer_ref: cube.planning.Budget...   │
└────────────────────┬───────────────────────────────────────────────┘
                     │
                     ▼
┌────────────────────────────────────────────────────────────────────┐
│ 3. CHECK TRIBAL KNOWLEDGE                                          │
│    Vector Search: "APAC revenue Q3 2024 issues"                   │
│    Graph Query: (tk:TribalKnowledge)-[:AFFECTS]->(net_revenue)   │
│    Result: No issues found for Q3 2024                            │
└────────────────────┬───────────────────────────────────────────────┘
                     │
                     ▼
┌────────────────────────────────────────────────────────────────────┐
│ 4. BUILD EXECUTION PLAN                                            │
│    Query 1: cube.finance.Revenue.netRevenue                       │
│             filters: {region: ['JP','KR',...], period: 'Q3-2024'} │
│    Query 2: cube.planning.Budget.netRevenueBudget                 │
│             filters: {region_group: 'APAC_FINANCE',               │
│                      period: 'Q3-2024'}                           │
│    Computation: variance = Q1 - Q2, variance_pct = (Q1-Q2)/Q2    │
└────────────────────┬───────────────────────────────────────────────┘
                     │
                     ▼
┌────────────────────────────────────────────────────────────────────┐
│ 5. AUTHORIZE (OPA Policy Check)                                   │
│    Input: {user: {role: 'analyst', dept: 'finance'},             │
│            data_products: ['net_revenue', 'budget_net_revenue']}  │
│    Policies: ['finance_data_access', 'regional_restrictions']    │
│    Result: AUTHORIZED (user has access to all requested data)     │
└────────────────────┬───────────────────────────────────────────────┘
                     │
                     ▼
┌────────────────────────────────────────────────────────────────────┐
│ 6. EXECUTE (Semantic Layer Calls)                                 │
│    Call 1: POST /cubejs-api/v1/load                              │
│            {measures: ["Revenue.netRevenue"], ...}               │
│            Result: 142,300,000 USD                               │
│    Call 2: POST /cubejs-api/v1/load                              │
│            {measures: ["Budget.netRevenueBudget"], ...}          │
│            Result: 135,000,000 USD                               │
│    Compute: variance = 7,300,000, variance_pct = 5.41%          │
└────────────────────┬───────────────────────────────────────────────┘
                     │
                     ▼
┌────────────────────────────────────────────────────────────────────┐
│ 7. VALIDATE RESULTS                                                │
│    Rule 1: revenue_non_negative → PASS (142.3M > 0)              │
│    Rule 2: budget_non_negative → PASS (135M > 0)                 │
│    Rule 3: variance_within_bounds → PASS (5.41% < 50%)           │
│    Rule 4: temporal_validity → PASS (Q3-2024 in valid range)     │
│    Overall: PASS, confidence = 0.94                              │
└────────────────────┬───────────────────────────────────────────────┘
                     │
                     ▼
┌────────────────────────────────────────────────────────────────────┐
│ 8. ASSEMBLE RESPONSE                                               │
│    {                                                               │
│      "answer": {                                                   │
│        "actual_revenue": 142300000,                               │
│        "budget": 135000000,                                       │
│        "variance": 7300000,                                       │
│        "variance_pct": 5.41                                       │
│      },                                                            │
│      "confidence_score": 0.94,                                    │
│      "definition_used": "net_revenue (ASC 606, finance context)", │
│      "source": "analytics.finance.fact_revenue_daily",            │
│      "lineage": [...],                                            │
│      "warnings": []                                               │
│    }                                                               │
└────────────────────────────────────────────────────────────────────┘
```

### 4.2 Store Query Patterns

**Vector Store Queries:**
```python
# Semantic search for glossary terms
vector_index.query(
    vector=embed("revenue"),
    filter={"type": "glossary_term"},
    top_k=5
)

# Find relevant tribal knowledge
vector_index.query(
    vector=embed("APAC revenue Q3 2024 issues"),
    filter={
        "type": "tribal_knowledge",
        "scope_dimensions": {"$contains": "region=APAC"}
    },
    top_k=10
)
```

**Graph Queries:**
```cypher
-- Find metric definition with variations
MATCH (m:Metric {id: 'net_revenue'})-[:DEFINED_BY]->(g:GlossaryTerm)
      -[:HAS_VARIATION]->(v:GlossaryTerm)
RETURN m, g, v

-- Trace column lineage
MATCH path = (m:Metric {id: 'net_revenue'})
             -[:COMPUTED_FROM]->(col:Column)
             -[:TRANSFORMS_FROM*1..5]->(src:Column)
             -[:BELONGS_TO]->(tbl:Table)
RETURN path

-- Find cross-domain entity mapping
MATCH path = (e1:Entity {domain: 'sales'})-[:MAPS_TO*1..3]-(e2:Entity {domain: 'finance'})
WHERE e1.id = 'customer'
RETURN path
```

**Asset Registry Queries:**
```sql
-- Get glossary term with variations
SELECT content 
FROM assets 
WHERE type = 'glossary_term' 
  AND content->>'canonical_name' = 'revenue';

-- Get tribal knowledge for scope
SELECT content 
FROM assets 
WHERE type = 'tribal_knowledge'
  AND content->'scope'->'dimensions'->>'region' LIKE '%APAC%'
  AND (metadata->>'active')::boolean = true;

-- Get data contract
SELECT content 
FROM assets 
WHERE type = 'data_contract' 
  AND content->>'name' = 'fact_revenue_daily';
```

---

## 5. DEPLOYMENT ARCHITECTURE

### 5.1 Kubernetes Deployment

```yaml
# Namespace
apiVersion: v1
kind: Namespace
metadata:
  name: ecp

---
# Resolution Orchestrator Deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: resolution-orchestrator
  namespace: ecp
spec:
  replicas: 3
  selector:
    matchLabels:
      app: resolution-orchestrator
  template:
    metadata:
      labels:
        app: resolution-orchestrator
    spec:
      containers:
      - name: orchestrator
        image: ecp/resolution-orchestrator:2.0
        ports:
        - containerPort: 8080
        env:
        - name: NEO4J_URI
          valueFrom:
            secretKeyRef:
              name: ecp-secrets
              key: neo4j-uri
        - name: PINECONE_API_KEY
          valueFrom:
            secretKeyRef:
              name: ecp-secrets
              key: pinecone-api-key
        - name: POSTGRES_DSN
          valueFrom:
            secretKeyRef:
              name: ecp-secrets
              key: postgres-dsn
        - name: REDIS_URL
          value: "redis://redis-service:6379"
        resources:
          requests:
            cpu: "500m"
            memory: "1Gi"
          limits:
            cpu: "2000m"
            memory: "4Gi"
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 8080
          initialDelaySeconds: 10
          periodSeconds: 5

---
# Service
apiVersion: v1
kind: Service
metadata:
  name: resolution-service
  namespace: ecp
spec:
  type: ClusterIP
  ports:
  - port: 80
    targetPort: 8080
  selector:
    app: resolution-orchestrator

---
# Ingress
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: ecp-ingress
  namespace: ecp
  annotations:
    cert-manager.io/cluster-issuer: "letsencrypt-prod"
    nginx.ingress.kubernetes.io/rate-limit: "100"
spec:
  tls:
  - hosts:
    - ecp.company.com
    secretName: ecp-tls
  rules:
  - host: ecp.company.com
    http:
      paths:
      - path: /api
        pathType: Prefix
        backend:
          service:
            name: resolution-service
            port:
              number: 80

---
# MCP Server Deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: mcp-server
  namespace: ecp
spec:
  replicas: 2
  template:
    spec:
      containers:
      - name: mcp-server
        image: ecp/mcp-server:2.0
        ports:
        - containerPort: 3000
        env:
        - name: RESOLUTION_SERVICE_URL
          value: "http://resolution-service:80"

---
# Redis (State Store)
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: redis
  namespace: ecp
spec:
  serviceName: redis-service
  replicas: 1
  selector:
    matchLabels:
      app: redis
  template:
    metadata:
      labels:
        app: redis
    spec:
      containers:
      - name: redis
        image: redis:7-alpine
        ports:
        - containerPort: 6379
        volumeMounts:
        - name: redis-data
          mountPath: /data
  volumeClaimTemplates:
  - metadata:
      name: redis-data
    spec:
      accessModes: ["ReadWriteOnce"]
      resources:
        requests:
          storage: 10Gi
```

### 5.2 Infrastructure Requirements

| Component | Minimum | Recommended | Scaling Strategy |
|-----------|---------|-------------|------------------|
| **Orchestrator** | 2 pods, 1 CPU, 2GB RAM | 3-5 pods, 2 CPU, 4GB RAM | Horizontal (HPA on CPU/memory) |
| **Redis** | 1 instance, 10GB | 3 instances (HA), 50GB | Vertical + replication |
| **Neo4j** | 1 instance, 4 CPU, 16GB RAM | 3 instances (cluster), 8 CPU, 32GB RAM | Cluster mode, read replicas |
| **PostgreSQL** | 1 instance, 4 CPU, 16GB RAM | Primary + replica, 8 CPU, 32GB RAM | Primary-replica, connection pooling |
| **Pinecone** | Serverless (auto-scaled) | Serverless | Auto-scales |
| **Cube.js** | 2 pods, 2 CPU, 4GB RAM | 3-5 pods, 4 CPU, 8GB RAM | Horizontal (HPA on query load) |

### 5.3 Network Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                        PUBLIC INTERNET                              │
└──────────────────────────────┬──────────────────────────────────────┘
                               │
                               │ HTTPS (TLS 1.3)
                               │
┌──────────────────────────────▼──────────────────────────────────────┐
│                     API GATEWAY (Nginx)                             │
│                 • Rate limiting: 100 req/sec/IP                     │
│                 • DDoS protection                                   │
│                 • TLS termination                                   │
└──────────────────────────────┬──────────────────────────────────────┘
                               │
                               │ HTTP (internal)
                               │
┌──────────────────────────────▼──────────────────────────────────────┐
│                        DMZ / PUBLIC SUBNET                          │
│                                                                     │
│  ┌──────────────────────┐     ┌──────────────────────┐            │
│  │ Resolution           │     │ MCP Server           │            │
│  │ Orchestrator         │     │ (Agent Integration)  │            │
│  └──────┬───────────────┘     └──────────────────────┘            │
└─────────┼──────────────────────────────────────────────────────────┘
          │
          │ Private network (VPC peering / PrivateLink)
          │
┌─────────▼──────────────────────────────────────────────────────────┐
│                     PRIVATE SUBNET                                  │
│                                                                     │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐               │
│  │   Neo4j     │  │  Pinecone   │  │ PostgreSQL  │               │
│  │  (Private)  │  │   (HTTPS)   │  │  (Private)  │               │
│  └─────────────┘  └─────────────┘  └─────────────┘               │
│                                                                     │
│  ┌─────────────┐  ┌─────────────┐                                 │
│  │   Redis     │  │  Cube.js    │                                 │
│  │  (Private)  │  │  (Private)  │                                 │
│  └─────────────┘  └─────────────┘                                 │
└─────────┬──────────────────────────────────────────────────────────┘
          │
          │ Private network / VPC peering
          │
┌─────────▼──────────────────────────────────────────────────────────┐
│                  DATA ESTATE (Existing VPC)                         │
│                                                                     │
│  Snowflake / Databricks / SQL Server / Oracle / Data Lake         │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 6. OPERATIONAL CONSIDERATIONS

### 6.1 Monitoring & Observability

**Key Metrics:**
```python
# Latency metrics
resolution_latency_p50 = Histogram('resolution_latency_seconds', 
                                   buckets=[0.1, 0.2, 0.5, 1.0, 2.0])
resolution_latency_p95 = Histogram('resolution_latency_p95_seconds')
resolution_latency_p99 = Histogram('resolution_latency_p99_seconds')

# Store query latencies
graph_query_latency = Histogram('graph_query_latency_seconds')
vector_query_latency = Histogram('vector_query_latency_seconds')
semantic_layer_latency = Histogram('semantic_layer_latency_seconds')

# Accuracy metrics
resolution_confidence = Histogram('resolution_confidence_score')
disambiguation_rate = Counter('disambiguation_requests_total')

# Error metrics
resolution_errors = Counter('resolution_errors_total', ['stage', 'error_type'])
policy_denials = Counter('policy_denials_total', ['reason'])

# Resource metrics
cache_hit_rate = Gauge('cache_hit_rate')
query_result_cache_size = Gauge('query_result_cache_size_mb')
```

**Distributed Tracing:**
```python
# OpenTelemetry instrumentation
from opentelemetry import trace
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

tracer = trace.get_tracer(__name__)

@app.post("/api/v1/resolve")
async def resolve(request: ResolveRequest):
    with tracer.start_as_current_span("resolve_request") as span:
        span.set_attribute("concept", request.concept)
        span.set_attribute("user_id", request.user_context.user_id)
        
        # Parse
        with tracer.start_as_current_span("parse_intent"):
            intent = await parse_intent(request.concept)
        
        # Resolve
        with tracer.start_as_current_span("resolve_concepts"):
            concepts = await resolve_concepts(intent)
        
        # ... rest of flow
        
        return response
```

### 6.2 Security Controls

**Authentication & Authorization:**
```yaml
# OIDC integration (Okta/Azure AD)
oidc:
  issuer: https://company.okta.com
  client_id: ${OIDC_CLIENT_ID}
  client_secret: ${OIDC_CLIENT_SECRET}
  scopes: [openid, profile, email]
  
# Role mapping
role_mapping:
  okta_group_finance_analysts: analyst
  okta_group_finance_leadership: executive
  okta_group_data_engineers: admin
```

**Network Policies:**
```yaml
# Kubernetes NetworkPolicy
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: orchestrator-network-policy
  namespace: ecp
spec:
  podSelector:
    matchLabels:
      app: resolution-orchestrator
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          name: ingress-nginx
    ports:
    - protocol: TCP
      port: 8080
  egress:
  - to:
    - podSelector:
        matchLabels:
          app: neo4j
    ports:
    - protocol: TCP
      port: 7687
  - to:
    - podSelector:
        matchLabels:
          app: redis
    ports:
    - protocol: TCP
      port: 6379
```

### 6.3 Disaster Recovery

**Backup Strategy:**
```bash
# Neo4j backup (daily)
neo4j-admin dump --database=ecp --to=/backups/neo4j-$(date +%Y%m%d).dump

# PostgreSQL backup (hourly via WAL)
pg_basebackup -D /backups/postgres-base -Ft -Xs -P

# Asset versioning (all changes logged)
INSERT INTO asset_history (asset_id, version, content, changed_by, changed_at)
SELECT id, version, content, updated_by, updated_at FROM assets;
```

**RTO/RPO:**
- **Neo4j**: RTO = 15 min, RPO = 1 hour (continuous backup)
- **PostgreSQL**: RTO = 5 min, RPO = 5 min (streaming replication)
- **Redis**: RTO = 1 min, RPO = acceptable (cache, can rebuild)
- **Pinecone**: RTO = N/A (serverless), RPO = can rebuild from source

---

## 7. PERFORMANCE OPTIMIZATION

### 7.1 Caching Strategy

```python
# Multi-level cache
class CacheStrategy:
    def __init__(self):
        self.l1_cache = LRUCache(maxsize=1000)        # In-memory, 1ms
        self.l2_cache = RedisCache(ttl=3600)          # Redis, 5ms
        self.l3_cache = PostgreSQLCache(ttl=86400)    # Postgres, 20ms
    
    async def get_resolution(self, concept: str, context: dict) -> Optional[Resolution]:
        cache_key = hash_key(concept, context)
        
        # Try L1
        if result := self.l1_cache.get(cache_key):
            return result
        
        # Try L2
        if result := await self.l2_cache.get(cache_key):
            self.l1_cache.set(cache_key, result)
            return result
        
        # Try L3
        if result := await self.l3_cache.get(cache_key):
            await self.l2_cache.set(cache_key, result)
            self.l1_cache.set(cache_key, result)
            return result
        
        return None
```

### 7.2 Query Optimization

```cypher
-- Neo4j query optimization
// Bad: Full graph scan
MATCH (m:Metric)-[*]-(related)
WHERE m.id = 'net_revenue'
RETURN related

// Good: Index-backed, depth-limited
MATCH (m:Metric {id: 'net_revenue'})-[r*1..3]-(related)
RETURN related
LIMIT 100

// Create indexes
CREATE INDEX metric_id_idx FOR (m:Metric) ON (m.id);
CREATE INDEX entity_domain_idx FOR (e:Entity) ON (e.domain);
```

**Connection Pooling:**
```python
# PostgreSQL connection pool
from asyncpg import create_pool

pool = await create_pool(
    dsn=POSTGRES_DSN,
    min_size=10,
    max_size=50,
    max_queries=50000,
    max_inactive_connection_lifetime=300
)

# Neo4j connection pool
from neo4j import AsyncGraphDatabase

driver = AsyncGraphDatabase.driver(
    NEO4J_URI,
    auth=(NEO4J_USER, NEO4J_PASSWORD),
    max_connection_pool_size=50
)
```

---

## 8. TESTING STRATEGY

```python
# Unit tests
def test_intent_parser():
    intent = parse_intent("APAC revenue last quarter")
    assert intent.concepts['metric'] == 'revenue'
    assert intent.concepts['region'] == 'APAC'
    assert intent.concepts['time'] == 'last quarter'

# Integration tests
@pytest.mark.asyncio
async def test_resolution_flow():
    request = ResolveRequest(
        concept="net revenue",
        user_context={"user_id": "test", "department": "finance"}
    )
    response = await resolve(request)
    assert response.status == "resolved"
    assert response.confidence_score > 0.8

# End-to-end tests (reference queries)
@pytest.mark.e2e
async def test_reference_query():
    # Reference answer: 142.3M
    response = await execute_query("APAC revenue Q3 2024")
    assert abs(response.result.value - 142300000) < 1000
```

---

This technical architecture provides implementable specifications for building the Enterprise Context Platform at production scale.