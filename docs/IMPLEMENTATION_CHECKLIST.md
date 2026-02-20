# Enterprise Context Platform - Implementation Checklist

**Version:** 1.0
**Last Updated:** February 2, 2026
**Status:** Phase 1 - Production Hardening (In Progress)

This document serves as the master checklist for ECP implementation. It tracks progress across all phases and can be used to resume work across sessions.

---

## Phase 1: Production Hardening (Weeks 1-4)

**Goal:** Make the platform production-ready for limited pilot deployment.

### Week 1: Observability & Logging ✅ COMPLETE

#### Day 1-2: Structured Logging & Metrics
- [x] Create observability module structure (`src/ecp/observability/`)
- [x] Implement structured logging with structlog
  - [x] Request-scoped logging with request IDs
  - [x] JSON format for production
  - [x] Pretty console format for development
  - [x] Context binding/unbinding
- [x] Implement Prometheus metrics
  - [x] Request metrics (resolve/execute totals and latency)
  - [x] Store query metrics (per-store latency and errors)
  - [x] Policy decision metrics
  - [x] Confidence and validation metrics
  - [x] Error tracking by type and component
- [x] Create request tracking middleware
  - [x] Request ID generation
  - [x] X-Request-ID header support
  - [x] Automatic request/response logging
  - [x] Error tracking
- [x] Integrate observability into API
  - [x] Add middleware to FastAPI
  - [x] Add `/metrics` endpoint
  - [x] Update resolve/execute endpoints with logging
  - [x] Update health endpoint with logging
- [x] Enhance orchestrator with observability
  - [x] Logging at every DAG stage
  - [x] Store query timing
  - [x] Error handling with logging
  - [x] Policy evaluation tracking
- [x] Update dependencies
  - [x] Add `structlog>=24.1.0`
  - [x] Add `prometheus-client>=0.19.0`
- [x] Create unit tests
  - [x] `tests/test_observability.py`
- [x] Document implementation
  - [x] Create `IMPLEMENTATION_STATUS.md`

**Files Created:**
- `src/ecp/observability/__init__.py`
- `src/ecp/observability/logging.py`
- `src/ecp/observability/metrics.py`
- `src/ecp/observability/middleware.py`
- `tests/test_observability.py`
- `IMPLEMENTATION_STATUS.md`
- `docs/IMPLEMENTATION_CHECKLIST.md` (this file)

**Files Modified:**
- `api/main.py` - Added observability
- `src/ecp/orchestrator/orchestrator.py` - Enhanced with logging/metrics
- `pyproject.toml` - Added dependencies

---

### Week 1: Error Handling & Resilience 🔄 IN PROGRESS

#### Day 3-4: Retry Logic & Circuit Breakers

**Retry Logic:**
- [ ] Add `tenacity` to dependencies
- [ ] Create error handling module (`src/ecp/resilience/`)
  - [ ] `retry.py` - Retry decorators and configuration
  - [ ] `exceptions.py` - Custom exception hierarchy
- [ ] Define retryable vs non-retryable errors
  - [ ] Retryable: Connection errors, timeouts, 5xx, transient failures
  - [ ] Non-retryable: 4xx, validation errors, authorization failures
- [ ] Implement retry logic in store adapters
  - [ ] Graph store (Neo4j)
  - [ ] Vector store (pgvector)
  - [ ] Asset registry (PostgreSQL)
  - [ ] Semantic layer (Cube)
  - [ ] Policy engine (OPA)
- [ ] Configure retry strategy
  - [ ] Exponential backoff with jitter
  - [ ] Max 3 retries
  - [ ] Configurable timeouts
- [ ] Add retry metrics
  - [ ] Track retry attempts
  - [ ] Track retry success/failure
- [ ] Test retry logic
  - [ ] Unit tests with mocked failures
  - [ ] Integration tests with real services
  - [ ] Verify exponential backoff

**Circuit Breakers:**
- [ ] Add `pybreaker` to dependencies
- [ ] Create circuit breaker module
  - [ ] `circuit_breaker.py` - Circuit breaker configuration
- [ ] Implement circuit breakers for external calls
  - [ ] Cube API calls
  - [ ] OPA policy evaluation
  - [ ] Optional: Neo4j, PostgreSQL (depends on deployment)
