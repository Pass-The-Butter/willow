# Economical Agent Spec

> "Run light, run fast."

**Goal**: Create a lightweight agent on N8N that uses **Groq** (Llama 3 70b) to perform routine tasks like "Resource Auditing" without costing API credits.

## Workflow Structure

1.  **Trigger**: Webhook (`/audit`) or Cron (Weekly).
2.  **Brain**: Groq Llama 3 (Free Tier).
3.  **Action**:
    - Connects to AuraDB (The Brain).
    - Connects to Postgres (Bunny).
    - Connects to `inventory.md` (via SSH/File Read).
    - Generates a report.
4.  **Output**: Telegram Message to Peter.

## Immediate Task

- Create N8N Workflow: `bootstrap/economical_audit_agent.json`
- This agent will scan the "Assets" and verify them against the actual infrastructure.
