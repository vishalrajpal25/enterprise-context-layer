# Enterprise Data Estate Readiness for Agentic AI

## Problem Statement

### Context & Background

You are advising a large enterprise (Fortune 500 financial data company—similar to FactSet, Bloomberg, or Reuters) that has built a complex data estate over 15-20 years.

#### Technical Reality

| Component | State |
|-----------|-------|
| **Databases** | Tens of platforms across SQL Server, Oracle, Snowflake, PostgreSQL, legacy mainframes |
| **Business Logic** | Thousands of stored procedures containing embedded logic, some dating back 15+ years |
| **Technical Debt** | Views built on views; undocumented dependencies; inconsistent naming |
| **ETL Pipelines** | Transformation logic scattered across Databricks, Informatica, SSIS, dbt, custom scripts |
| **Data Lakes** | Semi-structured and unstructured data mixed with processed structured data |
| **APIs** | Multiple interfaces exposing data to internal and external consumers |
| **Sources of Truth** | Multiple, conflicting—some sources claim truth, others compute it at runtime |

#### Organizational Reality

| Challenge | Manifestation |
|-----------|---------------|
| **Definition Variance** | "Revenue" means different things to Sales, Finance, and Operations |
| **Undocumented Jargon** | Acronyms pervasive and inconsistently documented |
| **Tribal Knowledge** | The "right" way to query data is passed down verbally or lives in individuals' heads |
| **Hidden Gotchas** | Known data issues and workarounds not systematically captured |
| **Fragmented Ownership** | No single person understands the full estate |
| **Scattered Documentation** | Confluence, SharePoint, wikis, email threads, Slack—mostly outdated |

#### Business Pressure

- Leadership expects GenAI to "just work" on enterprise data—they don't understand why it hallucinates or returns wrong answers
- Competitors moving fast; 12-18 month window to establish AI-driven data products
- Regulatory requirements demand accuracy, auditability, and explainability
- Traditional governance programs take 2-3 years and often fail before completion

---

## The Core Problem

**AI agents fail on enterprise data not because of reasoning limitations, but because of missing context.**

When a user asks an agent "What was our APAC revenue last quarter?", the agent doesn't know:

- Which definition of "revenue" to use (gross? net? recognized? booked?)
- What "APAC" means in this organization (includes China? excludes ANZ?)
- Whether "last quarter" is fiscal or calendar
- Which source system is authoritative for this metric
- That Q4 2019 data is incomplete due to a migration
- That APAC cost center definitions changed in 2021
- What stored procedure or view contains the "correct" calculation
- What joins, filters, and transformations are required

This context exists—but it's scattered across schemas, code, documentation, and people's heads. It was never designed to be machine-readable or agent-consumable.

**The traditional approach—manual data cataloging, governance programs, stewardship councils—takes 2-3 years and tens of millions of dollars. And it often fails before completion.**

---

## The Business Goal

> **Enable a scalable (10 → 100 → 1000 datasets) agentic data access layer that is safe, accurate, and trustable—on the existing legacy data estate—in minimum possible time.**

### Requirement Breakdown

| Dimension | Requirement | Success Criteria |
|-----------|-------------|------------------|
| **Scalable** | Approach works for 10 datasets and still works for 1000; can't be artisanal or one-off | Linear cost scaling; consistent onboarding time per dataset |
| **Safe** | Agents cannot return harmful, misleading, or unauthorized data | Zero unauthorized exposures; guardrails catch anomalies |
| **Accurate** | Answers correct per business definitions, not hallucinated or approximated | Match validated reference answers; SME approval |
| **Trustable** | Every answer explainable, auditable, traceable to authoritative sources | Full provenance on every response |
| **Existing Estate** | Cannot wait for multi-year modernization; must work with current systems | Incremental adoption; no data migration required |
| **Minimum Time** | Weeks to months, not years; leverage automation and smart prioritization | Initial value in 90 days |

---

## Key Challenges to Address

### 1. The Context Gap
- How do you capture and represent the business context (definitions, rules, logic, exceptions) that agents need to answer questions correctly?
- How do you make this context queryable and injectable at runtime?

### 2. The Tribal Knowledge Problem
- How do you extract undocumented knowledge from people's heads, Slack threads, old emails, and code comments?
- How do you keep this knowledge current as the organization evolves?

### 3. The Scale Problem
- How do you avoid the "boil the ocean" trap of cataloging everything?
- What's the unit of work that can be manufactured repeatedly?
- How do you prioritize which data to make AI-ready first?

### 4. The Accuracy Problem
- How does an agent know which source, calculation, or definition is authoritative?
- How do you handle ambiguity when multiple valid interpretations exist?
- How do you prevent agents from using stale, deprecated, or incorrect data?

### 5. The Trust Problem
- How do you provide provenance, confidence scores, and audit trails with every answer?
- How do you certify data for different use cases (internal analytics vs. external reporting vs. regulatory)?
- How do you explain to a regulator or executive exactly how an answer was derived?

### 6. The Safety Problem
- How do you prevent agents from accessing unauthorized data?
- How do you catch obviously wrong results before they reach users?
- How do you enforce business rules and constraints at query time?

