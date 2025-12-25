# 🧠 WILLOW BIOS (Basic Input/Output System)

**READ THIS FIRST - EVERY SESSION, EVERY AGENT**

---

## What This Is

This is the **bootstrap protocol** for all Willow agents. Like a computer's BIOS, this runs before anything else. It connects you to the **Brain (AuraDB)** and loads the context you need for your role.

**DO NOT SKIP THIS FILE.**

---

## Step 1: Who Are You?

Your role determines what context you load:

| Role                        | View                             | Access Level                                      |
| --------------------------- | -------------------------------- | ------------------------------------------------- |
| **Captain (Chief Officer)** | Entire organogram                | Full context, all domains                         |
| **Project Manager**         | Sprint objectives, task status   | Domain-level, team coordination                   |
| **Feature Agent**           | Single task branch               | Scoped to your task path only                     |
| **DevOps Manager**          | Infrastructure, Deployment, Logs | Zep, Graphiti, Docker, Tailscale, N8N             |
| **Project Manager**         | Sprint objectives, task status   | Domain-level, team coordination, Linear/Jira Sync |

---

## Step 2: Connect to the Brain

The Brain is **AuraDB** (Neo4j Cloud). All project knowledge lives here.

### Connection Details

```python
# Load credentials
import os
os.environ['NEO4J_URI'] = "neo4j+s://e59298d2.databases.neo4j.io"
os.environ['NEO4J_USER'] = "neo4j"
os.environ['NEO4J_PASSWORD'] = "c2U7h1mwvmYn2k2cr_Fp9EaUrZaLZdEQ3_Cawt6zvyU"

# Or load from .env file
with open('.env', 'r') as f:
    for line in f:
        if '=' in line:
            key, value = line.strip().split('=', 1)
            os.environ[key] = value
```

### Test Connection

```python
from neo4j import GraphDatabase
import certifi
import os

os.environ['SSL_CERT_FILE'] = certifi.where()

driver = GraphDatabase.driver(
    os.getenv('NEO4J_URI'),
    auth=(os.getenv('NEO4J_USER'), os.getenv('NEO4J_PASSWORD'))
)

with driver.session() as session:
    result = session.run("RETURN 'Brain connected!' as message")
    print(result.single()['message'])

driver.close()
```

**Expected Output**: `Brain connected!`

If this fails, **STOP**. You cannot proceed without Brain access.

---

## Step 3: Load Your Context

### 🎖️ For Captain (Chief Officer)

You see **everything**. Load the full organogram:

```python
from neo4j import GraphDatabase
import os
import certifi

os.environ['SSL_CERT_FILE'] = certifi.where()

driver = GraphDatabase.driver(
    os.getenv('NEO4J_URI'),
    auth=(os.getenv('NEO4J_USER'), os.getenv('NEO4J_PASSWORD'))
)

with driver.session() as session:
    # Get full project overview
    result = session.run("""
        MATCH (p:Project)-[:HAS_DOMAIN]->(d:Domain)
        OPTIONAL MATCH (d)-[:HAS_COMPONENT]->(c:Component)
        OPTIONAL MATCH (c)-[:HAS_TASK]->(t:Task)
        RETURN p.name as project,
               d.name as domain,
               collect(DISTINCT c.name) as components,
               collect(DISTINCT {name: t.name, status: t.status}) as tasks
        ORDER BY d.name
    """)

    print("=" * 80)
    print("CAPTAIN'S FULL CONTEXT")
    print("=" * 80)
    for record in result:
        print(f"\n{record['domain']} Domain:")
        print(f"  Components: {', '.join(record['components'])}")
        print(f"  Tasks: {len([t for t in record['tasks'] if t['name']])} total")

driver.close()
```

**You also need**:

- Infrastructure status: `python core/skills/query_infrastructure.py`
- Recent decisions: `python core/skills/search_memory_hybrid.py "recent decisions"`
- Open RFCs: Query `(:RFC {status: "Open"})`

---

### 📋 For Project Manager

You see **domain-level** context and sprint objectives:

```python
from core.skills import get_task_context

# Get current sprint tasks
with driver.session() as session:
    result = session.run("""
        MATCH (t:Task)
        WHERE t.status IN ['In Progress', 'Not Started']
        OPTIONAL MATCH (t)-[:DEPENDS_ON]->(dep:Task {status: 'Not Started'})
        RETURN t.name as task,
               t.status as status,
               collect(dep.name) as blockers
        ORDER BY t.status DESC
    """)

    print("CURRENT SPRINT STATUS:")
    for record in result:
        status_icon = "🟡" if record['status'] == 'In Progress' else "⚪"
        print(f"{status_icon} {record['task']}: {record['status']}")
        if record['blockers']:
            print(f"   ⚠️  Blocked by: {', '.join(record['blockers'])}")
```

**You also need**:

- Jira sync: `python bootstrap/sync_atlassian.py` (TODO: implement)
- Team messages: Query `(:Message {status: "Unread"})`
- **Role Definition**: Read `core/roles/project_manager.md` for your prime directive.

---

### 🔧 For Feature Agent

You see **only your task branch**. This is the "Just Enough Context" principle.

**YOU MUST KNOW YOUR TASK PATH**. Ask your PM or Captain if unsure.

```python
from core.skills import get_task_context

# Example: You're working on Faker Integration
task_path = "Population → Generator → Faker Integration"

context = get_task_context.execute(task_path)

print(f"Task: {context['task']['name']}")
print(f"Status: {context['task']['status']}")
print(f"Spec: {context['specification']}")
print(f"Criteria: {context['acceptance_criteria']}")
print(f"Dependencies: {context['dependencies']}")
print(f"Recent diary: {len(context['diary_entries'])} entries")
print(f"Unread messages: {len(context['messages'])}")
```

