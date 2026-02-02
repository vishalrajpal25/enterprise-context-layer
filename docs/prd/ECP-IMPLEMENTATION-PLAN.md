# ECP Implementation Plan

This document is the agreed implementation plan for the Enterprise Context Platform. Coding proceeds using this document and the PRD/spec as the source of truth.

**Authoritative references:**
- [docs/prd/enterprise-context-platform-spec.md](prd/enterprise-context-platform-spec.md) – Technical specification
- [docs/prd/PROMPT.md](prd/PROMPT.md) – Product requirements

---

## Part A: Spec Validation Summary

### A.1 Requirements Coverage (PROMPT vs Spec)

| PROMPT Requirement | Spec Location | Met? | Notes |
|--------------------|---------------|-----|-------|
| Scalable 10→100→1000 agentic layer | Part 2.2, 2.5, Part 9 | Yes | Success metrics and phases align |
| Safe, accurate, trustable | Part 2.2, Part 5, Part 8 | Yes | Resolution DAG includes authorize/validate |
| Existing estate, no migration | Part 1, 2.4, 3.1 | Yes | Semantic Firewall; agents never touch raw estate |
| Minimum time (90d value) | Part 9.1–9.2 | Yes | Foundation phase 1–30 days |
| Context-First, Semantic Firewall, Agent Never Does Math | Part 1, 3.1, 4.4.4 | Yes | Clear separation; computation in Semantic Layer |
| Manufacturing not Art (Factory) | Part 7 ref, Part 9 | Partial | Part 7 placeholder — inlined in spec fill-in |
| Knowledge Asset Taxonomy (10 types) | Part 4.3, 6.1 | Yes | Same 10 types with store mapping |
| Separation: Context Registry vs Semantic Layer | Part 4, 4.5 | Yes | Graph + Vector + Asset Registry vs Cube/dbt |
| Trust: certification tiers, provenance, caveats | Part 8 ref, Part 5 | Partial | Part 8 placeholder — inlined in spec fill-in |
| MCP, REST for agent integration | Part 3, Appendix B | Yes | MCP tools and REST patterns defined |
| Extraction Pipeline | Part 9 Phase 2 | Partial | Pipeline design added in spec fill-in |
| Data Model: Semantic Contracts | Part 4.4, 6 | Partial | Semantic Contract schema added in spec fill-in |
| Runtime Flow (query to answer) | Part 5 | Yes | End-to-end flow with 10 scenarios |
| Implementation Roadmap | Part 9 | Yes | Phases 1–5; Phase 1 week-by-week |
| Technology Recommendations | Part 11 | Yes | Stack table with alternatives |
| Risk Mitigation | Part 10 ref | Partial | Inlined in spec fill-in |

### A.2 Recommended Spec Updates (Pointers)

1. **Part 7 (Factory Model):** Inline Ingest → Synthesize → Ratify → Publish with roles and automation vs human steps.
2. **Part 8 (Trust Architecture):** Inline certification tiers (1–4), response requirements, mapping to DAG/API.
3. **Part 10 (Risk Management):** Inline risks and mitigations (SME, extraction, hallucination, security, maintenance, multi-cloud).
4. **Appendix A (API Reference):** OpenAPI 3.0 outline — implemented in `openapi/api.yaml`.
5. **Appendix C (Resolution DAG):** Minimal JSON Schema for resolution_dag — added in spec fill-in.
6. **7.2 Extraction Pipeline:** New subsection: inputs, stages (crawl → profile → infer → review → publish), output to stores.
7. **Semantic Contract schema:** New subsection in Part 4 or 6: composite schema (metric_id, glossary_refs, etc.).

### A.3 Conclusion

Core product and architecture are met by the spec. Placeholders (Factory, Trust, Risk, API, DAG schema, Extraction, Semantic Contract) are resolved in the spec fill-in (todo 10) and in this repo (OpenAPI in `openapi/api.yaml`).

---

## Part B: Implementation Plan (Component Bootstrapping)

### B.1 Principles

- **Demoable and testable without real data:** All features verifiable via mock/synthetic data only.
- **Local and prod parity:** Single codebase; env-driven config; Docker Compose locally; Kubernetes/PaaS for prod.
- **Enterprise standards:** Clean architecture, explicit API contracts, unit/integration/contract tests, observability, secrets outside code.

### B.2 Environment and Data Strategy

- **Environments:** Local (Docker Compose: Postgres, Neo4j, pgvector, Cube, OPA); Staging/Prod (same codebase, config via env/vault).
- **Mock/synthetic data:** Asset Registry seeds, Neo4j Cypher seeds, Vector seeds, Cube synthetic DW, OPA Rego + test data. No real enterprise data.
- **Testing:** Unit (mocked adapters), Integration (orchestrator + local stores), Contract (OpenAPI/MCP), E2E (curated NL queries + demo script).

### B.3 Component Bootstrapping Order

| Order | Component | Deliverable |
|-------|-----------|-------------|
| 1 | Repo, env, contracts | Repo structure, `.env.example`, OpenAPI YAML |
| 2 | Local infrastructure | `docker-compose.yml`, health checks |
| 3 | Synthetic data and seeds | Seed scripts, Cube models, OPA policies |
| 4 | Store adapters | Adapter interfaces + implementations |
| 5 | Resolution Orchestrator | `resolve(query, user_context) -> ResolutionResult` |
| 6 | REST API | FastAPI: /resolve, /execute, glossary, lineage, metrics |
| 7 | MCP Server | Five tools delegating to Orchestrator/API |
| 8 | E2E demo and regression | Demo script, E2E suite, 1-pager |
| 9 | Prod readiness | CI, observability, runbook |
| 10 | Spec fill-in | Updated spec (Factory, Trust, Risk, API, DAG, Extraction, Contract) |

### B.4 Clean Architecture and Standards

- Bounded contexts: Resolution, Context Registry, Semantic Layer, Policy, API/MCP.
- Store access behind interfaces (GraphStore, VectorStore, AssetRegistry, SemanticLayerClient, PolicyEngine).
- Configuration from environment; no hardcoded credentials.
- Structured errors; resolution_id for execute; idempotent read APIs.
- AuthN/AuthZ at API/MCP boundary; audit log for resolve/execute.
- Request IDs, structured logging, metrics, optional tracing.

### B.5 Deliverables Checklist

- [x] Repo structure, env config, OpenAPI skeleton
- [x] Docker Compose: Postgres, Neo4j, Vector, Cube, OPA + synthetic DW
- [x] Seed data: Asset Registry, Graph, Vector, Cube metrics, OPA policies
- [x] Store adapters + Resolution Orchestrator (single path)
- [x] REST API: /resolve, /execute, glossary, lineage, metrics
- [x] MCP Server: five tools
- [x] E2E test suite and demo script
- [x] CI: build, unit, integration, contract, E2E
- [x] Runbook and client one-pager
- [x] Spec placeholders filled