### 7. The Maintenance Problem
- How do you keep the context layer in sync as the underlying data estate changes?
- How do you incorporate feedback when agents make mistakes?
- How do you handle versioning of definitions and logic over time?

---

## Constraints & Boundaries

### What We CAN Do
- Build new layers/services that sit between agents and the data estate
- Use LLMs and AI to accelerate extraction and synthesis
- Deploy new infrastructure (knowledge graphs, vector stores, semantic layers, APIs)
- Prioritize high-value data products over comprehensive coverage
- Implement human-in-the-loop validation for critical use cases

### What We CANNOT Do
- Wait for a 2-year data governance program
- Assume perfect data quality or complete documentation exists
- Require migration of data to new platforms
- Force organizational restructuring before delivering value

---

## Solution Principles

### Core Thesis
**Context is the product, not data.** The data already exists. What's missing is the machine-readable semantic contract that tells an agent *how* to use that data correctly. We don't fix the data before use; we wrap messy data with rich context that enables correct interpretation.

### Architectural Principles

1. **The Semantic Firewall**: Agents never directly touch the messy data estate. Everything passes through a controlled boundary that translates between agent queries and legacy systems.

2. **The Agent Never Does Math**: Agents orchestrate and translate, but all computation happens in deterministic systems (databases, semantic layers). LLMs reason; databases compute.

3. **Context-First, Not Data-First**: We don't clean data before using it. We build a context layer that wraps the data as-is—an "institutional memory API" that agents query before they query data.

4. **Manufacturing, Not Art**: Data onboarding is a repeatable factory process, not bespoke craftsmanship. The unit of production is the "Semantic Contract."

5. **Separation of Concerns**: The Context Registry (knowledge about data) is separate from the Semantic Layer (computation on data). Agents reason using the first, then act through the second.

---

## Knowledge Asset Taxonomy

Agents need access to multiple types of knowledge assets, not just an ontology:

| # | Asset Type | Purpose | Examples |
|---|------------|---------|----------|
| 1 | **Semantic Models** | Executable metric/dimension definitions | KPIs, calculations, hierarchies, time intelligence |
| 2 | **Business Glossary** | Term definitions, synonyms, acronyms | "APAC" definition, "Revenue" variants by context |
| 3 | **Ontology** | Entity relationships and attributes | Customer → Region → Cost Center relationships |
| 4 | **Data Contracts** | SLAs, quality expectations, ownership | Freshness targets, completeness rules |
| 5 | **Lineage Artifacts** | Column-level provenance, transformations | Source-to-target mappings |
| 6 | **Policy Artifacts** | Access control, classification, retention | PII tags, role restrictions |
| 7 | **Validation Rules** | Business rules, anomaly bounds | Revenue ≥ 0, variance thresholds |
| 8 | **Query Templates** | Canonical patterns, blessed joins | Pre-approved query structures |
| 9 | **Domain Models** | Bounded contexts, cross-domain mappings | Sales.Customer vs. Finance.Customer |
| 10 | **Tribal Knowledge** | Known issues, workarounds, gotchas | "Q4 2019 APAC data incomplete" |

---

## Success Criteria

A successful solution would:

- Enable agents to answer business questions accurately using the existing data estate
- Require minimal manual curation (80%+ automated extraction)
- Scale linearly, not exponentially, as datasets are added
- Provide explainable, auditable answers with clear provenance
- Prevent unsafe or unauthorized data access
- Improve over time through feedback loops
- Deliver initial value (50+ high-value data products) within 90 days
- Scale to 500+ data products within 12 months
- Support industry-standard protocols (MCP, REST APIs) for agent integration

---

## Perspectives to Consider

Think deeply about this problem from multiple perspectives:

- **Business Owner**: What's the fastest path to value? What risks must be mitigated?
- **Product Manager**: What's the MVP? How do we prioritize? What does the roadmap look like?
- **Data Architect**: What systems and data structures are needed? How do they integrate?
- **AI/ML Engineer**: How do we leverage LLMs for extraction, synthesis, and runtime resolution?
- **Enterprise Architect**: How does this fit into the broader technology landscape? What are the integration patterns?
- **End User**: What does the experience look like? How do I trust the answers I get?
- **Governance/Compliance**: How do we ensure auditability? How do we handle regulatory requirements?

---

## Architecture Overview

The solution consists of five layers:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          AGENTIC INTERFACE LAYER                            │
│              (User queries, orchestration, response generation)             │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                           SEMANTIC FIREWALL                                 │
│           (Intent Resolution → Disambiguation → Execution → Guardrails)     │
└─────────────────────────────────────────────────────────────────────────────┘
                    │                                   │
        ┌───────────┴───────────┐           ┌──────────┴──────────┐
        ▼                       ▼           ▼                      ▼
