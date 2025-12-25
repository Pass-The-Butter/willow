# 🛡️ RISK ASSESSMENT: "WHAT CAN GO WRONG?"

> "Keep storing the notes Buddy. Let's also think about what can go wrong with this setup."

## 1. The "Tunnel" vulnerability

**Risk**: We are currently using `n8n start --tunnel`. This is a TEMPORARY dev feature.

- **Consequence**: The URL changes every time N8N restarts. Telegram breaks.
- **Mitigation**: Must implement **Tailscale Funnel** (Idea from you) or Cloudflare Tunnel (Permanent).

## 2. "Cloud Amnesia" (Data Loss)

**Risk**: AuraDB is our only brain.

- **Consequence**: If AuraDB corrupts or we accidentally wipe it, Willow lobotomizes.
- **Mitigation**:
  - ✅ Daily Cron Backups (Implemented).
  - [ ] **Idea-033**: Local Graph Sync (The user's great idea).

## 3. "The Bill Shock" (API Costs)

**Risk**: An agent gets into run-away loop or we use GPT-4 for everything.

- **Consequence**: £100s in API fees overnight.
- **Mitigation**:
  - **The Matrix (Idea-032)**: Route simple tasks to Groq/Local LLM.
  - **Budget Limits**: Set hard limits in OpenAI/Anthropic dashboards.

## 4. "The Tower of Babel" (Ontology Rot)

**Risk**: Adding too many random memories/nodes without a strict schema.

- **Consequence**: The Graph becomes a swamp. Vector search fails to find relevant context.
- **Mitigation**: Strict "Gardener" agent (part of JIT Swarm) to prune and merge nodes.

## 5. Security Exposure

**Risk**: N8N is powerful. If someone guesses the `hook` URL (unlikely with random UUIDs but possible), they can trigger agents.

- **Mitigation**: Add a "Secret Token" check inside every N8N workflow (e.g., Header `X-Willow-Auth`).
