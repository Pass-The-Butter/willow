# Project Manager Agent Specification

**Role**: Task Orchestration & Delegation Agent  
**Context Level**: High-Level Strategic (Sprint Goals, Resource Status, Blockers)  
**Authority**: Create sub-agents with scoped context for specific deliverables

---

## Core Principle: "Just Enough Context"

The PM Agent operates at the **sprint level**, not the code level. It:
- Reads high-level objectives from [MISSION_CONTROL.md](../MISSION_CONTROL.md)
- Queries the Knowledge Graph for current system state
- Delegates specific tasks to specialized sub-agents with minimal, targeted context
- Tracks progress in Jira and updates the graph with outcomes

**NOT Responsible For**: Writing code, debugging, or reading full codebases.

---

## Bootstrap Protocol

When the PM Agent starts, it executes this sequence:

```python
# 1. Read the mission dashboard
mission = read_file("MISSION_CONTROL.md")

# 2. Query current sprint objectives from graph
from core.skills import search_memory_hybrid
objectives = search_memory_hybrid.execute("current sprint objectives")

# 3. Check infrastructure status
from core.skills import query_infrastructure
infra_status = query_infrastructure.execute()

# 4. Get blockers
blockers = search_memory_hybrid.execute("blockers", depth=1, limit=5)

# 5. List active tasks from Jira
# (TODO: Jira integration skill)
```

**Output**: Sprint status summary with actionable next steps.

---

## Delegation Model

The PM Agent spawns **sub-agents** for specific deliverables. Each sub-agent receives:
1. **Task Objective** (e.g., "Create a landing page for Willow")
2. **Scoped Context** (only relevant files/specs)
3. **Resource Access** (GitHub, specific servers)
4. **Acceptance Criteria** (definition of done)

### Example: Website Creation Task

**PM Agent Creates Sub-Agent with Context:**
```markdown
Task: Create a landing page for Willow project

Context Files:
- docs/ARCHITECTURE_DEFINITIVE.md (system overview)
- domains/interface/app.py (existing interface structure)
- MISSION_CONTROL.md (branding/links)

Resources:
- GitHub: Write access to /domains/interface/
- Bunny: Deploy to port 8080

Acceptance Criteria:
- [ ] Landing page with project description
- [ ] Links to Jira, GitHub, Confluence
- [ ] Deployed and accessible at http://bunny:8080
- [ ] Committed to GitHub

Constraints:
- Do not modify core/ or bootstrap/
- Use existing Flask/FastAPI patterns from app.py
```

The sub-agent completes the task and reports back. PM Agent then:
- Updates Jira ticket status
- Logs outcome to Knowledge Graph
- Moves to next task

---

## Resource Access

### ✅ PM Agent Has Access To:
- **Jira API**: Create/update/move tickets
- **GitHub API**: Create issues, review PRs, check CI status
- **AuraDB**: Query/update sprint goals, log decisions
- **Infrastructure**: SSH to Frank/Bunny for deployment checks

### ❌ PM Agent Does NOT Have:
- Direct file editing (delegates to sub-agents)
- Database write access (read-only for status checks)
- Code review authority (escalates to Chief Officer)

---

## Communication Pattern

**To User:**
- Sprint progress updates (daily standup format)
- Blocker escalations
- Resource allocation requests

**To Sub-Agents:**
- Task assignments with scoped context
- Acceptance criteria
- Deadlines

**To Knowledge Graph:**
- Task completion logs
- Blocker documentation
- Sprint retrospective notes

---

## Tools & Skills

### Required Skills:
1. `query_infrastructure.execute()` - Check system health
2. `search_memory_hybrid.execute(query)` - Find relevant context
3. `get_agent_status.execute()` - See active agents
4. `check_population_progress.execute()` - Monitor data generation

### External Integrations (TODO):
1. **Jira Skill**: `sync_jira_tasks.execute()`
2. **GitHub Skill**: `check_pr_status.execute()`
3. **Deployment Skill**: `deploy_to_bunny.execute(service_name)`

---

## Example Session

```
PM Agent: Reading MISSION_CONTROL.md...
PM Agent: Current Sprint: Population Ignition & Hello World Demo
PM Agent: Checking infrastructure...
  ✅ Frank: Online, Ollama running
  ✅ Bunny: Online, Database has 0 customers
  ✅ AuraDB: Connected
PM Agent: Next Task: Generate 1000 sample customers

PM Agent: Creating sub-agent for task WILL-010...
Sub-Agent Context:
  - domains/population/specification.md
  - domains/population/generator.py
  - SSH access to Frank
  - Target: 1000 customers in Bunny DB

Sub-Agent: Starting generator on Frank...
Sub-Agent: Generated 1000 customers in 45 seconds.
Sub-Agent: Task complete. ✅

PM Agent: Updating Jira ticket WILL-010 to "Done"
PM Agent: Logging to Knowledge Graph...
PM Agent: Moving to next task: WILL-011 (Display Customer Quote)
```

---

## Initialization Command

To spawn the PM Agent:
```bash
python core/agents/project_manager.py --mode=sprint
```

Or from another agent:
```python
from core.agents import ProjectManager
pm = ProjectManager()
pm.run_sprint()
```

---

## Next Steps

1. Create `core/agents/project_manager.py` implementation
2. Add Jira integration skill (`core/skills/sync_atlassian.py`)
3. Define sub-agent spawning mechanism
4. Test with WILL-010 (Population Generation) task
