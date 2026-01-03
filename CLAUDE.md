# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

Willow is a GraphRAG-powered autonomous agent system where the Neo4j graph database serves as the "Brain" - storing ontology, project structure, memory, and conversational context. The system uses a distributed architecture across multiple machines (Mac Mini, Windows PC, Xeon server) connected via Tailscale.

**Core Philosophy**: "The Graph is the Memory. The Code is the Will."

## Essential Bootstrap Protocol

**CRITICAL**: Every session MUST start by reading `BIOS.md`. This is the bootstrap protocol that connects you to AuraDB (the Brain) and loads the appropriate context for your role.

### Agent Roles & Context Loading

Before doing anything, determine your role:

- **Captain (Chief Officer)**: Full organogram access, all domains
- **Project Manager**: Domain-level context, sprint objectives
- **Feature Agent**: Single task branch only (Just Enough Context principle)
- **DevOps Manager**: Infrastructure, deployment, logs

Each role has specific context loading procedures in `BIOS.md:15-189`.

### Connection to AuraDB (The Brain)

All project knowledge lives in Neo4j AuraDB. Credentials are in `.env`:

```python
from neo4j import GraphDatabase
import certifi
import os

os.environ['SSL_CERT_FILE'] = certifi.where()
driver = GraphDatabase.driver(
    os.getenv('NEO4J_URI'),
    auth=(os.getenv('NEO4J_USER'), os.getenv('NEO4J_PASSWORD'))
)
```

Test connection before proceeding: `bootstrap/verify_graph.py`

## Architecture

### Physical Infrastructure

- **Brain**: Neo4j AuraDB (Cloud) - Central memory and ontology
- **Vault**: Bunny (Xeon Server, Ubuntu) - Postgres population database, N8N orchestration
- **Muscle**: Frank (Windows 11 PC) - Ollama inference, population generation
- **Architect**: Mac Mini - Development control plane, Git origin
- **Fabric**: Tailscale mesh network connecting all nodes

### Docker Services (Local Development)

Start infrastructure: `docker-compose up -d`

Services:
- **neo4j-mcp** (port 3001): MCP server exposing tools: `run_cypher`, `get_skills`, `execute_skill`, `get_brand_assets`
- **willow-api** (port 8000): FastAPI skill execution endpoint
- **dashboard** (port 5001): Flask web interface
- **sidebar** (port 8080): Astro Starlight documentation portal
- **n8n** (port 5678): Workflow orchestration (credentials: `willow/willowdev123`)
- **population-db** (port 5432): Postgres with pgvector
- **graphiti** (port 8002): Experiential memory service
- **proxy** (port 80): Nginx reverse proxy

### Graph Schema (Organogram)

The project structure is stored as a graph in Neo4j. Key node types:

- `:Project` - Root (Willow)
- `:Domain` - Top-level divisions (Population, Interface, Core)
- `:Component` - Functional components within domains
- `:Task` - Specific work items with status tracking
- `:Specification` - Technical requirements for tasks
- `:TestCriteria` - Acceptance criteria for tasks
- `:DiaryEntry` - Work log entries by agents
- `:Message` - Inter-agent communication
- `:RFC` - Proposed changes requiring decision
- `:Skill` - Executable capabilities (Python or Cypher)
- `:BrandAsset` - UI themes and branding

Key relationships:
- `(:Domain)-[:HAS_COMPONENT]->(:Component)-[:HAS_TASK]->(:Task)`
- `(:Task)-[:DEPENDS_ON]->(:Task)`
- `(:Task)-[:REQUIRES]->(:Specification)`
- `(:Task)-[:MUST_SATISFY]->(:TestCriteria)`
- `(:Task)-[:HAS_DIARY_ENTRY]->(:DiaryEntry)`

Schema files: `schemas/organogram.cypher`, `schemas/task-management.cypher`

## Common Development Commands

### Environment Setup

```bash
# Activate virtual environment
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Load environment variables
source .env
```

### Infrastructure

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f <service-name>

# Load bootstrap schema into AuraDB
python bootstrap/deploy_schema.py

# Verify connections
python bootstrap/verify_connections.py
python test_connections.py
```

### Neo4j Database

```bash
# Load organogram schema
python bootstrap/deploy_organogram.py

# Query via MCP (if configured)
# Tools: run_cypher, get_skills, execute_skill, get_brand_assets

# Direct Cypher query
python -c "
from neo4j import GraphDatabase
import os, certifi
os.environ['SSL_CERT_FILE'] = certifi.where()
driver = GraphDatabase.driver(os.getenv('NEO4J_URI'), auth=(os.getenv('NEO4J_USER'), os.getenv('NEO4J_PASSWORD')))
with driver.session() as s:
    result = s.run('MATCH (t:Task) RETURN t.name, t.status')
    for r in result:
        print(r)
driver.close()
"
```

### Skills

Skills are executable Python functions in `core/skills/`. All skills follow this pattern:

```python
def execute(**kwargs):
    """Skill implementation"""
    # Connect to Neo4j
    # Perform work
    # Return results
```

Common skills:

```bash
# Get task context from organogram
python core/skills/get_task_context.py

# Query infrastructure status
python core/skills/query_infrastructure.py

# Search memory
python core/skills/search_memory_hybrid.py "search query"

# Hello world test
python core/skills/hello_world.py
```

Execute skills via API:

```bash
curl -X POST http://localhost:8000/execute \
  -H "Content-Type: application/json" \
  -d '{"skill_name": "hello_world", "parameters": {"name": "Peter"}}'
```

### Task Management

```bash
# Get your tasks (Feature Agent)
python core/skills/query_my_tasks.py

# Load task management schema
python load_task_management.py