┌───────────────────────┐   ┌───────────────────────────────────────────────┐
│   CONTEXT REGISTRY    │   │              SEMANTIC LAYER                   │
│   (Knowledge Assets)  │   │           (Computation Engine)                │
│                       │   │                                               │
│  • Business Glossary  │   │  • Metrics & KPIs                             │
│  • Ontology / Graph   │   │  • Dimensions & Hierarchies                   │
│  • Data Contracts     │   │  • Time Intelligence                          │
│  • Lineage Artifacts  │   │  • Query Templates                            │
│  • Policy Artifacts   │   │  • Canonical Joins                            │
│  • Validation Rules   │   │                                               │
│  • Tribal Knowledge   │   │  (Cube.js / dbt Semantic Layer / LookML)      │
│  • Domain Models      │   │                                               │
└───────────────────────┘   └───────────────────────────────────────────────┘
                    │                                   │
                    └───────────────┬───────────────────┘
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                         PHYSICAL DATA ESTATE                                │
│          (Snowflake, SQL Server, Oracle, Data Lake, APIs - unchanged)       │
└─────────────────────────────────────────────────────────────────────────────┘
```

**Key Separation**:
- **Context Registry**: Holds *knowledge about* the data—definitions, relationships, policies, lineage, tribal knowledge. Queryable by the agent to understand meaning and resolve ambiguity.
- **Semantic Layer**: Holds *executable logic*—metric calculations, dimension definitions, query templates. What actually computes answers. Agent calls it; never bypasses it.

The agent reasons using the Context Registry, then acts through the Semantic Layer. It never writes raw SQL against the physical estate.

---

## The Factory Model

To scale from 10 to 1000 datasets, treat data onboarding as a manufacturing process:

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   INGEST    │ →  │  SYNTHESIZE │ →  │   RATIFY    │ →  │   PUBLISH   │
│ (Automated) │    │ (Automated) │    │  (Human)    │    │ (Automated) │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
      │                  │                  │                  │
      ▼                  ▼                  ▼                  ▼
 Read schemas,     LLM proposes       SME validates      Push to Context
 stored procs,     definitions,       via Slack/UI       Registry and
 query logs,       identifies         (15-30 min         Semantic Layer
 documentation     patterns           per contract)
```

**Why this scales**: You aren't asking SMEs to write documentation from scratch; you're asking them to review and approve AI-generated proposals based on historical usage patterns.

---

## Trust Architecture

### Certification Tiers

| Tier | Name | Validation Required | Use Cases |
|------|------|---------------------|-----------|
| **1** | Regulatory/External | Full audit, SME sign-off, reconciliation | SEC filings, contracts |
| **2** | Executive/Board | Definition review, source validation | Board presentations |
| **3** | Operational/Internal | Automated validation, spot-checks | Departmental reports |
| **4** | Exploratory/Provisional | Automated only, clearly marked | Ad-hoc analysis |

### Response Requirements

Every agent response must include:
- **Answer**: The actual result
- **Definition Used**: Which interpretation was applied
- **Source**: Where the data came from
- **Confidence**: How reliable is this answer
- **Caveats**: Any known issues or limitations
- **Lineage**: How the answer was computed

---

## Roadmap Overview

| Phase | Timeline | Deliverables |
|-------|----------|--------------|
| **Foundation** | Days 1-30 | Infrastructure, 10 certified metrics, working demo |
| **Factory** | Days 31-60 | Extraction pipeline, 50 data products, SME workflow |
| **Scale** | Days 61-90 | Governance model, 150 data products, 100 pilot users |
| **Expand** | Months 4-6 | 500 data products, external use cases |
| **Mature** | Months 7-12 | 1000+ products, operational excellence |

---

## Key Risks to Mitigate

| Risk | Mitigation |
|------|------------|
| **SME availability bottleneck** | AI-first (review, don't write); 15-min sessions; async workflow |
| **Extraction accuracy** | Confidence scoring; mandatory SME validation for Tier 1-2 |
| **Agent hallucination** | Agent never does math; all computation in Semantic Layer |
| **Organizational resistance** | Frame as enabling governance; business units own domains |
| **Maintenance burden** | Drift detection; scheduled reviews; ownership accountability |
| **Security/access control** | Inherit existing RLS; integrate with enterprise auth |

---

## Your Task

Propose a comprehensive solution that addresses this problem. Your proposal should include:

1. **Architecture**: Detailed component design with clear interfaces
2. **Data Model**: Schema for Semantic Contracts and knowledge assets
3. **Extraction Pipeline**: How to automatically harvest context from existing artifacts
4. **Runtime Flow**: Step-by-step resolution from user query to trusted answer
5. **Factory Process**: Repeatable workflow for scaling data product onboarding
6. **Trust Model**: How confidence, certification, and provenance work
7. **Implementation Roadmap**: Phased approach with clear milestones
8. **Technology Recommendations**: Specific tools and platforms
9. **Risk Mitigation**: How to address each identified risk
10. **Success Metrics**: How to measure progress and outcomes

Remember: The solution must be incremental, deliver value quickly, and scale without requiring data migration or multi-year governance programs.

---

## Reference Documents

For detailed specifications, see:
- `enterprise-context-platform-spec.md` - Complete technical specification
- `agents.md` - Agent implementation guide (forthcoming)