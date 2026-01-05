# Neurosymbolic AI Architecture

**"Business Process as Code"**

> [!NOTE]
> This document captures the architectural vision established in Session 2026-01-05. It defines the "Willow Claims Engine" pattern.

## The Core Concept

**"Neurosymbolic AI turns your claims system into a brain with a rulebook — LLMs read the world, graphs understand it, and symbolic logic makes decisions you can actually trust."**

This architecture solves the "Black Box" problem of generative AI by strictly separating **Perception** (Neural) from **Decisioning** (Symbolic).

## The Stack (`The Fire Stack`)

| Component | Technology | Role |
|Data|Technology|Role|
|---|---|---|
| **Orchestration** | **Temporal** | The reliable execution engine. Runs "Playbooks" as versioned code. |
| **Symbolic Brain** | **Neo4j** | The source of truth. Stores rules, decisions, policies, and claim state as a graph. |
| **Neural Perception** | **LLMs** (Claude/OpenAI) | Fact extraction only. Turns documents/text into structured Facts in the graph. |
| **Memory** | **Weaviate/Pinecone** | Semantic search for similar claims and historical patterns. |
| **Event Backbone** | **Redpanda/Kafka** | Time-travel audit log. Every state change is an event. |
| **Interface** | **Streamlit/React** | "Glass Box" visibility into the decision path. |

## The Flow: "Business Process as Code"

1.  **Ingest**: A claim arrives (Email, API, Chat).
2.  **Perception (Neural)**:
    - LLM reads the FNOL (First Notice of Loss).
    - Extracts facts: `Date`, `Amount`, `Cause`, `Parties`.
    - Writes Facts to **Neo4j**.
3.  **Orchestration (Temporal)**:
    - The **Playbook Runner** (Python Worker) wakes up.
    - It reads the `InstantPropertyClaim` playbook (Code).
    - It executes steps sequentially:
      - `check_policy_active(claim_id)`
      - `check_coverage_match(claim_id)`
      - `assess_fraud_risk(claim_id)`
4.  **Decisioning (Symbolic)**:
    - Each step queries the Graph or runs a deterministic rule.
    - **No LLM decides the outcome.** Only code/rules decide.
5.  **Action**:
    - If properties match → Approve & Pay.
    - If not → Escalate to Human.
    - Result marked in Graph as `(:Decision)-[:JUSTIFIED_BY]->(:Reason)`.

## Key Terminology for Sales & Marketing

- **"Business Process as Code"**: Workflows are not drawings; they are executable, testable, versioned software.
- **"Glass Box AI"**: Unlike "Black Box" LLMs, you can see exactly _why_ a decision was made.
- **"The Brain with a Rulebook"**: Neuro (Creative/Reading) + Symbolic (Logical/Compliance).
- **"Memory at Scale"**: Using vectors to find "claims like this one" from millions of history records.

## Why This Wins

- **Auditability**: Regulators love it. Every decision path is traceable.
- **Reliability**: Temporal ensures no claim is ever "lost" in a server crash.
- **Agility**: Changing a rule is just a Git Commit.
