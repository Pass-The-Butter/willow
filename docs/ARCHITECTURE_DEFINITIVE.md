# Willow Architecture & Role Definition

> **"The Graph is the Memory."**

This document defines the definitive architecture for the Willow system. This state is mirrored in the AuraDB Knowledge Graph.

## 1. The Brain: AuraDB (Cloud)
*   **Role**: Central Memory, Ontology, and "Source of Truth" for the Agent's understanding of the world.
*   **Content**:
    *   **Ontology**: The schema of concepts (Person, Task, Skill).
    *   **Context**: The state of the infrastructure (this document).
    *   **Memory**: Logs of decisions, ideas, and project history.

## 2. The Vault: Bunny (Xeon Server)
*   **Hardware**: Xeon CPU, 128GB RAM, Ubuntu.
*   **Role**: Heavy Storage & Orchestration.
*   **Services**:
    *   **Postgres**: Stores the 100M Population entities (The "Body").
    *   **N8N** (Planned): Orchestration of AI workflows.
    *   **Docker**: Container host.

## 3. The Muscle: Frank (Windows 11 PC)
*   **Hardware**: Consumer PC, GPU (assumed).
*   **Role**: Inference & Generation.
*   **Services**:
    *   **Ollama**: LLM Inference API (Port 11434).
    *   **Python Scripts**: Running `remote_generator.py` to create population data.
    *   **OpenSSH**: Remote access point.

## 4. The Architect: Mac Mini (Local)
*   **Role**: Development, Control Plane, Git Origin.
*   **Action**: Where code is written and commands are issued.

## 5. The Fabric: Tailscale
*   **Role**: Secure Mesh Network connecting Mac, Bunny, and Frank.
*   **DNS**: `bunny`, `frank`.

---u

## Agent Memory Strategy (GraphRAG)
Willow utilizes a **GraphRAG (Graph Retrieval Augmented Generation)** approach.
*   **Structured Memory**: Nodes and Relationships in AuraDB (e.g., `(:Task)-[:BLOCKED_BY]->(:Issue)`).
*   **Unstructured Memory**: Vector embeddings of text chunks stored as properties on nodes, allowing for semantic search ("fuzzy recall") combined with precise graph traversal.
*   **Vector Index**: `willow_memory` (768 dimensions) on `(:Memory)` nodes.

## Tooling Decisions
*   **Orchestration**: N8N (Visual, Self-Hosted).
*   **Inference**: Hybrid.
    *   **Frank**: Ollama running `deepseek-r1:32b` (Reasoning) and `qwen2.5-coder:32b` (Coding).
    *   **Cloud**: OpenAI (Optional fallback).
