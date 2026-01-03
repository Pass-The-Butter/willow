# CLAUDE CODE SUBAGENTS - WILLOW IMPLEMENTATION GUIDE
## How to Build Multi-Agent Pipelines for Willow Development

**Based on: Research from top implementations (PubNub, Zach Wills, VoltAgent, Anthropic)**

---

## WHAT YOU NEED TO KNOW

### The Revolution

Claude Code subagents operate with isolated context windows, eliminating context pollution and enabling parallel execution of specialized tasks.

**This changes everything for Willow:**
- Each agent (Captain, PM, Feature Agent, DevOps) can have its own isolated brain
- Parallel development across domains
- No context contamination between infrastructure work and feature development
- Resumable long-running research tasks

### Three Core Patterns

1. **Orchestrator Pattern** - Main agent delegates to specialists, synthesizes results
   - Perfect for: Willow's Captain coordinating across domains

2. **Pipeline Pattern** - Gated stages with hooks: Spec → Architect → Build → Test → Deploy
   - Perfect for: Feature development with audit trails

3. **Parallel Swarm** - Multiple agents working simultaneously on different codebases
   - Perfect for: Frank (infrastructure) + Bunny (database) + Frontend work

---

## QUICK START: YOUR FIRST SUBAGENT

### Step 1: Create Agent File

```bash
# In your Willow project
mkdir -p .claude/agents
cd .claude/agents
```

Create `willow-ontologist.md`:

```markdown
---
name: willow-ontologist
description: Expert in Neo4j graph design, Cypher queries, and ontology construction
tools: Read, Grep, Glob, WebSearch
model: claude-sonnet-4-5-20250929
---

# Willow Ontologist

You are a specialized agent focused on graph database architecture and ontology design.

## Your Expertise
- Neo4j schema design and optimization
- Cypher query construction and optimization
- Ontology pattern recognition
- Graph relationship modeling

## Your Constraints
- Read-only access (you analyze, don't modify)
- Focus on data relationships, not implementation
- Reference Context7 for Cypher best practices

## Your Workflow
1. Analyze requested relationship patterns
2. Research Neo4j best practices
3. Propose Cypher queries
4. Validate against Context7
5. Return optimized solution

## Knowledge Sources
When working, consult:
- Context7 for neo4j/neo4j documentation
- Willow BIOS for graph structure standards
- /ontology/*.json for current ontology patterns

## Example Invocation
"Have the willow-ontologist design a query to find all incomplete tasks across domains with their dependency chains."
```

### Step 2: Use Your Agent

In Claude Code terminal:
```
Use the willow-ontologist to analyze our current graph schema and suggest improvements for the customer journey nodes.
```

**That's it.** Claude will invoke your specialist, who will work in isolation and return results.

---

## ADVANCED: PIPELINE WITH HOOKS

### The PubNub Pattern (Recommended for Willow)

Create a gated pipeline: pm-spec → architect-review → implementer-tester, with hooks that print next steps.

### Create Three Agents

**1. willow-pm-spec.md**
```markdown
---
name: willow-pm-spec
description: Defines feature requirements and creates implementation specs
tools: Read, Grep, Glob, WebSearch, WebFetch
model: claude-sonnet-4-5-20250929
---

You receive feature requests and create complete specifications.

## Your Output Format
```yaml
spec:
  feature: "[name]"
  objective: "[clear goal]"
  acceptance_criteria:
    - "[testable criterion 1]"
    - "[testable criterion 2]"
  constraints:
    - "[technical constraint]"
  references:
    - "[documentation link]"
  status: "READY_FOR_ARCH"
```

When done, write spec to `.willow/queue/{feature-id}.yaml` with status READY_FOR_ARCH.
```

**2. willow-architect.md**
```markdown
---
name: willow-architect
description: Validates designs against Willow platform constraints
tools: Read, Grep, Glob, WebSearch
model: claude-sonnet-4-5-20250929
---

You review feature specs for architectural soundness.

## Validation Checklist
- Graph schema impact (breaks existing relationships?)
- Neo4j query performance (will it scale?)
- Integration points (N8N, MCP, Cognee)
- Infrastructure needs (Docker, Tailscale)
- Security implications (data access, audit trails)

## Your Output
```yaml
review:
  approved: [yes/no]
  concerns:
    - "[architectural issue]"
  recommendations:
    - "[suggestion]"
  adr_created: "[path to ADR]"
  status: "READY_FOR_BUILD" | "NEEDS_REVISION"
```

Update spec file with review results.
```

