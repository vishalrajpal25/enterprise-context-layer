# Enterprise Context Platform: Technical Specification v2.0

## Document Information

| Attribute | Value |
|-----------|-------|
| Version | 2.0 |
| Status | Draft |
| Author | Enterprise Architecture Team |
| Last Updated | February 2025 |
| Classification | Internal - Strategy |
| Changes from v1.0 | Added hyperscaler integration patterns, revised storage architecture, detailed resolution orchestration |

---

## Executive Summary

Modern enterprises face a critical challenge: AI agents fail on enterprise data not because of reasoning limitations, but because of missing context. The knowledge required to correctly interpret and use enterprise data—business definitions, transformation rules, tribal knowledge, gotchas—exists but is scattered across schemas, code, documentation, and people's heads. It was never designed to be machine-readable or agent-consumable.

This specification defines the **Enterprise Context Platform (ECP)**—a semantic mediation layer that sits between AI agents and legacy data estates. The platform enables agents to query, analyze, and act on enterprise data accurately and safely, without requiring a multi-year data platform modernization.

### Core Thesis

**Context is the product, not data.** The data already exists. What's missing is the machine-readable semantic contract that tells an agent *how* to use that data correctly. Traditional approaches fail because they try to fix the data; this approach builds a context layer that wraps the data as-is—an "institutional memory API" that agents query before they query data.

### Key Principles

1. **The Semantic Firewall**: Agents never directly touch the messy data estate; everything passes through a controlled boundary that translates between agent queries and legacy systems.

2. **The Agent Never Does Math**: Agents orchestrate and translate, but all computation happens in deterministic systems (databases, semantic layers). This eliminates an entire class of hallucination risk.

3. **Context-First, Not Data-First**: We don't clean data before use; we wrap messy data with rich context that enables correct interpretation.

4. **Platform Agnostic**: The ECP is a **context service**, not an agent runtime. It integrates with Azure AI Foundry, Google Vertex AI/Agentspace, AWS Bedrock, or custom agent frameworks via standard protocols (MCP, REST, A2A).

5. **Manufacturing, Not Art**: Data onboarding is a repeatable factory process, not bespoke craftsmanship. The unit of production is the "Agent-Ready Data Product."

---

## Part 1: Problem Definition

### 1.1 The Enterprise Data Reality

A typical Fortune 500 enterprise (think FactSet, Bloomberg, Reuters) has built a complex data estate over 15-20 years:

#### Technical Landscape

| Component | Typical State |
|-----------|---------------|
| **Databases** | Tens of platforms across SQL Server, Oracle, Snowflake, PostgreSQL, legacy mainframes |
| **Stored Procedures** | Thousands containing embedded business logic, some 15+ years old |
| **Technical Debt** | Views built on views; undocumented dependencies; inconsistent naming |
| **ETL Pipelines** | Transformation logic scattered across Databricks, Informatica, SSIS, dbt, custom scripts |
| **Data Lakes** | Semi-structured and unstructured data mixed with processed structured data |
| **APIs** | Multiple interfaces exposing data to internal and external consumers |
| **Sources of Truth** | Multiple, conflicting—some sources claim truth, others compute it at runtime |

#### Organizational Reality

| Challenge | Manifestation |
|-----------|---------------|
| **Definition Variance** | "Revenue" means different things to Sales, Finance, and Operations |
| **Undocumented Jargon** | Acronyms are pervasive and inconsistently documented |
| **Tribal Knowledge** | The "right" way to query data is passed down verbally or lives in individuals' heads |
| **Hidden Gotchas** | Known data issues and workarounds aren't systematically captured |
| **Fragmented Ownership** | No single person understands the full estate |
| **Scattered Documentation** | Confluence, SharePoint, wikis, email threads, Slack—mostly outdated |

#### Business Pressure

- Leadership expects GenAI to "just work" on enterprise data
- Competitors moving fast; 12-18 month window to establish AI-driven data products
- Regulatory requirements demand accuracy, auditability, and explainability
- Traditional governance programs take 2-3 years and often fail before completion

### 1.2 The Context Gap

When a user asks an agent "What was our APAC revenue last quarter?", the agent doesn't know:

- Which definition of "revenue" to use (gross? net? recognized? booked?)
- What "APAC" means in this organization (includes China? excludes ANZ?)
- Whether "last quarter" is fiscal or calendar
- Which source system is authoritative for this metric
- That Q4 2019 data is incomplete due to a migration
- That APAC cost center definitions changed in 2021
- What stored procedure or view contains the "correct" calculation
- What joins, filters, and transformations are required

This context exists—but scattered and not machine-readable. **AI agents fail because they lack institutional context, not reasoning capability.**

### 1.3 Why Traditional Approaches Fail

| Approach | Failure Mode |
|----------|--------------|
| **Data Cataloging** | Produces metadata without semantic meaning; tells you *what* exists, not *how* to use it |
| **Data Governance Programs** | 2-3 year timelines; organizational fatigue; often abandoned before completion |
| **Data Quality Initiatives** | Fix symptoms not causes; don't address interpretation ambiguity |
| **Documentation Projects** | SMEs won't write docs; documentation immediately stale |
| **Data Warehouse Modernization** | Multi-year, tens of millions of dollars; doesn't solve the context problem |

The common failure pattern: **attempting to fix the data before using it.** This specification proposes the inverse: **wrap messy data with rich context that enables correct interpretation.**

---

## Part 2: Business Requirements

### 2.1 Primary Goal

> **Enable a scalable (10 → 100 → 1000 datasets) agentic data access layer that is safe, accurate, and trustable—on the existing legacy data estate—in minimum possible time.**

### 2.2 Requirement Breakdown

| Dimension | Requirement | Success Criteria |
|-----------|-------------|------------------|
| **Scalable** | Approach works for 10 datasets and still works for 1000; can't be artisanal | Linear cost scaling; consistent onboarding time per dataset |
| **Safe** | Agents cannot return harmful, misleading, or unauthorized data | Zero unauthorized data exposures; guardrails catch anomalies |
| **Accurate** | Answers correct per business definitions, not hallucinated | Match validated reference answers; SME approval |
| **Trustable** | Every answer explainable, auditable, traceable to authoritative sources | Full provenance on every response; audit trail |
| **Existing Estate** | No full overhaul; incremental adoption; no multi-year modernization wait | Works with current systems; phased rollout |
| **Minimum Time** | Weeks to months, not years; leverage automation and smart prioritization | Initial value in 90 days; 500+ data products in 12 months |
| **Platform Agnostic** | Works with any agent runtime (Azure, GCP, AWS, custom) | Standard protocol support; no vendor lock-in |

### 2.3 Key Challenges to Address

#### Challenge 1: The Context Gap
- How to capture and represent business context (definitions, rules, logic, exceptions)?
- How to make context queryable and injectable at runtime?

#### Challenge 2: The Tribal Knowledge Problem
- How to extract undocumented knowledge from people's heads, Slack threads, old emails, code comments?
- How to keep this knowledge current as the organization evolves?

#### Challenge 3: The Scale Problem
- How to avoid "boil the ocean" trap of cataloging everything?
- What's the repeatable unit of work?
- How to prioritize which data to make AI-ready first?

#### Challenge 4: The Accuracy Problem
- How does an agent know which source, calculation, or definition is authoritative?
- How to handle ambiguity when multiple valid interpretations exist?
- How to prevent agents from using stale, deprecated, or incorrect data?

#### Challenge 5: The Trust Problem
- How to provide provenance, confidence scores, audit trails with every answer?
- How to certify data for different use cases (internal vs. external vs. regulatory)?
- How to explain to a regulator or executive exactly how an answer was derived?

#### Challenge 6: The Safety Problem
- How to prevent agents from accessing unauthorized data?
- How to catch obviously wrong results before they reach users?
- How to enforce business rules and constraints at query time?

#### Challenge 7: The Maintenance Problem
- How to keep the context layer in sync as underlying data estate changes?
- How to incorporate feedback when agents make mistakes?
- How to handle versioning of definitions and logic over time?

#### Challenge 8: The Integration Problem (NEW)
- How to integrate with existing hyperscaler AI infrastructure?
- How to federate across multiple agent runtimes?
- How to maintain consistent context across multi-cloud deployments?

### 2.4 Constraints

#### What We CAN Do
- Build new layers/services between agents and data estate
- Use LLMs and AI to accelerate extraction and synthesis
- Deploy new infrastructure (knowledge graphs, vector stores, semantic layers, APIs)
- Prioritize high-value data products over comprehensive coverage
- Implement human-in-the-loop validation for critical use cases
- Integrate with existing enterprise agent infrastructure

#### What We CANNOT Do
- Wait for a 2-year data governance program
- Assume perfect data quality or complete documentation exists
- Require migration of data to new platforms
- Force organizational restructuring before delivering value
- Replace existing agent infrastructure investments

### 2.5 Success Metrics

| Metric | Target (90 Days) | Target (12 Months) |
|--------|------------------|---------------------|
| Agent-Ready Data Products | 50+ | 500+ |
| Query Accuracy (vs. validated reference) | >95% | >98% |
| Automated Extraction Rate | >70% | >85% |
| Onboarding Time per Dataset | <3 days | <1 day |
| User Satisfaction (pilot) | >4.0/5.0 | >4.5/5.0 |
| Zero unauthorized data exposures | 100% | 100% |
| Agent Runtime Integrations | 2+ | 5+ |

---

## Part 3: Hyperscaler & Agent Runtime Integration

### 3.1 Positioning: Context Service, Not Agent Runtime

The Enterprise Context Platform is **NOT** an agent runtime. It is a specialized **context resolution service** that any agent runtime can call. This is a critical architectural distinction.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        AGENT RUNTIME LAYER                                  │
│         (Azure AI Foundry / Google Vertex AI / AWS Bedrock / Custom)        │
│                                                                             │
│   Responsibilities:                                                         │
│   • User interaction & conversation management                              │
│   • LLM inference & orchestration                                          │
│   • Workflow execution & state management                                   │
│   • Memory & session management                                             │
│   • Content safety & filtering                                              │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                          ┌─────────┴─────────┐
                          │  Tool/Function    │
                          │  Calls (MCP/A2A)  │
                          └─────────┬─────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                    ENTERPRISE CONTEXT PLATFORM                              │
