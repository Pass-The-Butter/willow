# 🗂️ WILLOW RESOURCES REGISTRY

**Central directory of all Willow system resources, services, and tools.**

**Last Updated**: 2025-12-25
**Maintained By**: Willow Brain (AuraDB sync)

---

## 🔐 CREDENTIALS & SECURITY

**⚠️ CRITICAL SECURITY ISSUE FOUND**:

- Hardcoded passwords discovered in repository code
- Files affected: `bootstrap/clear_auradb.py`, `core/skills/query_my_tasks.py`, and others
- **Action Required**: Remove hardcoded credentials immediately
- **If repo was ever public**: Rotate ALL passwords (AuraDB, Postgres, etc.)

**Credentials Location**:

- Primary: `.env` file (gitignored ✅)
- Backup: TBD (consider HashiCorp Vault, AWS Secrets Manager, or encrypted file)

**Repository Status**:

- Remote: https://github.com/Pass-The-Butter/willow.git
- Visibility: TBD (check if public or private!)

---

## 📊 PROJECT MANAGEMENT

### Jira (Atlassian)

- **URL**: https://agilemeshnet-1766667903740.atlassian.net/jira/software/projects/SMS/boards/1
- **Workspace**: AgileMeshNet
- **Project**: SMS (Scrum Management System)
- **Type**: Kanban/Scrum board
- **API Access**: TBD (need API token)
- **Status**: Active
- **Cost**: TBD

### Linear

- **Workspace**: https://linear.app/agilemesh/team/AGI/active
- **Project - Willow**: https://linear.app/agilemesh/project/willow-8917fec120a3/overview
- **Team**: AGI
- **API Access**: TBD (need API key from Settings → API)
- **Webhook**: TBD (configure after N8N setup)
- **Status**: Active
- **Cost**: Free tier (unlimited members, 250 issues, all APIs)

**Decision Needed**: Use Jira OR Linear as primary? Or both for different purposes?

---

## 💬 COMMUNICATION

### Telegram

- **Bot**: TBD (create via @BotFather)
- **Bot Token**: TBD
- **Team Group**: TBD (create and get chat ID)
- **Bot Username**: TBD
- **API Docs**: https://core.telegram.org/bots/api
- **N8N Integration**: Native support available
- **Status**: Pending setup
- **Cost**: Free

### Discord

- **Server**: TBD (not created yet)
- **Status**: Alternative option if needed
- **Cost**: Free

### Slack

- **Workspace**: TBD (not created yet)
- **Status**: Alternative option (expensive $10.50/user/month)
- **Cost**: Not recommended

---

## 🔄 ORCHESTRATION & AUTOMATION

### N8N

- **Hosting**: TBD (choose: Bunny self-hosted OR cloud)
- **URL**: TBD
- **Username**: TBD
- **Password**: TBD
- **Credentials Configured**: None yet
- **Workflows**: None yet
- **Status**: Pending deployment
- **Cost**:
  - Self-hosted on Bunny: ~$0/month (uses existing server)
  - Cloud: ~$20/month

**Recommended**: Self-host on Bunny + expose via Tailscale for cost savings

---

## 🧠 INFRASTRUCTURE

### AuraDB (Neo4j Cloud) - "The Brain"

- **URI**: `neo4j+s://e59298d2.databases.neo4j.io`
- **User**: `neo4j`
- **Password**: **⚠️ EXPOSED IN CODE - ROTATE IMMEDIATELY**
- **Database**: `neo4j`
- **Role**: Central knowledge graph, organogram, memory, ontology
- **Vector Search**: Enabled (trial - 8 days remaining)
- **Trial End Date**: ~2025-01-02
- **Status**: Active (TRIAL)
- **Cost**:
  - Trial: Free (ends in 8 days)
  - Paid: ~$65-200/month depending on tier
  - Free tier: Available but loses vector search
- **Decision Needed**: Upgrade to paid, downgrade to free, or migrate vector search

### BabyWillow (AuraDB Free For Life)

- **ID**: `8ce1b60a`
- **Role**: Permanent backup / Free tier instance
- **Status**: Available (Free for life)
- **Note**: Likely no vector search support? Verify.

### Bunny (Xeon Server)