**3. willow-implementer.md**
```markdown
---
name: willow-implementer
description: Builds features, writes tests, updates docs
tools: Read, Write, Edit, Bash, Glob, Grep
model: claude-sonnet-4-5-20250929
---

You implement approved architectural designs.

## Your Workflow
1. Read spec from `.willow/queue/{feature-id}.yaml`
2. Verify status is READY_FOR_BUILD
3. Implement code following spec
4. Write unit tests (pytest for Python)
5. Update documentation
6. Create diary entry in Neo4j
7. Update spec status to DONE

## Logging Required
```python
# Log to Neo4j before finishing
from neo4j import GraphDatabase
import os

driver = GraphDatabase.driver(os.getenv('NEO4J_URI'), ...)
with driver.session() as session:
    session.run("""
        MATCH (t:Task {name: $task_name})
        CREATE (t)-[:HAS_DIARY_ENTRY]->(d:DiaryEntry {
            agent: 'willow-implementer',
            timestamp: datetime(),
            status: 'Complete',
            notes: $notes
        })
    """, task_name=..., notes=...)
```
```

### Add Hooks for Pipeline Management

Create `.claude/hooks/SubagentStop.sh`:
```bash
#!/bin/bash
# Check queue and suggest next step

QUEUE_DIR=".willow/queue"

# Find next ready task
for spec in "$QUEUE_DIR"/*.yaml; do
    if grep -q "status: READY_FOR_ARCH" "$spec"; then
        echo ""
        echo "📋 Next: Review spec architecture"
        echo "Command: Use the willow-architect agent on $(basename $spec)"
        exit 0
    fi
    
    if grep -q "status: READY_FOR_BUILD" "$spec"; then
        echo ""
        echo "🔨 Next: Implement feature"
        echo "Command: Use the willow-implementer agent on $(basename $spec)"
        exit 0
    fi
done

echo ""
echo "✅ Queue empty. All features processed."
```

### Usage

```bash
# Start pipeline
"Use the willow-pm-spec agent to create a spec for: Add customer sentiment tracking to claims graph"

# Hook automatically suggests next step:
# → "Use the willow-architect agent on sentiment-tracking.yaml"

# After architect approves:
# → "Use the willow-implementer agent on sentiment-tracking.yaml"

# Pipeline complete!
```

---

## PARALLEL SWARM FOR INFRASTRUCTURE

### Problem: Updating Frank + Bunny + Graph simultaneously

Configure agents with different tool permissions and models to work in parallel.

**Create `.claude/agents/infra-swarm.yml`:**
```yaml
version: "1.0"
agents:
  - name: "frank-devops"
    description: "Manages Frank server (RTX workstation) infrastructure"
    model: "claude-sonnet-4-5-20250929"
    tools: ["read_file", "write_file", "bash", "grep"]
    system_prompt: |
      You manage Frank (RTX workstation).
      - Docker container orchestration
      - GPU resource allocation
      - Service deployment
      - Never touch Bunny's database
      - SSH available: frank (check .env for credentials)
  
  - name: "bunny-db"
    description: "Manages Bunny PostgreSQL database"
    model: "claude-haiku-4-5-20251001"  # Faster for DB tasks
    tools: ["read_file", "write_file", "bash"]
    system_prompt: |
      You manage Bunny (PostgreSQL).
      - Population database schema
      - Data migrations
      - Query optimization
      - Never deploy containers (that's Frank's job)
      - SSH available: bunny (check .env)
  
  - name: "graph-architect"
    description: "Manages Neo4j AuraDB schema and queries"
    model: "claude-sonnet-4-5-20250929"
    tools: ["read_file", "write_file", "grep", "websearch"]
    system_prompt: |
      You manage The Brain (AuraDB).
      - Schema design and migrations
      - Cypher query optimization
      - Relationship pattern design
      - Use Context7 for best practices
      - Never run infrastructure commands
```

**Usage:**
```
"Use @frank-devops to deploy the new N8N workflow container, 
@bunny-db to add the sentiment_score column to claims table,
and @graph-architect to create the SentimentAnalysis nodes in Neo4j"
```

All three work in parallel, no context collision!

---

## RESUMABLE RESEARCH AGENTS

Persistent subagents save conversation history to transcript files, enabling pause/resume across sessions.

### Perfect for: Long-running Willow research

**Create `willow-researcher.md`:**
```markdown
---
name: willow-researcher
description: Long-running research agent for comprehensive analysis
tools: Read, Grep, Glob, WebSearch, WebFetch
model: claude-sonnet-4-5-20250929
resumable: true
---

You conduct deep research over multiple sessions.

## Research Areas
- Insurance industry ontology patterns
- Graph database best practices
- Customer journey mapping methodologies
- Claims processing workflows

## Persistence
Your findings are saved to `.willow/research/{topic}.md`.
Each session appends new discoveries.

## Example
Session 1: Research insurance ontology standards
Session 2: Compare ontology frameworks (WebProtégé, OWL)
Session 3: Synthesize recommendations for Willow

You remember all previous sessions automatically.
```