│                        (This Specification)                                 │
│                                                                             │
│   Responsibilities:                                                         │
│   • Semantic resolution (what does "APAC revenue" mean?)                   │
│   • Query generation (how do I compute it?)                                │
│   • Context retrieval (glossary, ontology, tribal knowledge)               │
│   • Guardrails & validation (is this result valid?)                        │
│   • Provenance generation (where did this come from?)                      │
│   • Policy enforcement (is user authorized?)                               │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                         PHYSICAL DATA ESTATE                                │
│          (Snowflake, SQL Server, Oracle, Data Lake, APIs - unchanged)       │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 3.2 Integration Patterns by Platform

#### 3.2.1 Azure AI Foundry Integration

Azure AI Foundry provides a managed agent runtime with Foundry Agent Service. The ECP integrates as a **connected tool** or **custom API** that agents call for context resolution.

**Integration Pattern: Function/Tool Calling**

```yaml
# Azure AI Foundry Agent Definition
agent:
  name: enterprise-data-analyst
  model: gpt-4o
  tools:
    - type: function
      function:
        name: resolve_business_concept
        description: Resolve a business term to its canonical definition and execution plan
        parameters:
          type: object
          properties:
            concept:
              type: string
              description: The business concept to resolve (e.g., "APAC revenue")
            user_context:
              type: object
              description: User's role, department, permissions
        endpoint: https://ecp.enterprise.com/api/v1/resolve
        
    - type: function
      function:
        name: execute_metric_query
        description: Execute a resolved metric query and return results with provenance
        parameters:
          type: object
          properties:
            resolution_id:
              type: string
            parameters:
              type: object
        endpoint: https://ecp.enterprise.com/api/v1/execute
```

**Deployment Options**:
1. **Standard Mode**: ECP deployed as Azure App Service, accessed via private endpoint from Foundry Agent Service
2. **VNet Integration**: ECP deployed within the same VNet as Foundry resources for secure, low-latency access
3. **Hybrid**: ECP components distributed across on-premises and Azure

**Key Integrations**:
- **Foundry IQ**: ECP can be registered as a grounding source for Foundry IQ's RAG capabilities
- **Semantic Kernel**: ECP tools registered in Semantic Kernel for multi-agent orchestration
- **Azure Monitor**: ECP emits traces compatible with Azure Monitor for end-to-end observability

#### 3.2.2 Google Vertex AI / Agentspace Integration

Google's Vertex AI Agent Builder and Agentspace provide agent development and enterprise deployment. ECP integrates via **ADK tools** or **MCP servers**.

**Integration Pattern: Agent Development Kit (ADK) Tool**

```python
# ADK Tool Definition for ECP
from google.adk import Tool, ToolParameter

ecp_resolve_tool = Tool(
    name="enterprise_context_resolve",
    description="Resolve business concepts using the Enterprise Context Platform",
    parameters=[
        ToolParameter(
            name="concept",
            type="string",
            description="Business concept to resolve"
        ),
        ToolParameter(
            name="context",
            type="object",
            description="User context for disambiguation"
        )
    ],
    endpoint="https://ecp.enterprise.com/api/v1/resolve"
)

# Register with Agent Engine
agent.add_tool(ecp_resolve_tool)
```

**Integration Pattern: MCP Server**

```yaml
# MCP Server Configuration
mcp_server:
  name: enterprise-context-platform
  transport: sse
  url: https://ecp.enterprise.com/mcp
  
  tools:
    - name: resolve_metric
      description: Resolve metric name to definition and execution plan
      
    - name: query_glossary
      description: Look up business term definitions
      
    - name: execute_query
      description: Execute metric query with full provenance
      
    - name: check_authorization
      description: Verify user access to requested data
```

**Key Integrations**:
- **Agent2Agent (A2A) Protocol**: ECP exposes A2A-compatible endpoints for cross-platform agent communication
- **Cloud API Registry**: Register ECP tools in Google's API Registry for centralized governance
- **Memory Bank**: ECP resolution traces can be stored in Vertex AI Memory Bank for agent learning

#### 3.2.3 AWS Bedrock Agents Integration

AWS Bedrock Agents supports custom action groups. ECP integrates as an **action group** with Lambda-backed functions.

**Integration Pattern: Action Group**

```yaml
# Bedrock Agent Action Group
action_group:
  name: EnterpriseContextPlatform
  description: Resolve business concepts and execute queries with enterprise context
  
  api_schema:
    openapi: "3.0.0"
    paths:
      /resolve:
        post:
          operationId: resolveBusinessConcept
          description: Resolve a business concept to canonical definition
          requestBody:
            content:
              application/json:
                schema:
                  type: object
                  properties:
                    concept:
                      type: string
                    user_context:
                      type: object
          responses:
            '200':
              description: Resolution result with execution plan
              
  lambda_function: arn:aws:lambda:us-east-1:123456789:function:ecp-bedrock-adapter
```

#### 3.2.4 Cloud-Native / Kubernetes Integration

For organizations running custom agent frameworks on Kubernetes, ECP deploys as a set of microservices with standard APIs.

**Deployment Architecture**:

```yaml
# Kubernetes Deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ecp-resolution-service
spec:
  replicas: 3
  template:
    spec:
      containers:
        - name: resolution-orchestrator
          image: ecp/resolution-orchestrator:latest
          ports:
            - containerPort: 8080
          env:
            - name: GRAPH_DB_URL
              valueFrom:
                secretKeyRef:
                  name: ecp-secrets
                  key: neo4j-url
            - name: VECTOR_DB_URL
              valueFrom:
                secretKeyRef:
                  name: ecp-secrets
                  key: pinecone-url
---
apiVersion: v1
kind: Service
metadata:
  name: ecp-service
spec:
  type: ClusterIP
  ports:
    - port: 80
      targetPort: 8080
  selector:
    app: ecp-resolution-service
---
# MCP Server Sidecar for Agent Frameworks
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ecp-mcp-server
spec:
  template:
    spec:
      containers:
        - name: mcp-server
          image: ecp/mcp-server:latest
          ports:
            - containerPort: 3000
          env:
            - name: ECP_SERVICE_URL
              value: "http://ecp-service:80"
```

**Integration with LangChain/LangGraph**:

```python
# LangGraph Integration
from langgraph.graph import StateGraph
from langchain_core.tools import tool

@tool
def resolve_business_concept(concept: str, user_context: dict) -> dict:
    """Resolve a business concept using the Enterprise Context Platform."""
    response = requests.post(
        "http://ecp-service/api/v1/resolve",
        json={"concept": concept, "user_context": user_context}
    )
    return response.json()

@tool
def execute_metric_query(resolution_id: str, parameters: dict) -> dict:
    """Execute a metric query using the resolved context."""
    response = requests.post(
        "http://ecp-service/api/v1/execute",
        json={"resolution_id": resolution_id, "parameters": parameters}
    )
    return response.json()

# Build agent graph with ECP tools
workflow = StateGraph(AgentState)
workflow.add_node("resolve", resolve_node)
workflow.add_node("execute", execute_node)
workflow.add_edge("resolve", "execute")
```

### 3.4 MCP as Data Product Delivery Protocol

For financial data companies, MCP becomes a new delivery channel for existing data products—enabling AI agents to consume data that was previously delivered via SFTP, REST APIs, or bulk downloads.

#### 3.4.1 The Strategic Opportunity

**Current delivery channels** (maintained):
- SFTP feeds (batch delivery)
- REST APIs (programmatic access)
- Web downloads (manual access)
- Streaming feeds (real-time)

**New delivery channel** (additive):
- MCP servers (AI-native access)

**Key insight**: MCP doesn't replace existing channels—it provides an AI-native interface that sits *above* them, using the ECP's resolution engine to translate agent queries into backend calls.

