# Willow - Quick Start Guide

## 🚀 Resume Development (Next Session)

### 1. Check Your Next Task
```bash
cd /Volumes/Delila/dev/Willow
python3 skills/query_my_tasks.py
```

**Expected output:**
```
=== Current Tasks ===
Found 1 tasks with status 'in_progress'
  [in_progress] WILL-018: Create GitHub Project kanban board

=== Next Task ===
Next task: WILL-001 - Reorganize file structure to match docker-compose
  Priority: critical
  Description: Move files to ./infrastructure/neo4j, ./core/api, ./core/skills, ./domains/
```

### 2. Critical Path (Do These First)

**WILL-001**: Reorganize files
```bash
# Create new directories
mkdir -p infrastructure/neo4j core/api core/skills domains

# Move files
mv mcp-servers/neo4j/* infrastructure/neo4j/
mv api/* core/api/
mv skills/* core/skills/

# Clean up old directories
rmdir mcp-servers/neo4j mcp-servers api skills
```

**WILL-003**: Start Docker containers
```bash
docker-compose up -d --build
```

**WILL-004-006**: Test skills
```bash
# Test MCP server
curl http://localhost:3001/tools/get_skills

# Test Willow API
curl http://localhost:8000/execute/hello_world

# Test memory retrieval
curl -X POST http://localhost:8000/execute \
  -H "Content-Type: application/json" \
  -d '{"skill_name": "retrieve_conversation_context", "parameters": {"keyword": "Docker"}}'
```

---

## 📊 Current State

### AuraDB Status
- **URI**: neo4j+s://e59298d2.databases.neo4j.io
- **Nodes**: ~48 (System, Skills, Decisions, Tasks, Sprints, Insights, BrandAssets)
- **Credentials**: `/Volumes/Delila/Downloads/Neo4j-e59298d2-Created-2025-12-17.txt`

### Docker Containers (Not Started Yet)
- `willow-neo4j-mcp` (port 3001)
- `willow-api` (port 8000)
- `willow-n8n` (port 5678)
- `willow-population-db` (Postgres, port 5432)

### GitHub
- **Repo**: github.com/Pass-The-Butter/willow
- **Status**: Not initialized (WILL-016 pending)

---

## 🗺️ Roadmap Overview

### Sprint 1: Bootstrap (Current)
- [x] AuraDB connection
- [x] Core schema loaded
- [x] Task management loaded
- [x] query_my_tasks skill created
- [ ] File structure reorganized (WILL-001)
- [ ] Containers running (WILL-003)
- [ ] Skills tested (WILL-004-006)
- [ ] Git initialized (WILL-016)

### Sprint 2: Population System
- [ ] SSH to bunny server (WILL-007)
- [ ] Design Postgres schema (WILL-008)
- [ ] Create Faker generator (WILL-009)
- [ ] Generate 10M NPCs via Ollama (WILL-010)
- [ ] Add vector embeddings (WILL-011)

### Sprint 3: Pet Claims Journey
- [ ] Design sub-ontology (WILL-012)
- [ ] Implement journey schema (WILL-013)
- [ ] Connect MSSQL (WILL-014, blocked)
- [ ] Accumulating snapshot (WILL-015)

---

## 🔑 Key Files

### Schemas
- `schemas/willow-bootstrap.cypher` - Core ontology
- `schemas/task-management.cypher` - Roadmap nodes

### Skills
- `skills/hello_world.py` - Test skill
- `skills/retrieve_conversation_context.py` - Memory retrieval
- `skills/ingest_mssql_claims.py` - MSSQL ingestion (blocked)
- `skills/query_my_tasks.py` - Claude's self-introspection

### Utilities
- `clear_auradb.py` - Wipe database
- `load_schema.py` - Load bootstrap schema
- `load_task_management.py` - Load tasks

### Documentation
- `SESSION_SUMMARY.md` - Full session notes
- `docs/GITHUB_PROJECT_SETUP.md` - Kanban board spec
- `QUICK_START.md` - This file

---

## 🎯 The Vision

**Willow** = Self-describing autonomous graph ontology system

### Key Innovations
1. **Capabilities AS nodes** - Skills stored in graph
2. **Memory AS nodes** - Decisions, insights preserved
3. **Roadmap AS nodes** - Tasks, sprints queryable
4. **Customer journey defines ontology** - Not business silos

### Architecture
```
Population DB (Postgres)     Local Ollama (RTX 3090 Ti)
    ↓ 10M NPCs                   ↓ Faker generation
    |                             |
    └──────────┬──────────────────┘
               ↓
         Willow Core (AuraDB)
         System, Skills, Tasks, Customers, Claims
               ↓
         ┌─────┴─────┐
    MCP Server    Willow API
         ↓              ↓
    Claude Code    Python Skills

         ↓ (future)
    VR Interface (MetaQuest 3)
    N8N SVG Sprite Generators
```

### Agent Roles
- **Claude Sonnet 4.5**: Orchestration, reasoning, architecture
- **Local Ollama**: Bulk work (10M NPC generation)
- **N8N agents**: SVG sprite generation for entities

---

## 🌳 Quick Commands

### Query AuraDB directly
```bash
python3 << 'EOF'
from neo4j import GraphDatabase
import certifi, os

os.environ['SSL_CERT_FILE'] = certifi.where()
driver = GraphDatabase.driver(
    "neo4j+s://e59298d2.databases.neo4j.io",
    auth=("neo4j", "c2U7h1mwvmYn2k2cr_Fp9EaUrZaLZdEQ3_Cawt6zvyU")
)

with driver.session() as session:
    # Show all skills
    result = session.run("MATCH (s:Skill) RETURN s.name, s.description")
    for record in result:
        print(f"- {record['s.name']}: {record['s.description']}")

driver.close()
EOF
```

### View task dependency graph
```bash
python3 << 'EOF'
from neo4j import GraphDatabase
import certifi, os

os.environ['SSL_CERT_FILE'] = certifi.where()
driver = GraphDatabase.driver(
    "neo4j+s://e59298d2.databases.neo4j.io",
    auth=("neo4j", "c2U7h1mwvmYn2k2cr_Fp9EaUrZaLZdEQ3_Cawt6zvyU")
)

with driver.session() as session:
    result = session.run("""
        MATCH (t:Task)-[:BLOCKED_BY]->(blocker:Task)
        RETURN t.id + ' blocked by ' + blocker.id as dependency
    """)
    for record in result:
        print(record['dependency'])

driver.close()
EOF
```

---

## 💡 New Ideas From This Session

### N8N SVG Sprite Generators
- N8N workflow triggered when entity created
- Local agent generates SVG sprite
- Stored in node property: `sprite_svg` or `sprite_url`
- VR interface pulls sprites from graph

### Population as NPC Sims
- 10M synthetic people with evolving personalities
- Vector embeddings for similarity (marketing)
- Faker-generated demographics (English locales)
- Gradual bio evolution over time

### Customer Journey Ontology
Jerry finds Barry → Quote → Policy → Vet → Claim → Payment

**This IS the schema.** Customer-first design.

---

## 📞 Server Access

| Server | Command | Purpose |
|--------|---------|---------|
| **Bunny (Xeon)** | `ssh bunny@bunny` (Chocolate1!) | Population DB (128GB) |
| **Local PC** | Tailscale → Ollama | RTX 3090 Ti for Faker |
| **N8N Cloud** | agilemesh.app.n8n.cloud | MCP-enabled workflows |

---

**Status**: Bootstrap in progress | **Next**: WILL-001 → File reorganization
**Built by**: Claude Code (Sonnet 4.5) + Peter | **Date**: Dec 21, 2025 🌳