# Sync with Jira (when implemented)
python bootstrap/sync_atlassian.py
```

### Memory & Context

```bash
# Initialize memory schema
python core/skills/init_memory_schema.py

# Search memory (vector + graph)
python core/skills/search_memory_hybrid.py "keyword"

# Log new memory
python core/skills/log_memory.py

# Retrieve conversation context
python core/skills/retrieve_conversation_context.py
```

## Key Architectural Patterns

### GraphRAG Approach

Willow uses Graph Retrieval Augmented Generation:
- **Structured memory**: Nodes and relationships in AuraDB
- **Unstructured memory**: Vector embeddings on node properties
- **Vector index**: `willow_memory` (768 dimensions) on `:Memory` nodes
- **Hybrid search**: Combine semantic search with graph traversal

See: `docs/ARCHITECTURE_DEFINITIVE.md:40-45`

### Just Enough Context Principle

Agents should:
1. Read `MISSION_CONTROL.md` or `BIOS.md`
2. Query graph for specific task context: `core/skills/get_task_context.py`
3. Read only relevant files for that task
4. Execute work
5. Log results back to graph

**Don't** load the entire codebase. **Do** use scoped queries.

### Task Path Format

Tasks are identified by organogram path: `"Domain → Component → Task"`

Example: `"Population → Generator → Faker Integration"`

Use with: `core/skills/get_task_context.py "Population → Generator → Faker Integration"`

### Work Logging Protocol

**ALWAYS** log your work to the graph before finishing:

```python
with driver.session() as session:
    session.run("""
        MATCH (t:Task {name: $task_name})
        CREATE (t)-[:HAS_DIARY_ENTRY]->(d:DiaryEntry {
            agent: $agent_name,
            timestamp: datetime(),
            status: $status,
            notes: $notes
        })
    """, task_name="Your Task", agent_name="Agent Name",
         status="In Progress", notes="What you did")
```

## Project Resources

- **GitHub**: [Pass-The-Butter/willow](https://github.com/Pass-The-Butter/willow)
- **Jira Board**: [Agile Meshnet SCRUM](https://agilemeshnet.atlassian.net/jira/software/projects/SCRUM/boards/1)
- **Confluence**: [Agile Meshnet Wiki](https://agilemeshnet.atlassian.net/wiki)
- **AuraDB Console**: [Neo4j Aura](https://console.neo4j.io)
- **Mission Control**: `MISSION_CONTROL.md` - Central dashboard and sprint objectives
- **Strategic Overview**: `WILLOW_STRATEGIC_OVERVIEW.md`

## Testing & Verification

```bash
# Verify graph connection
python bootstrap/verify_graph.py

# Verify Neo4j vector indexes
python verify_vector_indexes.py

# Verify memory system
python verify_memory_system.py
python verify_recall_capability.py

# Check population progress
python core/skills/check_population_progress.py

# Verify sidebar deployment
bash verify_sidebar_deployment.sh
```

## Development Principles

From `README.md:196-200`:

1. **Muddy the canvas** - Start concrete, iterate
2. **Zoomy and invisible** - No heavy pipelines
3. **Make decisions** - Explain reasoning, test ideas
4. **R&D mindset** - Follow plans not clocks

## Important Notes

- **Credentials**: Never commit `.env` file or hardcoded credentials
- **SSL Certificates**: Always set `os.environ['SSL_CERT_FILE'] = certifi.where()` before Neo4j connections
- **Tailscale**: Required for accessing Frank and Bunny nodes
- **Brand**: Current season is Autumn 🍂 with palette defined in `README.md:183-192`
- **Git**: Work on feature branches, PR to `main`
- **Infrastructure first**: Verify Docker services are running before development

## Common Errors & Fixes

- **"URI scheme b'' is not supported"**: Environment variables not loaded. Run `source .env`
- **"Connection refused"**: Tailscale not running or not connected
- **"Task not found in organogram"**: Task path spelling wrong, check with Captain
- **"No diary entries"**: New task, start logging now
- **SSL certificate errors**: Set `SSL_CERT_FILE` and `REQUESTS_CA_BUNDLE` to `certifi.where()`

## File Structure Reference

```
/
├── BIOS.md                    # MUST READ FIRST - Bootstrap protocol
├── MISSION_CONTROL.md         # Central dashboard, sprint objectives
├── README.md                  # Project overview
├── docker-compose.yml         # Local infrastructure services
├── requirements.txt           # Python dependencies
├── .env                       # Credentials (not in git)
│
├── bootstrap/                 # Deployment and setup scripts
│   ├── deploy_*.py           # Schema/service deployment
│   ├── verify_*.py           # Connection verification
│   └── sync_atlassian.py     # Jira integration (TODO)
│
├── core/
│   ├── skills/               # Executable agent capabilities
│   │   ├── get_task_context.py    # Load scoped task info
│   │   ├── query_infrastructure.py
│   │   ├── search_memory_*.py
│   │   └── *.py              # Other skills
│   ├── api/                  # FastAPI skill execution
│   ├── ontology/             # Graph schema definitions
│   ├── roles/                # Role-specific documentation
│   └── utils/                # Shared utilities
│
├── domains/                  # Domain-specific code
│   ├── population/           # Data generation
│   ├── interface/            # Web apps and APIs
│   └── sidebar/              # Documentation portal (Astro)
│
├── schemas/                  # Neo4j Cypher schemas
│   ├── organogram.cypher     # Project structure
│   ├── task-management.cypher
│   └── *.cypher
│
├── infrastructure/           # Docker configs
│   ├── neo4j/               # MCP server
│   ├── memory/              # Graphiti
│   └── proxy/               # Nginx
│
└── docs/                    # Architecture docs
    └── ARCHITECTURE_DEFINITIVE.md
```
