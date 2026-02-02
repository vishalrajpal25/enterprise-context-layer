# Cogentiq Studio
## Complete Platform Product Requirements Document

**Version:** 3.0.0-FINAL  
**Status:** Approved for Implementation  
**Classification:** Internal - Confidential  
**Date:** January 26, 2026

---

# TABLE OF CONTENTS

1. [Executive Summary](#1-executive-summary)
2. [Platform Architecture Overview](#2-platform-architecture-overview)
3. [Layer 1: Infrastructure & Runtime Abstraction](#3-layer-1-infrastructure--runtime-abstraction)
4. [Layer 2: Domain Intelligence Layer](#4-layer-2-domain-intelligence-layer)
5. [Layer 3: Agentic Layer](#5-layer-3-agentic-layer)
6. [Layer 4: Knowledge Asset Registry](#6-layer-4-knowledge-asset-registry)
7. [Layer 5: Governance & Reliability Framework](#7-layer-5-governance--reliability-framework)
8. [Layer 6: Integration Fabric](#8-layer-6-integration-fabric)
9. [Ontology Workbench](#9-ontology-workbench)
10. [Neuro-Symbolic Router](#10-neuro-symbolic-router)
11. [Semantic Catalog & Constraint Engine](#11-semantic-catalog--constraint-engine)
12. [Legacy Logic Ingestion Module](#12-legacy-logic-ingestion-module)
13. [Data Models & Schemas](#13-data-models--schemas)
14. [API Specifications](#14-api-specifications)
15. [Security & Governance](#15-security--governance)
16. [Domain Templates](#16-domain-templates)
17. [Deployment Architecture](#17-deployment-architecture)
18. [Non-Functional Requirements](#18-non-functional-requirements)
19. [Testing Strategy](#19-testing-strategy)
20. [Rollout Plan](#20-rollout-plan)
21. [Appendices](#21-appendices)

---

# 1. EXECUTIVE SUMMARY

## 1.1 What Cogentiq Studio Is

**Cogentiq Studio is a Domain Intelligence Platform for Enterprise Agentic AI.**

It is NOT:
- Another agent orchestrator (like LangChain, CrewAI)
- A data platform (use Databricks, Snowflake)
- A model training system (use Foundry, SageMaker)
- A BI tool (use Tableau, Power BI)

It IS:
- A domain intelligence authoring and deployment system
- A semantic model tooling platform
- A multi-platform agent deployment system
- A knowledge asset registry with compounding value

## 1.2 The Strategic Proposition

| The Commodity | The Cogentiq Moat |
|---------------|-------------------|
| Agents that call tools | Agents that understand business physics |
| Generic LLM reasoning | Deterministic calculation from formal definitions |
| Prompt-based context | Versioned, governed semantic models |
| Platform-locked agents | Transpilable agents across Foundry/Bedrock/Native |
| One-off implementations | Reusable domain knowledge packs |

## 1.3 Competitive Positioning

| Competitor | What They Have | What They Lack (Your Moat) |
|------------|----------------|---------------------------|
| **Azure AI Foundry / Bedrock** | Infrastructure, orchestration, model access | Domain intelligence layer, semantic tooling, reusable knowledge assets |
| **Generic Frameworks (CrewAI, LangGraph)** | Developer flexibility, open-source | Enterprise governance, domain pre-packaging, multi-platform deployment |
| **Palantir** | Ontology, platform depth, capital | AI-native (no legacy), faster time-to-value, accessible price point |
| **Consulting Firms** | Domain expertise, client relationships | Productized reuse, software economics, compounding knowledge |

## 1.4 Core Value Propositions

1. **Time-to-Value**: 12 weeks → 2-4 weeks using automated ontology harvesting + domain packs
2. **Consistency**: Deterministic answers from formal definitions, not LLM guessing
3. **Auditability**: Full lineage from output to definition to data source
4. **Portability**: Write once, deploy to Foundry, Bedrock, or native runtime
5. **Compounding**: Each engagement enriches domain packs for future clients

## 1.5 Tagline

**Cogentiq Studio: Turn Domain Expertise into Autonomous Decision Intelligence**

---

# 2. PLATFORM ARCHITECTURE OVERVIEW

## 2.1 The Dual-Loop Architecture

Cogentiq operates on two distinct but connected loops:

**HARVESTING LOOP (Build Time)**: Ingesting legacy logic, documents, and SME knowledge to build the Domain Model.

**REASONING LOOP (Runtime)**: Using that model to answer user queries deterministically and safely.

## 2.2 Complete Platform Stack

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                              COGENTIQ STUDIO PLATFORM                                   │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  ╔═════════════════════════════════════════════════════════════════════════════════╗   │
│  ║                        LAYER 6: USER INTERFACES                                 ║   │
│  ║  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐            ║   │
│  ║  │  Ontology   │  │   Agent     │  │  Knowledge  │  │ Governance  │            ║   │
│  ║  │  Workbench  │  │   Studio    │  │  Registry   │  │  Console    │            ║   │
│  ║  │     UI      │  │     UI      │  │     UI      │  │     UI      │            ║   │
│  ║  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘            ║   │
│  ╚═════════════════════════════════════════════════════════════════════════════════╝   │
│                                         │                                               │
│  ╔═════════════════════════════════════════════════════════════════════════════════╗   │
│  ║                        LAYER 5: GOVERNANCE & RELIABILITY                        ║   │
│  ║  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐            ║   │
│  ║  │  Decision   │  │    Risk     │  │    Cost     │  │ Compliance  │            ║   │
│  ║  │   Audit     │  │  Controls   │  │  Guardrails │  │   Tagging   │            ║   │
│  ║  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘            ║   │
│  ╚═════════════════════════════════════════════════════════════════════════════════╝   │
│                                         │                                               │
│  ╔═════════════════════════════════════════════════════════════════════════════════╗   │
│  ║                        LAYER 4: KNOWLEDGE ASSET REGISTRY                        ║   │
│  ║  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐            ║   │
│  ║  │   Domain    │  │   Prompt    │  │    Tool     │  │  Workflow   │            ║   │
│  ║  │   Packs     │  │  Libraries  │  │ Definitions │  │  Templates  │            ║   │
│  ║  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘            ║   │
│  ╚═════════════════════════════════════════════════════════════════════════════════╝   │
│                                         │                                               │
│  ╔═════════════════════════════════════════════════════════════════════════════════╗   │
│  ║                        LAYER 3: AGENTIC LAYER                                   ║   │
│  ║  ┌───────────────────────────────────────────────────────────────────────────┐  ║   │
│  ║  │                    AGENT DEVELOPMENT KIT (ADK)                            │  ║   │
│  ║  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐      │  ║   │
│  ║  │  │   Agent     │  │  Transpiler │  │   Agent     │  │   Agent     │      │  ║   │
│  ║  │  │    Spec     │  │   Engine    │  │  Patterns   │  │   Testing   │      │  ║   │
│  ║  │  │  (YAML)     │  │             │  │  Library    │  │   Harness   │      │  ║   │
│  ║  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘      │  ║   │
│  ║  └───────────────────────────────────────────────────────────────────────────┘  ║   │
│  ║  ┌───────────────────────────────────────────────────────────────────────────┐  ║   │
│  ║  │                    NEURO-SYMBOLIC ROUTER                                  │  ║   │
│  ║  │        Symbolic Path ◄──────► Hybrid Path ◄──────► Neural Path           │  ║   │
│  ║  └───────────────────────────────────────────────────────────────────────────┘  ║   │
│  ╚═════════════════════════════════════════════════════════════════════════════════╝   │
│                                         │                                               │
│  ╔═════════════════════════════════════════════════════════════════════════════════╗   │
│  ║                        LAYER 2: DOMAIN INTELLIGENCE LAYER                       ║   │
│  ║  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐            ║   │
│  ║  │  Ontology   │  │  Semantic   │  │ Constraint  │  │  Context    │            ║   │
│  ║  │  Registry   │  │  Catalog    │  │   Engine    │  │   Graph     │            ║   │
│  ║  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘            ║   │
│  ║  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐                             ║   │
│  ║  │   Entity    │  │  Lineage    │  │  Ingestion  │                             ║   │
│  ║  │ Resolution  │  │  Service    │  │   Module    │                             ║   │
│  ║  └─────────────┘  └─────────────┘  └─────────────┘                             ║   │
│  ╚═════════════════════════════════════════════════════════════════════════════════╝   │
│                                         │                                               │
│  ╔═════════════════════════════════════════════════════════════════════════════════╗   │
│  ║                        LAYER 1: RUNTIME ABSTRACTION LAYER                       ║   │
│  ║  ┌───────────────────────────────────────────────────────────────────────────┐  ║   │
│  ║  │                         EXECUTION TARGETS                                 │  ║   │
│  ║  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐      │  ║   │
│  ║  │  │   Azure     │  │    AWS      │  │   Google    │  │   Native    │      │  ║   │
│  ║  │  │    AI       │  │  Bedrock    │  │   Agent     │  │  Runtime    │      │  ║   │
│  ║  │  │  Foundry    │  │   Agents    │  │   Space     │  │ (K8s/LangG) │      │  ║   │
│  ║  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘      │  ║   │
│  ║  └───────────────────────────────────────────────────────────────────────────┘  ║   │
│  ║  ┌───────────────────────────────────────────────────────────────────────────┐  ║   │
│  ║  │                         UNIFIED OBSERVABILITY                             │  ║   │
│  ║  │              Traces │ Metrics │ Logs │ Cost Tracking                      │  ║   │
│  ║  └───────────────────────────────────────────────────────────────────────────┘  ║   │
│  ╚═════════════════════════════════════════════════════════════════════════════════╝   │
│                                         │                                               │
│  ╔═════════════════════════════════════════════════════════════════════════════════╗   │
│  ║                        LAYER 0: INTEGRATION FABRIC                              ║   │
│  ║  ┌─────────────────────────────────────────────────────────────────────────────┐║   │
│  ║  │  Enterprise Systems  │  Data Platforms  │  Semantic Layers  │  External AI  │║   │
│  ║  │  (SAP, SFDC, Workday)│(Snowflake,DBricks)│ (dbt, Cube)      │  (3rd Party)  │║   │
│  ║  └─────────────────────────────────────────────────────────────────────────────┘║   │
│  ╚═════════════════════════════════════════════════════════════════════════════════╝   │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

## 2.3 Component Summary

| Layer | Component | Role |
|-------|-----------|------|
| **L0: Integration** | Connectors, Adapters | Connect to enterprise data and systems |
| **L1: Runtime** | Transpiler, Executors | Deploy agents to any platform |
| **L2: Domain Intel** | Ontology, Semantic, Constraints | Encode and execute business logic |
| **L3: Agentic** | ADK, Router, Patterns | Build and route agent workflows |
| **L4: Registry** | Domain Packs, Prompts, Tools | Store and reuse knowledge assets |
| **L5: Governance** | Audit, Risk, Cost, Compliance | Control and monitor everything |
| **L6: UI** | Workbench, Studio, Console | Human interfaces for all functions |

---

# 3. LAYER 1: INFRASTRUCTURE & RUNTIME ABSTRACTION

## 3.1 Design Philosophy

**Write Once, Deploy Anywhere**: Agent specifications are written in a platform-neutral format and transpiled to target runtimes.

**Azure AI Foundry First**: Primary development target, but not locked in.

**Graceful Degradation**: If a target platform lacks a capability, the transpiler provides fallback implementations.

## 3.2 Execution Targets

### 3.2.1 Target Platform Matrix

| Target | Primary Use Case | Transpiler Output | Limitations |
|--------|------------------|-------------------|-------------|
| **Azure AI Foundry** | Enterprise Microsoft shops | Foundry Agent YAML + Tools | Foundry-specific constructs |
| **AWS Bedrock Agents** | AWS-native enterprises | Bedrock Agent Schema + Lambdas | Limited orchestration patterns |
| **Google Agent Space** | GCP customers | Agent Builder config | Early stage, fewer patterns |
| **Native Runtime (K8s)** | Full control, air-gapped | LangGraph + FastAPI on K8s | Self-managed infrastructure |

### 3.2.2 Target: Azure AI Foundry (Primary)

**Why Foundry First:**
- Enterprise budgets flowing to Azure
- Tight integration with enterprise identity (Entra ID)
- Responsible AI features built-in
- Foundry Ontology alignment opportunity

**Transpiler Output:**
```yaml
# Cogentiq Agent Spec (Source)
agent:
  name: claims_triage_agent
  version: "1.0.0"
  description: "Triages incoming insurance claims"
  
  ontology_context:
    domain_pack: "insurance/claims"
    entities: [Claim, Policy, Member, Provider]
    
  tools:
    - name: lookup_claim
      type: semantic_query
      metric: claim_details
    - name: check_policy_status
      type: semantic_query
      metric: policy_status
    - name: flag_for_review
      type: action
      target: claims_workflow_system
      
  patterns:
    - type: reflection_loop
      max_iterations: 3
    - type: validation_gate
      constraint: claim_amount_within_bounds
    - type: hitl_breakpoint
      condition: "claim.amount > 50000"

# ═══════════════════════════════════════════════════════
# TRANSPILED TO: Azure AI Foundry Agent
# ═══════════════════════════════════════════════════════

type: foundry_agent
name: claims_triage_agent
model:
  deployment: gpt-4o
  parameters:
    temperature: 0.1
    max_tokens: 4096
    
instructions: |
  You are a claims triage agent for an insurance company.
  
  ## Domain Context (Injected from Ontology)
  {ontology_context_injection}
  
  ## Available Entities
  - Claim: A request for payment...
  - Policy: An insurance contract...
  
  ## Business Rules
  - Claims over $50,000 require human review
  - Non-preferred providers require manual adjudication
  
tools:
  - type: function
    function:
      name: lookup_claim
      description: "Look up claim details by claim ID"
      parameters:
        type: object
        properties:
          claim_id:
            type: string
        required: [claim_id]
        
  - type: function
    function:
      name: check_policy_status
      description: "Check if a policy is active"
      parameters:
        type: object
        properties:
          policy_id:
            type: string
            
  - type: function  
    function:
      name: flag_for_review
      description: "Flag a claim for human review"
      parameters:
        type: object
        properties:
          claim_id:
            type: string
          reason:
            type: string

# Tool implementations deployed as Azure Functions
tool_implementations:
  - name: lookup_claim
    type: azure_function
    function_app: cogentiq-claims-tools
    function_name: LookupClaim
    binding: semantic_catalog  # Executes via Cogentiq Semantic Layer
    
  - name: check_policy_status
    type: azure_function
    function_app: cogentiq-claims-tools
    function_name: CheckPolicyStatus
    binding: semantic_catalog
```

### 3.2.3 Target: AWS Bedrock Agents

**Transpiler Output:**
```yaml
# TRANSPILED TO: AWS Bedrock Agent
# ═══════════════════════════════════════════════════════

bedrock_agent:
  agent_name: claims_triage_agent
  foundation_model: anthropic.claude-3-sonnet
  instruction: |
    You are a claims triage agent...
    {ontology_context_injection}
    
  action_groups:
    - action_group_name: claims_actions
      action_group_executor:
        lambda: arn:aws:lambda:us-east-1:123456789:function:cogentiq-claims-handler
      api_schema:
        type: OPENAPI
        payload: |
          openapi: "3.0.0"
          paths:
            /lookup_claim:
              post:
                operationId: lookup_claim
                ...
                
  knowledge_bases:
    - knowledge_base_id: kb-claims-ontology
      description: "Claims domain knowledge"
```

### 3.2.4 Target: Native Runtime (Kubernetes + LangGraph)

**Transpiler Output:**
```python
# TRANSPILED TO: LangGraph Agent on Kubernetes
# ═══════════════════════════════════════════════════════

from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from cogentiq.runtime import CogentiqSemanticTools, OntologyContext

# Load ontology context
ontology = OntologyContext.load("insurance/claims")

# Define tools bound to Cogentiq Semantic Layer
tools = CogentiqSemanticTools(
    ontology=ontology,
    tools=[
        {"name": "lookup_claim", "metric": "claim_details"},
        {"name": "check_policy_status", "metric": "policy_status"},
        {"name": "flag_for_review", "type": "action"}
    ]
)

# Define state
class AgentState(TypedDict):
    messages: list
    claim_context: dict
    iteration_count: int

# Define nodes
def triage_node(state: AgentState) -> AgentState:
    """Main triage logic with reflection loop."""
    # Cogentiq Router determines symbolic vs neural path
    from cogentiq.router import NeuroSymbolicRouter
    router = NeuroSymbolicRouter(ontology=ontology)
    
    response = router.process(
        query=state["messages"][-1],
        context=state["claim_context"]
    )
    
    return {"messages": state["messages"] + [response]}

def validation_gate(state: AgentState) -> str:
    """Constraint-based routing."""
    from cogentiq.constraints import ConstraintEngine
    engine = ConstraintEngine(ontology=ontology)
    
    result = engine.evaluate(
        rule="claim_amount_within_bounds",
        context=state["claim_context"]
    )
    
    if result.violated:
        return "escalate"
    return "continue"

def hitl_check(state: AgentState) -> str:
    """Human-in-the-loop breakpoint."""
    if state["claim_context"].get("amount", 0) > 50000:
        return "human_review"
    return "auto_process"

# Build graph
workflow = StateGraph(AgentState)
workflow.add_node("triage", triage_node)
workflow.add_node("tools", ToolNode(tools.as_langchain_tools()))
workflow.add_node("escalate", escalate_node)
workflow.add_node("human_review", human_review_node)

workflow.add_conditional_edges("triage", validation_gate)
workflow.add_conditional_edges("triage", hitl_check)

# Compile
agent = workflow.compile()

# Kubernetes deployment spec generated separately
```

## 3.3 Transpiler Architecture

### 3.3.1 Transpiler Pipeline

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         TRANSPILER PIPELINE                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────┐                                                            │
│  │  Cogentiq   │                                                            │
│  │ Agent Spec  │                                                            │
│  │   (YAML)    │                                                            │
│  └──────┬──────┘                                                            │
│         │                                                                   │
│         ▼                                                                   │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                         PARSER & VALIDATOR                          │   │
│  │  • Schema validation                                                │   │
│  │  • Ontology reference resolution                                    │   │
│  │  • Tool contract validation                                         │   │
│  │  • Pattern compatibility check                                      │   │
│  └──────────────────────────────┬──────────────────────────────────────┘   │
│                                 │                                           │
│                                 ▼                                           │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                    INTERMEDIATE REPRESENTATION (IR)                 │   │
│  │  • Normalized agent graph                                           │   │
│  │  • Resolved ontology context                                        │   │
│  │  • Expanded tool definitions                                        │   │
│  │  • Constraint rules compiled                                        │   │
│  └──────────────────────────────┬──────────────────────────────────────┘   │
│                                 │                                           │
│         ┌───────────────────────┼───────────────────────┐                  │
│         ▼                       ▼                       ▼                  │
│  ┌─────────────┐         ┌─────────────┐         ┌─────────────┐          │
│  │  Foundry    │         │  Bedrock    │         │  Native     │          │
│  │  Emitter    │         │  Emitter    │         │  Emitter    │          │
│  └──────┬──────┘         └──────┬──────┘         └──────┬──────┘          │
│         │                       │                       │                  │
│         ▼                       ▼                       ▼                  │
│  ┌─────────────┐         ┌─────────────┐         ┌─────────────┐          │
│  │  Foundry    │         │  Bedrock    │         │  LangGraph  │          │
│  │  Agent +    │         │  Agent +    │         │  + K8s      │          │
│  │  Functions  │         │  Lambdas    │         │  Manifests  │          │
│  └─────────────┘         └─────────────┘         └─────────────┘          │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                    DEPLOYMENT ORCHESTRATOR                          │   │
│  │  • Provisions target resources                                      │   │
│  │  • Deploys tool implementations                                     │   │
│  │  • Configures observability                                         │   │
│  │  • Registers with Cogentiq control plane                           │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 3.3.2 Feature Mapping Across Targets

| Cogentiq Feature | Azure Foundry | AWS Bedrock | Native (K8s) |
|------------------|---------------|-------------|--------------|
| **Reflection Loop** | Native support | Custom Lambda orchestration | LangGraph cycle |
| **Validation Gate** | Pre/post hooks | Lambda middleware | Graph conditional edge |
| **HITL Breakpoint** | Foundry approval flow | Step Functions wait | Custom webhook + pause |
| **Semantic Query Tool** | Azure Function → Cogentiq | Lambda → Cogentiq | Direct Cogentiq SDK |
| **Ontology Context** | System prompt injection | Instruction injection | State injection |
| **Cost Guardrails** | Token tracking | Bedrock metrics | Custom middleware |
| **Lineage Capture** | Callback hooks | CloudWatch events | OpenTelemetry |

### 3.3.3 Fallback Implementations

When target platform lacks native support:

```yaml
# Cogentiq pattern that Bedrock doesn't natively support
patterns:
  - type: reflection_loop
    max_iterations: 3
    
# Transpiler generates Lambda-based implementation
bedrock_fallback:
  reflection_loop:
    implementation: step_functions
    state_machine:
      Comment: "Reflection loop fallback"
      StartAt: "InitialCall"
      States:
        InitialCall:
          Type: Task
          Resource: arn:aws:lambda:...:agent_invoke
          Next: CheckReflection
        CheckReflection:
          Type: Choice
          Choices:
            - Variable: "$.iteration"
              NumericLessThan: 3
              Next: ReflectionCall
          Default: Complete
        ReflectionCall:
          Type: Task
          Resource: arn:aws:lambda:...:agent_reflect
          Next: CheckReflection
        Complete:
          Type: Succeed
```

## 3.4 Unified Observability

### 3.4.1 Cross-Platform Telemetry

Regardless of execution target, all agents report to unified observability:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      UNIFIED OBSERVABILITY LAYER                            │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐       │
│  │   Foundry   │  │   Bedrock   │  │   Native    │  │   Other     │       │
│  │   Agent     │  │   Agent     │  │   Agent     │  │   Agent     │       │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘       │
│         │                │                │                │               │
│         └────────────────┴────────────────┴────────────────┘               │
│                                   │                                         │
│                                   ▼                                         │
│                    ┌─────────────────────────────┐                          │
│                    │   OpenTelemetry Collector   │                          │
│                    └──────────────┬──────────────┘                          │
│                                   │                                         │
│         ┌─────────────────────────┼─────────────────────────┐              │
│         ▼                         ▼                         ▼              │
│  ┌─────────────┐           ┌─────────────┐           ┌─────────────┐      │
│  │   Traces    │           │   Metrics   │           │    Logs     │      │
│  │  (Jaeger)   │           │(Prometheus) │           │   (Loki)    │      │
│  └─────────────┘           └─────────────┘           └─────────────┘      │
│         │                         │                         │              │
│         └─────────────────────────┼─────────────────────────┘              │
│                                   ▼                                         │
│                    ┌─────────────────────────────┐                          │
│                    │   Cogentiq Observability    │                          │
│                    │        Dashboard            │                          │
│                    │                             │                          │
│                    │  • Agent performance        │                          │
│                    │  • Routing decisions        │                          │
│                    │  • Token usage & cost       │                          │
│                    │  • Constraint violations    │                          │
│                    │  • Lineage explorer         │                          │
│                    └─────────────────────────────┘                          │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 3.4.2 Standard Metrics

| Metric Category | Metrics |
|-----------------|---------|
| **Performance** | Latency (p50, p95, p99), throughput, error rate |
| **Routing** | Symbolic vs hybrid vs neural path distribution |
| **Accuracy** | Entity resolution confidence, constraint violations |
| **Cost** | Token usage by model, cost per query, budget utilization |
| **Business** | Queries by domain, agent utilization, SLA compliance |

---

# 4. LAYER 2: DOMAIN INTELLIGENCE LAYER

## 4.1 Component Overview

The Domain Intelligence Layer is the core differentiator—it encodes enterprise business logic into machine-executable form.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      DOMAIN INTELLIGENCE LAYER                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐            │
│  │    ONTOLOGY     │  │    SEMANTIC     │  │   CONSTRAINT    │            │
│  │    REGISTRY     │  │    CATALOG      │  │     ENGINE      │            │
│  │   ───────────   │  │   ───────────   │  │   ───────────   │            │
│  │   The Dictionary│  │  The Calculator │  │  The Guardrails │            │
│  │                 │  │                 │  │                 │            │
│  │  • Entities     │  │  • Metrics      │  │  • Business     │            │
│  │  • Attributes   │  │  • Dimensions   │  │    Rules        │            │
│  │  • Relationships│  │  • Calculations │  │  • Access       │            │
│  │  • Taxonomies   │  │  • Data Binding │  │    Control      │            │
│  │  • Glossary     │  │  • Contracts    │  │  • Validation   │            │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘            │
│                                                                             │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐            │
│  │    CONTEXT      │  │     ENTITY      │  │    LINEAGE      │            │
│  │     GRAPH       │  │   RESOLUTION    │  │    SERVICE      │            │
│  │   ───────────   │  │   ───────────   │  │   ───────────   │            │
│  │   The Memory    │  │  The Translator │  │  The Black Box  │            │
│  │                 │  │                 │  │                 │            │
│  │  • Session      │  │  • Exact Match  │  │  • Definition   │            │
│  │  • Scope        │  │  • Fuzzy Match  │  │    Lineage      │            │
│  │  • Coreference  │  │  • Semantic     │  │  • Data Lineage │            │
│  │  • Bindings     │  │  • Contextual   │  │  • Decision     │            │
│  │  • Cache        │  │  • LLM-Assisted │  │    Lineage      │            │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘            │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                     INGESTION MODULE                                │   │
│  │   ───────────────────────────────────────────────────────────────   │   │
│  │                        The Harvester                                │   │
│  │                                                                      │   │
│  │   SQL Parser  │  Excel Parser  │  Doc Extractor  │  SME Interview  │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

## 4.2 Ontology Registry

### 4.2.1 Purpose

The Ontology Registry stores the "vocabulary" of the business domain—entities, their properties, relationships, and formal definitions.

### 4.2.2 Core Artifacts

| Artifact | Description | Example |
|----------|-------------|---------|
| **Entities** | Real-world business objects | Claim, Policy, Member, Product |
| **Attributes** | Properties with types, constraints | Claim.total_billed_amount (decimal, ≥0) |
| **Relationships** | Typed connections with cardinality | Claim --submitted_by--> Member (N:1) |
| **Taxonomies** | Hierarchical classifications | Claim Type: Medical > Inpatient > Surgery |
| **Glossary** | Canonical definitions, synonyms | "Member" = "Policyholder" = "Insured" |

### 4.2.3 Hierarchical Namespace Support

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      NAMESPACE HIERARCHY                                    │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  cogentiq.core                     (Platform primitives)                   │
│       │                                                                     │
│       ├── cogentiq.core.entity                                             │
│       ├── cogentiq.core.metric                                             │
│       └── cogentiq.core.constraint                                         │
│                                                                             │
│  cogentiq.domains                  (Industry domain packs)                 │
│       │                                                                     │
│       ├── cogentiq.domains.insurance                                       │
│       │       ├── cogentiq.domains.insurance.claims                        │
│       │       │       ├── Claim                                            │
│       │       │       ├── ClaimLine                                        │
│       │       │       └── Adjudication                                     │
│       │       ├── cogentiq.domains.insurance.policy                        │
│       │       └── cogentiq.domains.insurance.member                        │
│       │                                                                     │
│       ├── cogentiq.domains.cpg                                             │
│       │       ├── cogentiq.domains.cpg.product                             │
│       │       ├── cogentiq.domains.cpg.trade                               │
│       │       └── cogentiq.domains.cpg.retail                              │
│       │                                                                     │
│       └── cogentiq.domains.healthcare                                      │
│               ├── cogentiq.domains.healthcare.clinical                     │
│               ├── cogentiq.domains.healthcare.revenue_cycle                │
│               └── cogentiq.domains.healthcare.population_health            │
│                                                                             │
│  tenant.{tenant_id}                (Client-specific extensions)            │
│       │                                                                     │
│       └── tenant.acme.insurance.claims                                     │
│               ├── Claim (extends cogentiq.domains.insurance.claims.Claim)  │
│               │       └── + custom_field_1                                 │
│               │       └── + regional_code                                  │
│               └── AcmeSpecificEntity                                       │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 4.2.4 Versioning Strategy

| Change Type | Version Bump | Backward Compatible | Migration Required |
|-------------|--------------|---------------------|-------------------|
| Add optional attribute | MINOR | Yes | No |
| Add entity | MINOR | Yes | No |
| Add relationship | MINOR | Yes | No |
| Rename (with alias) | MINOR | Yes | No |
| Remove attribute | MAJOR | No | Yes |
| Change data type | MAJOR | No | Yes |
| Change cardinality | MAJOR | No | Yes |
| Documentation only | PATCH | Yes | No |

## 4.3 Semantic Catalog

### 4.3.1 Purpose

The Semantic Catalog stores executable business logic—metrics, dimensions, and their calculation rules.

### 4.3.2 Metric Definition Structure

```yaml
metric:
  # Identity
  id: "insurance.claims.loss_ratio"
  name: "loss_ratio"
  display_name: "Loss Ratio"
  description: "Ratio of incurred losses plus adjustment expenses to earned premium"
  domain: "insurance.claims"
  version: "2.1.0"
  
  # Calculation
  calculation:
    type: derived
    formula: "(${incurred_losses} + ${loss_adjustment_expenses}) / ${earned_premium}"
    dependencies:
      - "insurance.claims.incurred_losses"
      - "insurance.claims.loss_adjustment_expenses"
      - "insurance.claims.earned_premium"
  
  # Dimensions
  dimensions:
    - dimension_id: "common.time"
      required: true
      default_granularity: "month"
    - dimension_id: "insurance.line_of_business"
      required: false
    - dimension_id: "insurance.state"
      required: false
  
  # Data Contract
  data_contract:
    source_of_truth: "actuarial.loss_triangles"
    freshness_sla: "monthly"
    quality_rules:
      - "loss_ratio >= 0"
      - "loss_ratio <= 2.0"  # Warning if > 200%
    owner: "actuarial-team"
  
  # Business Context
  thresholds:
    target: 0.65
    warning: 0.75
    critical: 0.85
  
  # Formatting
  formatting:
    unit: ratio
    display_as: percentage
    decimals: 1
  
  # Governance
  governance:
    classification: "confidential"
    regulatory_tags: ["NAIC", "state_filing"]
    approved_uses: ["actuarial_analysis", "executive_reporting"]
    certifications: ["actuarial_approved", "finance_approved"]
  
  # Aliases
  aliases:
    - "LR"
    - "loss rate"
    - "claims ratio"
  
  # Lineage
  lineage:
    source_system: "actuarial_workbench"
    extraction_method: "sme_interview"
    extraction_date: "2025-01-15"
    extracted_by: "jsmith@fractal.ai"
```

## 4.4 Constraint Engine

### 4.4.1 Rule Categories

| Category | Purpose | Evaluation Point | Example |
|----------|---------|------------------|---------|
| **Access Control** | Who can see what | Pre-execution | "Analysts cannot query PII" |
| **Data Quality** | Validate results | Post-execution | "Volume cannot be negative" |
| **Business Logic** | Enforce rules | Post-execution | "Trade rate ≤ 40%" |
| **Confidence Gate** | Control output | Post-execution | "If confidence < 0.7, clarify" |
| **Cost Guard** | Limit spending | Pre-execution | "Max 10K tokens per query" |
| **Compliance** | Regulatory rules | Both | "PHI requires aggregation ≥ 11" |

### 4.4.2 CEL Rule Definitions

```yaml
constraints:
  # Access Control
  - id: "ac.analyst_pii_restriction"
    name: "Analyst PII Restriction"
    expression: |
      request.user.role == 'admin' || 
      !resource.contains_pii
    evaluation_point: pre_execution
    severity: error
    action: block
    message: "Access denied: PII requires admin role"
    
  # Business Logic
  - id: "bl.high_dollar_claim_review"
    name: "High Dollar Claim Review"
    expression: |
      !(claim.total_billed_amount > 50000 && 
        claim.provider.tier != 'preferred')
      || claim.requires_manual_review == true
    evaluation_point: post_execution
    severity: error
    action: escalate
    message: "High-value claims from non-preferred providers require review"
    
  # Confidence Gate
  - id: "cg.confidence_threshold"
    name: "Confidence Threshold"
    expression: "result.confidence >= 0.7"
    evaluation_point: post_execution
    severity: warning
    action: clarify
    message: "Low confidence result - requesting clarification"
    
  # Cost Guard
  - id: "cost.token_limit"
    name: "Token Limit"
    expression: "request.estimated_tokens <= 10000"
    evaluation_point: pre_execution
    severity: error
    action: block
    message: "Query exceeds token budget"
    
  # Compliance
  - id: "hipaa.minimum_aggregation"
    name: "HIPAA Minimum Aggregation"
    expression: |
      !resource.contains_phi ||
      result.patient_count >= 11 ||
      context.user.has_role('phi_authorized')
    evaluation_point: post_execution
    severity: error
    action: block
    message: "PHI requires minimum 11 patients for aggregation"
```

## 4.5 Context Graph

### 4.5.1 Session State Structure

```json
{
  "session_id": "sess_abc123",
  "tenant_id": "tenant_acme",
  "user_id": "user_jane",
  "created_at": "2025-01-26T10:00:00Z",
  "last_activity": "2025-01-26T10:15:32Z",
  
  "user_context": {
    "roles": ["analyst", "claims_user"],
    "permissions": ["read:claims", "read:policies"],
    "allowed_regions": ["US", "CA"],
    "clearance_level": 2
  },
  
  "entity_scope": [
    {
      "entity_type": "Claim",
      "entity_id": "claim_12345",
      "display_name": "Claim #12345",
      "salience": 0.95,
      "added_at": "2025-01-26T10:05:00Z"
    },
    {
      "entity_type": "Member",
      "entity_id": "member_67890",
      "display_name": "John Smith",
      "salience": 0.80,
      "added_at": "2025-01-26T10:05:00Z"
    }
  ],
  
  "bindings": {
    "temporal": {
      "last quarter": {
        "start_date": "2025-10-01",
        "end_date": "2025-12-31",
        "period_type": "quarter"
      },
      "this year": {
        "start_date": "2025-01-01",
        "end_date": "2025-12-31",
        "period_type": "year"
      }
    },
    "entity": {
      "the claim": "claim_12345",
      "this member": "member_67890",
      "it": "claim_12345"
    }
  },
  
  "conversation": {
    "turns": [
      {
        "role": "user",
        "content": "Look up claim 12345",
        "timestamp": "2025-01-26T10:05:00Z",
        "entities_mentioned": ["claim_12345"]
      },
      {
        "role": "assistant",
        "content": "Claim #12345 is for member John Smith...",
        "timestamp": "2025-01-26T10:05:15Z"
      }
    ],
    "current_topic": "claims_inquiry",
    "pending_clarification": null
  },
  
  "cache": {
    "claim_12345_details": {
      "value": {"status": "pending", "amount": 5420.00},
      "computed_at": "2025-01-26T10:05:10Z",
      "ttl_seconds": 300
    }
  }
}
```

## 4.6 Entity Resolution Service

### 4.6.1 Resolution Strategy Chain

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      ENTITY RESOLUTION PIPELINE                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  Input: "Apple"                                                            │
│         │                                                                   │
│         ▼                                                                   │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ 1. EXACT MATCH (Confidence: 1.0)                                    │   │
│  │    Lookup canonical names: "Apple" → Not found                      │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│         │                                                                   │
│         ▼                                                                   │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ 2. ALIAS MATCH (Confidence: 0.95)                                   │   │
│  │    Lookup alias registry: "Apple" →                                 │   │
│  │      - company:AAPL (alias: "Apple", "Apple Inc")                   │   │
│  │      - position:AAPL (alias: "Apple stock", "AAPL")                │   │
│  │      - product:apple (alias: "apple", "apples")                     │   │
│  │    Candidates: [company:AAPL, position:AAPL, product:apple]        │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│         │                                                                   │
│         ▼                                                                   │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ 3. CONTEXT SCORING (Bonus: +0.15)                                   │   │
│  │    Session context: "Tech Portfolio Analysis"                       │   │
│  │    Entities in scope: [portfolio:tech_growth, position:MSFT]       │   │
│  │                                                                      │   │
│  │    Adjusted scores:                                                 │   │
│  │      - position:AAPL: 0.95 + 0.15 (in portfolio) = 1.10 → cap 1.0  │   │
│  │      - company:AAPL: 0.95 + 0.05 (related) = 1.00                  │   │
│  │      - product:apple: 0.95 + 0.00 (no context) = 0.95              │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│         │                                                                   │
│         ▼                                                                   │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ 4. CONFIDENCE GATE                                                  │   │
│  │    Top: position:AAPL (1.0)                                        │   │
│  │    Second: company:AAPL (1.0)                                      │   │
│  │    Gap: 0.0 < 0.1 threshold → AMBIGUOUS                            │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│         │                                                                   │
│         ▼                                                                   │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ 5. CLARIFICATION REQUEST                                            │   │
│  │    "I found multiple matches for 'Apple'. Did you mean:            │   │
│  │     1. Apple (AAPL) - your stock position                          │   │
│  │     2. Apple Inc. - the company                                    │   │
│  │    Or tell me more about what you're looking for."                 │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

## 4.7 Lineage Service

### 4.7.1 Lineage Record Structure

```yaml
LineageRecord:
  lineage_id: "lin_xyz789"
  output_id: "out_abc123"
  session_id: "sess_def456"
  tenant_id: "tenant_acme"
  timestamp: "2025-01-26T10:30:00Z"
  
  # What was asked
  request:
    original_query: "What is the loss ratio for Q3?"
    parsed_intent: "metric_query"
    confidence: 0.92
  
  # How it was routed
  routing:
    path_selected: "symbolic"
    symbolic_confidence: 0.94
    reasoning: "All entities resolved with high confidence"
    
  # What definitions were used
  definitions_used:
    - type: metric
      id: "insurance.claims.loss_ratio"
      version: "2.1.0"
      formula: "(incurred_losses + loss_adjustment_expenses) / earned_premium"
    - type: dimension
      id: "common.time.quarter"
      version: "1.0.0"
      
  # What data was accessed
  data_sources:
    - source: "snowflake://insurance_dw/actuarial/loss_triangles"
      columns: ["incurred_losses", "lae", "earned_premium", "accident_quarter"]
      filter: "accident_quarter = '2025-Q3'"
      row_count: 156
      freshness: "2025-01-25T06:00:00Z"
      
  # What was computed
  execution:
    generated_sql: |
      SELECT 
        (SUM(incurred_losses) + SUM(lae)) / SUM(earned_premium) as loss_ratio
      FROM actuarial.loss_triangles
      WHERE accident_quarter = '2025-Q3'
    execution_time_ms: 234
    rows_returned: 1
    
  # What constraints were checked
  constraints_evaluated:
    - rule_id: "bl.loss_ratio_bounds"
      result: "passed"
    - rule_id: "cg.confidence_threshold"
      result: "passed"
      
  # Final result
  result:
    value: 0.682
    formatted: "68.2%"
    confidence: 0.94
```

---

# 5. LAYER 3: AGENTIC LAYER

## 5.1 Agent Development Kit (ADK)

### 5.1.1 Purpose

The ADK provides a declarative, platform-neutral way to define agents that can be transpiled to multiple execution targets.

### 5.1.2 Agent Specification Format

```yaml
# Cogentiq Agent Specification (CAS) Format
# Version: 1.0.0

agent:
  # Identity
  id: "insurance.claims.triage_agent"
  name: "Claims Triage Agent"
  version: "1.2.0"
  description: "Triages incoming insurance claims for processing priority and routing"
  
  # Domain Context (from Ontology)
  ontology_context:
    domain_pack: "cogentiq.domains.insurance.claims"
    entities:
      - Claim
      - Policy
      - Member
      - Provider
    metrics:
      - claim_severity_score
      - provider_fraud_score
      - policy_coverage_status
    constraints:
      - high_dollar_claim_review
      - provider_network_check
      
  # Model Configuration
  model:
    provider: "azure_openai"  # or "anthropic", "bedrock", etc.
    model_id: "gpt-4o"
    parameters:
      temperature: 0.1
      max_tokens: 4096
      
  # System Prompt (with ontology injection points)
  instructions: |
    You are a claims triage agent for {tenant.name}, an insurance company.
    
    ## Your Role
    You help triage incoming claims by:
    1. Validating claim information
    2. Checking policy status and coverage
    3. Assessing claim priority
    4. Routing to appropriate handling queue
    
    ## Domain Knowledge
    {ontology_context}  # Injected at runtime
    
    ## Business Rules
    {constraint_rules}  # Injected at runtime
    
    ## Guidelines
    - Always verify member eligibility before processing
    - Flag claims over $50,000 from non-preferred providers for review
    - Maintain HIPAA compliance in all communications
    
  # Tools
  tools:
    - id: lookup_claim
      type: semantic_query
      description: "Look up claim details by ID"
      metric: claim_details
      parameters:
        - name: claim_id
          type: string
          required: true
          
    - id: check_policy_status
      type: semantic_query
      description: "Check if policy is active and covers the service"
      metric: policy_coverage_status
      parameters:
        - name: policy_id
          type: string
          required: true
        - name: service_code
          type: string
          required: false
          
    - id: calculate_severity
      type: semantic_query
      description: "Calculate claim severity score"
      metric: claim_severity_score
      parameters:
        - name: claim_id
          type: string
          required: true
          
    - id: flag_for_review
      type: action
      description: "Flag claim for manual review"
      target: claims_workflow_system
      parameters:
        - name: claim_id
          type: string
          required: true
        - name: reason
          type: string
          required: true
        - name: priority
          type: string
          enum: [low, medium, high, urgent]
          
    - id: route_to_queue
      type: action
      description: "Route claim to processing queue"
      target: claims_workflow_system
      parameters:
        - name: claim_id
          type: string
          required: true
        - name: queue
          type: string
          enum: [auto_adjudicate, medical_review, fraud_investigation, manual_processing]
          
  # Agent Patterns
  patterns:
    - type: reflection_loop
      config:
        max_iterations: 3
        reflection_prompt: "Review your triage decision. Is there anything you missed?"
        
    - type: validation_gate
      config:
        constraint: high_dollar_claim_review
        on_violation: escalate
        
    - type: hitl_breakpoint
      config:
        condition: "claim.amount > 100000 || claim.fraud_score > 0.7"
        approval_required: true
        timeout_minutes: 60
        escalation_queue: "supervisor_review"
        
    - type: fallback_chain
      config:
        primary_model: "gpt-4o"
        fallback_models: ["gpt-4o-mini", "claude-3-sonnet"]
        trigger: "rate_limit_or_error"
        
  # Governance
  governance:
    cost_budget:
      max_tokens_per_request: 10000
      max_cost_per_day_usd: 100
    audit:
      log_all_decisions: true
      retain_days: 90
    compliance:
      pii_handling: "mask_in_logs"
      regulatory_tags: ["HIPAA", "state_insurance_regulations"]
      
  # Testing
  test_cases:
    - name: "Simple claim lookup"
      input: "Look up claim 12345"
      expected_tool_calls: ["lookup_claim"]
      expected_entities: ["claim:12345"]
      
    - name: "High dollar claim routing"
      input: "Process claim 67890 for $75,000 from out-of-network provider"
      expected_tool_calls: ["lookup_claim", "check_policy_status", "flag_for_review"]
      expected_routing: "manual_processing"
```

### 5.1.3 Built-in Agent Patterns

| Pattern | Purpose | Configuration |
|---------|---------|---------------|
| **Reflection Loop** | Self-critique and improve | max_iterations, reflection_prompt |
| **Validation Gate** | Constraint checkpoint | constraint_id, on_violation action |
| **HITL Breakpoint** | Human approval point | condition, timeout, escalation |
| **Fallback Chain** | Model redundancy | primary, fallbacks, trigger |
| **Parallel Execution** | Concurrent tool calls | max_parallel, merge_strategy |
| **Memory Injection** | Context loading | memory_source, relevance_threshold |
| **Confidence Gate** | Output quality control | threshold, on_low_confidence |

### 5.1.4 Agent Testing Harness

```yaml
# Agent Test Suite Definition

test_suite:
  agent_id: "insurance.claims.triage_agent"
  version: "1.2.0"
  
  # Test fixtures
  fixtures:
    claims:
      - id: "claim_simple"
        data:
          claim_id: "12345"
          amount: 500.00
          provider_tier: "preferred"
          service_type: "preventive"
          
      - id: "claim_high_dollar"
        data:
          claim_id: "67890"
          amount: 75000.00
          provider_tier: "out_of_network"
          service_type: "surgery"
          
      - id: "claim_fraud_suspect"
        data:
          claim_id: "11111"
          amount: 15000.00
          fraud_score: 0.85
          
  # Test cases
  test_cases:
    - name: "Simple claim processed automatically"
      fixture: "claim_simple"
      input: "Process claim 12345"
      assertions:
        - type: tool_called
          tool: "lookup_claim"
          with_params: {claim_id: "12345"}
        - type: tool_called
          tool: "route_to_queue"
          with_params: {queue: "auto_adjudicate"}
        - type: no_hitl_triggered
        - type: response_contains
          text: "routed for automatic adjudication"
          
    - name: "High dollar claim flagged for review"
      fixture: "claim_high_dollar"
      input: "Process claim 67890"
      assertions:
        - type: constraint_evaluated
          constraint: "high_dollar_claim_review"
          result: "violated"
        - type: tool_called
          tool: "flag_for_review"
        - type: hitl_triggered
          reason: "claim.amount > 50000"
          
    - name: "Fraud suspect routed to investigation"
      fixture: "claim_fraud_suspect"
      input: "Process claim 11111"
      assertions:
        - type: tool_called
          tool: "calculate_severity"
        - type: tool_called
          tool: "route_to_queue"
          with_params: {queue: "fraud_investigation"}
          
  # Performance benchmarks
  benchmarks:
    - name: "Latency"
      metric: "end_to_end_latency_ms"
      threshold_p95: 5000
      
    - name: "Token efficiency"
      metric: "tokens_per_request"
      threshold_avg: 3000
      
  # Accuracy metrics (against golden dataset)
  accuracy:
    golden_dataset: "claims_triage_golden_v1"
    metrics:
      - name: "Routing accuracy"
        type: "classification"
        threshold: 0.92
      - name: "HITL trigger precision"
        type: "binary"
        threshold: 0.95
```

## 5.2 Neuro-Symbolic Router

### 5.2.1 Purpose

The Neuro-Symbolic Router determines how to process each query—using deterministic symbolic execution when possible, LLM reasoning when needed, and hybrid approaches when both are required.

### 5.2.2 Execution Paths

| Path | When Used | Characteristics |
|------|-----------|-----------------|
| **Symbolic** | All entities resolve, confidence ≥ 0.85 | Deterministic, no LLM in calculation, full lineage |
| **Hybrid** | Partial match, confidence 0.50-0.85 | Calculation symbolic, interpretation neural |
| **Neural** | No entity match, confidence < 0.50 | Full LLM reasoning, marked as AI-generated |
| **Clarification** | Ambiguous, multiple candidates | Ask user to disambiguate |

### 5.2.3 Confidence-Gated Response System

| Confidence | Action | User Experience |
|------------|--------|-----------------|
| ≥ 0.85 | Return result | Direct answer |
| 0.70-0.84 | Return with caveat | "Based on my interpretation..." |
| 0.50-0.69 | Offer clarification | "Did you mean...?" |
| 0.30-0.49 | Request clarification | "I'm not sure. Can you specify...?" |
| < 0.30 | Graceful decline | "I don't have enough information." |

### 5.2.4 Router API

```yaml
# POST /router/analyze
request:
  query: "What was the loss ratio last quarter?"
  session_id: "sess_abc123"
  force_path: null  # optional: "symbolic" | "neural" | "hybrid"
  
response:
  decision_id: "dec_xyz789"
  
  intent:
    category: "metric_query"
    confidence: 0.94
    
  entity_matches:
    - source_text: "loss ratio"
      entity_type: "metric"
      entity_id: "insurance.claims.loss_ratio"
      confidence: 0.98
      method: "exact"
    - source_text: "last quarter"
      entity_type: "time_reference"
      resolved_value: "2025-Q3"
      confidence: 0.95
      method: "temporal_binding"
      
  selected_path: "symbolic"
  
  confidence_scores:
    symbolic: 0.94
    overall: 0.94
    
  path_reasoning: "All entities resolved with high confidence. Metric definition found."
  
  clarification: null  # or clarification request if needed
```

---

# 6. LAYER 4: KNOWLEDGE ASSET REGISTRY

## 6.1 Purpose

The Knowledge Asset Registry stores reusable components that compound across engagements:
- Domain Knowledge Packs
- Prompt Libraries
- Tool Definitions
- Workflow Templates

## 6.2 Domain Knowledge Packs

### 6.2.1 Pack Structure

```
insurance_domain_pack/
├── manifest.yaml                    # Pack metadata and dependencies
├── ontology/
│   ├── entities/
│   │   ├── claim.com.yaml
│   │   ├── policy.com.yaml
│   │   ├── member.com.yaml
│   │   └── provider.com.yaml
│   ├── relationships/
│   │   └── insurance_relationships.yaml
│   ├── taxonomies/
│   │   ├── claim_types.yaml
│   │   ├── denial_reasons.yaml
│   │   └── procedure_codes.yaml     # Links to external CPT/ICD
│   └── glossary/
│       └── insurance_terms.yaml
├── semantic/
│   ├── metrics/
│   │   ├── claims_metrics.yaml       # Loss ratio, cycle time, etc.
│   │   ├── underwriting_metrics.yaml
│   │   └── member_metrics.yaml
│   └── dimensions/
│       ├── time.yaml
│       ├── geography.yaml
│       └── line_of_business.yaml
├── constraints/
│   ├── business_rules.yaml
│   ├── compliance/
│   │   ├── hipaa.yaml
│   │   └── state_regulations.yaml
│   └── data_quality.yaml
├── workflow_patterns/
│   ├── claims_adjudication.workflow.yaml
│   ├── prior_authorization.workflow.yaml
│   └── appeals_process.workflow.yaml
├── agent_templates/
│   ├── claims_triage_agent.cas.yaml
│   ├── fraud_detection_agent.cas.yaml
│   └── member_service_agent.cas.yaml
├── prompt_library/
│   ├── claims_analysis/
│   └── member_communication/
├── data_bindings/
│   ├── common_schemas/
│   │   ├── edi_837.mapping.yaml     # Industry standard claim format
│   │   └── edi_835.mapping.yaml     # Remittance format
│   └── vendor_specific/
│       ├── guidewire.mapping.yaml
│       └── duck_creek.mapping.yaml
├── test_data/
│   ├── golden_datasets/
│   └── fixtures/
└── documentation/
    ├── README.md
    └── implementation_guide.md
```

### 6.2.2 Pack Manifest

```yaml
# manifest.yaml
pack:
  id: "cogentiq.domains.insurance"
  name: "Insurance Domain Pack"
  version: "2.1.0"
  description: "Comprehensive ontology and assets for P&C and Life insurance"
  
  # Dependencies
  dependencies:
    - pack: "cogentiq.core"
      version: ">=1.0.0"
    - pack: "cogentiq.domains.common.finance"
      version: ">=1.0.0"
      
  # External standards
  standards_compliance:
    - standard: "ACORD"
      version: "2024"
    - standard: "HL7_FHIR"
      version: "R4"
      scope: "healthcare_claims"
      
  # Contents summary
  contents:
    entities: 47
    metrics: 89
    constraints: 156
    workflow_templates: 12
    agent_templates: 8
    
  # Governance
  governance:
    owner: "insurance-domain-team"
    classification: "internal"
    license: "cogentiq-commercial"
    
  # Quality metrics
  quality:
    test_coverage: 0.87
    documentation_coverage: 0.92
    client_deployments: 14
    
  # Changelog
  changelog:
    - version: "2.1.0"
      date: "2025-01-15"
      changes:
        - "Added prior authorization workflow"
        - "Updated state-specific compliance rules"
        - "New fraud detection agent template"
```

## 6.3 Prompt Libraries

### 6.3.1 Prompt Template Structure

```yaml
# claims_analysis/severity_assessment.prompt.yaml
prompt:
  id: "insurance.claims.severity_assessment"
  name: "Claim Severity Assessment"
  version: "1.3.0"
  description: "Assess the severity and priority of an insurance claim"
  
  # Template with injection points
  template: |
    You are assessing the severity of an insurance claim.
    
    ## Claim Details
    {claim_details}
    
    ## Member History
    {member_history}
    
    ## Provider Information
    {provider_info}
    
    ## Assessment Criteria
    Consider the following factors:
    1. Claim amount relative to policy limits
    2. Service type and medical necessity
    3. Provider network status
    4. Member claim history
    5. Potential fraud indicators
    
    ## Output Format
    Provide your assessment in the following format:
    - Severity Score (1-10): 
    - Priority Level (low/medium/high/urgent):
    - Key Risk Factors:
    - Recommended Routing:
    - Explanation:
    
  # Variable specifications
  variables:
    - name: claim_details
      type: object
      source: semantic_query
      metric: claim_details
      required: true
      
    - name: member_history
      type: object
      source: semantic_query
      metric: member_claim_history
      required: false
      
    - name: provider_info
      type: object
      source: semantic_query
      metric: provider_details
      required: true
      
  # Governance
  governance:
    classification: "confidential"
    pii_handling: "mask_ssn_dob"
    approved_uses: ["claims_processing", "fraud_detection"]
    review_required: true
    last_reviewed: "2025-01-10"
    reviewed_by: "claims-governance-team"
    
  # Performance
  performance:
    avg_tokens_in: 1200
    avg_tokens_out: 350
    avg_latency_ms: 2100
    
  # Test cases
  tests:
    - name: "Standard claim assessment"
      inputs:
        claim_details: {amount: 5000, service_type: "outpatient"}
        provider_info: {tier: "preferred", fraud_score: 0.1}
      expected_output_contains:
        - "Severity Score"
        - "Priority Level"
```

## 6.4 Workflow Templates

### 6.4.1 Workflow Definition

```yaml
# claims_adjudication.workflow.yaml
workflow:
  id: "insurance.claims.adjudication"
  name: "Claims Adjudication Workflow"
  version: "2.0.0"
  description: "End-to-end claims adjudication process"
  
  # Trigger
  trigger:
    type: event
    event: "claim.submitted"
    
  # Workflow steps
  steps:
    - id: intake
      name: "Claim Intake"
      type: agent_task
      agent: "claims_intake_agent"
      inputs:
        claim_id: "{trigger.claim_id}"
      outputs:
        - validated_claim
        - intake_status
      on_error: escalate_to_human
      
    - id: eligibility_check
      name: "Eligibility Verification"
      type: semantic_query
      metric: "member_eligibility_status"
      inputs:
        member_id: "{intake.validated_claim.member_id}"
        service_date: "{intake.validated_claim.service_date}"
      outputs:
        - eligibility_result
      conditions:
        - if: "{eligibility_result.eligible} == false"
          goto: denial_processing
          
    - id: coverage_check
      name: "Coverage Verification"
      type: semantic_query
      metric: "policy_coverage_details"
      inputs:
        policy_id: "{intake.validated_claim.policy_id}"
        service_codes: "{intake.validated_claim.service_codes}"
      outputs:
        - coverage_result
        
    - id: medical_review_decision
      name: "Medical Review Decision"
      type: constraint_evaluation
      constraints:
        - medical_review_required
        - high_dollar_threshold
      inputs:
        claim: "{intake.validated_claim}"
        coverage: "{coverage_check.coverage_result}"
      routing:
        - if: requires_medical_review
          goto: medical_review
        - else:
          goto: auto_adjudication
          
    - id: medical_review
      name: "Medical Review"
      type: human_task
      assignee_role: "medical_reviewer"
      sla_hours: 48
      inputs:
        claim: "{intake.validated_claim}"
        clinical_notes: "{intake.clinical_documentation}"
      outputs:
        - review_decision
        - review_notes
        
    - id: auto_adjudication
      name: "Automatic Adjudication"
      type: agent_task
      agent: "auto_adjudication_agent"
      inputs:
        claim: "{intake.validated_claim}"
        coverage: "{coverage_check.coverage_result}"
      outputs:
        - adjudication_result
        - payment_amount
        
    - id: payment_processing
      name: "Payment Processing"
      type: action
      target: "payment_system"
      action: "initiate_payment"
      inputs:
        claim_id: "{trigger.claim_id}"
        amount: "{auto_adjudication.payment_amount}"
        payee: "{intake.validated_claim.provider_id}"
        
    - id: denial_processing
      name: "Denial Processing"
      type: agent_task
      agent: "denial_processing_agent"
      inputs:
        claim: "{intake.validated_claim}"
        denial_reason: "{eligibility_check.eligibility_result.denial_code}"
        
  # Workflow-level configuration
  config:
    timeout_hours: 72
    retry_policy:
      max_retries: 3
      backoff: exponential
    audit:
      log_all_steps: true
      retain_days: 2555  # 7 years for insurance
```

## 6.5 Knowledge Flywheel

### 6.5.1 Compounding Value Model

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                     KNOWLEDGE FLYWHEEL                                      │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│    ENGAGEMENT 1                  ENGAGEMENT 2                  ENGAGEMENT 3 │
│    (Insurance Co A)              (Insurance Co B)              (Insurance Co C)
│         │                              │                              │     │
│         ▼                              ▼                              ▼     │
│    ┌─────────┐                   ┌─────────┐                   ┌─────────┐ │
│    │ Extract │                   │ Extract │                   │ Extract │ │
│    │ Domain  │                   │ Domain  │                   │ Domain  │ │
│    │Knowledge│                   │Knowledge│                   │Knowledge│ │
│    └────┬────┘                   └────┬────┘                   └────┬────┘ │
│         │                              │                              │     │
│         └──────────────────────────────┼──────────────────────────────┘     │
│                                        │                                    │
│                                        ▼                                    │
│                         ┌──────────────────────────┐                        │
│                         │   INSURANCE DOMAIN PACK  │                        │
│                         │                          │                        │
│                         │   Entities: 47           │                        │
│                         │   Metrics: 89            │                        │
│                         │   Workflows: 12          │                        │
│                         │   Agents: 8              │                        │
│                         │                          │                        │
│                         │   Client-specific:       │                        │
│                         │   - Co A extensions      │                        │
│                         │   - Co B extensions      │                        │
│                         │   - Co C extensions      │                        │
│                         └──────────────────────────┘                        │
│                                        │                                    │
│                                        ▼                                    │
│                         ┌──────────────────────────┐                        │
│                         │   ENGAGEMENT 4           │                        │
│                         │   (Insurance Co D)       │                        │
│                         │                          │                        │
│                         │   Time to Value:         │                        │
│                         │   Before: 12 weeks       │                        │
│                         │   Now: 3 weeks           │                        │
│                         │                          │                        │
│                         │   Reuse Rate: 75%        │                        │
│                         └──────────────────────────┘                        │
│                                                                             │
│   METRICS:                                                                  │
│   • Deployment 1: 0% reuse, 12 weeks                                       │
│   • Deployment 5: 50% reuse, 6 weeks                                       │
│   • Deployment 10: 70% reuse, 4 weeks                                      │
│   • Deployment 20: 80% reuse, 2 weeks                                      │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

# 7. LAYER 5: GOVERNANCE & RELIABILITY FRAMEWORK

## 7.1 Decision Audit Trail

### 7.1.1 Audit Record Structure

```yaml
AuditRecord:
  audit_id: "aud_abc123"
  timestamp: "2025-01-26T10:30:00.123Z"
  
  # Context
  session_id: "sess_xyz789"
  tenant_id: "tenant_acme"
  user_id: "user_jane"
  agent_id: "insurance.claims.triage_agent"
  
  # Decision
  decision_type: "routing_decision"  # or "tool_call", "constraint_evaluation", etc.
  decision_id: "dec_456"
  
  # Inputs
  inputs:
    query: "Process claim 12345"
    context:
      entities_in_scope: ["claim:12345"]
      
  # Outputs
  outputs:
    selected_path: "symbolic"
    confidence: 0.92
    result: {claim_status: "approved", amount: 5420.00}
    
  # Explainability
  explanation:
    reasoning_trace:
      - step: "entity_resolution"
        result: "claim_id resolved to claim:12345"
      - step: "constraint_check"
        result: "all constraints passed"
      - step: "path_selection"
        result: "symbolic path selected (confidence: 0.92)"
    contributing_factors:
      - factor: "exact_entity_match"
        weight: 0.4
      - factor: "metric_definition_found"
        weight: 0.3
      - factor: "context_available"
        weight: 0.3
        
  # Lineage reference
  lineage_id: "lin_789"
  
  # Governance tags
  governance:
    classification: "confidential"
    pii_accessed: false
    regulatory_tags: ["HIPAA"]
```

## 7.2 Risk-Based Execution Controls

### 7.2.1 Risk Scoring Model

```yaml
RiskAssessment:
  # Input factors
  factors:
    - name: query_complexity
      weight: 0.15
      scoring:
        simple_lookup: 0.1
        multi_step_calculation: 0.5
        open_ended_analysis: 0.9
        
    - name: data_sensitivity
      weight: 0.25
      scoring:
        public: 0.1
        internal: 0.3
        confidential: 0.6
        pii_phi: 0.9
        
    - name: confidence_level
      weight: 0.20
      scoring:
        high: 0.1  # >= 0.85
        medium: 0.4  # 0.50-0.85
        low: 0.8  # < 0.50
        
    - name: action_reversibility
      weight: 0.25
      scoring:
        read_only: 0.1
        reversible_action: 0.4
        irreversible_action: 0.9
        
    - name: financial_impact
      weight: 0.15
      scoring:
        none: 0.1
        low: 0.3
        medium: 0.5
        high: 0.9
        
  # Risk thresholds
  thresholds:
    low: 0.3      # Proceed automatically
    medium: 0.5   # Proceed with logging
    high: 0.7     # Require confirmation
    critical: 0.9 # Require human approval
    
  # Actions by risk level
  actions:
    low:
      - log_decision
    medium:
      - log_decision
      - notify_user
    high:
      - log_decision
      - require_confirmation
      - notify_supervisor
    critical:
      - log_decision
      - require_human_approval
      - notify_compliance
```

## 7.3 Cost Guardrails

### 7.3.1 Token Budget Management

```yaml
CostGuardrails:
  # Per-request limits
  request_limits:
    max_input_tokens: 10000
    max_output_tokens: 4000
    max_total_tokens: 14000
    max_tool_calls: 10
    
  # Per-session limits
  session_limits:
    max_tokens_per_session: 100000
    max_cost_per_session_usd: 5.00
    max_duration_minutes: 60
    
  # Per-user limits (daily)
  user_limits:
    max_tokens_per_day: 500000
    max_cost_per_day_usd: 50.00
    max_requests_per_day: 1000
    
  # Per-tenant limits (monthly)
  tenant_limits:
    max_tokens_per_month: 10000000
    max_cost_per_month_usd: 5000.00
    
  # Model-specific pricing
  model_pricing:
    gpt-4o:
      input_per_1k: 0.005
      output_per_1k: 0.015
    gpt-4o-mini:
      input_per_1k: 0.00015
      output_per_1k: 0.0006
    claude-3-sonnet:
      input_per_1k: 0.003
      output_per_1k: 0.015
      
  # Enforcement actions
  enforcement:
    soft_limit_action: "warn_and_continue"
    hard_limit_action: "block_and_notify"
    overage_handling: "queue_for_next_period"
```

## 7.4 Compliance Tagging

### 7.4.1 Compliance Framework

```yaml
ComplianceFramework:
  # Regulatory tags
  regulatory_tags:
    - id: "HIPAA"
      description: "Health Insurance Portability and Accountability Act"
      requirements:
        - minimum_aggregation: 11
        - phi_encryption: required
        - audit_logging: required
        - access_control: role_based
        
    - id: "GDPR"
      description: "General Data Protection Regulation"
      requirements:
        - consent_tracking: required
        - right_to_erasure: supported
        - data_portability: supported
        - dpo_notification: on_breach
        
    - id: "SOX"
      description: "Sarbanes-Oxley Act"
      requirements:
        - financial_data_controls: required
        - audit_trail: immutable
        - segregation_of_duties: required
        
    - id: "NAIC"
      description: "National Association of Insurance Commissioners"
      requirements:
        - state_filing_compliance: required
        - rate_calculation_audit: required
        
  # Data classification
  data_classification:
    - level: "public"
      handling: "standard"
      retention_days: 90
      
    - level: "internal"
      handling: "access_controlled"
      retention_days: 365
      
    - level: "confidential"
      handling: "encrypted_at_rest"
      retention_days: 2555  # 7 years
      
    - level: "restricted"
      handling: "encrypted_plus_audit"
      retention_days: 2555
      access_logging: "mandatory"
      
  # PII/PHI handling
  sensitive_data_handling:
    pii_fields:
      - ssn
      - date_of_birth
      - driver_license
      - passport_number
      - bank_account
      - credit_card
    phi_fields:
      - medical_record_number
      - diagnosis_codes
      - treatment_records
      - prescription_history
    handling_rules:
      - mask_in_logs: true
      - encrypt_at_rest: true
      - encrypt_in_transit: true
      - access_audit: true
```

---

# 8. LAYER 6: INTEGRATION FABRIC

## 8.1 Connector Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         INTEGRATION FABRIC                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                    CONNECTOR REGISTRY                               │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                        │
│         ┌──────────────────────────┼──────────────────────────┐            │
│         ▼                          ▼                          ▼            │
│  ┌─────────────────┐      ┌─────────────────┐      ┌─────────────────┐    │
│  │ ENTERPRISE      │      │ DATA            │      │ SEMANTIC        │    │
│  │ SYSTEMS         │      │ PLATFORMS       │      │ LAYERS          │    │
│  │                 │      │                 │      │                 │    │
│  │ • SAP S/4HANA   │      │ • Snowflake     │      │ • dbt Semantic  │    │
│  │ • Salesforce    │      │ • Databricks    │      │ • Cube          │    │
│  │ • Workday       │      │ • BigQuery      │      │ • AtScale       │    │
│  │ • ServiceNow    │      │ • Redshift      │      │ • Looker        │    │
│  │ • Oracle EBS    │      │ • Fabric        │      │                 │    │
│  │ • Epic/Cerner   │      │ • PostgreSQL    │      │                 │    │
│  └─────────────────┘      └─────────────────┘      └─────────────────┘    │
│         │                          │                          │            │
│         └──────────────────────────┼──────────────────────────┘            │
│                                    ▼                                        │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                    MCP ADAPTER INTERFACE                            │   │
│  │                                                                      │   │
│  │  Methods:                                                           │   │
│  │  • connect(config) → Connection                                     │   │
│  │  • list_resources() → ResourceList                                  │   │
│  │  • get_schema(resource) → Schema                                    │   │
│  │  • execute_query(sql) → ResultSet                                   │   │
│  │  • execute_action(action, params) → ActionResult                   │   │
│  │  • get_sample_data(resource, limit) → SampleData                   │   │
│  │                                                                      │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                        │
│                                    ▼                                        │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                    THIRD-PARTY AGENT INTEROP                        │   │
│  │                                                                      │   │
│  │  • Consume external agents as tools                                 │   │
│  │  • Publish Cogentiq agents as external tools                       │   │
│  │  • Cross-platform agent orchestration                              │   │
│  │                                                                      │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

## 8.2 Connector Specifications

### 8.2.1 Snowflake Connector

```yaml
connector:
  id: "snowflake"
  name: "Snowflake Data Cloud"
  version: "1.2.0"
  
  # Connection
  connection:
    auth_methods:
      - oauth2
      - key_pair
      - password  # deprecated
    required_params:
      - account
      - warehouse
    optional_params:
      - database
      - schema
      - role
      
  # Capabilities
  capabilities:
    - execute_query
    - list_databases
    - list_schemas
    - list_tables
    - get_table_schema
    - get_sample_data
    - execute_stored_procedure
    - stream_results
    
  # Semantic mapping
  semantic_mapping:
    type_mapping:
      NUMBER: decimal
      VARCHAR: string
      TIMESTAMP_NTZ: datetime
      BOOLEAN: boolean
      VARIANT: object
    supports_time_travel: true
    supports_streams: true
    
  # Query optimization
  optimization:
    pushdown_filters: true
    pushdown_aggregations: true
    result_caching: true
    warehouse_auto_scaling: true
    
  # Security
  security:
    row_level_security: true
    column_masking: true
    network_policies: true
    
  # Monitoring
  monitoring:
    query_history: true
    cost_tracking: true
    usage_metrics: true
```

### 8.2.2 Semantic Layer Adapters

```yaml
# dbt Semantic Layer Adapter
adapter:
  id: "dbt_semantic"
  name: "dbt Semantic Layer"
  version: "1.0.0"
  
  # Connection
  connection:
    auth: dbt_cloud_api_key
    endpoint: dbt_semantic_layer_endpoint
    
  # Mapping to Cogentiq
  mapping:
    dbt_metric → cogentiq_metric:
      name: metric.name
      description: metric.description
      calculation: metric.expression
      dimensions: metric.dimensions
      time_grains: metric.time_grains
      
    dbt_entity → cogentiq_entity:
      name: entity.name
      primary_key: entity.primary_key
      
  # Import capabilities
  import:
    - metrics
    - dimensions
    - entities
    - semantic_models
    
  # Sync
  sync:
    mode: incremental
    frequency: daily
    conflict_resolution: prefer_dbt
```

---

# 9. ONTOLOGY WORKBENCH

## 9.1 Purpose

The Ontology Workbench is the primary interface for creating, editing, and managing domain models. It is the **main moat builder** for Cogentiq.

## 9.2 Ingestion Pipelines

### 9.2.1 Multi-Source Ingestion Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        ONTOLOGY INGESTION PIPELINES                         │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐  │
│  │ STRUCTURED  │    │  DOCUMENTS  │    │   HUMAN     │    │  EXISTING   │  │
│  │    DATA     │    │             │    │  EXPERTS    │    │   MODELS    │  │
│  │             │    │             │    │             │    │             │  │
│  │ • Databases │    │ • Data Dict │    │ • SME       │    │ • ERD       │  │
│  │ • DWH       │    │ • SOPs      │    │   Interviews│    │ • dbt YAML  │  │
│  │ • Semantic  │    │ • Reqs Docs │    │ • Workshops │    │ • Salesforce│  │
│  │   Layers    │    │ • Standards │    │             │    │ • FHIR/FIBO │  │
│  └──────┬──────┘    └──────┬──────┘    └──────┬──────┘    └──────┬──────┘  │
│         │                  │                  │                  │          │
│         ▼                  ▼                  ▼                  ▼          │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐  │
│  │   Schema    │    │     LLM     │    │  Interview  │    │   Import    │  │
│  │  Crawler    │    │  Extractor  │    │    Agent    │    │   Adapter   │  │
│  └──────┬──────┘    └──────┬──────┘    └──────┬──────┘    └──────┬──────┘  │
│         │                  │                  │                  │          │
│         └──────────────────┴────────┬─────────┴──────────────────┘          │
│                                     ▼                                       │
│                    ┌─────────────────────────────┐                          │
│                    │  RECONCILIATION & CONFLICT  │                          │
│                    │         RESOLUTION          │                          │
│                    │                             │                          │
│                    │  • Duplicate detection      │                          │
│                    │  • Conflict identification  │                          │
│                    │  • Merge suggestions        │                          │
│                    │  • Quality scoring          │                          │
│                    └──────────────┬──────────────┘                          │
│                                   ▼                                         │
│                    ┌─────────────────────────────┐                          │
│                    │   CANDIDATE DEFINITION      │                          │
│                    │        QUEUE                │                          │
│                    └──────────────┬──────────────┘                          │
│                                   ▼                                         │
│                    ┌─────────────────────────────┐                          │
│                    │   HUMAN-IN-LOOP REVIEW      │                          │
│                    │   (Ontology Workbench UI)   │                          │
│                    │                             │                          │
│                    │   "GitHub PR for Logic"     │                          │
│                    └──────────────┬──────────────┘                          │
│                                   ▼                                         │
│                    ┌─────────────────────────────┐                          │
│                    │   ONTOLOGY REGISTRY         │                          │
│                    │   (Published Definitions)   │                          │
│                    └─────────────────────────────┘                          │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 9.2.2 Schema Crawler Pipeline

```yaml
SchemaC rawlerPipeline:
  # Input
  input:
    source_type: database
    connection: snowflake_connection
    scope:
      databases: ["CLAIMS_DW"]
      schemas: ["CLAIMS", "REFERENCE"]
      
  # Extraction steps
  steps:
    - step: physical_schema_extraction
      actions:
        - extract_tables
        - extract_columns
        - extract_constraints
        - extract_foreign_keys
        - extract_indexes
        
    - step: metadata_enrichment
      sources:
        - data_catalog: alation
        - lineage_tool: monte_carlo
      actions:
        - pull_descriptions
        - pull_tags
        - pull_owners
        - pull_lineage
        
    - step: llm_inference
      model: gpt-4o
      prompts:
        entity_inference: |
          Given table name "{table_name}" and columns {columns},
          suggest a business entity name and description.
        relationship_inference: |
          Given foreign key from {source_table}.{source_col} to {target_table}.{target_col},
          describe the business relationship.
        taxonomy_inference: |
          Given lookup table "{table_name}" with values {sample_values},
          suggest a taxonomy name and hierarchy.
          
    - step: candidate_generation
      output_format: cogentiq_ontology_model
      confidence_threshold: 0.6
      
  # Output
  output:
    candidates:
      entities: []
      relationships: []
      taxonomies: []
    quality_report:
      completeness_score: 0.85
      confidence_distribution: {}
```

### 9.2.3 SME Interview Agent

```yaml
InterviewAgent:
  id: "ontology.interview_agent"
  version: "1.0.0"
  
  # Configuration
  config:
    model: gpt-4o
    session_duration_minutes: 45
    auto_transcription: true
    real_time_extraction: true
    
  # Interview structure
  interview_structure:
    phases:
      - phase: domain_overview
        duration_minutes: 10
        objectives:
          - Understand SME's role and expertise
          - Identify key business processes
          - Map domain boundaries
        sample_questions:
          - "Walk me through your typical day working with claims."
          - "What are the most important things you track?"
          - "Who else is involved in this process?"
          
      - phase: entity_elicitation
        duration_minutes: 15
        objectives:
          - Identify core business objects
          - Understand entity attributes
          - Capture business definitions
        sample_questions:
          - "What is a claim in your context?"
          - "What information do you capture about each claim?"
          - "How do you categorize different types of claims?"
          
      - phase: relationship_mapping
        duration_minutes: 10
        objectives:
          - Understand entity connections
          - Capture cardinality
          - Identify key constraints
        sample_questions:
          - "How does a claim relate to a policy?"
          - "Can a member have multiple active policies?"
          - "What determines which provider handles a claim?"
          
      - phase: rule_extraction
        duration_minutes: 10
        objectives:
          - Capture business rules
          - Identify edge cases
          - Document exceptions
        sample_questions:
          - "What makes a claim require manual review?"
          - "Are there any claims that get auto-approved?"
          - "What happens if the policy has lapsed?"
          
  # Real-time extraction
  extraction:
    entity_pattern: |
      When SME mentions a business object, extract:
      - Name (singular, PascalCase)
      - Description (in SME's words)
      - Key attributes mentioned
      
    relationship_pattern: |
      When SME describes how things connect, extract:
      - Source entity
      - Relationship verb
      - Target entity
      - Cardinality (1:1, 1:N, N:N)
      
    rule_pattern: |
      When SME describes conditions or logic, extract:
      - Rule name
      - Condition (as pseudo-code)
      - Action or outcome
      
  # Validation
  validation:
    end_of_session_summary: true
    sme_confirmation_required: true
    followup_questions_generated: true
```

## 9.3 Workbench UI

### 9.3.1 Review Interface ("GitHub PR for Business Logic")

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  ONTOLOGY WORKBENCH - Review Candidate: Claim Entity                        │
│  ═══════════════════════════════════════════════════════════════════════════│
│                                                                             │
│  ┌─────────────────────────────────┐  ┌─────────────────────────────────┐  │
│  │         ORIGINAL SOURCE         │  │        PROPOSED DEFINITION       │  │
│  │         (SQL Schema)            │  │        (Ontology YAML)          │  │
│  ├─────────────────────────────────┤  ├─────────────────────────────────┤  │
│  │                                 │  │                                 │  │
│  │  CREATE TABLE TBL_CLM_HDR (     │  │  entity:                        │  │
│  │    CLM_ID VARCHAR(20) PK,       │  │    name: Claim                  │  │
│  │    CLM_STAT_CD VARCHAR(2),      │  │    description: "A request for  │  │
│  │    TOT_BILLED_AMT DECIMAL(12,2),│  │      payment submitted by a     │  │
│  │    MBR_ID VARCHAR(20) FK,       │  │      member or provider"        │  │
│  │    PROV_ID VARCHAR(20) FK,      │  │                                 │  │
│  │    SVC_DT DATE,                 │  │    attributes:                  │  │
│  │    ...                          │  │      - name: claim_id           │  │
│  │  );                             │  │        type: string             │  │
│  │                                 │  │        primary_key: true        │  │
│  │  -- From Alation:               │  │                                 │  │
│  │  -- "Main claims header table"  │  │      - name: status             │  │
│  │  -- Owner: claims-team          │  │        type: ClaimStatusTaxonomy│  │
│  │                                 │  │        description: "Current    │  │
│  │                                 │  │          processing status"     │  │
│  │                                 │  │                                 │  │
│  │                                 │  │      - name: total_billed_amount│  │
│  │                                 │  │        type: currency_usd       │  │
│  │                                 │  │        description: "Total      │  │
│  │                                 │  │          amount billed by       │  │
│  │                                 │  │          provider"              │  │
│  │                                 │  │                                 │  │
│  │                                 │  │    relationships:               │  │
│  │                                 │  │      - name: submitted_by       │  │
│  │                                 │  │        target: Member           │  │
│  │                                 │  │        cardinality: N:1         │  │
│  │                                 │  │                                 │  │
│  └─────────────────────────────────┘  └─────────────────────────────────┘  │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  EXTRACTION DETAILS                                                  │   │
│  │  ─────────────────────────────────────────────────────────────────  │   │
│  │  Sources:                                                           │   │
│  │    • Schema: snowflake://claims_dw/claims/tbl_clm_hdr               │   │
│  │    • Metadata: alation://datasets/12345                             │   │
│  │    • Interview: SME session with J. Smith (2025-01-15)              │   │
│  │                                                                      │   │
│  │  Confidence: 0.87                                                   │   │
│  │  Conflicts: None detected                                           │   │
│  │  Similar existing: None                                             │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  REVIEW ACTIONS                                                      │   │
│  │                                                                      │   │
│  │  [✓ Approve]  [✗ Reject]  [✎ Edit]  [💬 Request Changes]           │   │
│  │                                                                      │   │
│  │  Comments:                                                          │   │
│  │  ┌───────────────────────────────────────────────────────────────┐ │   │
│  │  │ Add a comment...                                               │ │   │
│  │  └───────────────────────────────────────────────────────────────┘ │   │
│  │                                                                      │   │
│  │  Assigned Reviewers: @jane-domain-lead, @bob-sme                    │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

## 9.4 Cogentiq Ontology Model (COM) Format

### 9.4.1 JSON-LD Based Storage

```json
{
  "@context": {
    "com": "https://cogentiq.ai/ontology/v1/",
    "xsd": "http://www.w3.org/2001/XMLSchema#",
    "rdfs": "http://www.w3.org/2000/01/rdf-schema#"
  },
  "@graph": [
    {
      "@id": "com:insurance/Claim",
      "@type": "com:Entity",
      "com:name": "Claim",
      "com:description": "A request for payment submitted by a member or provider for covered services",
      "com:domain": "com:domains/Insurance",
      "com:version": "2.3.0",
      "com:attributes": [
        {
          "@id": "com:insurance/Claim/claim_id",
          "@type": "com:Attribute",
          "com:name": "claim_id",
          "com:dataType": "xsd:string",
          "com:isPrimaryKey": true,
          "com:dataBinding": {
            "com:source": "snowflake://claims_dw/claims/tbl_clm_hdr",
            "com:column": "CLM_ID"
          }
        },
        {
          "@id": "com:insurance/Claim/total_billed_amount",
          "@type": "com:Attribute",
          "com:name": "total_billed_amount",
          "com:dataType": "xsd:decimal",
          "com:semanticType": "com:types/CurrencyUSD",
          "com:description": "Total amount billed by provider before adjustments"
        }
      ],
      "com:lineage": {
        "com:extractedFrom": [
          {"@id": "com:sources/snowflake_claims_schema", "com:method": "schema_crawler"},
          {"@id": "com:sources/interview_jsmith_20250115", "com:method": "sme_interview"}
        ]
      }
    }
  ]
}
```

### 9.4.2 Export Targets

| Target Format | Use Case |
|---------------|----------|
| **Azure Foundry Ontology** | Native Foundry deployment |
| **GraphQL Schema** | Agent query interface |
| **dbt Semantic Layer** | BI tool integration |
| **OWL/RDF** | Standards compliance |
| **OpenAPI Spec** | Auto-generate APIs |
| **Markdown Docs** | Human documentation |
| **Agent Context** | System prompt injection |

---

# 10. NEURO-SYMBOLIC ROUTER

*(Full specification as previously detailed)*

## 10.1 Execution Paths Summary

| Path | Confidence | Characteristics |
|------|------------|-----------------|
| **Symbolic** | ≥ 0.85 | Deterministic, no LLM in calculation |
| **Hybrid** | 0.50-0.85 | Calculation symbolic, interpretation neural |
| **Neural** | < 0.50 | Full LLM reasoning |
| **Clarification** | Ambiguous | Ask user to disambiguate |

## 10.2 Path Selection Algorithm

```python
def select_path(query, intent, entity_matches, context):
    symbolic_confidence = calculate_symbolic_confidence(
        intent, entity_matches, context
    )
    
    if symbolic_confidence >= 0.85:
        return Path.SYMBOLIC
    elif symbolic_confidence >= 0.50:
        return Path.HYBRID
    elif needs_clarification(entity_matches):
        return Path.CLARIFICATION
    else:
        return Path.NEURAL
```

---

# 11. SEMANTIC CATALOG & CONSTRAINT ENGINE

*(Full specifications as previously detailed)*

---

# 12. LEGACY LOGIC INGESTION MODULE

## 12.1 Supported Source Types

| Source | Parser | Confidence |
|--------|--------|------------|
| SQL Views | SQLGlot | High |
| Stored Procedures | SQLGlot + AST | Medium-High |
| dbt Models | Custom | High |
| Excel Formulas | openpyxl | Medium |
| Python Scripts | AST | Medium |
| SAP ABAP | Custom | Low-Medium |

## 12.2 Extraction Pipeline

*(6-phase pipeline as previously detailed)*

---

# 13. DATA MODELS & SCHEMAS

## 13.1 Core Database Schema

```sql
-- Tenant Management
CREATE TABLE tenants (
    tenant_id UUID PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    settings JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Ontology Registry
CREATE TABLE namespaces (
    namespace_id UUID PRIMARY KEY,
    tenant_id UUID REFERENCES tenants(tenant_id),
    name VARCHAR(255) NOT NULL,
    parent_namespace_id UUID REFERENCES namespaces(namespace_id),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(tenant_id, name)
);

CREATE TABLE ontology_classes (
    class_id UUID PRIMARY KEY,
    namespace_id UUID REFERENCES namespaces(namespace_id),
    name VARCHAR(255) NOT NULL,
    version VARCHAR(50) NOT NULL,
    definition JSONB NOT NULL,
    status VARCHAR(50) DEFAULT 'draft',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    created_by VARCHAR(255),
    UNIQUE(namespace_id, name, version)
);

-- Semantic Catalog
CREATE TABLE metrics (
    metric_id UUID PRIMARY KEY,
    namespace_id UUID REFERENCES namespaces(namespace_id),
    name VARCHAR(255) NOT NULL,
    version VARCHAR(50) NOT NULL,
    definition JSONB NOT NULL,
    status VARCHAR(50) DEFAULT 'draft',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(namespace_id, name, version)
);

CREATE TABLE dimensions (
    dimension_id UUID PRIMARY KEY,
    namespace_id UUID REFERENCES namespaces(namespace_id),
    name VARCHAR(255) NOT NULL,
    version VARCHAR(50) NOT NULL,
    definition JSONB NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Constraints
CREATE TABLE constraints (
    constraint_id UUID PRIMARY KEY,
    namespace_id UUID REFERENCES namespaces(namespace_id),
    name VARCHAR(255) NOT NULL,
    expression TEXT NOT NULL,
    evaluation_point VARCHAR(50) NOT NULL,
    severity VARCHAR(50) NOT NULL,
    action VARCHAR(50) NOT NULL,
    enabled BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Entity Resolution
CREATE TABLE aliases (
    alias_id UUID PRIMARY KEY,
    entity_type VARCHAR(50) NOT NULL,
    entity_id UUID NOT NULL,
    alias VARCHAR(500) NOT NULL,
    tenant_id UUID REFERENCES tenants(tenant_id),
    created_at TIMESTAMPTZ DEFAULT NOW()
);
CREATE INDEX idx_aliases_lookup ON aliases(tenant_id, LOWER(alias));

-- Sessions
CREATE TABLE sessions (
    session_id UUID PRIMARY KEY,
    tenant_id UUID REFERENCES tenants(tenant_id),
    user_id VARCHAR(255) NOT NULL,
    context JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    last_activity TIMESTAMPTZ DEFAULT NOW()
);

-- Agents
CREATE TABLE agents (
    agent_id UUID PRIMARY KEY,
    namespace_id UUID REFERENCES namespaces(namespace_id),
    name VARCHAR(255) NOT NULL,
    version VARCHAR(50) NOT NULL,
    specification JSONB NOT NULL,
    status VARCHAR(50) DEFAULT 'draft',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Routing Decisions
CREATE TABLE routing_decisions (
    decision_id UUID PRIMARY KEY,
    session_id UUID REFERENCES sessions(session_id),
    query_text TEXT NOT NULL,
    intent_category VARCHAR(50) NOT NULL,
    selected_path VARCHAR(20) NOT NULL,
    symbolic_confidence DECIMAL(4,3) NOT NULL,
    decision_record JSONB NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Lineage
CREATE TABLE lineage_records (
    lineage_id UUID PRIMARY KEY,
    output_id UUID NOT NULL,
    session_id UUID REFERENCES sessions(session_id),
    tenant_id UUID REFERENCES tenants(tenant_id),
    record JSONB NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Audit
CREATE TABLE audit_log (
    audit_id UUID PRIMARY KEY,
    tenant_id UUID REFERENCES tenants(tenant_id),
    user_id VARCHAR(255),
    action_type VARCHAR(100) NOT NULL,
    resource_type VARCHAR(100),
    resource_id UUID,
    details JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
```

---

# 14. API SPECIFICATIONS

## 14.1 REST API Overview

```yaml
# Base URL: https://api.cogentiq.ai/v1

# Authentication
security:
  - bearerAuth: []
  - apiKey: []

# Endpoints

# Ontology
/ontology/classes:
  GET: List classes
  POST: Create class

/ontology/classes/{id}:
  GET: Get class
  PUT: Update class
  DELETE: Delete class

# Semantic
/semantic/metrics:
  GET: List metrics
  POST: Create metric

/semantic/metrics/{id}/calculate:
  POST: Execute metric calculation

# Agents
/agents:
  GET: List agents
  POST: Create agent

/agents/{id}/deploy:
  POST: Deploy agent to target platform

/agents/{id}/test:
  POST: Run agent test suite

# Router
/router/analyze:
  POST: Analyze query and select path

/router/execute:
  POST: Execute query via selected path

# Sessions
/sessions:
  POST: Create session

/sessions/{id}/context:
  GET: Get context
  PATCH: Update context

# Lineage
/lineage/{outputId}:
  GET: Get lineage record

# Knowledge Registry
/registry/packs:
  GET: List domain packs
  POST: Import pack

/registry/prompts:
  GET: List prompts
  POST: Create prompt
```

---

# 15. SECURITY & GOVERNANCE

## 15.1 Authentication

- **Primary**: OAuth2 / OIDC (Azure AD, Okta)
- **Service-to-Service**: API Keys with rotation
- **SSO**: SAML 2.0

## 15.2 Authorization (RBAC + ABAC)

| Role | Permissions |
|------|-------------|
| Platform Admin | Full access |
| Tenant Admin | Full tenant access |
| Domain Engineer | Create/edit ontologies |
| Agent Developer | Create/edit agents |
| Analyst | Query, read-only |

## 15.3 Data Protection

- Encryption at rest (AES-256)
- Encryption in transit (TLS 1.3)
- PII/PHI masking
- Row-level security pass-through

---

# 16. DOMAIN TEMPLATES

## 16.1 Available Packs

| Pack | Entities | Metrics | Status |
|------|----------|---------|--------|
| **Insurance (P&C)** | 47 | 89 | Production |
| **Insurance (Life)** | 38 | 72 | Production |
| **CPG** | 52 | 94 | Production |
| **Healthcare Provider** | 61 | 103 | Production |
| **Healthcare Payer** | 55 | 87 | Beta |
| **Financial Services** | 44 | 78 | Beta |

---

# 17. DEPLOYMENT ARCHITECTURE

## 17.1 Kubernetes Deployment

```yaml
# High-level deployment
services:
  api-gateway:
    replicas: 3
    resources: {cpu: 1, memory: 2Gi}
    
  router-service:
    replicas: 5
    resources: {cpu: 2, memory: 4Gi}
    hpa: {min: 3, max: 20}
    
  ontology-service:
    replicas: 3
    resources: {cpu: 1, memory: 2Gi}
    
  semantic-service:
    replicas: 5
    resources: {cpu: 2, memory: 4Gi}
    
  agent-runtime:
    replicas: 10
    resources: {cpu: 4, memory: 8Gi}
    hpa: {min: 5, max: 50}

databases:
  postgresql:
    mode: primary + 2 replicas
    storage: 500GB
    
  neo4j:
    mode: cluster (3 nodes)
    storage: 200GB
    
  redis:
    mode: cluster (6 nodes)
    memory: 48GB total
    
  clickhouse:
    mode: cluster (3 shards, 2 replicas)
    storage: 2TB per shard
```

## 17.2 Deployment Options

| Option | Description |
|--------|-------------|
| **SaaS Multi-tenant** | Shared infrastructure |
| **Dedicated Tenant** | Isolated compute |
| **Customer VPC** | Full customer deployment |
| **Hybrid** | Control plane SaaS, data plane customer |

---

# 18. NON-FUNCTIONAL REQUIREMENTS

## 18.1 Performance

| Metric | Target |
|--------|--------|
| Router decision | < 200ms p95 |
| Symbolic query | < 500ms p95 |
| Agent response | < 5s p95 |
| Throughput | 1000 req/sec/tenant |

## 18.2 Availability

| Metric | Target |
|--------|--------|
| Uptime | 99.9% |
| RTO | < 4 hours |
| RPO | < 1 hour |

---

# 19. TESTING STRATEGY

## 19.1 Test Categories

| Category | Coverage Target |
|----------|-----------------|
| Unit Tests | 80% |
| Integration Tests | 70% |
| Semantic Accuracy | 90%+ |
| Agent Test Suites | 85%+ |

## 19.2 Golden Datasets

- 500+ queries per domain pack
- Expected intents, entities, paths, results
- Automated regression on every deployment

---

# 20. ROLLOUT PLAN

## Phase 1: Foundation (Weeks 1-8)

- Ontology Registry + Workbench
- Schema Crawler + LLM Extractor
- Insurance domain pack (v1)

## Phase 2: Reasoning (Weeks 9-16)

- Neuro-Symbolic Router
- Semantic Catalog + Constraint Engine
- Azure Foundry transpiler

## Phase 3: Platform (Weeks 17-24)

- Agent Development Kit
- Knowledge Registry
- Native runtime (K8s + LangGraph)
- Bedrock transpiler

## Phase 4: Scale (Weeks 25-32)

- Multi-tenancy
- Additional domain packs
- Enterprise governance
- GA release

---

# 21. APPENDICES

## Appendix A: Glossary

| Term | Definition |
|------|------------|
| **COM** |  Ontology Model - JSON-LD based format |
| **CAS** | Cogentiq Agent Specification - YAML agent definition |
| **ADK** | Agent Development Kit |
| **NSR** | Neuro-Symbolic Router |
| **DIL** | Domain Intelligence Layer |

## Appendix B: Technology Stack Summary

| Component | Technology |
|-----------|------------|
| API | Python FastAPI |
| Primary DB | PostgreSQL |
| Graph DB | Neo4j |
| Cache | Redis |
| Lineage | ClickHouse |
| Rule Engine | CEL |
| ML | OpenAI GPT-4o, Claude 3 |

## Appendix C: References

- Azure AI Foundry Documentation
- AWS Bedrock Agent Documentation
- Model Context Protocol Specification
- CEL Language Specification

---

**Document Control**

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | Jan 2026 | Platform Team | Initial draft |
| 2.0.0 | Jan 2026 | Platform Team | Added Neuro-Symbolic Router |
| 3.0.0 | Jan 2026 | Platform Team | Complete platform spec with transpiler |

---

*End of Document*