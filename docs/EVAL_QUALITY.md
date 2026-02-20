# Trust & Quality 

**Approach Arch Multi-Tenant Agentic + MCP**

---

## 1. Trust Framework

Trust in agentic systems requires systematic controls across the entire lifecycle. The framework consists of 6 pillars that work together to ensure safe, reliable, and high-quality AI operations.

### Why This Matters for Platform Providers
When serving external customers (e.g., Cogentiq → Apple, Cox), trust isn't optional—it's the foundation. Each customer needs:
- **Data isolation**: Their data never leaks to competitors
- **Quality guarantees**: SLOs on accuracy, latency, cost
- **Compliance**: Audit trails, data residency, regulatory adherence
- **Transparency**: Visibility into how agents make decisions

---

## 2. The Six Areas in Trust: Metrics & Lifecycle Mapping

### 1: Security & Access Control
### 2: Quality & Correctness
### 3: Observability & Monitoring
### 4: Governance & Compliance
### 5: Reliability & Resilience
### 6: Evaluation & Testing



---
### 1: Security & Access Control

**Lifecycle Coverage**: Pre-execution → Runtime → Continuous

| Metric | Formula | Target | Collection Point | Lifecycle Phase |
|--------|---------|--------|------------------|-----------------|
| Input Attack Prevention | `blocked_injections / total_requests` | 100% | Pre-execution guardrails | Pre-exec |
| PII Leakage Rate | `leaked_pii_events / total_responses` | 0% | Post-execution NER scan | Post-exec |
| Unauthorized Access | `blocked_access / access_attempts` | <0.01% | Runtime policy engine | Runtime |
| MCP Server Auth Failures | `failed_auths / total_mcp_calls` | <0.1% | MCP middleware | Runtime |

**Key Controls**:
- Input validation (prompt injection, jailbreaks)
- PII detection & redaction (Presidio, custom NER)
- Row-level security on data access
- MCP server authentication & authorization

---

### 2: Quality & Correctness

**Lifecycle Coverage**: Pre-execution → Post-execution → Continuous

| Metric | Formula | Target | Collection Point | Lifecycle Phase |
|--------|---------|--------|------------------|-----------------|
| Answer Accuracy | `correct_answers / total_evaluated` | >90% | Post-exec LLM-as-judge | Post-exec |
| Hallucination Rate | `ungrounded_responses / total_responses` | <5% | Post-exec claim verification | Post-exec |
| Groundedness Score | `grounded_claims / total_claims` | >95% | Post-exec NLI model | Post-exec |
| Context Precision (RAG) | `relevant_retrieved / total_retrieved` | >0.9 | Runtime retrieval scoring | Runtime |
| Context Recall (RAG) | `relevant_retrieved / total_relevant` | >0.85 | Continuous eval vs ground truth | Continuous |

**Key Controls**:
- LLM-as-judge evaluation (correctness, relevance)
- Claim-level groundedness checking (NLI models)
- RAG pipeline metrics (RAGAS framework)
- Regression test suites (golden datasets)

---

### Pillar 3: Observability & Monitoring

**Lifecycle Coverage**: Pre-execution → Runtime → Post-execution → Continuous

| Metric | Formula | Target | Collection Point | Lifecycle Phase |
|--------|---------|--------|------------------|-----------------|
| Trace Coverage | `traced_requests / total_requests` | 100% | Pre-exec span initialization | Pre-exec |
| End-to-End Latency P95 | `95th percentile request duration` | <4000ms | Post-exec span aggregation | Post-exec |
| LLM Call Latency P95 | `95th percentile LLM duration` | <2000ms | Runtime span timing | Runtime |
| MCP Call Latency P95 | `95th percentile MCP duration` | <1000ms | Runtime MCP instrumentation | Runtime |
| Error Rate | `failed_requests / total_requests` | <1% | Continuous error span analysis | Continuous |
| Cost per Request | `Σ(token_cost + infra_cost) / requests` | <$0.05 | Post-exec cost attribution | Post-exec |

**Key Controls**:
- OpenTelemetry instrumentation (spans, traces, metrics)
- Distributed tracing across agent → MCP → data sources
- Real-time dashboards (Grafana)
- Cost attribution per customer/tenant

---

### Pillar 4: Governance & Compliance

