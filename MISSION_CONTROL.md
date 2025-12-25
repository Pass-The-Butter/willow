# 🚀 Willow Mission Control

**"The Graph is the Memory. The Code is the Will."**

This document serves as the central dashboard for the Willow project. All resources, links, and status indicators are aggregated here.

## 🔗 Critical Resources

| Resource | Link | Description |
| :--- | :--- | :--- |
| **GitHub Repo** | [Pass-The-Butter/willow](https://github.com/Pass-The-Butter/willow) | Source Code & Version Control |
| **Jira Board** | [Agile Meshnet Board](https://agilemeshnet.atlassian.net/jira/software/projects/SCRUM/boards/1) | Task Management & Kanban |
| **Confluence** | [Agile Meshnet Wiki](https://agilemeshnet.atlassian.net/wiki) | Documentation & Specifications |
| **AuraDB Console** | [Neo4j Aura](https://console.neo4j.io) | The Brain (Graph Database) |
| **Bunny (Vault)** | `ssh user@bunny` | Postgres Database (Population) |
| **Frank (Muscle)** | `ssh peter@frank` | Inference & Generation Node |

---

## 🎯 Current Sprint Objectives

1.  **Sync Resources**: Establish this Mission Control and ensure all nodes (Mac, Frank, Bunny) are code-synced.
2.  **Ignite Population**: Frank runs `remote_generator.py` to populate Postgres on Bunny.
3.  **Hello World**: Display a "Customer Quote" from the generated data to prove the pipeline.
4.  **Ontology Building**: Map the generated data concepts into the Neo4j Graph.

---

## 🧠 Development Philosophy

**The "Just Enough Context" Principle**
> An agent should be able to read the high-level plan, traverse the graph to a specific function, and have *just enough* information in its context window to complete a task.

*   **Don't** load the whole codebase.
*   **Do** read `MISSION_CONTROL.md` -> Query Graph for Task -> Read specific file -> Execute.

---

## 🛠 System Status

| Node | Role | Status | Notes |
| :--- | :--- | :--- | :--- |
| **Mac Mini** | Architect | 🟢 Online | Control Plane Active |
| **Frank** | Generator | 🟡 Standby | Needs to run `run_on_frank.ps1` |
| **Bunny** | Database | 🟢 Online | Postgres Ready |
| **AuraDB** | Memory | 🟢 Online | Architecture Memorized |

---

## 📝 Notes for Next Agent

*   **Priorities**:
    1.  Verify Frank is generating data (check Postgres counts).
    2.  Run `core/skills/hello_willow.py` to demonstrate success.
    3.  Begin mapping Postgres schema to Neo4j Ontology (Ingestion).
*   **Context**:
    *   We are using a **GraphRAG** approach.
    *   Infrastructure is distributed (Mac/Win/Linux).
    *   Use `bootstrap/` scripts for environment changes.