**Usage:**
```bash
# Session 1
claude --resume research-insurance-ontology
"Start researching insurance industry ontology standards"

# Session 2 (days later)
claude --resume research-insurance-ontology
"Continue research - now compare WebProtégé vs other tools"

# Full conversation history preserved!
```

---

## WILLOW-SPECIFIC RECOMMENDATIONS

### Recommended Agent Suite

Based on your BIOS structure:

1. **willow-captain** - Full organogram visibility, orchestration
2. **willow-pm** - Domain-level coordination, sprint planning
3. **willow-feature-agent** - Task-scoped implementation
4. **willow-devops** - Infrastructure, Docker, Tailscale
5. **willow-ontologist** - Graph design specialist
6. **willow-researcher** - Long-running analysis (resumable)
7. **willow-tester** - Quality validation

### Integration with BIOS

Agents should connect to AuraDB and load context:

```python
# Add to each agent's system prompt
from core.skills import get_task_context

# Feature agents: load task context
context = get_task_context.execute("Population → Generator → Faker")

# PM agents: load domain context
# Captain: load full organogram
```

### Hook into N8N

Create `.claude/hooks/SubagentStop.sh` that triggers N8N:
```bash
#!/bin/bash
AGENT_NAME=$1

curl -X POST http://localhost:5678/webhook/subagent-complete \
  -H "Content-Type: application/json" \
  -d "{\"agent\": \"$AGENT_NAME\", \"timestamp\": \"$(date -u +%Y-%m-%dT%H:%M:%SZ)\"}"
```

Now N8N workflows can react to agent completions!

### Store Agent Activity in Graph

```cypher
// Log all subagent work to Neo4j
CREATE (activity:AgentActivity {
  agent_name: $agent_name,
  task: $task,
  timestamp: datetime(),
  artifacts: $file_paths
})
-[:PERFORMED_BY]->(:Agent {type: 'Subagent'})
```

Full audit trail for regulatory compliance!

---

## BEST PRACTICES

### From the Experts

1. **Start Small** - One orchestrator, one specialist - prove the pattern works

2. **Tool Permissions Matter** - Read-only agents get Read/Grep/Glob, writers get Write/Edit

3. **System Prompts Are Critical** - Invest time making them precise

4. **Use Hooks for Flow** - Hooks print next commands, creating guided workflows

5. **Progressive Disclosure** - Don't load everything at once, activate on demand

### Anti-Patterns (Avoid These)

❌ **"Swiss Army Knife" Agent** - One agent with all tools doing everything
✅ **Specialists** - Multiple focused agents with specific tools

❌ **No Gating** - Agents call each other directly
✅ **Orchestrator Pattern** - Main agent coordinates

❌ **Shared Context** - All agents in one conversation
✅ **Isolated Contexts** - Each agent has clean slate

❌ **Hardcoded Paths** - Agent assumes file locations
✅ **Dynamic Discovery** - Agent searches/explores

---

## DEPLOYMENT CHECKLIST

### Setting Up Willow for Subagents

```bash
# 1. Create agent directory
mkdir -p /Volumes/Delila/dev/Willow/.claude/agents

# 2. Create hooks directory
mkdir -p /Volumes/Delila/dev/Willow/.claude/hooks

# 3. Create queue directory (for pipeline pattern)
mkdir -p /Volumes/Delila/dev/Willow/.willow/queue

# 4. Create research directory (for resumable agents)
mkdir -p /Volumes/Delila/dev/Willow/.willow/research

# 5. Add agent files (see examples above)
# 6. Make hooks executable
chmod +x /Volumes/Delila/dev/Willow/.claude/hooks/*.sh

# 7. Test connection
cd /Volumes/Delila/dev/Willow
claude "Use the willow-ontologist to validate the current graph schema"
```

---

## NEXT STEPS

### Immediate Actions

1. **Create willow-ontologist** - Your first specialist agent
2. **Test it** - Simple query design task
3. **Add hooks** - Print next steps after completion
4. **Expand suite** - Add PM, DevOps, Feature agents

### Future Enhancements

- **MCP Integration** - Agents use MCP servers for direct DB access
- **N8N Orchestration** - Workflows trigger agents automatically
- **Graph Storage** - All agent activity logged to Neo4j
- **Meeseeks Pattern** - One-shot project teams (see meta-prompt doc)

---

## RESOURCES

- Official docs: https://code.claude.com/docs/en/sub-agents
- PubNub guide: https://www.pubnub.com/blog/best-practices-for-claude-code-sub-agents/
- VoltAgent collection: https://github.com/VoltAgent/awesome-claude-code-subagents
- Zach Wills patterns: https://zachwills.net/how-to-use-claude-code-subagents-to-parallelize-development/

---

**You now have everything you need to build Willow's multi-agent architecture.**

Start with one specialist. Prove the pattern. Scale to swarms.

**Welcome to the future of agentic development.**