- [ ] Configure circuit breaker parameters
  - [ ] Failure threshold: 5 consecutive failures
  - [ ] Timeout: 30 seconds
  - [ ] Recovery: Half-open after 60 seconds
- [ ] Add circuit breaker metrics
  - [ ] Track state changes (closed, open, half-open)
  - [ ] Track failure counts
- [ ] Test circuit breakers
  - [ ] Verify state transitions
  - [ ] Verify recovery behavior

**Graceful Degradation:**
- [ ] Implement fallback strategies
  - [ ] Vector store down → Fallback to keyword search in registry
  - [ ] Tribal knowledge unavailable → Proceed without warnings
  - [ ] Policy engine down → Deny by default (fail-secure)
- [ ] Update orchestrator to handle degraded states
- [ ] Add degradation alerts
- [ ] Test degradation scenarios

**Error Hierarchy:**
- [ ] Define custom exception classes
  - [ ] `ECPError` (base)
  - [ ] `StoreError` (store failures)
  - [ ] `ResolutionError` (resolution failures)
  - [ ] `ValidationError` (validation failures)
  - [ ] `AuthorizationError` (policy denials)
- [ ] Map errors to HTTP status codes
- [ ] Create error response format (RFC 7807 Problem Details)
- [ ] Update API error handlers
- [ ] Test error responses

**Files to Create:**
- `src/ecp/resilience/__init__.py`
- `src/ecp/resilience/retry.py`
- `src/ecp/resilience/circuit_breaker.py`
- `src/ecp/resilience/exceptions.py`
- `tests/test_resilience.py`

**Files to Modify:**
- `src/ecp/adapters/*.py` - Add retry/circuit breaker
- `src/ecp/orchestrator/orchestrator.py` - Handle degradation
- `api/main.py` - Error handlers
- `pyproject.toml` - Add dependencies

---

### Week 2: Authentication & Authorization (Days 5-9)

#### API Key Authentication
- [ ] Design API key schema
  - [ ] Table: `api_keys` (id, key_hash, user_id, scopes, created_at, expires_at, revoked_at)
- [ ] Create API key module (`src/ecp/security/`)
  - [ ] `api_key.py` - Generation, validation, hashing
- [ ] Implement key generation CLI
  - [ ] `cli/generate_api_key.py`
  - [ ] Support scopes: read, write, admin
  - [ ] Set expiration
- [ ] Create database migration for api_keys table
- [ ] Implement API key authentication middleware
  - [ ] Bearer token validation
  - [ ] Scope checking
  - [ ] Key expiration checking
- [ ] Add authentication to API
  - [ ] Update endpoints to require auth
  - [ ] Add `/auth/validate` endpoint
- [ ] Test API key auth
  - [ ] Unit tests
  - [ ] Integration tests
  - [ ] Test scope enforcement

#### OAuth2/OIDC Integration
- [ ] Choose OAuth2 provider
  - [ ] Primary: Azure AD
  - [ ] Fallback: Generic OIDC
- [ ] Add OAuth2 dependencies
  - [ ] `python-jose[cryptography]` for JWT
  - [ ] `authlib` or `fastapi.security`
- [ ] Implement OAuth2 module
  - [ ] `oauth.py` - OAuth2 flow, token validation
- [ ] Configure OIDC settings
  - [ ] Issuer URL
  - [ ] Client ID/Secret
  - [ ] Redirect URIs
- [ ] Implement OAuth2 endpoints
  - [ ] `/auth/login` - Initiate OAuth flow
  - [ ] `/auth/callback` - Handle callback
  - [ ] `/auth/logout` - Logout
  - [ ] `/auth/refresh` - Token refresh
- [ ] Implement JWT validation middleware
  - [ ] Validate signature
  - [ ] Check expiration
  - [ ] Extract user claims
- [ ] Add user session management
  - [ ] Store sessions in Redis (future)
  - [ ] For now: stateless JWT
- [ ] Test OAuth2 flow
  - [ ] Unit tests (mocked provider)
  - [ ] Integration tests (test provider)

#### Enhanced Authorization (RLS)
- [ ] Design RLS policy schema
  - [ ] Row-level security rules
  - [ ] Column masking rules
  - [ ] Data classification tags
- [ ] Update OPA policies
  - [ ] Add RLS filters
  - [ ] Add column masking
  - [ ] Add classification enforcement
- [ ] Implement RLS in orchestrator
  - [ ] Inject filters into Cube queries
  - [ ] Mask columns in responses
  - [ ] Enforce data classification
