# Enterprise Context Platform (ECP) – Demo One-Pager

## What It Is

ECP is a **semantic mediation layer** between AI agents and your legacy data. It resolves business concepts (e.g. “APAC revenue last quarter”) to canonical definitions and execution plans, runs queries through a semantic layer, and returns answers with **full provenance** and **guardrails**.

## Key Points for Clients

- **Context-first:** We don’t fix the data first; we wrap it with machine-readable context so agents use it correctly.
- **Semantic firewall:** Agents never write raw SQL against your estate; they call ECP, which resolves and executes via a governed semantic layer.
- **Provenance on every answer:** Every response includes definition used, source, confidence, and lineage.
- **Demo uses synthetic data only:** No connection to real systems; safe for client demos.

## Demo Flow (5 minutes)

1. **Resolve** – “What was APAC revenue last quarter?”  
   ECP returns a resolution (metric = Net Revenue, region = APAC, time = Q3 2024) and an execution plan.

2. **Execute** – Use the resolution ID to run the query.  
   Response includes result plus provenance (sources, definitions).

3. **Glossary** – Search for “revenue” to show business-term definitions and context.

4. **Lineage** – Ask “Where does net_revenue come from?” to show upstream tables and transformations.

5. **Metrics list** – List metrics available for a dimension (e.g. region) to show discoverability.

## How to Run the Demo

- **Local:** `docker compose up -d` → run seed scripts → start API (`uvicorn api.main:app --port 8000`) → run `./scripts/demo.sh`.
- **Staging:** Same flow against the staging API URL; no real data.

## References

- Technical spec: `docs/prd/enterprise-context-platform-spec.md`
- Product requirements: `docs/prd/PROMPT.md`
- Implementation plan: `docs/ECP-IMPLEMENTATION-PLAN.md`
