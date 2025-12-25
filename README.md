# Willow 🌳

**Autonomous Agent Population & Reasoning System**

> **Current Status**: Bootstrapping Phase
> **Mission Control**: See [MISSION_CONTROL.md](MISSION_CONTROL.md) for links, status, and objectives.

## Overview

Willow is a self-describing, introspective system where skills, workflows, brand assets, and conversational memory are stored AS graph nodes in Neo4j. Claude can query "what can I do?" by querying the ontology itself.

**Project Management**: [Jira Board (SCRUM)](https://agilemeshnet.atlassian.net/jira/software/projects/SCRUM/boards/1)

## Quick Start

1.  **Check Mission Control**: Ensure you understand the current sprint.
2.  **Bootstrap**:
    ```bash
    pip install -r requirements.txt
    python bootstrap/verify_graph.py
    ```
3.  **Run Hello World**:
    ```bash
    python core/skills/hello_willow.py
    ```

## Architecture

*   **Brain**: Neo4j AuraDB (Graph Memory)
*   **Vault**: Xeon Server (Postgres Population DB)
*   **Muscle**: Windows 11 PC (Inference & Generation)
*   **Architect**: Mac Mini (Control Plane)

See [docs/ARCHITECTURE_DEFINITIVE.md](docs/ARCHITECTURE_DEFINITIVE.md) for details.

```
┌─────────────────┐
│  Claude Code    │
│  (AntiGravity)  │
└────────┬────────┘
         │
    ┌────┴────┐
    │   MCP   │
    └────┬────┘
         │
┌────────┴──────────────────────────────┐
│         Docker Infrastructure         │
│                                       │
│  ┌─────────┐  ┌──────────┐          │
│  │ Neo4j   │  │ Neo4j    │          │
│  │ Dev     │  │ MCP      │          │
│  │ :7474   │  │ Server   │          │
│  │ :7687   │  │ :3001    │          │
│  └─────────┘  └──────────┘          │
│                                       │
│  ┌─────────┐  ┌──────────┐          │
│  │ Willow  │  │   N8N    │          │
│  │ API     │  │ :5678    │          │
│  │ :8000   │  └──────────┘          │
│  └─────────┘                         │
└───────────────────────────────────────┘
```

## Quick Start

### 1. Start the infrastructure

```bash
docker-compose up -d
```

### 2. Load the bootstrap schema

```bash
docker exec -i willow-neo4j cypher-shell -u neo4j -p willowdev123 < schemas/willow-bootstrap.cypher
```

### 3. Verify system health

- **Neo4j Browser**: http://localhost:7474
- **Willow API**: http://localhost:8000
- **Neo4j MCP Server**: http://localhost:3001
- **N8N**: http://localhost:5678

## Services

### Neo4j (Graph Database)
- Port: 7474 (HTTP), 7687 (Bolt)
- Credentials: `neo4j / willowdev123`
- APOC plugins enabled

### Neo4j MCP Server
- Port: 3001
- Exposes tools: `run_cypher`, `get_skills`, `execute_skill`, `get_brand_assets`
- Logs all queries as `:ExecutionLog` nodes

### Willow API
- Port: 8000
- Executes Python skills dynamically
- Mounts `/skills` directory

### N8N
- Port: 5678
- Workflow orchestration
- Credentials: `willow / willowdev123`

## Skills

### hello_world.py
Simple greeting skill to verify system is operational

```python
execute(name="Peter")
# Returns: "Hello, Peter! Willow is alive."
```

### retrieve_conversation_context.py
Query decisions and insights by keyword

```python
execute(keyword="Docker", depth=2, limit=10)
# Returns: Decisions mentioning "Docker" with related context
```

### ingest_mssql_claims.py
Read from MSSQL and create graph nodes (Phase 5)

```python
execute(table="Claims", limit=100)
# Placeholder - waiting for MSSQL credentials
```

## Graph Schema

### Core Node Types

- `:System` - System metadata
- `:Skill` - Executable capabilities (Python or Cypher)
- `:BrandAsset` - Seasonal UI themes and branding
- `:Workflow` - N8N orchestration definitions
- `:Decision` - Conversational memory (why we built things)
- `:Insight` - Key learnings
- `:ConversationSession` - Discussion history
- `:ExecutionLog` - Query audit trail

### Key Relationships

- `(:System)-[:HAS_CAPABILITY]->(:Skill)`
- `(:System)-[:HAS_DECISION]->(:Decision)`
- `(:System)-[:HAS_INSIGHT]->(:Insight)`
- `(:Decision)-[:LED_TO_INSIGHT]->(:Insight)`
- `(:Skill)-[:IMPLEMENTS_INSIGHT]->(:Insight)`

## Testing

### Verify Neo4j Connection

```bash
docker exec -it willow-neo4j cypher-shell -u neo4j -p willowdev123
```

### Query Skills

```cypher
MATCH (s:Skill) RETURN s.name, s.language, s.description;
```

### Get Active Brand Palette

```cypher
MATCH (b:BrandAsset {active: true}) RETURN b.palette;
```

### Test Hello World Skill

```bash
curl -X POST http://localhost:8000/execute \
  -H "Content-Type: application/json" \
  -d '{"skill_name": "hello_world", "parameters": {"name": "Peter"}}'
```

## Brand Identity

**Active Season**: Autumn 🍂

**Palette**:
- Primary: `#8B9D83` (muted sage green)
- Accent: `#C17A5C` (burnt amber)
- Grey: `#A89F91`
- Burgundy: `#6B4444`
- Background: `#F5F1E8` (warm cream)

**Logo**: Minimalist geometric willow tree ([Canva](https://www.canva.com/d/r1GY4_LfcJpg1xA))

## Development Principles

1. **Muddy the canvas** - Start concrete, iterate
2. **Zoomy and invisible** - No heavy pipelines
3. **Make decisions** - Explain reasoning, test ideas
4. **R&D mindset** - Follow plans not clocks

## Next Steps

- [ ] Connect to Peter's MSSQL database
- [ ] Build graph visualization skill
- [ ] Create dashboard using brand assets
- [ ] Sync to AuraDB for durability
- [ ] Add VR visualization integration

## License

Proprietary - Semantic Arts Innovations Team R&D

---

**Built with**: Neo4j, Docker, FastAPI, Python
**For**: Peter (DBA & Ontologist at Semantic Arts)
**By**: Claude Desktop + Claude Code (AntiGravity)