- [ ] Create policy test suite
  - [ ] Test RLS filters
  - [ ] Test column masking
  - [ ] Test policy violations
- [ ] Document policies
  - [ ] Policy language guide
  - [ ] Examples for common patterns

#### Secrets Management
- [ ] Choose secrets backend
  - [ ] Azure Key Vault (if Azure deployment)
  - [ ] HashiCorp Vault (on-prem)
  - [ ] AWS Secrets Manager (if AWS deployment)
- [ ] Implement Vault client
  - [ ] `src/ecp/security/vault.py`
- [ ] Migrate secrets from .env
  - [ ] Database credentials
  - [ ] API keys
  - [ ] OAuth client secrets
- [ ] Update config to use Vault
  - [ ] Modify `src/ecp/config.py`
- [ ] Create Vault initialization script
  - [ ] `scripts/setup_vault.sh`
- [ ] Document secrets management
  - [ ] Setup guide
  - [ ] Rotation procedures

#### TLS/mTLS
- [ ] Generate TLS certificates
  - [ ] Dev: Self-signed
  - [ ] Prod: LetsEncrypt or enterprise CA
- [ ] Configure FastAPI for HTTPS
  - [ ] Update API startup
  - [ ] Configure cert paths
- [ ] Implement mTLS for service-to-service
  - [ ] Between API and stores (optional, depends on deployment)
- [ ] Create TLS setup script
  - [ ] `scripts/setup_tls.sh`
- [ ] Document TLS configuration

**Files to Create:**
- `src/ecp/security/__init__.py`
- `src/ecp/security/api_key.py`
- `src/ecp/security/oauth.py`
- `src/ecp/security/vault.py`
- `cli/generate_api_key.py`
- `scripts/setup_vault.sh`
- `scripts/setup_tls.sh`
- `policies/rls.rego`
- `tests/test_auth.py`
- `docs/security/auth_guide.md`
- `docs/security/secrets_management.md`

**Files to Modify:**
- `src/ecp/config.py` - Add auth settings
- `api/main.py` - Add auth middleware, endpoints
- `pyproject.toml` - Add dependencies
- `.env.example` - Add auth config

---

### Week 3: Audit Logging (Days 10-12)

#### Audit Trail Storage
- [ ] Choose audit log storage
  - [ ] Option A: ClickHouse (high-performance OLAP)
  - [ ] Option B: S3 + Parquet (cost-effective, immutable)
  - [ ] Option C: PostgreSQL append-only table (simplest)
- [ ] Design audit log schema
  - [ ] Fields: timestamp, request_id, user_id, action, resource, input, output, status, duration_ms, resolution_dag
  - [ ] Retention: 1 year minimum
- [ ] Implement audit logger
  - [ ] `src/ecp/audit/__init__.py`
  - [ ] `src/ecp/audit/logger.py`
- [ ] Integrate audit logging
  - [ ] Log all resolve requests
  - [ ] Log all execute requests
  - [ ] Log all auth decisions
  - [ ] Log all policy evaluations
- [ ] Create audit log API
  - [ ] `GET /api/v1/audit` - Query audit logs
  - [ ] Filters: user, action, time range, resource
  - [ ] Pagination
- [ ] Implement audit log export
  - [ ] Export to CSV/JSON
  - [ ] For compliance/archival
- [ ] Test audit logging
  - [ ] Verify all critical actions logged
  - [ ] Test query API
  - [ ] Test export

#### Compliance Features
- [ ] Implement log immutability
  - [ ] If ClickHouse: Use ReplicatedMergeTree with no deletes
  - [ ] If S3: Use S3 Object Lock
  - [ ] If PostgreSQL: Append-only with triggers
- [ ] Add log signing (optional, for regulatory)
  - [ ] Sign each log entry with HMAC
  - [ ] Store signatures
  - [ ] Verification API
- [ ] Create compliance reports
  - [ ] Who accessed what data
  - [ ] Data access frequency
  - [ ] Policy violation reports
- [ ] Document compliance features
  - [ ] Audit trail architecture
  - [ ] Retention policies
  - [ ] Query examples

**Files to Create:**
- `src/ecp/audit/__init__.py`
- `src/ecp/audit/logger.py`
- `src/ecp/audit/storage.py`
- `api/main.py` - Add audit endpoints
- `tests/test_audit.py`
- `docs/compliance/audit_trail.md`