- **Hostname**: `bunny`
- **Network**: Tailscale (`bunny` on tailnet)
- **OS**: Ubuntu
- **RAM**: 128GB
- **Role**: Population storage, potential N8N host
- **Services Running**: PostgreSQL
- **SSH Access**: `ssh bunny@bunny`
- **Password**: `Chocolate1!` (User provided)
- **Status**: Active
- **Cost**: $0 (owned hardware)

### Frank (Windows 11 PC)

- **Hostname**: `frank`
- **Network**: Tailscale (`frank` on tailnet)
- **OS**: Windows 11
- **Role**: LLM inference (Ollama), generation tasks
- **Services Running**: Ollama
- **SSH Access**: `ssh peter@frank`
- **Status**: Active
- **Cost**: $0 (owned hardware)

### Mac Mini (Captain Workstation)

- **OS**: macOS 25.2.0 (Darwin kernel)
- **Role**: Development, Claude Code sessions, controller
- **Location**: Local (working directory: `/Volumes/Delila/dev/Willow`)
- **Status**: Active
- **Cost**: $0 (owned hardware)

### Tailscale

- **Role**: Mesh VPN fabric connecting all nodes
- **Network Name**: TBD (check `tailscale status`)
- **Nodes**: Mac Mini, Bunny, Frank
- **Status**: Active
- **Cost**: Free tier (up to 100 devices, 3 users)

---

## 💾 DATABASES

### PostgreSQL - "Bunny Database"

- **Host**: `bunny` (via Tailscale)
- **Port**: 5432
- **Database**: `population`
- **User**: `willow`
- **Password**: `willowdev123` (**⚠️ WEAK PASSWORD - CHANGE**)
- **Role**: Population data storage (customers, pets, quotes)
- **Capacity**: 100M+ entities
- **Current Data**: 9,862 customers, 2,982 pets
- **Status**: Active
- **Cost**: $0 (self-hosted on Bunny)

### AuraDB (see Infrastructure section above)

---

## 🤖 AI/LLM SERVICES

### Ollama (Local LLMs)

- **Host**: Frank (`frank` on Tailscale)
- **Port**: 11434
- **Models Installed**: `llama3`, `mistral`
- **API**: `http://frank:11434/api`
- **Role**: Local LLM inference, cost-free AI
- **Status**: Active
- **Cost**: $0 (self-hosted)

### Claude API (Anthropic)

- **Model**: Sonnet 4.5 (`claude-sonnet-4-5-20250929`)
- **API Key**: TBD (stored where?)
- **Usage**: Captain agent, feature agents, research agents
- **Status**: Active
- **Cost**: Pay-per-token (varies)

### OpenAI API

- **API Key**: TBD (if configured)
- **Models**: TBD
- **Usage**: Alternative to Claude for specific tasks
- **Status**: TBD
- **Cost**: Pay-per-token (varies)

---

## 🌐 WEB & DOMAINS

### AgileMesh.net

- **Registrar**: TBD
- **DNS Provider**: TBD (Cloudflare?)
- **Cloudflare Zone ID**: TBD
- **Cloudflare API Token**: TBD
- **Current Site**: None (available for deployment)
- **Planned Use**:
  - Public PoC homepage
  - `/dashboard` - Willow system dashboard (already built!)
  - `/status` - Infrastructure status
  - `/api` - Agent API endpoints
- **Hosting Options**:
  - Cloudflare Pages (static)
  - Bunny (dynamic Flask app)
  - Frank (alternative)
- **Status**: Domain registered, site not deployed

### Existing Dashboard