#### 3.4.2 MCP Gateway Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      CUSTOMER AI AGENTS                                     │
│         (Running in customer's Azure/GCP/AWS/custom environment)           │
└─────────────────────────────────────────────────────────────────────────────┘
                                   │
                                   │ MCP Protocol (SSE/WebSocket)
                                   ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                           MCP GATEWAY                                       │
│                                                                             │
│   ┌─────────────────────────────────────────────────────────────────────┐  │
│   │                     MCP SERVER LAYER                                 │  │
│   │                                                                      │  │
│   │   Discovery    Query      Streaming     Bulk        Semantic        │  │
│   │   Server       Server     Server        Export      Query Server    │  │
│   │                                                                      │  │
│   │   list_tools   get_price  subscribe     export_     query_          │  │
│   │   get_schema   get_metric unsubscribe   dataset     financial_data  │  │
│   │   search       compare    get_updates               (NL interface)  │  │
│   └─────────────────────────────────────────────────────────────────────┘  │
│                                    │                                        │
│   ┌────────────────────────────────▼────────────────────────────────────┐  │
│   │              CONTEXT & RESOLUTION LAYER (ECP Core)                  │  │
│   │                                                                      │  │
│   │   • Entity Resolution: "Tesla" → ISIN, CUSIP, internal IDs         │  │
│   │   • Metric Resolution: "P/E ratio" → pe_ratio_ttm definition       │  │
│   │   • Query Disambiguation: context-aware interpretation              │  │
│   │   • Coverage Mapping: which backend has this data?                  │  │
│   │   • Schema Translation: normalize across sources                    │  │
│   └────────────────────────────────┬────────────────────────────────────┘  │
│                                    │                                        │
│   ┌────────────────────────────────▼────────────────────────────────────┐  │
│   │                    BACKEND ADAPTER LAYER                            │  │
│   │                                                                      │  │
│   │   REST API    SFTP      Snowflake    Kafka       Redis     Legacy   │  │
│   │   Adapter     Adapter   Adapter      Adapter     Adapter   Adapter  │  │
│   └─────────────────────────────────────────────────────────────────────┘  │
│                                    │                                        │
│   ┌────────────────────────────────▼────────────────────────────────────┐  │
│   │                 ENTITLEMENT & METERING LAYER                        │  │
│   │                                                                      │  │
│   │   • Customer Authentication (API keys, OAuth, mTLS)                 │  │
│   │   • Subscription Validation (same entitlement rules)                │  │
│   │   • Usage Metering (billable queries, data volume)                  │  │
│   │   • Rate Limiting (per customer/tier)                               │  │
│   │   • Audit Logging (compliance)                                      │  │
│   └─────────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────┘
```

#### 3.4.3 Dynamic Tool Generation

Instead of manually defining thousands of MCP tools, generate them from the data product catalog:

```yaml
# Data Product Catalog Entry (internal)
data_product:
  id: "equity_fundamentals"
  name: "Equity Fundamentals"
  entities: ["security"]
  metrics:
    - id: "pe_ratio_ttm"
      aliases: ["P/E", "PE ratio", "price to earnings"]
      definition: "Price / Trailing 12-month diluted EPS"
    - id: "eps_diluted"
      aliases: ["EPS", "earnings per share"]
  dimensions: ["as_of_date", "currency", "period"]
  backends: ["rest_api", "snowflake"]

# Auto-generated MCP Tool
generated_tool:
  name: "get_equity_fundamental"
  description: "Retrieve fundamental metrics for equities (P/E, EPS, revenue, margins, etc.)"
  inputSchema:
    type: object
    properties:
      identifier:
        type: string
        description: "Security identifier (ticker, ISIN, CUSIP, SEDOL, FIGI)"
      metric:
        type: string
        description: "Metric name or alias"
      as_of_date:
        type: string
        format: date
      currency:
        type: string
        enum: ["USD", "EUR", "GBP", "local"]
    required: ["identifier", "metric"]
```

#### 3.4.4 Semantic Query Interface

For complex queries, expose a natural language interface:

```yaml
- name: "query_financial_data"
  description: |
    Natural language interface to financial data. Automatically resolves 
    entity references, metric names, and time periods.
    
    Examples:
    - "Tesla's P/E ratio"
    - "Revenue growth for FAANG stocks over 5 years"
    - "S&P 500 companies with P/E under 15 and dividend yield over 3%"
    
  inputSchema:
    type: object
    properties:
      query:
        type: string
      output_format:
        type: string
        enum: ["json", "table", "chart_data"]
      include_metadata:
        type: boolean
        description: "Include data lineage and quality information"
    required: ["query"]
```

#### 3.4.5 Entitlement Enforcement

MCP access respects existing subscription models:

```yaml
entitlement_mapping:
  tiers:
    basic:
      tools: ["get_price", "get_equity_fundamental"]
      rate_limit: 1000/day
      
    professional:
      tools: ["get_price", "get_price_history", "get_equity_fundamental", 
              "compare_equity_fundamentals", "screen_equities"]
      rate_limit: 10000/day
      
    enterprise:
      tools: ["*"]
      rate_limit: unlimited
      streaming: true
      bulk_export: true
      
  metering:
    billable_events:
      - tool: "query_financial_data"
        cost: 1  # credit per query
      - tool: "screen_equities"
        cost: 5  # screening is expensive
      - tool: "get_price_history"
        cost_formula: "0.01 * data_points"
```

#### 3.4.6 Example Resolution Flow

When a customer's agent asks "What's Tesla's P/E ratio compared to the auto industry?":

```
1. AUTHENTICATE: Validate API key → Customer "hedge_fund_abc" (professional tier)

2. PARSE: Extract intent → comparison(Tesla P/E, industry average P/E)

3. RESOLVE:
   - "Tesla" → ISIN: US88160R1014, GICS: 25102010
   - "P/E ratio" → pe_ratio_ttm (TTM diluted)
   - "auto industry" → GICS Industry Group 2510

4. CHECK ENTITLEMENT: Customer has equity_fundamentals + industry_analytics ✓

5. PLAN:
   - Query 1: REST API → /fundamentals/metrics?isin=US88160R1014&metric=pe_ratio_ttm
   - Query 2: Snowflake → SELECT AVG(pe_ratio_ttm) FROM metrics WHERE gics='2510'

6. EXECUTE: Run both queries in parallel

7. ASSEMBLE: 
   {
     "tesla_pe": 72.3,
     "industry_avg_pe": 18.7,
     "premium": "287%",
     "metadata": {
       "sources": ["equity_fundamentals", "industry_analytics"],
       "freshness": "T+1",
       "definitions": {...}
     }
   }

8. METER: Log 2 billable credits
```

### 3.5 Multi-Cloud & Federated Deployment

For enterprises with multi-cloud strategies, ECP supports federated deployment:

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   Azure AI      │     │  Google Vertex  │     │   AWS Bedrock   │
│   Foundry       │     │   AI / Agents   │     │     Agents      │
└────────┬────────┘     └────────┬────────┘     └────────┬────────┘
         │                       │                       │
         │    A2A Protocol       │    MCP Protocol       │
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                                 ▼
              ┌──────────────────────────────────────┐
              │     ECP FEDERATION GATEWAY           │
              │  (API Gateway / Load Balancer)       │
              └──────────────────────────────────────┘
                                 │
         ┌───────────────────────┼───────────────────────┐
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  ECP Instance   │     │  ECP Instance   │     │  ECP Instance   │
│    (Azure)      │     │    (GCP)        │     │    (AWS)        │
└─────────────────┘     └─────────────────┘     └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                    ┌────────────┴────────────┐
                    │  Shared Context Stores  │
                    │  (Graph DB, Vector DB)  │
                    └─────────────────────────┘
```

**Federation Patterns**:

1. **Centralized Context, Distributed Compute**: Single Context Registry replicated across clouds; resolution happens in each cloud
2. **Federated Context**: Context partitioned by domain/region; cross-cloud queries federated at query time
3. **Hybrid**: Core context centralized; domain-specific context distributed

---

## Part 4: Revised Storage Architecture

### 4.1 Design Principles

The storage architecture is designed around three principles:

1. **Separation of Concerns**: Distinguish between storage (where canonical artifacts live), indexing (how we find them), and runtime (how we execute them)
2. **Query Pattern Alignment**: Each store optimized for its primary access pattern
3. **Cross-Reference via Graph**: The knowledge graph is the "index of everything" that knows where assets live and how they connect

### 4.2 Core Stores

| Store | Technology | Primary Purpose | Access Pattern |
|-------|------------|-----------------|----------------|
| **Knowledge Graph** | Neo4j / Neptune | Relationships, cross-references, lineage | Traversal, path finding |
| **Semantic Index** | Pinecone / Weaviate | Semantic search over text | Similarity search |
| **Asset Registry** | PostgreSQL (JSONB) | Structured artifact storage | CRUD, JSON queries |
| **Semantic Layer** | Cube.js / dbt | Executable metric definitions | API calls |
| **Policy Engine** | OPA / Cedar | Runtime policy evaluation | Policy checks |

### 4.3 Asset-to-Store Mapping

Each asset type has a **primary store** (where the canonical artifact lives) and **indexes** (how we find and traverse to it):

| Asset Type | Primary Store | Indexed In | Runtime Component |
|------------|---------------|------------|-------------------|
| **Semantic Models (Metrics)** | Semantic Layer (code) | Graph (metadata), Vector (descriptions) | Semantic Layer API |
| **Business Glossary** | Asset Registry (JSONB) | Vector (definitions), Graph (relationships) | Resolution Engine |
| **Ontology / Entities** | Knowledge Graph | Vector (descriptions) | Graph queries |
| **Data Contracts** | Asset Registry (JSONB) | Graph (links to entities) | Guardrail Engine |
| **Lineage Artifacts** | Knowledge Graph | — | Graph traversal |
| **Policy Artifacts** | Asset Registry (JSONB) | Graph (links to assets) | Policy Engine (OPA) |
| **Validation Rules** | Asset Registry (JSONB) | Graph (links to metrics) | Guardrail Engine |
| **Query Templates** | Semantic Layer (code) | Graph (metadata) | Semantic Layer API |
| **Domain Models** | Knowledge Graph | — | Graph queries |
| **Tribal Knowledge** | Asset Registry (JSONB) | Vector (semantic search), Graph (links) | Resolution Engine |

### 4.4 Detailed Store Specifications

#### 4.4.1 Knowledge Graph (Neo4j / Neptune)

**Purpose**: The spine of the system. Stores all relationships between entities and serves as the "index of everything."

**What It Stores**:
- **Ontology**: Entities, attributes, relationships (Customer, Product, Region, etc.)
- **Lineage**: Column-level data flow as a directed acyclic graph
- **Cross-References**: Links between all assets (metric → glossary term → source table → policy)
- **Domain Models**: Bounded contexts and cross-domain mappings

**What It Does NOT Store**:
- Full artifact definitions (those live in Asset Registry or Semantic Layer)
- Text content for semantic search (that's in Vector Store)
- Executable logic (that's in Semantic Layer)

**Schema Example**:

```cypher
// Ontology: Entity and relationships
CREATE (c:Entity {id: 'customer', name: 'Customer', domain: 'sales'})
CREATE (r:Entity {id: 'region', name: 'Region', domain: 'reference'})
CREATE (c)-[:BELONGS_TO]->(r)

// Metric with cross-references
CREATE (m:Metric {
  id: 'net_revenue',
  name: 'Net Revenue',
  semantic_layer_ref: 'cube.finance.net_revenue',  // Reference to Semantic Layer
  asset_registry_id: 'ar_m_001'  // Reference to full definition in Asset Registry
})
CREATE (g:GlossaryTerm {id: 'revenue', asset_registry_id: 'ar_g_042'})
CREATE (m)-[:DEFINED_BY]->(g)

// Lineage as graph
CREATE (src:Column {id: 'raw.erp.gl.amount'})
CREATE (tgt:Column {id: 'analytics.finance.revenue'})
CREATE (src)-[:TRANSFORMS_TO {logic: 'currency_convert'}]->(tgt)

// Cross-reference to tribal knowledge
CREATE (tk:TribalKnowledge {id: 'tk_001', asset_registry_id: 'ar_tk_001'})
CREATE (m)-[:HAS_KNOWN_ISSUE]->(tk)
```

**Query Patterns**:

```cypher
// Find all assets related to a metric
MATCH (m:Metric {id: 'net_revenue'})-[r]-(related)
RETURN m, type(r), related

// Trace lineage from source to metric
MATCH path = (src:Table)-[:CONTAINS]->(col:Column)-[:TRANSFORMS_TO*]->(tgt:Column)<-[:USES]-(m:Metric)
WHERE m.id = 'net_revenue'
RETURN path

// Find cross-domain mapping path
MATCH path = (e1:Entity {domain: 'sales'})-[:MAPS_TO*1..3]-(e2:Entity {domain: 'finance'})
RETURN path
```

#### 4.4.2 Semantic Index (Vector Store - Pinecone / Weaviate)

**Purpose**: Enable semantic search over unstructured and semi-structured content.

**What It Stores**:
- Embeddings of glossary term definitions
- Embeddings of tribal knowledge descriptions
- Embeddings of metric descriptions
- Embeddings of documentation chunks

**What It Does NOT Store**:
- The canonical artifacts themselves (those are in Asset Registry)
- Relationships between items (that's in Knowledge Graph)

**Schema Example**:

```json
// Vector record for glossary term
{
  "id": "vec_g_042",
  "values": [0.012, -0.034, ...],  // Embedding vector
  "metadata": {
    "type": "glossary_term",
    "term": "revenue",
    "asset_registry_id": "ar_g_042",
    "graph_node_id": "g_042",
    "domain": "finance",
    "contexts": ["sales", "finance", "ops"]
  }
}

// Vector record for tribal knowledge
{
  "id": "vec_tk_001",
  "values": [0.045, 0.012, ...],
  "metadata": {
    "type": "tribal_knowledge",
    "summary": "Q4 2019 APAC data incomplete due to migration",
    "asset_registry_id": "ar_tk_001",
    "graph_node_id": "tk_001",
    "scope_tables": ["finance.fact_revenue_daily"],
    "scope_dimensions": ["region=APAC", "period=2019-Q4"]
  }
}
```

**Query Patterns**:

```python
# Semantic search for glossary terms
results = vector_index.query(
    vector=embed("What is recognized revenue?"),
    filter={"type": "glossary_term"},
    top_k=5
)

# Find relevant tribal knowledge for a query scope
results = vector_index.query(
    vector=embed("APAC revenue issues"),
    filter={
        "type": "tribal_knowledge",
        "scope_dimensions": {"$contains": "region=APAC"}
    },
    top_k=10
)
```

#### 4.4.3 Asset Registry (PostgreSQL JSONB)

**Purpose**: Store canonical definitions of structured artifacts with schema flexibility.

**Why PostgreSQL JSONB**:
- ACID transactions for reliable updates
- Rich JSON querying for structured artifacts
- Familiar SQL interface for operations teams
- Easy to backup, replicate, and manage

**Schema**:

```sql
CREATE TABLE assets (
    id VARCHAR(50) PRIMARY KEY,
    type VARCHAR(50) NOT NULL,  -- glossary_term, data_contract, validation_rule, tribal_knowledge, policy
    version INT NOT NULL DEFAULT 1,
    content JSONB NOT NULL,
    metadata JSONB,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    created_by VARCHAR(100),
    updated_by VARCHAR(100)
);

CREATE INDEX idx_assets_type ON assets(type);
CREATE INDEX idx_assets_content ON assets USING GIN(content);
CREATE INDEX idx_assets_metadata ON assets USING GIN(metadata);

-- Example: Glossary Term
INSERT INTO assets (id, type, content, metadata) VALUES (
    'ar_g_042',
    'glossary_term',
    '{
        "canonical_name": "revenue",
        "display_name": "Revenue",
        "definition": "Income generated from normal business operations",
        "variations": [
            {"context": "sales", "name": "bookings", "definition": "Value of signed contracts"},
            {"context": "finance", "name": "recognized_revenue", "definition": "Per ASC 606"}
        ],
        "synonyms": ["income", "sales"],
        "owner": "finance_operations"
    }',
    '{"domain": "finance", "certification_tier": 2}'
);

-- Example: Data Contract
INSERT INTO assets (id, type, content, metadata) VALUES (
    'ar_dc_001',
    'data_contract',
    '{
        "name": "fact_revenue_daily",
        "owner": {"team": "finance_data_engineering", "contact": "fin-data@company.com"},
        "source": {"platform": "snowflake", "schema": "finance", "table": "fact_revenue_daily"},
        "sla": {"freshness_hours": 6, "availability_pct": 99.5},
        "quality_rules": [
            {"rule": "transaction_id is unique", "severity": "critical"},
            {"rule": "amount >= 0", "severity": "warning"}
        ]
    }',
    '{"last_validated": "2025-01-15"}'
);

-- Example: Tribal Knowledge
INSERT INTO assets (id, type, content, metadata) VALUES (
    'ar_tk_001',
    'tribal_knowledge',
    '{
        "type": "known_issue",
        "scope": {
            "tables": ["finance.fact_revenue_daily"],
            "dimensions": {"region": "APAC", "fiscal_period": "2019-Q4"}
        },
        "description": "Q4 2019 APAC data is incomplete",
        "reason": "Oracle to Snowflake migration caused data loss",
        "impact": "Revenue underreported by approximately 15%",
        "workaround": "Use Q4 2018 growth-adjusted estimate for trend analysis",
        "discovered_by": "maria.chen@company.com",
        "verified": true
    }',
    '{"severity": "high", "active": true}'
);
```

#### 4.4.4 Semantic Layer (Cube.js / dbt Semantic Layer)

**Purpose**: Deterministic computation engine. All metric calculations happen here—not in the LLM.

**What It Stores**:
- Metric definitions (as code)
- Dimension hierarchies
- Time intelligence rules
- Query templates
- Canonical join paths

**Key Principle**: The Semantic Layer is **code**, not documentation. Definitions are version-controlled, testable, and deterministic.

**Example (Cube.js)**:

```javascript
// schema/Revenue.js
cube('Revenue', {
  sql: `SELECT * FROM analytics.finance.fact_revenue_daily`,
  
  measures: {
    netRevenue: {
      type: 'sum',
      sql: `${CUBE}.amount`,
      filters: [{ sql: `${CUBE}.type = 'recognized'` }],
      meta: {
        certification_tier: 1,
        owner: 'sarah.johnson@company.com',
        definition: 'Recognized revenue per ASC 606 minus refunds'
      }
    },
    
    refunds: {
      type: 'sum',
      sql: `${CUBE}.amount`,
      filters: [{ sql: `${CUBE}.type = 'refund'` }]
    }
  },
  
  dimensions: {
    region: {
      type: 'string',
      sql: `${CUBE}.region_code`,
      meta: {
        variations: {
          finance: ['JP', 'KR', 'SG', 'HK', 'TW', 'AU', 'NZ', 'IN', 'CN'],
          sales: ['JP', 'KR', 'SG', 'HK', 'TW', 'IN', 'CN']  // excludes ANZ
        }
      }
    },
    
    fiscalPeriod: {
      type: 'string',
      sql: `${CUBE}.fiscal_period`
    }
  },
  
  preAggregations: {
    revenueByRegionQuarter: {
      measures: [netRevenue],
      dimensions: [region, fiscalPeriod],
      timeDimension: transactionDate,
      granularity: 'quarter'
    }
  }
});
```

#### 4.4.5 Policy Engine (OPA / Cedar)

**Purpose**: Runtime policy evaluation for access control and data governance.

**What It Stores**:
- Compiled policy rules
- Role-based access definitions
- Row-level security rules
- Data classification enforcement

**Example (OPA/Rego)**:

```rego
# policy/data_access.rego
package ecp.data_access

default allow = false

# Allow if user has required role for the data product
allow {
    input.action == "query"
    input.data_product.certification_tier <= user_max_tier[input.user.role]
}

# Role to max certification tier mapping
user_max_tier := {
    "executive": 1,
    "finance_analyst": 2,
    "analyst": 3,
    "explorer": 4
}

# Row-level security for regional data
row_filter[filter] {
    input.data_product.has_regional_restriction
    filter := sprintf("region IN ('%s')", [concat("','", input.user.allowed_regions)])
}

# Deny access to PII columns unless authorized
deny_columns[col] {
    col := input.data_product.pii_columns[_]
    not input.user.pii_authorized
}
```

### 4.5 Cross-Store Coordination

The Knowledge Graph serves as the coordination layer, storing references to assets in other stores:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         KNOWLEDGE GRAPH                                     │
│                    (Neo4j / Neptune)                                        │
│                                                                             │
│   ┌─────────────────────────────────────────────────────────────────────┐  │
│   │  Metric Node: net_revenue                                            │  │
│   │  ├── semantic_layer_ref: "cube.finance.Revenue.netRevenue"          │  │
│   │  ├── asset_registry_id: "ar_m_001"                                   │  │
│   │  ├── vector_id: "vec_m_001"                                          │  │
│   │  │                                                                    │  │
│   │  Relationships:                                                       │  │
│   │  ├── [:DEFINED_BY] → GlossaryTerm (revenue)                         │  │
│   │  ├── [:USES_DIMENSION] → Dimension (region)                          │  │
│   │  ├── [:GOVERNED_BY] → Policy (finance_data_access)                  │  │
│   │  ├── [:VALIDATED_BY] → ValidationRule (revenue_non_negative)        │  │
│   │  └── [:HAS_KNOWN_ISSUE] → TribalKnowledge (apac_q4_2019)            │  │
│   └─────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
         │                    │                    │                    │
         │                    │                    │                    │
         ▼                    ▼                    ▼                    ▼
┌─────────────┐      ┌─────────────┐      ┌─────────────┐      ┌─────────────┐
│  Semantic   │      │   Asset     │      │   Vector    │      │   Policy    │
│   Layer     │      │  Registry   │      │    Store    │      │   Engine    │
│             │      │             │      │             │      │             │
│ Executable  │      │ Full JSON   │      │ Embeddings  │      │ Runtime     │
│ Definitions │      │ Definitions │      │ for Search  │      │ Evaluation  │
└─────────────┘      └─────────────┘      └─────────────┘      └─────────────┘
```

---

## Part 5: Resolution Orchestration Engine

### 5.1 The Core Challenge

The Resolution Orchestration Engine is the "brain" of the ECP. It must:

1. **Decompose** natural language queries into semantic components
2. **Resolve** each component by querying appropriate stores
3. **Handle ambiguity** through context-based defaults or user clarification
4. **Build execution plans** that span multiple data sources
5. **Validate results** against business rules and anomaly bounds
6. **Generate provenance** for every answer

This requires coordinating across multiple stores with different query interfaces, handling complex branching logic, and maintaining state throughout the resolution process.

### 5.2 Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      RESOLUTION ORCHESTRATION ENGINE                        │
│                                                                             │
│  ┌───────────┐  ┌───────────┐  ┌───────────┐  ┌───────────┐  ┌───────────┐│
│  │  Parser   │  │  Planner  │  │ Resolver  │  │ Executor  │  │ Assembler ││
│  │           │→ │           │→ │           │→ │           │→ │           ││
│  │ NLU +     │  │ DAG       │  │ Multi-    │  │ Query     │  │ Response  ││
│  │ Intent    │  │ Builder   │  │ Store     │  │ Execution │  │ + Prove-  ││
│  │ Extraction│  │           │  │ Queries   │  │           │  │ nance     ││
│  └───────────┘  └───────────┘  └───────────┘  └───────────┘  └───────────┘│
│        │              │              │              │              │       │
│        └──────────────┴──────────────┴──────────────┴──────────────┘       │
│                                      │                                      │
│                                      ▼                                      │
│        ┌─────────────────────────────────────────────────────────────┐     │
│        │                   RESOLUTION STATE                           │     │
│        │                                                              │     │
│        │  • query_id, user_context                                   │     │
│        │  • resolution_dag (nodes, edges, status)                    │     │
│        │  • resolved_concepts (term → definition mapping)            │     │
│        │  • pending_disambiguations                                  │     │
│        │  • execution_plan (semantic layer calls)                    │     │
│        │  • provenance_trace (audit trail)                           │     │
│        │  • confidence_scores                                        │     │
│        │  • validation_results                                       │     │
│        │                                                              │     │
│        └─────────────────────────────────────────────────────────────┘     │
│                                      │                                      │
└──────────────────────────────────────┼──────────────────────────────────────┘
                                       │
                       ┌───────────────┼───────────────┐
                       │               │               │
                       ▼               ▼               ▼
              ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
              │    Graph     │ │   Vector     │ │    Asset     │
              │   Adapter    │ │   Adapter    │ │   Registry   │
              │              │ │              │ │   Adapter    │
              └──────────────┘ └──────────────┘ └──────────────┘
                       │               │               │
                       ▼               ▼               ▼
              ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
              │   Neo4j      │ │  Pinecone    │ │  PostgreSQL  │
              └──────────────┘ └──────────────┘ └──────────────┘
```

### 5.3 The Resolution DAG

Every query creates a **Resolution DAG** (Directed Acyclic Graph) that tracks the resolution process:

```yaml
resolution_dag:
  query_id: "q_12345"
  timestamp: "2025-02-01T14:30:00Z"
  user_context:
    user_id: "u_789"
    department: "finance"
    role: "analyst"
    allowed_regions: ["APAC", "EMEA", "NA"]
  
  original_query: "What was APAC revenue last quarter compared to budget?"
  
  nodes:
    # Stage 1: Parse Intent
    - id: "parse_intent"
      type: "parse"
      status: "complete"
      started_at: "2025-02-01T14:30:00.100Z"
      completed_at: "2025-02-01T14:30:00.350Z"
      output:
        concepts:
          - type: "metric"
            raw: "revenue"
            confidence: 0.95
          - type: "dimension_filter"
            raw: "APAC"
            dimension: "region"
            confidence: 0.98
          - type: "time_filter"
            raw: "last quarter"
            confidence: 0.92
          - type: "comparison"
            raw: "compared to budget"
            comparison_type: "vs_target"
            confidence: 0.88
    
    # Stage 2: Resolve Concepts (parallel)
    - id: "resolve_revenue"
      type: "resolve_concept"
      depends_on: ["parse_intent"]
      status: "complete"
      started_at: "2025-02-01T14:30:00.360Z"
      completed_at: "2025-02-01T14:30:00.520Z"
      stores_queried:
        - store: "vector"
          query: "semantic_search('revenue', type='glossary_term')"
          latency_ms: 45
        - store: "graph"
          query: "MATCH (m:Metric)-[:DEFINED_BY]->(g:GlossaryTerm {name: 'revenue'}) RETURN m, g"
          latency_ms: 23
      output:
        matches:
          - id: "gross_revenue"
            confidence: 0.70
            contexts: ["sales", "ops"]
            semantic_layer_ref: "cube.finance.Revenue.grossRevenue"
          - id: "net_revenue"
            confidence: 0.85
            contexts: ["finance"]
            semantic_layer_ref: "cube.finance.Revenue.netRevenue"
          - id: "recognized_revenue"
            confidence: 0.60
            contexts: ["accounting"]
            semantic_layer_ref: "cube.finance.Revenue.recognizedRevenue"
        selected: "net_revenue"
        selection_reason: "User in finance department; net_revenue is default for finance context"
        selection_method: "context_based_default"
    
    - id: "resolve_apac"
      type: "resolve_concept"
      depends_on: ["parse_intent"]
      status: "complete"
      started_at: "2025-02-01T14:30:00.360Z"
      completed_at: "2025-02-01T14:30:00.480Z"
      stores_queried:
        - store: "graph"
          query: "MATCH (r:Region {code: 'APAC'})-[:HAS_VARIATION]->(v) RETURN r, v"
          latency_ms: 18
      output:
        entity_type: "Region"
        entity_id: "region_apac"
        variations_found:
          - context: "finance"
            countries: ["JP", "KR", "SG", "HK", "TW", "AU", "NZ", "IN", "CN"]
          - context: "sales"
            countries: ["JP", "KR", "SG", "HK", "TW", "IN", "CN"]  # excludes ANZ
        selected_variation: "finance"
        selected_countries: ["JP", "KR", "SG", "HK", "TW", "AU", "NZ", "IN", "CN"]
        selection_reason: "User department is finance"
    
    - id: "resolve_time"
      type: "resolve_concept"
      depends_on: ["parse_intent"]
      status: "complete"
      started_at: "2025-02-01T14:30:00.360Z"
      completed_at: "2025-02-01T14:30:00.410Z"
      stores_queried:
        - store: "asset_registry"
          query: "SELECT content FROM assets WHERE type='calendar_config'"
          latency_ms: 12
      output:
        calendar_type: "fiscal"
        current_date: "2025-02-01"
        resolved_period: "Q3-2024"
        start_date: "2024-10-01"
        end_date: "2024-12-31"
        note: "Enterprise uses April fiscal year; Q3 = Oct-Dec"
    
    - id: "resolve_budget"
      type: "resolve_concept"
      depends_on: ["parse_intent"]
      status: "complete"
      started_at: "2025-02-01T14:30:00.360Z"
      completed_at: "2025-02-01T14:30:00.490Z"
      stores_queried:
        - store: "graph"
          query: "MATCH (m:Metric {name: 'budget'})-[:FOR_METRIC]->(r:Metric {name: 'net_revenue'}) RETURN m"
          latency_ms: 21
      output:
        metric_id: "budget_net_revenue"
        semantic_layer_ref: "cube.planning.Budget.netRevenueBudget"
        grain: ["region", "fiscal_quarter"]
    
    # Stage 3: Check for Tribal Knowledge
    - id: "check_tribal_knowledge"
      type: "enrich"
      depends_on: ["resolve_revenue", "resolve_apac", "resolve_time"]
      status: "complete"
      started_at: "2025-02-01T14:30:00.530Z"
      completed_at: "2025-02-01T14:30:00.620Z"
      stores_queried:
        - store: "vector"
          query: "semantic_search('APAC revenue Q3 2024 issues')"
          latency_ms: 38
        - store: "graph"
          query: "MATCH (tk:TribalKnowledge)-[:AFFECTS]->(m:Metric {id: 'net_revenue'}) WHERE tk.scope CONTAINS 'APAC' RETURN tk"
          latency_ms: 15
      output:
        relevant_knowledge: []  # No issues for Q3 2024; Q4 2019 issue not relevant
        warnings: []
    
    # Stage 4: Build Execution Plan
    - id: "build_execution_plan"
      type: "plan"
      depends_on: ["resolve_revenue", "resolve_apac", "resolve_time", "resolve_budget"]
      status: "complete"
      started_at: "2025-02-01T14:30:00.630Z"
      completed_at: "2025-02-01T14:30:00.680Z"
      output:
        plan_type: "comparison_query"
        queries:
          - id: "actual_revenue"
            semantic_layer_call:
              cube: "finance.Revenue"
              measure: "netRevenue"
              dimensions: ["region"]
              filters:
                region: ["JP", "KR", "SG", "HK", "TW", "AU", "NZ", "IN", "CN"]
                fiscalPeriod: "Q3-2024"
          - id: "budget_revenue"
            semantic_layer_call:
              cube: "planning.Budget"
              measure: "netRevenueBudget"
              dimensions: ["region"]
              filters:
                region_group: "APAC_FINANCE"
                fiscalPeriod: "Q3-2024"
        computation:
          variance: "actual_revenue - budget_revenue"
          variance_pct: "(actual_revenue - budget_revenue) / budget_revenue * 100"
    
    # Stage 5: Check Authorization
    - id: "check_authorization"
      type: "authorize"
      depends_on: ["build_execution_plan"]
      status: "complete"
      started_at: "2025-02-01T14:30:00.690Z"
      completed_at: "2025-02-01T14:30:00.720Z"
      stores_queried:
        - store: "policy_engine"
          query: "evaluate(user='u_789', action='query', data_products=['net_revenue', 'budget_net_revenue'])"
          latency_ms: 18
      output:
        authorized: true
        policies_evaluated: ["finance_data_access", "regional_restrictions"]
        row_filters_applied: []  # User has full APAC access
        column_restrictions: []
    
    # Stage 6: Execute Queries
    - id: "execute_queries"
      type: "execute"
      depends_on: ["check_authorization"]
      status: "complete"
      started_at: "2025-02-01T14:30:00.730Z"
      completed_at: "2025-02-01T14:30:01.580Z"
      output:
        results:
          actual_revenue:
            value: 142300000
            currency: "USD"
            rows_scanned: 1247832
            execution_time_ms: 623
          budget_revenue:
            value: 135000000
            currency: "USD"
            rows_scanned: 156
            execution_time_ms: 89
        computed:
          variance: 7300000
          variance_pct: 5.41
    
    # Stage 7: Validate Results
    - id: "validate_results"
      type: "validate"
      depends_on: ["execute_queries"]
      status: "complete"
      started_at: "2025-02-01T14:30:01.590Z"
      completed_at: "2025-02-01T14:30:01.650Z"
      stores_queried:
        - store: "asset_registry"
          query: "SELECT content FROM assets WHERE type='validation_rule' AND id IN ('vr_revenue_positive', 'vr_variance_bounds')"
          latency_ms: 8
      output:
        rules_evaluated: 4
        results:
          - rule: "revenue_non_negative"
            passed: true
          - rule: "budget_non_negative"
            passed: true
          - rule: "variance_within_bounds"
            passed: true
            note: "Variance 5.41% within ±50% threshold"
          - rule: "temporal_validity"
            passed: true
            note: "Q3-2024 within valid data range (2018-present)"
        overall_status: "pass"
        warnings: []
    
    # Stage 8: Assemble Response
    - id: "assemble_response"
      type: "assemble"
      depends_on: ["validate_results", "check_tribal_knowledge"]
      status: "complete"
      started_at: "2025-02-01T14:30:01.660Z"
      completed_at: "2025-02-01T14:30:01.700Z"
      output:
        answer:
          actual_revenue: 142300000
          budget: 135000000
          variance: 7300000
          variance_pct: 5.41
        confidence_score: 0.94
        confidence_level: "high"
```

### 5.4 Resolution Patterns & Scenarios

The orchestrator must handle many different query patterns. Here are the key scenarios:

#### Scenario 1: Simple Lookup (Single Store)

**Query**: "What is the definition of ARR?"

**Resolution Flow**:
```
parse_intent → resolve_concept (vector search) → assemble_response
```

**Stores Used**: Vector (glossary search) → Asset Registry (full definition)

**DAG Complexity**: Linear, 3 nodes

---

#### Scenario 2: Single Metric Query (Multi-Store)

**Query**: "What was revenue last month?"

**Resolution Flow**:
```
parse_intent → [resolve_revenue, resolve_time] → build_plan → authorize → execute → validate → assemble
```

**Stores Used**: 
- Vector + Graph (revenue resolution)
- Asset Registry (time/calendar config)
- Semantic Layer (execution)
- Policy Engine (authorization)

**DAG Complexity**: Parallel resolution, 7 nodes

---

#### Scenario 3: Ambiguous Term Requiring Disambiguation

**Query**: "Show me the data"

**Resolution Flow**:
```
parse_intent → detect_ambiguity → request_clarification → [wait for user] → resume_resolution
```

**Disambiguation Strategies**:
1. **Context-based default**: Use user's department/role to select most likely interpretation
2. **Confidence threshold**: If confidence < 0.7, request clarification
3. **Multiple results**: Present top 3 interpretations with confidence scores

**Example Response**:
```json
{
  "status": "disambiguation_required",
  "message": "I found multiple interpretations for 'the data'. Which do you mean?",
  "options": [
    {"id": 1, "interpretation": "Revenue Dashboard (finance.revenue_summary)", "confidence": 0.65},
    {"id": 2, "interpretation": "Customer Analytics (sales.customer_360)", "confidence": 0.58},
    {"id": 3, "interpretation": "Operations Metrics (ops.daily_metrics)", "confidence": 0.45}
  ],
  "suggestion": "Based on your role in Finance, I recommend option 1."
}
```

---

#### Scenario 4: Cross-Domain Query

**Query**: "Revenue by customer segment for enterprise customers in APAC"

**Resolution Flow**:
```
parse_intent 
  → [resolve_revenue (finance domain), 
     resolve_customer_segment (mdm domain), 
     resolve_enterprise_filter (mdm domain),
     resolve_apac (reference domain)]
  → find_cross_domain_path
  → build_federated_plan
  → authorize
  → execute
  → validate
  → assemble
```

**Cross-Domain Path Finding**:
```cypher
// Find how finance.revenue connects to mdm.customer
MATCH path = (m:Metric {id: 'net_revenue', domain: 'finance'})
  -[:USES_DIMENSION]->(d:Dimension {name: 'customer_id'})
  -[:MAPS_TO*1..3]->(c:Entity {name: 'Customer', domain: 'mdm'})
RETURN path

// Result: finance.fact_revenue.customer_id → mdm.customer_xref.customer_id → mdm.customer.id
```

**Execution Plan**:
```yaml
federated_query:
  - source: semantic_layer
    cube: finance.Revenue
    measure: netRevenue
    join_key: customer_id
  - source: semantic_layer
    cube: mdm.Customer
    dimension: segment
    filter: tier = 'Enterprise'
  - join_logic: |
      SELECT r.netRevenue, c.segment
      FROM finance.Revenue r
      JOIN mdm.customer_xref x ON r.customer_id = x.finance_customer_id
      JOIN mdm.Customer c ON x.mdm_customer_id = c.id
      WHERE c.tier = 'Enterprise'
      AND r.region IN ('APAC countries...')
      GROUP BY c.segment
```

---

#### Scenario 5: Query with Known Data Issues

**Query**: "APAC revenue for Q4 2019"

**Resolution Flow**:
```
parse_intent 
  → [resolve_revenue, resolve_apac, resolve_time]
  → check_tribal_knowledge  ← FINDS ISSUE
  → build_plan_with_caveat
  → authorize
  → execute
  → validate
  → assemble_with_warning
```

**Tribal Knowledge Check**:
```cypher
MATCH (tk:TribalKnowledge)-[:AFFECTS]->(m:Metric {id: 'net_revenue'})
WHERE 'APAC' IN tk.scope_regions 
  AND '2019-Q4' IN tk.scope_periods
RETURN tk
```

**Result**: Found tk_001 - "Q4 2019 APAC data incomplete due to Oracle migration"

**Response with Caveat**:
```json
{
  "answer": {
    "value": 98500000,
    "currency": "USD"
  },
  "confidence_score": 0.65,
  "confidence_level": "medium",
  "warnings": [
    {
      "type": "known_data_issue",
      "severity": "high",
      "message": "Q4 2019 APAC data is incomplete due to Oracle to Snowflake migration",
      "impact": "Revenue may be underreported by approximately 15%",
      "workaround": "For trend analysis, consider using Q4 2018 growth-adjusted estimate",
      "source": "tribal_knowledge:tk_001",
      "discovered_by": "maria.chen@company.com"
    }
  ],
  "provenance": {...}
}
```

---

#### Scenario 6: Unauthorized Access

**Query**: "Show me executive compensation data"

**Resolution Flow**:
```
parse_intent → resolve_concept → build_plan → authorize ← DENIED → assemble_denial
```

**Policy Evaluation**:
```rego
# OPA Policy Check
allow {
    input.data_product == "executive_compensation"
    input.user.role == "hr_admin"
}
allow {
    input.data_product == "executive_compensation"
    input.user.role == "executive"
}
# User role is "analyst" - DENIED
```

**Response**:
```json
{
  "status": "access_denied",
  "message": "You don't have permission to access executive compensation data",
  "reason": "This data product requires 'hr_admin' or 'executive' role",
  "your_role": "analyst",
  "action": "Contact your manager or HR to request access",
  "audit_logged": true
}
```

---

#### Scenario 7: Multi-Hop Reasoning

**Query**: "Show me revenue for all products owned by teams reporting to Sarah Chen"

**Resolution Flow**:
```
parse_intent
  → resolve_sarah_chen (find person entity)
  → traverse_org_structure (find reporting teams)
  → find_team_products (products owned by those teams)
  → resolve_revenue_for_products
  → build_plan
  → authorize
  → execute
  → validate
  → assemble
```

**Graph Traversal**:
```cypher
// Multi-hop: Person → Teams → Products → Revenue
MATCH (p:Person {name: 'Sarah Chen'})
  <-[:REPORTS_TO*1..3]-(t:Team)
  -[:OWNS]->(prod:Product)
  <-[:FOR_PRODUCT]-(m:Metric {name: 'net_revenue'})
RETURN DISTINCT prod.id AS product_id, prod.name AS product_name
```

---

#### Scenario 8: Aggregation Question

**Query**: "How many active customers do we have?"

**Resolution Flow**:
```
parse_intent
  → resolve_active_customer_definition
  → check_for_precomputed_metric
  → [if exists: use metric]
  → [if not: build_aggregation_plan]
  → authorize
  → execute
  → validate
  → assemble
```

**Definition Resolution**:
```yaml
# From Glossary
active_customer:
  definition: "Customer with at least one transaction in trailing 12 months"
  calculation: "COUNT(DISTINCT customer_id) WHERE last_transaction_date > DATEADD(month, -12, CURRENT_DATE)"
  semantic_layer_ref: "cube.sales.Customers.activeCustomerCount"
  note: "Some teams use 6-month window; clarify if needed"
```

---

#### Scenario 9: Lineage Question

**Query**: "Where does the APAC revenue number come from?"

**Resolution Flow**:
```
parse_intent (type: lineage_query)
  → resolve_apac_revenue
  → traverse_lineage_graph
  → format_lineage_response
```

**Lineage Traversal**:
```cypher
// Trace lineage backwards from metric
MATCH path = (m:Metric {id: 'net_revenue'})
  -[:COMPUTED_FROM]->(col:Column)
  -[:TRANSFORMS_FROM*1..5]->(src:Column)
  -[:BELONGS_TO]->(tbl:Table)
RETURN path
```

**Response**:
```json
{
  "metric": "net_revenue",
  "lineage": {
    "immediate_source": {
      "table": "analytics.finance.fact_revenue_daily",
      "column": "converted_amount_usd",
      "transformation": "SUM with recognized revenue filter"
    },
    "upstream_sources": [
      {
        "level": 1,
        "table": "staging.finance.stg_revenue",
        "transformation": "Currency conversion (local_amount * fx_rate)"
      },
      {
        "level": 2,
        "table": "raw.erp.gl_transactions",
        "transformation": "Filter to revenue accounts (4000-4999)"
      }
    ],
    "original_source": {
      "system": "SAP ERP",
      "table": "BKPF/BSEG",
      "extraction": "Daily CDC via Fivetran"
    }
  }
}
```

---

#### Scenario 10: Meta Question (Catalog Query)

**Query**: "What metrics are available for APAC analysis?"

**Resolution Flow**:
```
parse_intent (type: catalog_query)
  → resolve_apac
  → find_metrics_with_dimension
  → filter_by_user_access
  → format_catalog_response
```

**Graph Query**:
```cypher
MATCH (m:Metric)-[:HAS_DIMENSION]->(d:Dimension {name: 'region'})
WHERE EXISTS((m)-[:CERTIFIED])
RETURN m.id, m.name, m.description, m.certification_tier
ORDER BY m.certification_tier, m.name
```

**Response**:
```json
{
  "available_metrics": [
    {
      "id": "net_revenue",
      "name": "Net Revenue",
      "description": "Recognized revenue per ASC 606",
      "certification_tier": 1,
      "dimensions": ["region", "product", "customer", "time"],
      "owner": "finance_operations"
    },
    {
      "id": "gross_revenue",
      "name": "Gross Revenue",
      "description": "Total invoiced revenue before adjustments",
      "certification_tier": 2,
      "dimensions": ["region", "product", "customer", "time"],
      "owner": "sales_ops"
    }
    // ... more metrics
  ],
  "total_count": 47,
  "filters_applied": {
    "has_region_dimension": true,
    "user_has_access": true
  }
}
```

### 5.5 Intelligent Routing

The orchestrator uses multiple strategies to efficiently route queries to the right stores:

#### 5.5.1 Concept Type → Store Mapping (Rules-Based)

```yaml
routing_rules:
  metric_resolution:
    primary: vector  # Semantic search for term matching
    secondary: graph  # Relationship traversal for related concepts
    
  entity_lookup:
    primary: graph  # Direct entity lookup
    fallback: vector  # Semantic search if not found
    
  time_resolution:
    primary: asset_registry  # Calendar configuration
    
  policy_check:
    primary: policy_engine  # Always
    
  tribal_knowledge:
    primary: vector  # Semantic search over knowledge base
    secondary: graph  # Relationship-based lookup
    
  lineage:
    primary: graph  # DAG traversal
    
  cross_domain_mapping:
    primary: graph  # Path finding across domains
```

#### 5.5.2 Learned Routing (ML-Based)

Train a lightweight classifier on past resolution traces:

```python
# Features extracted from query
features = {
    "query_type": "metric_query",  # Classified by intent parser
    "concepts_detected": ["revenue", "region", "time"],
    "user_department": "finance",
    "historical_pattern": "revenue_by_region"  # Matched to known pattern
}

# Model predicts optimal store sequence
predicted_routing = routing_model.predict(features)
# Output: ["vector", "graph", "asset_registry"]
```

#### 5.5.3 Speculative Execution

For ambiguous queries, start multiple resolution paths in parallel:

```python
async def resolve_with_speculation(concept):
    # Start multiple resolutions in parallel
    tasks = [
        resolve_in_vector(concept),
        resolve_in_graph(concept),
        resolve_in_semantic_layer(concept)
    ]
    
    # Return first high-confidence result
    for coro in asyncio.as_completed(tasks):
        result = await coro
        if result.confidence > 0.8:
            # Cancel remaining tasks
            for task in tasks:
                task.cancel()
            return result
    
    # If no high-confidence result, merge all results
    all_results = await asyncio.gather(*tasks, return_exceptions=True)
    return merge_and_rank(all_results)
```

#### 5.5.4 Resolution Cache

Cache common resolution patterns to skip repeated lookups:

```python
# Cache key: normalized concept + context hash
cache_key = f"{normalize(concept)}:{hash(user_context)}"

# Check cache
cached = resolution_cache.get(cache_key)
if cached and cached.age < TTL:
    return cached.resolution

# If not cached, resolve and cache
resolution = await full_resolution(concept, user_context)
resolution_cache.set(cache_key, resolution, ttl=3600)
```

### 5.6 State Machine Model

The orchestrator can be modeled as a state machine for predictable behavior:

```
                    ┌─────────────────────────────────────────────────────┐
                    │                                                     │
                    ▼                                                     │
              ┌──────────┐                                               │
              │  PARSE   │                                               │
              └────┬─────┘                                               │
                   │                                                     │
                   ▼                                                     │
              ┌──────────┐      ambiguity      ┌──────────────┐         │
              │ RESOLVE  │────────────────────▶│ DISAMBIGUATE │         │
              └────┬─────┘                     └──────┬───────┘         │
                   │                                  │                  │
                   │ all resolved                     │ user clarified   │
                   │                                  │                  │
                   ▼                                  │                  │
              ┌──────────┐◀──────────────────────────┘                  │
              │   PLAN   │                                               │
              └────┬─────┘                                               │
                   │                                                     │
                   ▼                                                     │
              ┌──────────┐      denied        ┌──────────┐              │
              │AUTHORIZE │───────────────────▶│  DENIED  │              │
              └────┬─────┘                    └──────────┘              │
                   │                                                     │
                   │ authorized                                          │
                   ▼                                                     │
              ┌──────────┐                                               │
              │ EXECUTE  │                                               │
              └────┬─────┘                                               │
                   │                                                     │
                   ▼                                                     │
              ┌──────────┐      failed        ┌──────────┐              │
              │ VALIDATE │───────────────────▶│  ERROR   │──────────────┘
              └────┬─────┘                    └──────────┘   retry
                   │
                   │ passed
                   ▼
              ┌──────────┐
              │ RESPOND  │
              └────┬─────┘
                   │
                   ▼
              ┌──────────┐      correction    ┌──────────┐
              │   DONE   │◀───────────────────│ FEEDBACK │
              └──────────┘                    └──────────┘
```

---

## Part 6: Knowledge Asset Taxonomy

### 6.1 Asset Type Overview

| # | Asset Type | Primary Store | Indexed In | Runtime Component | Update Frequency |
|---|------------|---------------|------------|-------------------|------------------|
| 1 | Semantic Models | Semantic Layer | Graph, Vector | Semantic Layer API | On change |
| 2 | Business Glossary | Asset Registry | Vector, Graph | Resolution Engine | Weekly |
| 3 | Ontology | Knowledge Graph | Vector | Graph queries | Monthly |
| 4 | Data Contracts | Asset Registry | Graph | Guardrail Engine | On change |
| 5 | Lineage Artifacts | Knowledge Graph | — | Graph traversal | On change |
| 6 | Policy Artifacts | Asset Registry | Graph | Policy Engine (OPA) | On change |
| 7 | Validation Rules | Asset Registry | Graph | Guardrail Engine | On change |
| 8 | Query Templates | Semantic Layer | Graph | Semantic Layer API | On change |
| 9 | Domain Models | Knowledge Graph | — | Graph queries | Quarterly |
| 10 | Tribal Knowledge | Asset Registry | Vector, Graph | Resolution Engine | Continuous |

### 6.1.1 Semantic Contract (First-Class Schema)

A **Semantic Contract** is the composite bundle that makes one data product agent-ready. It is not a single stored document but a logical composition of references, validated for onboarding and demos.

**Schema (composite):**

| Field | Type | Description |
|-------|------|-------------|
| `metric_id` | string | Canonical metric identifier (e.g. net_revenue) |
| `glossary_refs` | array of asset_registry_id | Glossary terms that define the metric and dimensions |
| `ontology_refs` | graph node refs | Entity/dimension relationships in Knowledge Graph |
| `lineage_ref` | graph path | Column-level lineage (metric → columns → sources) |
| `policy_refs` | array of asset_registry_id | Policy artifacts governing access |
| `validation_refs` | array of asset_registry_id | Validation rules applied at execute time |
| `tribal_knowledge_refs` | array of asset_registry_id | Known issues and caveats |
| `certification_tier` | integer (1–4) | Trust tier per Part 8 |
| `semantic_layer_ref` | string | Executable ref (e.g. cube.finance.Revenue.netRevenue) |

**JSON schema (minimal):**

```json
{
  "type": "object",
  "required": ["metric_id", "certification_tier", "semantic_layer_ref"],
  "properties": {
    "metric_id": { "type": "string" },
    "glossary_refs": { "type": "array", "items": { "type": "string" } },
    "ontology_refs": { "type": "array" },
    "lineage_ref": { "type": "object" },
    "policy_refs": { "type": "array", "items": { "type": "string" } },
    "validation_refs": { "type": "array", "items": { "type": "string" } },
    "tribal_knowledge_refs": { "type": "array", "items": { "type": "string" } },
    "certification_tier": { "type": "integer", "minimum": 1, "maximum": 4 },
    "semantic_layer_ref": { "type": "string" }
  }
}
```

### 6.2 Detailed Asset Specifications

[Detailed specifications for each asset type as in v1.0, with updated storage mappings per the revised architecture]

---

## Part 7: The Factory Model

### 7.1 Ingest → Synthesize → Ratify → Publish

Repeatable workflow for scaling data product onboarding:

| Stage | Owner | Automation vs Human | Inputs | Outputs |
|-------|--------|----------------------|--------|---------|
| **Ingest** | Data engineering | Automated | Schemas, stored procs, query logs, docs (Confluence, code) | Raw artifacts in staging |
| **Synthesize** | LLM + pipeline | Automated | Raw artifacts | Proposed glossary terms, metric definitions, lineage stubs |
| **Ratify** | SME (domain owner) | Human (15–30 min per contract) | Proposed definitions | Approved Semantic Contract |
| **Publish** | Pipeline | Automated | Approved contract | Asset Registry, Graph, Vector, Semantic Layer |

**Roles:** Data engineering runs ingest/synthesize and publish; SME ratifies via Slack/UI. **Unit of work:** One Agent-Ready Data Product (one metric or one glossary domain).

### 7.2 Extraction Pipeline

**Purpose:** Automatically harvest context from existing artifacts so that the Context Registry and Semantic Layer can be populated with minimal manual curation.

**Inputs:** Database metadata (information_schema, column comments), stored procedure source code, ETL/dbt/code repos, Confluence/SharePoint pages, query logs (anonymized).

**Stages:**

1. **Crawl:** Scan DB metadata, code repos, and doc URLs; extract raw text and DDL. Output: normalized raw artifacts (tables, columns, procedures, doc chunks).
2. **Profile:** Infer basic semantics (distinct values, data types, naming patterns). Output: profile summaries per table/column.
3. **Infer (LLM):** Propose glossary terms, metric-to-column mappings, lineage hypotheses, tribal-knowledge candidates. Output: draft Semantic Contract components.
4. **Review:** Human-in-the-loop (SME) approves or corrects drafts via UI or Slack. Output: approved assets.
5. **Publish:** Write approved assets to Asset Registry, Graph, and Vector; deploy Semantic Layer changes. Output: updated Context Registry and Semantic Layer.

**Output population:** Glossary/contracts/tribal knowledge → Asset Registry (JSONB); entity/metric/lineage nodes → Knowledge Graph; embeddings of definitions → Vector store; metric definitions → Semantic Layer (Cube/dbt).

---

## Part 8: Trust Architecture

### 8.1 Certification Tiers

| Tier | Name | Validation Required | Use Cases |
|------|------|---------------------|-----------|
| **1** | Regulatory/External | Full audit, SME sign-off, reconciliation | SEC filings, contracts |
| **2** | Executive/Board | Definition review, source validation | Board presentations |
| **3** | Operational/Internal | Automated validation, spot-checks | Departmental reports |
| **4** | Exploratory/Provisional | Automated only, clearly marked | Ad-hoc analysis |

### 8.2 Response Requirements

Every agent response must include:

- **Answer:** The actual result (or disambiguation options).
- **Definition Used:** Which interpretation was applied (e.g. net_revenue per ASC 606).
- **Source:** Where the data came from (semantic layer ref, table, system).
- **Confidence:** Score and level (e.g. high/medium/low).
- **Caveats:** Known issues, tribal knowledge, data quality notes.
- **Lineage:** How the answer was computed (Resolution DAG reference).

**Mapping to Resolution DAG and API:** The Resolution DAG nodes (parse, resolve, plan, authorize, execute, validate, assemble) produce structured output that the API returns as `provenance.dag`, `resolved_concepts`, `confidence_score`, and `warnings`. The execute response includes `results` and `provenance` (resolution_id, resolved_concepts, lineage references).

---

## Part 9: Implementation Roadmap

### 9.1 Phase Overview

| Phase | Timeline | Focus | Key Deliverables |
|-------|----------|-------|------------------|
| **1: Foundation** | Days 1-30 | Prove it works | End-to-end demo, 10 data products, 1 agent integration |
| **2: Factory** | Days 31-60 | Automate inputs | Extraction pipeline, 50 data products, MCP server |
| **3: Scale** | Days 61-90 | Operationalize | Governance model, 150 data products, 2+ agent integrations |
| **4: Expand** | Months 4-6 | Enterprise rollout | 500 data products, multi-cloud support |
| **5: Mature** | Months 7-12 | Operational excellence | 1000+ products, self-sustaining |

### 9.2 Phase 1: Foundation (Days 1-30)

**Week 1: Infrastructure Setup**
- Deploy core stores: Neo4j (graph), Pinecone (vector), PostgreSQL (asset registry)
- Deploy Semantic Layer (Cube.js)
- Configure connectivity to primary data warehouse
- Set up development environment

**Week 2: First Domain Selection & Analysis**
- Select target domain (recommend: "Core Financial Metrics")
- Inventory existing assets: schemas, stored procedures, documentation
- Identify top 10 metrics by business value
- Map tribal knowledge holders

**Week 3: Manual Semantic Contract Creation**
- Build metric definitions in Semantic Layer (manual)
- Create glossary entries in Asset Registry
- Build ontology in Knowledge Graph
- Index glossary in Vector Store
- Define validation rules

**Week 4: Agent Integration & Demo**
- Build Resolution Orchestrator (basic version)
- Create MCP server for agent integration
- Integrate with ONE agent runtime (Azure Foundry OR Vertex AI OR custom)
- Prepare executive demo

**Deliverables**:
- [ ] Infrastructure deployed and operational
- [ ] 10 certified metrics (Tier 2) in Semantic Layer
- [ ] Basic Context Registry operational
- [ ] Working MCP server
- [ ] Integration with 1 agent runtime
- [ ] Working demo: executive asks question, gets accurate cited answer

### 9.3 Phases 2-5

[Detailed phase content similar to v1.0 with agent integration milestones added]

---

## Part 10: Risk Management

### 10.1 Risks and Mitigations

| Risk | Mitigation |
|------|-------------|
| **SME bottleneck** | AI-first (review, don't write); 15–30 min sessions; async workflow; prioritization by business value |
| **Extraction accuracy** | Confidence scoring; mandatory SME validation for Tier 1–2; automated tests against reference answers |
| **Agent hallucination** | Agent never does math; all computation in Semantic Layer; guardrails and validation rules |
| **Security / unauthorized access** | Policy Engine (OPA) at resolve/execute; inherit RLS; integrate with enterprise auth (OIDC); audit log for every resolve/execute |
| **Maintenance burden** | Drift detection; scheduled reviews; ownership accountability; versioning of definitions |
| **Multi-cloud / federation** | Centralized or federated context stores; consistent API and MCP across clouds; shared policy and certification model |

---

## Part 11: Technology Stack

### 11.1 Recommended Components

| Component | Primary Option | Alternatives | Notes |
|-----------|----------------|--------------|-------|
| **Knowledge Graph** | Neo4j | AWS Neptune, Azure Cosmos (Gremlin) | Neo4j for rich Cypher queries |
| **Vector Store** | Pinecone | Weaviate, Milvus, pgvector | Pinecone for managed service |
| **Asset Registry** | PostgreSQL (JSONB) | MongoDB | PostgreSQL for ACID + JSON flexibility |
| **Semantic Layer** | Cube.js | dbt Semantic Layer, LookML | Cube.js for API-first approach |
| **Policy Engine** | OPA | Cedar, custom | OPA for Rego language flexibility |
| **Resolution Orchestrator** | Custom (Python/Go) | Temporal, LangGraph | Custom for full control |
| **Agent Integration** | MCP Server | REST API, gRPC | MCP for standard protocol |
| **LLM (for extraction)** | Claude | GPT-4, open-source | Claude for long context |
| **Monitoring** | Datadog | New Relic, Prometheus | For platform observability |

### 11.2 Integration Protocols

| Protocol | Use Case | Implementation |
|----------|----------|----------------|
| **MCP** | Agent tool integration | MCP Server exposing ECP tools |
| **A2A** | Cross-platform agent communication | A2A-compatible endpoints |
| **REST** | General API access | OpenAPI 3.0 spec |
| **GraphQL** | Flexible querying | Optional, for complex queries |
| **gRPC** | High-performance internal | Between ECP microservices |

---

## Appendices

### Appendix A: API Reference

The API is specified in OpenAPI 3.0. Reference implementation: `openapi/api.yaml` in the ECP repository.

**Endpoints:**

- **POST /api/v1/resolve** — Resolve a business concept to canonical definition and execution plan. Request: `{ concept, user_context? }`. Response: `resolution_id`, `status`, `execution_plan`, `resolved_concepts`, `confidence_score`, `provenance`, `warnings`.
- **POST /api/v1/execute** — Execute a previously resolved query. Request: `{ resolution_id, parameters? }`. Response: `results`, `provenance`, `confidence_score`, `warnings`.
- **GET /api/v1/glossary** — Search glossary (query, domain?). Response: `terms`, `total`.
- **GET /api/v1/lineage** — Get lineage for metric or table (target, depth?). Response: `target`, `nodes`, `edges`.
- **GET /api/v1/metrics** — List metrics (dimension?, domain?, certification_tier?). Response: `metrics`, `total`.
- **GET /api/v1/health** — Health check. Response: `status`, `stores`.

### Appendix B: MCP Tool Definitions

```yaml
# Enterprise Context Platform MCP Server
mcp_server:
  name: enterprise-context-platform
  version: "1.0"
  transport: sse
  
  tools:
    - name: resolve_business_concept
      description: |
        Resolve a business concept (metric, dimension, entity) to its canonical 
        definition and execution plan. This is the primary entry point for 
        semantic resolution.
      input_schema:
        type: object
        properties:
          concept:
            type: string
            description: The business concept to resolve (e.g., "APAC revenue")
          user_context:
            type: object
            properties:
              user_id:
                type: string
              department:
                type: string
              role:
                type: string
        required: [concept]
      
    - name: execute_metric_query
      description: |
        Execute a metric query using a previously resolved execution plan.
        Returns results with full provenance.
      input_schema:
        type: object
        properties:
          resolution_id:
            type: string
            description: ID from a previous resolve_business_concept call
          parameters:
            type: object
            description: Runtime parameters (filters, time range, etc.)
        required: [resolution_id]
      
    - name: query_glossary
      description: |
        Search the business glossary for term definitions.
      input_schema:
        type: object
        properties:
          query:
            type: string
            description: Search query
          domain:
            type: string
            description: Optional domain filter
        required: [query]
      
    - name: get_lineage
      description: |
        Get data lineage for a metric or table.
      input_schema:
        type: object
        properties:
          target:
            type: string
            description: Metric ID or table name
          depth:
            type: integer
            description: How many hops to traverse (default 3)
        required: [target]
      
    - name: list_available_metrics
      description: |
        List metrics available for a given dimension or domain.
      input_schema:
        type: object
        properties:
          dimension:
            type: string
            description: Filter by dimension (e.g., "region")
          domain:
            type: string
            description: Filter by domain (e.g., "finance")
          certification_tier:
            type: integer
            description: Minimum certification tier
```

### Appendix C: Resolution DAG Schema

Minimal JSON Schema for the Resolution DAG (query_id, user_context, nodes, original_query):

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["query_id", "nodes"],
  "properties": {
    "query_id": { "type": "string" },
    "user_context": { "type": "object" },
    "original_query": { "type": "string" },
    "nodes": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["id", "type", "status"],
        "properties": {
          "id": { "type": "string" },
          "type": { "type": "string", "enum": ["parse", "resolve_concept", "plan", "authorize", "execute", "validate", "assemble"] },
          "status": { "type": "string" },
          "depends_on": { "type": "array", "items": { "type": "string" } },
          "output": { "type": "object" }
        }
      }
    }
  }
}
```

Edges are implied by `depends_on` (node A depends_on node B → edge B → A).

### Appendix D: Glossary

| Term | Definition |
|------|------------|
| **Semantic Contract** | Complete specification enabling correct agent use of a data product |
| **Context Registry** | Collective term for all context stores (graph + vector + asset registry) |
| **Semantic Layer** | Deterministic computation engine for metrics |
| **Semantic Firewall** | Boundary between agents and physical data estate |
| **Resolution Orchestrator** | Engine that coordinates multi-store queries to resolve business concepts |
| **Resolution DAG** | Directed acyclic graph tracking the resolution process for a query |
| **Agent-Ready Data Product** | Data asset with complete Semantic Contract, ready for agent consumption |
| **Tribal Knowledge** | Undocumented institutional knowledge |
| **Certification Tier** | Trust level assigned to a data product |
| **MCP** | Model Context Protocol - standard for agent-tool communication |
| **A2A** | Agent-to-Agent protocol - standard for cross-platform agent communication |

---

*End of Specification v2.0*