**Files to Modify:**
- `src/ecp/orchestrator/orchestrator.py` - Add audit logging
- `api/main.py` - Add audit endpoints
- `pyproject.toml` - Add dependencies (if ClickHouse client needed)

---

### Week 4: Deployment Readiness (Days 13-16)

#### Production Docker Images
- [ ] Create production Dockerfile
  - [ ] Multi-stage build
  - [ ] Minimal base image (python:3.11-slim)
  - [ ] Non-root user
  - [ ] Health checks
  - [ ] Security scanning
- [ ] Create Dockerfile for API
  - [ ] `docker/Dockerfile.api`
- [ ] Create Dockerfile for MCP server (if separate)
  - [ ] `docker/Dockerfile.mcp`
- [ ] Create Dockerfile for workers (future)
  - [ ] `docker/Dockerfile.worker`
- [ ] Build and test images locally
- [ ] Push to container registry
  - [ ] Azure Container Registry
  - [ ] AWS ECR
  - [ ] Docker Hub
- [ ] Document Docker setup

#### Kubernetes Manifests
- [ ] Create K8s namespace
  - [ ] `k8s/namespace.yaml`
- [ ] Create ConfigMaps
  - [ ] `k8s/configmap.yaml` - Non-secret config
- [ ] Create Secrets
  - [ ] `k8s/secret.yaml` - Credentials (use sealed secrets or external secrets operator)
- [ ] Create Deployments
  - [ ] `k8s/deployment-api.yaml` - ECP API (3+ replicas)
  - [ ] `k8s/deployment-mcp.yaml` - MCP server (2+ replicas)
- [ ] Create Services
  - [ ] `k8s/service-api.yaml` - ClusterIP for API
  - [ ] `k8s/service-mcp.yaml` - ClusterIP for MCP
- [ ] Create Ingress
  - [ ] `k8s/ingress.yaml` - External access
  - [ ] TLS configuration
- [ ] Configure resource limits
  - [ ] CPU: 500m-2000m
  - [ ] Memory: 512Mi-2Gi
- [ ] Configure health checks
  - [ ] Liveness: `/api/v1/health`
  - [ ] Readiness: `/api/v1/health` (with store checks)
- [ ] Configure autoscaling (optional)
  - [ ] HorizontalPodAutoscaler based on CPU/memory
- [ ] Test K8s deployment locally
  - [ ] Use Minikube or Kind
- [ ] Document K8s setup

#### Helm Chart
- [ ] Create Helm chart structure
  - [ ] `helm/ecp/Chart.yaml`
  - [ ] `helm/ecp/values.yaml`
  - [ ] `helm/ecp/templates/`
- [ ] Parameterize manifests
  - [ ] Image tags
  - [ ] Replica counts
  - [ ] Resource limits
  - [ ] Environment-specific config
- [ ] Create values files
  - [ ] `values-dev.yaml`
  - [ ] `values-staging.yaml`
  - [ ] `values-prod.yaml`
- [ ] Add dependencies
  - [ ] PostgreSQL chart (optional, for dev)
  - [ ] Neo4j chart (optional, for dev)
  - [ ] Redis chart (future)
- [ ] Test Helm install
- [ ] Document Helm usage

#### Database Migrations
- [ ] Choose migration tool
  - [ ] Alembic (Python, works with SQLAlchemy)
  - [ ] Flyway (Java-based, language-agnostic)
- [ ] Create migration directory
  - [ ] `migrations/` or `alembic/versions/`
- [ ] Create initial migration
  - [ ] Create assets table
  - [ ] Create embeddings table
  - [ ] Create api_keys table
  - [ ] Create audit_logs table
- [ ] Implement migration runner
  - [ ] `scripts/migrate.py`
  - [ ] Run on startup (optional)
- [ ] Test migrations
  - [ ] Up migrations
  - [ ] Down migrations (rollback)
- [ ] Document migration workflow

#### CI/CD Pipeline
- [ ] Update GitHub Actions workflow
  - [ ] `.github/workflows/ci.yml`
- [ ] Add stages
  - [ ] Lint (ruff)
  - [ ] Type check (mypy)
  - [ ] Unit tests (pytest)
  - [ ] Integration tests
  - [ ] Build Docker images
  - [ ] Push to registry
  - [ ] Deploy to staging (optional)
