# Enterprise Context Platform (ECP)

Semantic mediation layer between AI agents and legacy data estates. Enables agents to query, analyze, and act on enterprise data accurately and safely via context resolution and a semantic firewall.

## References

- **PRD / Product requirements:** [docs/prd/PROMPT.md](docs/prd/PROMPT.md)
- **Technical specification:** [docs/prd/enterprise-context-platform-spec.md](docs/prd/enterprise-context-platform-spec.md)
- **Implementation plan:** [docs/ECP-IMPLEMENTATION-PLAN.md](docs/ECP-IMPLEMENTATION-PLAN.md)

## Quick Start (Local)

1. Copy `.env.example` to `.env` and set values.
2. Start infrastructure: `docker compose up -d`
3. Run seeds: `scripts/seed_all.sh` (or per-store scripts)
4. Start API: `uvicorn api.main:app --reload --port 8000`
5. Resolve: `POST http://localhost:8000/api/v1/resolve` with `{"concept": "APAC revenue last quarter", "user_context": {"department": "finance"}}`

## Repo Layout

- `src/ecp/` – Core: adapters, orchestrator, domain models
- `api/` – FastAPI REST app
- `mcp_server/` – MCP server (tools delegate to API)
- `scripts/` – Seed and demo scripts
- `tests/` – Unit, integration, contract, E2E
- `openapi/` – OpenAPI 3.0 spec
- `docker/` – Dockerfiles and compose

## Environments

- **Local:** Docker Compose (Postgres, Neo4j, pgvector, Cube, OPA); synthetic data only.
- **Staging/Prod:** Same codebase; config via env/vault; deploy via Kubernetes or PaaS.

## License

Proprietary.
