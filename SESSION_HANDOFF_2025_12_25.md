# 💾 SESSION HANDOFF: CHRISTMAS 2025

**Date**: 2025-12-25
**System Version**: Willow v2.0 (The Swarm)
**Status**: OPERATIONAL (Requires API Keys)

## 🧠 System State (The "Save Game")

### 1. The Nervous System (N8N)

- **URL**: `http://lisa:5678` (or `http://localhost:5678` via tunnel).
- **Connectivity**: Uses `n8n start --tunnel` (Temporary `hooks.n8n.cloud` URL).
- **Workflows Installed**:
  - `Grapevine Core` (Event Bus)
  - `Telegram Listener` (The Ear)
  - `Delegation Matrix` (The Router)
  - `Economical Audit` (The Accountant)
- **Action Required**: Open N8N -> Telegram Workflow -> Toggle Active OFF/ON to pick up new Tunnel URL.

### 2. The Memory (Zep & AuraDB)

- **Fact Memory**: Neo4j AuraDB (Cloud).
- **Episodic Memory**: **Zep Community Edition** (Deployed on `bunny:8001`).
  - _Network_: Internal `http://agilemesh-zep:8000`.
- **Action Required**: Ensure `OPENAI_API_KEY` is in `.env` (Zep needs it for embeddings).

### 3. The Ledger (Cost Center)

- **Database**: Postgres (`population` DB on `bunny`).
- **Table**: `token_usage` (Created).
- **Role**: Tracks every token spent by the Swarm.
- **Action Required**: Update N8N Matrix to log costs to this table.

### 4. The Organization (People & Agents)

- **CEO**: Willow.
- **Board**: Peter.
- **New Hires**:
  - "The Plumber" (Infrastructure Agent).
  - "CFO" (Token Tracker).

## 🔑 Credentials & Secrets

- **Location**: `.env` (Local).
- **Status**: Sanitized. Hardcoded passwords removed from `deploy_n8n.py` and `deploy_bunny.py`.
- **Missing**: `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, `GROQ_API_KEY` (User must fill these).

## 📜 Next Session "Respawn" Tasks

1.  **Fill The Matrix Keys**:

    - Open `.env`.
    - Add keys for OpenAI, Anthropic, Groq.

2.  **Activate communication**:

    - Go to N8N.
    - Re-activate Telegram Listener.
    - Text "Hello" to `@Willow_AgileMesh_Bot`.

3.  **Execute "The Plumber's" Vision**:
    - Replace N8N Tunnel with **Tailscale Funnel** (Permanent URL).
    - See `infrastructure/tailscale_integration.md`.

## 📂 Artifacts Manifest

- `WILLOW_ORGANIZATION.md`: The Org Chart.
- `RESOURCES.md`: The Map.
- `bootstrap/*.json`: The Brain Logic.
- `schemas/cost_center.sql`: The Ledger.
- `docs/RISK_ASSESSMENT.md`: The Safety Net.

---

_"We can only manage what we can see."_ - Willow v2.0