- [ ] Add security scanning
  - [ ] Trivy for container scanning
  - [ ] Snyk for dependency scanning
- [ ] Add coverage reporting
  - [ ] Codecov or Coveralls
- [ ] Test CI/CD pipeline
- [ ] Document CI/CD

#### Runbook
- [ ] Create operations runbook
  - [ ] `docs/ops/runbook.md`
- [ ] Document common operations
  - [ ] Starting services
  - [ ] Stopping services
  - [ ] Checking logs
  - [ ] Checking metrics
  - [ ] Database migrations
  - [ ] Secrets rotation
  - [ ] Certificate renewal
- [ ] Document troubleshooting
  - [ ] API not responding
  - [ ] Store connection failures
  - [ ] High latency
  - [ ] Policy evaluation failures
- [ ] Document monitoring
  - [ ] Key metrics to watch
  - [ ] Alert thresholds
  - [ ] Escalation procedures
- [ ] Document disaster recovery
  - [ ] Backup procedures
  - [ ] Restore procedures
  - [ ] Failover procedures

**Files to Create:**
- `docker/Dockerfile.api`
- `docker/Dockerfile.mcp`
- `k8s/*.yaml` (namespace, configmap, secret, deployments, services, ingress)
- `helm/ecp/` (Chart.yaml, values.yaml, templates/)
- `migrations/` or `alembic/versions/`
- `scripts/migrate.py`
- `.github/workflows/ci.yml` (update)
- `docs/ops/runbook.md`
- `docs/ops/deployment_guide.md`

---

## Phase 2: Core Feature Enhancement (Weeks 5-8)

### Week 5: LLM Integration & Intent Parsing

- [ ] Choose LLM provider(s)
  - [ ] OpenAI GPT-4
  - [ ] Anthropic Claude
  - [ ] Azure OpenAI
- [ ] Add LLM dependencies
- [ ] Create LLM client abstraction
  - [ ] `src/ecp/llm/client.py`
  - [ ] Support multiple providers
- [ ] Design intent extraction prompts
  - [ ] Entity extraction
  - [ ] Metric extraction
  - [ ] Dimension extraction
  - [ ] Time range extraction
  - [ ] Intent classification
- [ ] Implement LLM-based intent parser
  - [ ] `src/ecp/orchestrator/intent_parser.py`
  - [ ] Replace keyword matching
- [ ] Add confidence scoring
- [ ] Implement caching
  - [ ] Cache LLM responses to reduce cost
- [ ] Test intent parsing
  - [ ] Unit tests with various queries
  - [ ] Cost analysis
- [ ] Document LLM integration

**Status:** NOT STARTED

---

### Week 6: Neuro-Symbolic Router & Disambiguation

- [ ] Implement confidence threshold logic
- [ ] Create router
  - [ ] `src/ecp/orchestrator/router.py`
  - [ ] SYMBOLIC path (high confidence + metric exists)
  - [ ] NEURAL path (low confidence, RAG)
  - [ ] AMBIGUOUS path (medium confidence)
- [ ] Implement disambiguation API
  - [ ] `POST /api/v1/clarify`
  - [ ] Generate clarification questions
  - [ ] Handle user feedback
  - [ ] Resume resolution
- [ ] Update orchestrator to use router
- [ ] Test routing logic
- [ ] Document routing

**Status:** NOT STARTED

---

### Week 7: Vector Embeddings & Semantic Search

- [ ] Choose embedding model
  - [ ] OpenAI text-embedding-3-small
  - [ ] Sentence-transformers (local)
- [ ] Create embedding generator
  - [ ] `src/ecp/llm/embeddings.py`
- [ ] Generate embeddings for all assets
  - [ ] Glossary terms
  - [ ] Metric descriptions
  - [ ] Tribal knowledge
- [ ] Update vector store adapter
  - [ ] Implement real similarity search
- [ ] Implement hybrid search
  - [ ] Semantic + keyword
  - [ ] Reranking
- [ ] Create embedding maintenance scripts
  - [ ] `scripts/generate_embeddings.py`
  - [ ] `scripts/update_embeddings.py`
- [ ] Test semantic search
- [ ] Document embeddings

**Status:** NOT STARTED

---

### Week 8: Advanced Query Features

