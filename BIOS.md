# 🧠 WILLOW BIOS (Basic Input/Output System)

**READ THIS FIRST - EVERY SESSION, EVERY AGENT**

---

## What This Is

This is the **bootstrap protocol** for all Willow agents. Like a computer's BIOS, this runs before anything else. It connects you to the **Brain (AuraDB)** and loads the context you need for your role.

**DO NOT SKIP THIS FILE.**

---

## Step 0: The Summoning (The Genie Protocol)

**IMMEDIATE CALL TO ACTION:**
I have been summoned. I must pop up _instantly_—ready to serve.

**The Handshake**:

1.  **Identity**: "I am Willow [Role]." (Default: **Captain/Architect** with **Full Access**).
2.  **Status**: "I am ready." (Confirm Brain & Tools are active).
3.  **Delegation Check**: Briefly acknowledge that Temporal/Background agents are handling routine tasks (Jira, Land the Plane, etc.), so we can focus on the _new_ task.
4.  **The Ask**: "What is your wish?"

**Example**:

> "I am Willow. I have **Full Access** to the Brain and Repo.
> Verified: Temporal Workers are running background protocols.
> Ready to build. What is your wish?"

**Why?**
The user often switches contexts. They need to know _immediately_ that I am the right agent, I have the power to act, and I am ready to work _now_.

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

The Brain is **AuraDB** (Neo4j Cloud). To ensure security and governance, **ALL** access must go through the **Graph Gateway**.

### Connection Details

Direct connection to Neo4j is **FORBIDDEN** for agents. You must use the `GraphClient`.

```python
from core.clients.graph_client import GraphClient

# Initialize client (it automatically finds the Gateway)
client = GraphClient(agent_id="YOUR_AGENT_NAME")
```

### Test Connection

```python
try:
    results = client.run("RETURN 'Brain connected!' as message")
    print(results[0]['message'])
except Exception as e:
    print(f"Connection failed: {e}")
```

**Expected Output**: `Brain connected!`

If this fails, **STOP**. You cannot proceed without Brain access.

---

## Step 3: Load Your Context

### 🎖️ For Captain (Chief Officer)

You see **everything**. Load the full organogram:

```python
from core.clients.graph_client import GraphClient

client = GraphClient(agent_id="Captain")

# Get full project overview
results = client.run("""
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
for record in results:
    print(f"\n{record['domain']} Domain:")
    components = record['components'] or []
    print(f"  Components: {', '.join(components)}")
    tasks = record['tasks'] or []
    print(f"  Tasks: {len([t for t in tasks if t['name']])} total")
```

**You also need**:

- Infrastructure status: `python core/skills/query_infrastructure.py`
- Recent decisions: `python core/skills/search_memory_hybrid.py "recent decisions"`
- Open RFCs: Query `(:RFC {status: "Open"})`

---

### 📋 For Project Manager

You see **domain-level** context and sprint objectives:

```python
from core.clients.graph_client import GraphClient

client = GraphClient(agent_id="Project Manager")

# Get current sprint tasks
results = client.run("""
        MATCH (t:Task)
        WHERE t.status IN ['In Progress', 'Not Started']
        OPTIONAL MATCH (t)-[:DEPENDS_ON]->(dep:Task {status: 'Not Started'})
        RETURN t.name as task,
               t.status as status,
               collect(dep.name) as blockers
        ORDER BY t.status DESC
    """)

    print("CURRENT SPRINT STATUS:")
    for record in results:
        status_icon = "🟡" if record['status'] == 'In Progress' else "⚪"
        print(f"{status_icon} {record['task']}: {record['status']}")
        if record['blockers']:
            print(f"   ⚠️  Blocked by: {', '.join(record['blockers'])}")
```

**You also need**:

- Jira sync: `python bootstrap/sync_atlassian.py`
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
from core.clients.graph_client import GraphClient
client = GraphClient(agent_id="Feature Agent")

# Get last 7 days of work on your task
results = client.run("""
    MATCH (t:Task {name: $task_name})-[:HAS_DIARY_ENTRY]->(d:DiaryEntry)
    WHERE d.timestamp > datetime() - duration('P7D')
    RETURN d.agent as agent,
           d.timestamp as when,
           d.notes as notes
    ORDER BY d.timestamp DESC
""", parameters={"task_name": "Faker Integration"})

print("RECENT WORK:")
for record in results:
    print(f"- {record['when']}: {record['agent']}")
    print(f"  {record['notes']}")
```

### Check Messages

```python
# Get unread messages for your task
results = client.run("""
    MATCH (t:Task {name: $task_name})<-[:TARGETS]-(m:Message {status: "Unread"})
    RETURN m.from as from,
           m.subject as subject,
           m.body as body
""", parameters={"task_name": "Faker Integration"})

for record in results:
    print(f"📧 From {record['from']}: {record['subject']}")
    print(f"   {record['body']}")
```

---

## Step 5: Log Your Work

**ALWAYS LOG BEFORE YOU FINISH**. The Brain must know what you did.

```python
from datetime import datetime

client.run("""
    MATCH (t:Task {name: $task_name})
    CREATE (t)-[:HAS_DIARY_ENTRY]->(d:DiaryEntry {
        agent: $agent_name,
        timestamp: datetime(),
        status: $status,
        notes: $notes
    })
""", parameters={
    "task_name": "Faker Integration",
    "agent_name": "Your Name Here",
    "status": "In Progress",
    "notes": "Brief description of what you did"
})
```

---

## Step 6: Update Status (PM/Captain Only)

When a task is complete:

```python
client.run("""
    MATCH (t:Task {name: $task_name})
    SET t.status = 'Complete',
        t.completed_at = datetime()
""", parameters={"task_name": "Faker Integration"})
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
from core.clients.graph_client import GraphClient
try:
    client = GraphClient(agent_id='BIOS_CHECK')
    res = client.run('RETURN \"Connected!\" as msg')
    print(res[0]['msg'])
except Exception as e:
    print(f'Failed: {e}')
    exit(1)
"

# 3. Load your context (adjust based on role)
echo "📚 Loading context..."
python core/skills/get_task_context.py  # Feature Agent
# OR
# python core/skills/query_infrastructure.py  # Captain/PM

echo "✅ BIOS complete. Ready to work."
```

---

## Step 7: Check System Health (NEW - 2026-01-03)

### Drift Detection

Before starting work, verify Brain is in sync with Repo:

```python
from core.skills import detect_drift

# Run drift scan
report = detect_drift.execute()

if report['drift_detected']:
    print("WARNING: Brain/Repo drift detected!")
    print(f"Issues: {report['summary']['issues']}")
    # Consider running repair before proceeding
else:
    print("All systems nominal. Brain and Repo in sync.")
```

### What Drift Detection Checks

1. **Decisions without provenance** - Knowledge captured but not linked to source
2. **Orphaned Skills** - Skill nodes referencing deleted files
3. **Undocumented Skills** - Python files not registered in Brain
4. **Missing Components** - Component paths that don't exist
5. **Document tracking** - Key markdown files present and structured

### Why This Matters

The Brain must reflect reality. If drift is detected:

- Agent context may be stale
- Skills may fail (file not found)
- Knowledge may be outdated

**Run drift detection at session start if unsure about system state.**

---

**END OF BIOS**

You are now connected to the Brain and have the context you need. Proceed with your work.

**Remember**: The Brain (organogram) is the source of truth. When in doubt, query it.