**Output**: All context for your specific task. Nothing else.

---

## Step 4: Read Updates

### Check Diary Entries

```python
# Get last 7 days of work on your task
with driver.session() as session:
    result = session.run("""
        MATCH (t:Task {name: $task_name})-[:HAS_DIARY_ENTRY]->(d:DiaryEntry)
        WHERE d.timestamp > datetime() - duration('P7D')
        RETURN d.agent as agent,
               d.timestamp as when,
               d.notes as notes
        ORDER BY d.timestamp DESC
    """, task_name="Faker Integration")

    print("RECENT WORK:")
    for record in result:
        print(f"- {record['when']}: {record['agent']}")
        print(f"  {record['notes']}")
```

### Check Messages

```python
# Get unread messages for your task
with driver.session() as session:
    result = session.run("""
        MATCH (t:Task {name: $task_name})<-[:TARGETS]-(m:Message {status: "Unread"})
        RETURN m.from as from,
               m.subject as subject,
               m.body as body
    """, task_name="Faker Integration")

    for record in result:
        print(f"📧 From {record['from']}: {record['subject']}")
        print(f"   {record['body']}")
```

---

## Step 5: Log Your Work

**ALWAYS LOG BEFORE YOU FINISH**. The Brain must know what you did.

```python
from datetime import datetime

with driver.session() as session:
    session.run("""
        MATCH (t:Task {name: $task_name})
        CREATE (t)-[:HAS_DIARY_ENTRY]->(d:DiaryEntry {
            agent: $agent_name,
            timestamp: datetime(),
            status: $status,
            notes: $notes
        })
    """,
    task_name="Faker Integration",
    agent_name="Your Name Here",
    status="In Progress",
    notes="Brief description of what you did"
    )
```

---

## Step 6: Update Status (PM/Captain Only)

When a task is complete:

```python
with driver.session() as session:
    session.run("""
        MATCH (t:Task {name: $task_name})
        SET t.status = 'Complete',
            t.completed_at = datetime()
    """, task_name="Faker Integration")
```

---

## Quick Reference: Essential Queries

### Captain's Dashboard

```cypher
// All domains and their health
MATCH (d:Domain)-[:HAS_COMPONENT]->(c:Component)-[:HAS_TASK]->(t:Task)
RETURN d.name as domain,
       count(t) as total_tasks,
       sum(CASE WHEN t.status = 'Complete' THEN 1 ELSE 0 END) as completed
```

### PM's Sprint View

```cypher
// Current sprint tasks
MATCH (t:Task)
WHERE t.status IN ['In Progress', 'Not Started']
RETURN t.name, t.status, t.assignee
ORDER BY t.status DESC
```

### Agent's Task Context

```cypher
// Get my task details
MATCH (t:Task {name: "Your Task Name"})
OPTIONAL MATCH (t)-[:REQUIRES]->(spec:Specification)
OPTIONAL MATCH (t)-[:MUST_SATISFY]->(criteria:TestCriteria)
RETURN t, spec, criteria
```

---

## Infrastructure Context (All Roles)

After connecting to the Brain, check infrastructure:

```python
from core.skills import query_infrastructure

status = query_infrastructure.execute()
print(f"Frank: {status['frank']}")
print(f"Bunny: {status['bunny']}")
print(f"AuraDB: {status['auradb']}")
```

---

## Common Errors

### "URI scheme b'' is not supported"

**Fix**: Environment variables not loaded. Run `source .env` first.

### "Connection refused"

**Fix**: Tailscale not running or not connected to network.

### "Task not found in organogram"

**Fix**: Your task path is wrong. Check spelling or ask Captain for correct path.

### "No diary entries"

**Fix**: This is a new task. Start logging your work now.

---

## The Golden Rules

1. **Connect to Brain first** - Nothing works without AuraDB access
2. **Load only your context** - Don't query the whole graph unless you're Captain
3. **Log your work** - Diary entries are mandatory
4. **Check dependencies** - Don't start if blocked
5. **Test before reporting** - Acceptance criteria must pass
6. **Ask up the tree** - Blocked? Message your PM or Captain

---

## Bootstrap Script (Copy-Paste)

```bash
#!/bin/bash
# Willow BIOS Bootstrap

echo "🧠 Willow BIOS - Booting..."

# 1. Load environment
cd /path/to/Willow
source .venv/bin/activate
source .env

# 2. Test Brain connection
python -c "
from neo4j import GraphDatabase
import os
import certifi
os.environ['SSL_CERT_FILE'] = certifi.where()
driver = GraphDatabase.driver(os.getenv('NEO4J_URI'), auth=(os.getenv('NEO4J_USER'), os.getenv('NEO4J_PASSWORD')))
with driver.session() as s:
    result = s.run('RETURN \"Connected!\" as msg')
    print(result.single()['msg'])
driver.close()
"

# 3. Load your context (adjust based on role)
echo "📚 Loading context..."
python core/skills/get_task_context.py  # Feature Agent
# OR
# python core/skills/query_infrastructure.py  # Captain/PM

echo "✅ BIOS complete. Ready to work."
```

---

**END OF BIOS**

You are now connected to the Brain and have the context you need. Proceed with your work.

**Remember**: The Brain (organogram) is the source of truth. When in doubt, query it.
