# 📋 Task List: Centralized Command Center & Autogen Orchestration

**Objective**: Consolidate all web-based interfaces onto `bunny` (exposed via Tailscale), create a unified Table of Contents, implement an interactive Organogram visualization, and integrate Linear for project management.
**Status Update**: We have "landed" the infrastructure; now implementing the formal verification routine ("Landing the Plane") and setting up Autogen.

- [/] **Phase 1: Centralized Web Server (Bunny)** <!-- id: 1 -->

  - [x] Stop local Flask instance on Mac. <!-- id: 2 -->
  - [x] Deploy `domains/interface/app.py` to `bunny` (Docker or Systemd). <!-- id: 3 -->
  - [x] Configure `nginx` or `caddy` on `bunny` as a reverse proxy (single entry point). <!-- id: 4 -->
  - [x] Create a root `index.html` (Table of Contents) linking to: <!-- id: 5 -->
    - Dashboard (`/board`)
    - Memory Report (`/report/memory`)
    - API Docs
    - Organogram
  - [x] Verify access via `http://bunny` (Tailscale). <!-- id: 6 -->

- [/] **Phase 2: Visual Organogram** <!-- id: 7 -->

  - [x] Research D3.js or GoJS for hierarchical/network visualization. <!-- id: 8 -->
  - [x] Create a new endpoint `/organogram` JSON API in Flask. <!-- id: 9 -->
  - [x] Build the frontend view (`organogram.html`) to render the `(:Domain)-[:HAS_COMPONENT]->(:Task)` graph. <!-- id: 10 -->

- [x] **Phase 3: Linear Integration & Visual Kanban** <!-- id: 11 -->

  - [x] Enhance `core/skills/sync_linear.py` for robust bidirectional sync. <!-- id: 12 -->
  - [x] Create `core/skills/sync_brain_tasks.py` to keep AuraDB in sync with repo. <!-- id: 14 -->
  - [x] Implement Visual Kanban Board (`/kanban`) in Flask Dashboard. <!-- id: 20 -->
  - [x] Upgrade `core/agents/project_manager.py` to automate all syncs. <!-- id: 13 -->

- [x] **Phase 4: Landing the Plane (Verification)** <!-- id: 15 -->

  - [x] Implement `core/skills/land_the_plane.py` (Beads-style check).
  - [x] Verify connectivity (Ping).
  - [x] Verify Services (Docker PS).
  - [x] Verify System Consistency (DBs).
  - [x] Verify Memory Flush (Log/Graph) (404 confirmed service active).

- [x] **Phase 5: Agent Orchestration (Autogen)** <!-- id: 16 -->

  - [x] Set up `pyautogen` environment (Library installed, used custom Agent wrapper).
  - [x] Create `core/agents/flight_controller.py` (Custom Agent).
  - [x] Connect Flight Controller to `land_the_plane` skill.
  - [x] Test modular remote execution.

- [x] **Phase 6: Willow Sidebar (Astro Starlight)** <!-- id: 17 -->

  - [x] Initialize Starlight project in `domains/sidebar`. <!-- id: 19 -->
  - [x] Configure `starlight` sidebar with vertical taxonomy (Network, Nodes, Memory, Artifacts).
  - [x] Deploy to `bunny` and configure Nginx.
  - [x] Create automated report posting (integrated into `land_the_plane.py`).

- [x] **Phase 7: Modularise & Store Verification** <!-- id: 18 -->

  - [x] Integrate MongoDB Artifact Store for backups.
  - [x] Verify automated reporting from `flight_controller.py` to Starlight.

- [/] **Phase 8: Security & Governance** <!-- id: 19 -->

  - [x] Perform initial Security Audit (Captain Willow).
  - [x] Create `core/skills/security_audit.py` for automated scanning.
  - [x] Implement Drift Detection & Repair (`detect_drift.py`, `repair_drift.py`).
  - [x] Ingest `Willow_Graph_Gateway_Policy_2026.yaml`.
  - [x] Remediate hardcoded credentials (deploy_bunny.py).

- [/] **Phase 9: Graph Gateway & Security** <!-- id: 20 -->

  - [x] Create `domains/gateway` service and policy.
  - [x] Create `core/clients/graph_client.py`.
  - [x] Verify Gateway locally (`verify_gateway.py`).
  - [ ] Deploy Gateway to `bunny` and verify health. (BLOCKED: Network Unreachable)
  - [x] Migrate Agents to use `GraphClient`.
    - [x] Project Manager Agent
    - [/] Feature Agent (Code updated, verification blocked by missing task data)
  - [x] Deprecate direct Neo4j access for Agents (Code updated).

- [x] **Maintenance: Jira Configuration Update** <!-- id: 21 -->

  - [x] Verify new Project Key for "Willow". <!-- id: 22 -->
  - [x] Update `bootstrap/sync_atlassian.py` with correct key. <!-- id: 23 -->

- [x] **Maintenance: Linear Configuration Update** <!-- id: 24 -->

  - [x] Rewrite `core/skills/sync_linear.py` for 'Architect' protocol. <!-- id: 25 -->
  - [x] Verify Linear hierarchy (Phases -> Projects). <!-- id: 26 -->
  - [x] Create unified `core/skills/sync_project_management.py` skill. <!-- id: 27 -->

- [/] **Phase 10: Business Ontology Construction** <!-- id: 28 -->

  - [x] Analysis of Claims Story & Ontology Vision (See `domains/claims/ontology_vision.md`) <!-- id: 29 -->
  - [x] Implement Ontology Schema (Cypher) (`schemas/business_ontology.cypher`) <!-- id: 30 -->
  - [x] Verify Ontology with Jane Winterbottom Story (`schemas/verify_business_ontology.py`) <!-- id: 31 -->
  - [x] Diarise Request & Vision <!-- id: 32 -->

- [/] **Phase 11: Insurance Factory Visualization** <!-- id: 33 -->
  - [x] Plan Scrollytelling Experience (GSAP) <!-- id: 34 -->
  - [x] Implement `/factory` endpoint in Flask <!-- id: 35 -->
  - [x] Create `factory.html` with GSAP animations <!-- id: 36 -->
  - [ ] Verify accessibility and flow <!-- id: 37 -->

- [ ] **Phase 12: Deep Research Agent** <!-- id: 38 -->
  - [ ] Get Gemini API key from AI Studio <!-- id: 39 -->
  - [ ] Get Brave Search API key (free tier) <!-- id: 40 -->
  - [ ] Deploy AuraDB schema (`bootstrap/deploy_research_schema.py`) <!-- id: 41 -->
  - [ ] Create N8N workflow (`bootstrap/deep_research_workflow.json`) <!-- id: 42 -->
    - [ ] Telegram trigger node
    - [ ] Groq intent classifier
    - [ ] Brave Search integration
    - [ ] Semantic Scholar integration
    - [ ] arXiv integration
    - [ ] Gemini synthesis node
    - [ ] AuraDB write nodes
    - [ ] Telegram notification
  - [ ] Test with sample query: "AI Agent Memory Architectures" <!-- id: 43 -->
  - [ ] Verify < $5/month running costs <!-- id: 44 -->
  - **Spec**: `docs/specs/DEEP_RESEARCH_AGENT_SPEC.md`
  - **Plan**: `.github/prompts/plan-deepResearchAgent.prompt.md`