**Lifecycle Coverage**: Pre-execution → Runtime → Continuous

| Metric | Formula | Target | Collection Point | Lifecycle Phase |
|--------|---------|--------|------------------|-----------------|
| Audit Log Completeness | `logged_events / total_events` | 100% | Runtime immutable log | Runtime |
| Retention Compliance | `logs_meeting_retention / total_logs` | 100% | Continuous lifecycle policies | Continuous |
| Policy Violations | `blocked_requests / total_requests` | Track trend | Pre-exec policy evaluation | Pre-exec |
| Data Access Audit Trail | `data_access_logged / data_access_events` | 100% | Runtime policy engine | Runtime |

**Key Controls**:
- Immutable audit logs (append-only PostgreSQL)
- Policy-as-code (OPA for declarative rules)
- Data lineage tracking (Unity Catalog)
- Compliance reporting (GDPR, SOC2, HIPAA)

---

### Pillar 5: Reliability & Resilience

**Lifecycle Coverage**: Runtime → Continuous

| Metric | Formula | Target | Collection Point | Lifecycle Phase |
|--------|---------|--------|------------------|-----------------|
| System Uptime | `available_time / total_time` | >99.9% | Continuous health checks | Continuous |
| MTBF (Mean Time Between Failures) | `total_uptime / number_of_failures` | >720hrs | Continuous incident tracking | Continuous |
| MTTR (Mean Time To Recovery) | `total_recovery_time / incidents` | <30min | Runtime incident timestamps | Runtime |
| Circuit Breaker Trips | `circuit_breaks / total_calls` | <0.5% | Runtime failure detection | Runtime |

**Key Controls**:
- Health check probes (liveness, readiness)
- Circuit breakers on MCP/LLM calls
- Automatic retry with exponential backoff
- Graceful degradation (fallback responses)

---

### Pillar 6: Evaluation & Testing

**Lifecycle Coverage**: Pre-execution → Post-execution → Continuous

| Metric | Formula | Target | Collection Point | Lifecycle Phase |
|--------|---------|--------|------------------|-----------------|
| Regression Test Pass Rate | `passed_tests / total_tests` | 100% | Pre-exec CI/CD pipeline | Pre-exec |
| Production Eval Score | `avg_quality_score across evaluators` | >0.85 | Post-exec async evaluation | Post-exec |
| Dataset Freshness | `days_since_last_update` | <30 days | Continuous dataset versioning | Continuous |
| Evaluator Coverage | `requests_evaluated / total_requests` | Sample rate varies | Post-exec sampling | Post-exec |

**Key Controls**:
- Golden dataset creation (curated examples)
- Automated regression tests (CI/CD integration)
- Continuous evaluation (sample production traffic)
- A/B testing framework (compare versions)

---

## 3. Where Does Eval & Testing Fit in Trust?

### Evaluation is Both a Pillar AND Cross-Cutting Concern

**As a Pillar (Pillar 6)**:
- Systematic quality gates before deployment
- Regression test suites prevent regressions
- Dataset-driven validation ensures coverage
- Experiment tracking enables safe iteration

**As Cross-Cutting Concern**:
- **Security**: Test for prompt injection vulnerabilities
- **Quality**: Measure hallucination, correctness, groundedness
- **Observability**: Validate that traces capture all needed data
- **Governance**: Verify policy enforcement works correctly
- **Reliability**: Load testing, chaos engineering

### Lifecycle Integration

```
Pre-Execution (Development/Staging):
├── Unit tests on agent logic
├── Integration tests on MCP connections
├── Regression tests on golden datasets
└── Policy tests (security, compliance)

Runtime (Production):
├── Sampling (1-10% of traffic)
├── Async evaluation (non-blocking)
└── Real-time guardrails (blocking)

Post-Execution:
├── Batch evaluation on completed traces
├── Human annotation queues
└── A/B test analysis

Continuous:
├── Daily regression runs
├── Dataset updates from production
└── Model performance drift detection
```

---

## 4. Evaluation & Quality Testing Framework

### Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    AGENT EXECUTION                          │
│  (LangGraph/CrewAI/Custom + MCP Calls)                     │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  ├─── Tracing (OpenTelemetry)
                  │    └── Spans: LLM, Tool, MCP, Retrieval
                  │
                  ├─── Real-time Guardrails (Blocking)
                  │    ├── Input validation
                  │    ├── PII redaction
                  │    └── Content safety
                  │
                  └─── Async Evaluation (Non-blocking)
                       └── Queue traces for evaluation
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────┐
│              EVALUATION PIPELINE                            │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. Dataset Creation                                        │
│     ├── Filter: production traces                          │
│     ├── Transform: {input, output, context, metadata}      │
│     └── Store: Phoenix Dataset / Delta table               │
│                                                             │
│  2. Evaluator Execution (Parallel)                         │
│     ├── LLM-as-judge (GPT-4 scoring)                       │
│     │   ├── Correctness (vs expected answer)               │
│     │   ├── Hallucination (groundedness check)             │
│     │   └── Relevance (query alignment)                    │
│     ├── Code-based evaluators                              │
│     │   ├── Exact match                                    │
│     │   ├── Regex validation                               │
│     │   └── JSON schema compliance                         │
│     ├── Model-based evaluators                             │
│     │   ├── NLI for entailment                             │
│     │   └── Semantic similarity (embeddings)               │
│     └── RAG-specific (RAGAS)                               │
│         ├── Context precision                              │
│         ├── Context recall                                 │
│         ├── Answer relevance                               │
│         └── Faithfulness                                   │
│                                                             │
│  3. Result Aggregation                                      │
│     ├── Per-example scores                                 │
│     ├── Statistical analysis (mean, P95, distribution)     │
│     └── Store in ClickHouse (time-series)                  │
│                                                             │
│  4. Feedback Loop                                           │
│     ├── Failed examples → debugging dataset                │
│     ├── Low scores → prompt engineering queue              │
│     ├── High-quality → few-shot examples                   │
│     └── Eval results stored as spans (queryable)           │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Key Framework Components

**1. Evaluator Types**

| Type | Use Case | Cost | Latency | Accuracy |
|------|----------|------|---------|----------|
| LLM-as-Judge | Complex reasoning, subjective quality | $0.002-0.01/eval | 1-3s | High (0.85-0.95 correlation with human) |
| Code-based | Deterministic checks (format, schema) | $0.000001/eval | <10ms | Perfect (if rule is correct) |
| Model-based | Entailment, similarity, classification | $0.0001/eval | 100-500ms | Medium-High (0.75-0.90) |
| Human-in-loop | Ground truth, edge cases, calibration | $1-5/eval | Hours-days | Gold standard |

**2. Dataset Strategy**

```python
# Production sampling
production_dataset = {
    "source": "Sample 1% of production traffic",
    "frequency": "Daily",
    "size": "~1000 examples/day",
    "use": "Continuous monitoring, drift detection"
}

# Golden dataset
golden_dataset = {
    "source": "Manually curated + high-quality production",
    "frequency": "Weekly updates",
    "size": "100-500 examples",
    "use": "Regression tests, model comparison"
}

# Adversarial dataset
adversarial_dataset = {
    "source": "Red team, failure cases, edge cases",
    "frequency": "Monthly updates",
    "size": "50-100 examples",
    "use": "Security testing, robustness validation"
}
```

**3. Evaluation Cadence**

| When | What | Why |
|------|------|-----|
| **Pre-commit** | Unit tests on agent logic | Fast feedback loop |
| **Pre-deploy** | Regression tests on golden dataset | Prevent regressions |
| **Post-deploy (sampling)** | 1-10% of production traffic | Monitor quality drift |
| **Post-deploy (batch)** | Daily batch on all production traces | Comprehensive analysis |
| **On-demand** | Manual evaluation for debugging | Root cause analysis |

**4. Metrics Hierarchy**

```
System-Level SLO (Customer-facing)
├── P95 Latency < 4s
├── Error Rate < 1%
└── Quality Score > 0.85
     │
     ├── Correctness > 0.90
     ├── Hallucination < 0.05
     ├── Groundedness > 0.95
     └── Relevance > 0.85
          │
          ├── Context Precision > 0.90 (RAG)
          ├── Context Recall > 0.85 (RAG)
          └── Answer Faithfulness > 0.90
```

---

## 5. Observability & Evaluation Tools Comparison

### Decision Matrix for Platform Providers

