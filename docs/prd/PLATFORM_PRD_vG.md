# Cogentiq Studio: Complete Platform Product Requirements Document

**Version:** 5.0.0-MASTER-FINAL
**Status:** READY FOR ENGINEERING
**Classification:** Internal - Confidential
**Date:** January 26, 2026

---

# 1. EXECUTIVE SUMMARY

## 1.1 Product Vision
Cogentiq Studio is the **Logic Control Plane** for Enterprise AI Agents. We decouple the **"Brain"** (Business Physics, Rules, Definitions) from the **"Body"** (LLM, Runtime, Orchestration). While the Body runs on platforms like Azure AI Foundry or AWS Bedrock, the Brain lives in Cogentiq.

This platform solves the "Last Mile" problem: transforming stochastic LLM reasoning into deterministic business actions.

## 1.2 Core Value Propositions
1.  **Deterministic Accuracy:** Force LLMs to call governed tools (e.g., `calculate_metric`) rather than hallucinating SQL logic.
2.  **Day 2 Survival:** Automated protection against schema drift. When the database changes, Cogentiq adapts; the agent prompt does not need rewriting.
3.  **Audit Defense:** Full lineage tracking for every generated answer, tracing back to specific metric versions and data snapshots.
4.  **IP Acceleration:** Pre-built "Domain Packs" (Insurance, CPG) allowing rapid deployment of industry-standard logic.

---

# 2. PLATFORM ARCHITECTURE

## 2.1 Architecture Pattern: The Logic Control Plane
We do not build the runtime; we inject intelligence into existing runtimes. A lightweight SDK (**"Brain Stem"**) sits inside the client's agent (on Azure/AWS) and makes API calls to Cogentiq for routing, logic retrieval, and validation.

## 2.2 Component Stack
| Layer | Component | Role |
| :--- | :--- | :--- |
| **L6: Interfaces** | Ontology Workbench (UI), CLI | Authoring & management tools. |
| **L5: Governance** | Drift Monitor, Impact Analysis | "Day 2" protection & simulation. |
| **L4: Registry** | Domain Packs, Prompts | Reusable IP assets. |
| **L3: Orchestration** | Neuro-Symbolic Router | Decides Symbolic (SQL) vs. Neural (RAG) execution. |
| **L2: Domain Intel** | Ontology, Semantic, Constraint | The "Brain" encoding business physics. |
| **L1: Control Plane** | Brain Stem SDK, MCP Adapters | Connects to Runtime & Data. |

---

# 3. DETAILED FUNCTIONAL REQUIREMENTS

## 3.1 Layer 1: Runtime Injection (The SDK)
* **Context Injection:** Dynamically inserts relevant Ontology definitions into the System Prompt based on user query intent.
* **Tool Routing:** Intercepts generic tool calls and routes them to the Semantic Catalog for execution.
* **Supported Runtimes:**
    * **Azure AI Foundry:** Deployed as a "Custom Skill".
    * **AWS Bedrock:** Deployed as a "Lambda Action Group".
    * **Python Native:** PyPI library for LangChain/LangGraph.

## 3.2 Layer 2: Domain Intelligence
* **Ontology Registry:**
    * Support hierarchical namespaces: `core` -> `industry` (e.g., finance) -> `tenant` (client extension).
    * Storage: Hybrid relational (PostgreSQL) for metadata and Graph (Neo4j) for traversal.
* **Semantic Catalog:**
    * YAML-based metric definitions.
    * Must support compilation of formulas (e.g., `revenue - cost`) into dialect-specific SQL (Snowflake/Databricks).
* **Constraint Engine:**
    * **Pre-Compute:** Validate user permissions against query intent (e.g., "Analyst cannot query PII").
    * **Post-Compute:** Validate data sanity (e.g., "Gross Margin cannot be > 100%").
    * Technology: Common Expression Language (CEL).

## 3.3 Layer 3: Orchestration
* **Neuro-Symbolic Router:**
    * **Symbolic Path:** High confidence mapping to a defined Metric -> Execute deterministic SQL.
    * **Neural Path:** Low mapping confidence / Unstructured data -> Execute RAG/LLM reasoning.
    * **Ambiguous Path:** Trigger clarification flow ("Did you mean A or B?").

## 3.4 Layer 5: Governance & Observability
* **Schema Drift Monitor:** Automated job that runs daily. Validates that all defined metrics still compile against the live database schema. Alerts on failure.
* **Impact Analysis Engine:** Simulation capability. Before publishing a metric change, replay the last 1,000 queries to quantify variance/errors.
* **Reinforcement Loop:** "Thumbs down" feedback creates a ticket in the Ontology Workbench for review.

---

# 4. INGESTION & HARVESTING MODULE
* **Objective:** Automate the migration from Legacy (SQL/Excel) to Cogentiq.
* **Pipeline:**
    1.  **Crawl:** Scan Database Information Schema.
    2.  **Profile:** Sample data to infer semantics (e.g., distinct values, distribution).
    3.  **Infer:** LLM suggests Entity/Attribute mappings.
    4.  **Review:** Human-in-the-loop approval via Workbench.
    5.  **Publish:** Commit to Registry.

---

# 5. DATA MODELS
* **Primary Entities:** `Tenant`, `OntologyClass`, `Metric`, `DataSource`, `LineageRecord`.
* **Storage Strategy:**
    * **Metadata:** PostgreSQL (ACID compliance).
    * **Relationships:** Neo4j (Entity resolution/traversal).
    * **Session State:** Redis (Fast context retrieval).
    * **Logs:** ClickHouse/S3 (Immutable audit trail).

---

# 6. NON-FUNCTIONAL REQUIREMENTS
* **Latency:** Cogentiq processing overhead < 200ms (p95).
* **Scalability:** Horizontal scaling for API and Worker nodes.
* **Security:** OIDC Authentication; Pass-through RLS (Database enforces row security).