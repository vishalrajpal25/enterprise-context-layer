# ECP Runbook

## Local Development

1. **Start infrastructure:** `docker compose up -d`
2. **Seed data:** Run `scripts/seed_all.sh` (and Neo4j seed via `scripts/seed_neo4j.cypher` if needed)
3. **Start API:** `uvicorn api.main:app --reload --port 8000`
4. **Demo:** `./scripts/demo.sh`
5. **Tests:** `pytest tests/ -v --ignore=tests/test_e2e.py`

## Health Checks

- **API:** `GET http://localhost:8000/api/v1/health` — returns status of each store (graph, vector, registry, semantic, policy).
- **Postgres:** `pg_isready -U ecp -d ecp_registry`
- **Neo4j:** `curl http://localhost:7474`
- **Cube:** `curl http://localhost:4000/readyz`
- **OPA:** `curl http://localhost:8181/health`

## Common Issues

| Issue | Check | Action |
|-------|--------|--------|
| Resolve returns access_denied | OPA policy and user role | Ensure user_context.role is in policy (e.g. analyst, finance_analyst). |
| Execute returns not found | Resolution cache | Resolution IDs are in-memory; restart API clears cache. Call resolve then execute in same session. |
| Glossary/lineage empty | Seeds | Re-run seed_registry.sql and seed_neo4j.cypher. |
| Cube query error | Cube schema and DW | Ensure ecp_dw has fact_revenue_daily and Cube schema matches. |

## Staging / Prod

- **Config:** Set env from vault or secret manager (no .env in prod).
- **Secrets:** POSTGRES_PASSWORD, NEO4J_PASSWORD, CUBE_API_TOKEN, etc. from vault.
- **Deploy:** Kubernetes or PaaS; use health endpoint for readiness/liveness.
- **E2E:** Run E2E suite against staging URL with SKIP_E2E=0 and ECP_E2E_URL=<staging>.