| Dimension | Phoenix (Arize) | LangSmith | MLflow | AgentBricks (DBX) | TruLens | LangFuse | Weights & Biases |
|-----------|----------------|-----------|--------|-------------------|---------|----------|------------------|
| **Primary Use Case** | Production LLM observability | LLM app development | ML experiment tracking | Databricks-native eval | LLM evaluation library | OSS LLM monitoring | ML experiment tracking |
| **Tracing Standard** | OpenTelemetry | Proprietary (LangChain) | Proprietary (MLflow) | MLflow-based | No (library only) | OpenTelemetry-compatible | Proprietary |
| **Multi-Tenant Isolation** | ✅ Native (Projects) | ⚠️ Soft (Organizations) | ❌ Manual (tags) | ⚠️ Workspaces | ❌ Not designed for | ⚠️ Projects | ❌ Not designed for |
| **Self-Hosting** | ✅ OSS, Docker/K8s | ⚠️ Enterprise tier only | ✅ OSS, easy setup | ⚠️ Databricks required | ✅ Library (BYO infra) | ✅ OSS, Docker | ⚠️ Enterprise tier |
| **White-Labeling** | ✅ Full (OSS UI) | ❌ Limited (API only) | ✅ Full (OSS UI) | ❌ DBX branding | ✅ Build your own | ✅ Full (OSS UI) | ❌ Vendor UI |
| **Framework Support** | ✅ All (OTel-based) | ⚠️ Best: LangChain | ✅ All via MLflow | ✅ All via MLflow | ⚠️ LangChain-first | ✅ All (OTel) | ✅ All |
| **MCP Integration** | ✅ Tool spans (OpenInference) | ⚠️ Generic tools | ⚠️ Generic tools | ✅ Unity Catalog tools | ❌ Manual | ⚠️ Generic tools | ❌ Manual |
| **Real-Time Observability** | ✅ Streaming traces | ✅ Streaming traces | ❌ Batch-focused | ⚠️ Batch-focused | ❌ Evaluation only | ✅ Real-time | ✅ Real-time |
| **Evaluation Framework** | ✅ Built-in + integrations | ✅ Comprehensive | ⚠️ mlflow.evaluate | ✅ Agent Evaluation + Review App | ✅ Best-in-class (library) | ⚠️ Basic | ✅ Comprehensive |
| **Annotation Queues** | ❌ Build your own | ✅ Best-in-class | ❌ Not available | ✅ Review App | ❌ Not available | ⚠️ Basic | ⚠️ Basic |
| **Query Performance (1M+ traces)** | ✅ Excellent (ClickHouse) | ✅ Good (vendor DB) | ❌ Slow (RDBMS) | ⚠️ Databricks SQL | N/A | ⚠️ PostgreSQL | ✅ Good |
| **Cost Model (100 customers)** | ✅ Infra only (~$4K/mo) | ❌ Per-seat + usage ($15K+/mo) | ✅ Infra only (~$1K/mo) | ❌ DBU consumption ($5K+/mo) | ✅ Free (library) | ✅ Infra only (~$2K/mo) | ❌ Per-seat ($10K+/mo) |
| **Developer Experience** | ⚠️ Technical (3/5) | ✅ Excellent (5/5) | ⚠️ Familiar if using MLflow (4/5) | ⚠️ Databricks UX (3/5) | ⚠️ Code-heavy (3/5) | ✅ Good (4/5) | ✅ Excellent (5/5) |
| **Time to First Trace** | ⚠️ 1-2 hours (infra setup) | ✅ 5 minutes (SaaS) | ✅ 10 minutes | ⚠️ 1+ hours (DBX setup) | ⚠️ 30 min (code integration) | ⚠️ 30 min (Docker) | ✅ 5 minutes (SaaS) |
| **Community & Support** | ⚠️ Growing (Arize-backed) | ✅ Large (LangChain) | ✅ Mature (Databricks) | ✅ Databricks ecosystem | ⚠️ Active (OSS) | ⚠️ Growing | ✅ Large (ML community) |
| **Data Residency Control** | ✅ Full (self-host anywhere) | ❌ Limited (SaaS/Enterprise) | ✅ Full (self-host) | ⚠️ Databricks regions | ✅ Full (library) | ✅ Full (self-host) | ❌ Limited |