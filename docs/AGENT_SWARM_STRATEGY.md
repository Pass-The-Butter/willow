# 🐝 Willow Agent Swarm Strategy

> **"A swarm of clever agents doing stuff in their own little agentic offices."**

This document outlines the strategy for evolving Willow from a single-agent system into a multi-agent swarm, managed by a dedicated Project Manager Agent.

## 1. The Project Manager Agent ("The Boss")
*   **Role**: Orchestration, Prioritization, and "Keeping the Vision".
*   **Responsibilities**:
    *   Reads `MISSION_CONTROL.md` and the Jira Board.
    *   Breaks down Epics into Tasks.
    *   Assigns tasks to specialized agents (Dev, QA, Research).
    *   **Crucial**: Maintains the "Golden Thread" of context (The Graph).

## 2. The Swarm Architecture
We will use a **Hub-and-Spoke** model, anchored by the Graph.

*   **Hub**: AuraDB (The Shared Memory).
*   **Spokes (Agents)**:
    *   **Arch-Willow**: System Architect (Infrastructure, Ontology).
    *   **Dev-Willow**: Code implementation (Python, SQL, React).
    *   **Research-Willow**: Deep dives (e.g., "Agentic Memory Patterns").
    *   **Frank-Willow**: The Muscle (Population Generation).

## 3. Agentic Memory (The "File Cabinet")
As per our research into **GraphRAG**:
*   **Shared Context**: Agents do NOT pass huge context windows to each other.
*   **The Handoff**:
    1.  Agent A finishes a task.
    2.  Agent A logs the result (Decision/Code/Insight) to a Node in AuraDB.
    3.  Agent A notifies the PM.
    4.  PM assigns Agent B.
    5.  Agent B queries AuraDB for the specific context needed.

## 4. Implementation Plan & Tooling

### A. The Framework: N8N (Not CrewAI)
We have chosen **N8N** (running on Bunny) as our orchestration layer instead of code-heavy frameworks like CrewAI.
*   **Why?**: N8N provides a visual "Office" where we can see data moving between agents. It has native nodes for Postgres, Neo4j, and HTTP Requests (to Ollama).
*   **Cost**: Free (Self-Hosted).

### B. The Brains: Hybrid Inference
*   **Tier 1 (The Workers)**: **Ollama on Frank** (Free).
    *   Used for: Population generation, summarization, data formatting.
    *   Cost: $0.
*   **Tier 2 (The Boss)**: **OpenAI / Anthropic** (Paid - Optional).
    *   Used for: Complex project planning, conflict resolution.
    *   Cost: Pay-per-token. *We can start without this and only add it if Frank isn't smart enough.*

### C. Execution Steps
1.  **Define Agent Roles in Graph**: Create `(:Agent)` nodes in Neo4j.
2.  **Task Queues**: Use Jira or a Graph-based queue (`(:Task {status: 'Ready'})`).
3.  **Orchestrator**: Use **N8N** (on Bunny) to trigger agents based on graph events.

## 5. Current Status
*   **Research**: "GraphRAG" pattern confirmed.
*   **Infrastructure**: Distributed nodes (Mac, Frank, Bunny) ready.
*   **Next Step**: Build the "Project Manager" workflow in N8N.
