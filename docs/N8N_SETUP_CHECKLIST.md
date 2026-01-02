# N8N Setup Checklist (The "Housekeeping" Protocol)

**When to use this:** After re-installing N8N, restarting the container (if volumes weren't persistent), or when moving to a new server.

## 1. Initial Access & User Setup

- [ ] **Log in**: Go to `https://bunny.clouded-newton.ts.net/` (or `http://bunny:5678` locally).
- [ ] **Create Owner Account**: If prompted, set up the initial admin user (email/password). This defines the "Owner".

## 2. Restore Credentials (CRITICAL)

_Because encryption keys are often regenerated on new installs, old credentials may be broken._

- [ ] **Neo4j (The Brain)**
  - Type: `Neo4j`
  - Name: `Neo4j connection`
  - Host: `neo4j+s://e59298d2.databases.neo4j.io` (See `.env`)
  - User/Pass: `neo4j` / `[See .env]`
- [ ] **Postgres (Bunny)**
  - Type: `Postgres`
  - Name: `Postgres connection`
  - Host: `agilemesh-postgres` (Internal Docker network name)
  - User/Pass: `willow` / `willowdev123`
  - Database: `population`
- [ ] **Telegram**
  - Type: `Telegram API`
  - Name: `Telegram account`
  - Access Token: `[See .env]`
- [ ] **OpenAI**
  - Type: `OpenAI API`
  - Name: `OpenAI account`
  - API Key: `[See .env]`

## 3. Global Variables

_Ensure these are accessible to workflows._

- [ ] Check **Variables** panel (or verify via `n8n_compose.yml` injection):
  - `TELEGRAM_CHAT_ID`
  - `OPENAI_API_KEY` (if used directly in HTTP nodes)

## 4. Import Workflows

_Restore the nervous system._

- [ ] **System Heartbeat**: Import `bootstrap/heartbeat_workflow.json`
  - _Status_: Active
- [ ] **Willow Chat**: Import `bootstrap/willow_chat_workflow.json`
  - _Status_: Active
- [ ] **Engineering Meeseeks**: Import `bootstrap/engineering_meeseeks.json`
  - _Status_: Active (or set to Trigger only)

## 5. Verification

- [ ] Run **Engineering Meeseeks** manually.
- [ ] Confirm "Aye, Aye, Captain" message in Telegram.