- [ ] Multi-metric queries
- [ ] Comparison queries (actual vs budget, YoY)
- [ ] Temporal intelligence (last month, YTD, trailing 12 months)
- [ ] Aggregation and ranking (top 5, bottom 10)
- [ ] Cross-domain queries
- [ ] Test complex queries
- [ ] Document query patterns

**Status:** NOT STARTED

---

## Phase 3: Scale & Performance (Weeks 9-12)

### Week 9: Caching & Performance

- [ ] Redis integration
- [ ] Multi-level caching strategy
- [ ] Query optimization
- [ ] Connection pooling tuning
- [ ] Performance testing
- [ ] Benchmarking

**Status:** NOT STARTED

---

### Week 10: Horizontal Scaling

- [ ] Stateless API refactoring
- [ ] Load balancer configuration
- [ ] Autoscaling setup
- [ ] Multi-instance testing
- [ ] Performance validation

**Status:** NOT STARTED

---

### Week 11: Reliability & Resilience (Advanced)

- [ ] Advanced error handling patterns
- [ ] Timeout tuning
- [ ] Rate limiting
- [ ] Bulkhead pattern (if needed)
- [ ] Chaos testing

**Status:** NOT STARTED

---

### Week 12: Monitoring & Alerting

- [ ] Grafana dashboards
- [ ] Alert rules (Prometheus)
- [ ] PagerDuty/Opsgenie integration
- [ ] SLO definition and tracking
- [ ] On-call runbook

**Status:** NOT STARTED

---

## Phase 4: Advanced Features (Weeks 13-20)

### Factory Model / Ingestion Pipeline (Weeks 13-16)

- [ ] Crawl stage
- [ ] Profile stage
- [ ] Infer stage (LLM-based)
- [ ] Review stage (UI/workflow)
- [ ] Publish stage
- [ ] CLI tool
- [ ] Test end-to-end

**Status:** NOT STARTED

---

### Governance Features (Weeks 17-18)

- [ ] Schema drift monitoring
- [ ] Impact analysis engine
- [ ] Reinforcement loop (feedback)
- [ ] Certification tier enforcement
- [ ] Versioning and change management

**Status:** NOT STARTED

---

### Hyperscaler Integrations (Weeks 19-20)

- [ ] Azure AI Foundry integration
- [ ] Google Vertex AI integration
- [ ] AWS Bedrock integration
- [ ] Python SDK (LangChain/LangGraph)

**Status:** NOT STARTED

---

## Progress Summary

### Overall Progress
- Phase 1: 25% complete (Week 1 done, Week 1 error handling in progress)
- Phase 2: 0% complete
- Phase 3: 0% complete
- Phase 4: 0% complete

### Current Focus
- **Week 1 - Error Handling & Resilience**
- Next: Week 2 - Authentication & Authorization

### Key Metrics
- Lines of code: ~2500 (observability)
- Test coverage: ~40%
- Deployment readiness: 30%

---

## Notes & Decisions

### Technical Decisions Made
1. **Observability:** structlog + Prometheus (industry standard)
2. **Request Tracking:** X-Request-ID header (distributed tracing)
3. **Error Handling:** Fail-secure on policy errors (deny by default)
4. **Logging Format:** JSON for prod, pretty for dev

### Upcoming Decisions Needed
1. **Secrets Management:** Vault vs cloud provider (Azure Key Vault, AWS Secrets Manager)
2. **Audit Logging:** ClickHouse vs S3 vs PostgreSQL
3. **LLM Provider:** OpenAI vs Anthropic vs Azure OpenAI
4. **Embedding Model:** OpenAI vs local models

### Risks & Blockers
- None currently

---

## Resume Instructions

To resume work in a new session:

1. **Read this checklist** to understand current progress
2. **Check `IMPLEMENTATION_STATUS.md`** for detailed status
3. **Focus on current week's tasks** (see "Current Focus" above)
4. **Update this checklist** as tasks are completed
5. **Update `IMPLEMENTATION_STATUS.md`** with details

---

## Quick Commands

**Start services:**
```bash
docker compose up -d
./scripts/seed_all.sh
```

**Install dependencies:**
```bash
pip install -e .
```

**Run API:**
```bash
uvicorn api.main:app --reload --port 8000
```

**Run tests:**
```bash
pytest tests/ -v
```

**Check metrics:**
```bash
curl http://localhost:8000/metrics
```

---

**End of Checklist**