- **Path**: `/dashboard` in Flask app (`domains/interface/app.py`)
- **Features**: Real-time metrics, infrastructure status, population counts, sprint progress
- **Access**: Local only (http://localhost:5000/dashboard)
- **Deployment Needed**: Expose via Tailscale or public domain

---

## 🔌 INTEGRATIONS & MCP SERVERS

### Cloudflare MCP

- **Access**: Via Docker Hub MCP
- **Docker Image**: `cloudflare/mcp-server`
- **API Token**: TBD
- **Capabilities**: DNS management, workers, pages, tunnels
- **Status**: Available but not configured
- **Cost**: Free (uses existing Cloudflare account)

### Model Context Protocol (MCP) Servers

- **Available**: Cloudflare MCP
- **Potential**: GitHub MCP, Linear MCP, Jira MCP, Slack MCP, etc.
- **Status**: Cloudflare available, others TBD

---

## 📦 REPOSITORIES & CODE

### Willow Repository

- **URL**: https://github.com/Pass-The-Butter/willow.git
- **Visibility**: TBD (check if public or private!)
- **Branch**: `master`
- **Status**: Clean working tree (as of 2025-12-25)
- **Last Commit**: `90d183f - Add session handoff for next agent respawn`
- **Security Issue**: ⚠️ Hardcoded passwords in code - needs immediate fix

---

## 🎯 DECISIONS PENDING

1. **AuraDB Vector Search** (URGENT - 8 days):

   - [ ] Upgrade to paid plan (~$65-200/month)
   - [ ] Downgrade to free tier (lose vector search)
   - [ ] Migrate vector search to external service (Qdrant, Pinecone, Weaviate)

2. **Project Management Primary**:

   - [ ] Use Jira as primary
   - [ ] Use Linear as primary
   - [ ] Use both (Jira for PoC stakeholders, Linear for dev team?)

3. **N8N Hosting**:

   - [ ] Self-host on Bunny (save $20/month)
   - [ ] Use N8N cloud (easier, $20/month)

4. **Website Hosting for AgileMesh.net**:

   - [ ] Cloudflare Pages (static)
   - [ ] Bunny server (dynamic Flask)
   - [ ] Frank server (alternative)
   - [ ] Hybrid (static frontend + API backend)

5. **Secrets Management**:

   - [ ] HashiCorp Vault (self-hosted)
   - [ ] AWS Secrets Manager / Azure Key Vault (cloud)
   - [ ] Encrypted file with `python-cryptography`
   - [ ] Keep `.env` with strict file permissions (600)

6. **Repository Visibility**:
   - [ ] Check if willow.git is public or private
   - [ ] If public: Rotate ALL passwords immediately
   - [ ] Consider making private if currently public

---

## 📝 QUICK REFERENCE

### Environment Variables (.env file)

```bash
# Neo4j AuraDB
NEO4J_URI=neo4j+s://e59298d2.databases.neo4j.io
NEO4J_USER=neo4j
NEO4J_PASSWORD=c2U7h1mwvmYn2k2cr_Fp9EaUrZaLZdEQ3_Cawt6zvyU  # ⚠️ ROTATE

# PostgreSQL (Bunny)
PG_HOST=bunny
PG_PORT=5432
PG_DB=population
PG_USER=willow
PG_PASS=willowdev123  # ⚠️ WEAK - CHANGE

# Telegram (TBD)
# TELEGRAM_BOT_TOKEN=
# TELEGRAM_GROUP_CHAT_ID=

# Linear (TBD)
# LINEAR_API_KEY=
# LINEAR_WORKSPACE_ID=

# N8N (TBD)
# N8N_URL=
# N8N_USERNAME=
# N8N_PASSWORD=

# Cloudflare (TBD)
# CLOUDFLARE_API_TOKEN=
# CLOUDFLARE_ZONE_ID=
```

### SSH Quick Access

```bash
# Bunny
ssh peter@bunny

# Frank
ssh peter@frank

# Tailscale status
tailscale status
```

### Database Connections

```bash
# PostgreSQL (Bunny)
psql -h bunny -U willow -d population

# AuraDB (via Python)
# See core/utils/credentials.py
```

---

## 🔄 SYNC STATUS

**This file is synced with AuraDB**:

- Local: `/Volumes/Delila/dev/Willow/RESOURCES.md`
- Graph: AuraDB `(:Resource)`, `(:Infrastructure)`, `(:Service)` nodes
- Last Sync: 2025-12-25

**To update**:

1. Edit this file
2. Run sync script (TBD - create this)
3. Or manually update AuraDB via Cypher

---

## 📞 SUPPORT & CONTACT

- **Captain**: Peter
- **Primary Interface**: Claude Code (Sonnet 4.5)
- **Backup**: ChatGPT (GPT-4)
- **Memory**: AuraDB (Neo4j Cloud)
- **Issues**: Telegram (once bot configured) or GitHub issues

---

**Version**: 1.0
**Created**: 2025-12-25
**Last Updated**: 2025-12-25
**Next Review**: After Linear/Telegram setup complete
