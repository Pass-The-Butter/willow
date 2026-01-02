# Willow: Strategic Overview & System Architecture

**Version**: 2025-12-28
**Mission**: Autonomous Living Ontology for Insurance

---

## 1. Executive Summary

Willow is a **cloud-agnostic, agent-driven AI system** operating on a decentralized swarm architecture. Its primary goal is to simulate a functioning insurance ecosystem ("The Population") underpinned by a living knowledge graph ("The Brain").

Unlike traditional apps, Willow is designed to be **autonomous**. Agents (Meeseeks Squad) wake up, read the `BIOS`, understand their role from the ontology, perform work (Research -> Plan -> Execute -> Verify), and log their actions back to the Brain.

**Current Strategic Focus**: Aligning the synthetic population with the **Purely Pets Insurance** product model to enable realistic customer journey simulations.

---

## 2. Infrastructure: The Cloud-Agnostic Swarm

The system runs on a **Tailscale Mesh**, allowing seamless communication between disparate hardware as if they were on a single LAN.

| Node       | Role                       | Hardware                | Key Services                                                       |
| ---------- | -------------------------- | ----------------------- | ------------------------------------------------------------------ |
| **Bunny**  | **Runtime & Population**   | Xeon Server (128GB RAM) | Docker Swarm (Dashboard, N8N, API), Postgres (100M NPCs), Graphiti |
| **Frank**  | **Inference & Simulation** | Win 11 + RTX 3090Ti     | Local LLM Inference (Ollama/VLLM), 3D Rendering (Unreal - Planned) |
| **AuraDB** | **The Brain**              | Neo4j Cloud             | Knowledge Graph, Ontology, Epidsodic Memory, Skills Registry       |
| **Mac**    | **Controller**             | Mac Mini M4             | Development Controller, Codebase Source of Truth                   |

**Universal Access (Tailscale Funnel)**:

All resources both local and cloud are abstracted via Tailscale Overlay VPN, allowing seamless access to any resource from any node.

---

## 3. Core Components

### A. The Brain (Neo4j AuraDB)

The central nervous system. It stores:

- **Ontology**: Definitions of "Person", "Pet", "Policy", "Claim" and their relationships.
- **Skills**: Executable code capabilities (`manage_memory`, `run_query`) stored as nodes.

### B. Memory Architecture (The "Three Pillars")

Willow uses a composite memory system to maintain state and context across sessions.

| Pillar          | Tech                        | Purpose                                                                                                                                                                            | Python Tool                          |
| --------------- | --------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------ |
| **1. Episodic** | Neo4j (`:Session`, `:Turn`) | **"What did we say?"**<br>Logs every conversation turn, user request, and agent response. Links back to the specific task (Bead) being worked on.                                  | `core.skills.manage_episodic_memory` |
| **2. Beads**    | Neo4j (`:Bead`)             | **"What am I doing?"**<br>State management graph. Represents Tasks, Epics, and Decisions. A "Bead" is a unit of work that can be picked up by any agent.                           | `core.skills.manage_beads`           |
| **3. Graphiti** | Docker Service (Bunny)      | **"What happened?"**<br>Experiential memory. Stores temporal events and entity interactions (e.g., "Deployed Database", "Fixed Bug") to allow semantic recall of past experiences. | `core.skills.client_graphiti`        |

### C. The Population (Postgres on Bunny)

The "Matter" of the simulation. A massive dataset of synthetic entities.

- **Scale**: Target 100 Million entities.
- **Schema**: Strictly typed relational data (Customers, Pets, Quotes).
- **Tech**: Postgres 15 + `pgvector` for semantic personality search (e.g., "Find me 500 angry dog owners in London").
- **Current Mandate**: Strict adherence to **Purely Pets Insurance** input fields.

### D. The Runtime (Docker on Bunny)

The operational layer where services live.

- **Dashboard**: Flask-based "Single Pane of Glass" for monitoring the system.
- **N8N**: Workflow automation (the "Nervous System") connecting webhooks, Telegram, and internal events.
- **Graphiti**: Experimental "Experiential Memory" service for temporal graph events.

---

## 4. **Agentic Architecture ("The Meeseeks Squad")**

The system allows primarily ephemeral, task-specific agents ("Meeseeks") to perform work and then cease processing.

### A. The Meeseeks Class (`core/agent/meeseeks.py`)

A Python implementation of the "Research -> Plan -> Execute -> Check" loop.

- **Spawn**: Created with a `session_id` and `role`.
- **Research**: Queries Episodic Memory (for context) and Graphiti (for facts).
- **Execute**: Runs tools/code.
- **Check**: Verifies output against success criteria.
- **Land the Plane**: Consolidates memory, updates the Bead graph, and terminates.

### B. Engineering Meeseeks ("The Spider")

An N8N-based agent (`bootstrap/engineering_meeseeks.json`) responsible for system health.

- **Trigger**: Webhook or Daily Schedule.
- **Actions**: Pings Dashboard Pulse, Checks OpenAI API, Verifies DB Connectivity.
- **Output**: Reports status to **Telegram** (as a cheerful/pained Meeseeks).

### C. Agent Lifecycle (BIOS Protocol)

Willow agents follow a strict protocol:

**Key Protocols**:

- **BIOS**: The immutable bootstrap script every agent runs first.
- **Task.md**: The current sprint checklist.
- **Session Handoff**: The baton pass between agent instantiations.

---

## 5. Current Implementation Plan (Session: 2025-12-28)

**Objective**: Fix Data Consistency & Alignment.

1.  **Database Upgrade**: Update `population-db` to `pgvector` enabled image (Bunny).
2.  **Schema Enforcement**: Apply `correct_schema.sql` to enforce Purely Pets structure:
    - `customers` table (Name, Email, Address, DOB, Vector).
    - `pets` table (Species, Breed, Microchip Status).
3.  **Generator Rewrite**: Update `remote_generator.py` to seed this schema using Faker (en_GB) and Ollama (on Frank).
4.  **Verification**: Ensure the "People Viewer" on the Dashboard successfully renders this new data.

---

_Use this overview to orient any new agent to the Willow ecosystem without needing to parse the entire repo._
