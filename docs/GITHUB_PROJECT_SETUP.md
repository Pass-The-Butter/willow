# GitHub Project Board Setup for Willow

**Jira Board**: [Agile Meshnet Jira (SCRUM)](https://agilemeshnet.atlassian.net/jira/software/projects/SCRUM/boards/1)

## Project Name
**Willow - Autonomous Graph Ontology System**

## Project Description
Self-describing ontology system where capabilities, memory, and roadmap live as graph nodes. The specification IS the product.

## Board Structure

### Columns

1. **📥 Backlog**
   - All tasks not yet prioritized
   - Ideas and proposals
   - Tasks waiting for dependencies

2. **🎯 Next Sprint**
   - Tasks planned for upcoming sprint
   - Prioritized and ready to start
   - No blockers

3. **🔄 In Progress**
   - Currently being worked on
   - Limited WIP (max 3 tasks)
   - Assigned to specific agent/human

4. **✅ Done**
   - Completed tasks
   - Verified and tested
   - Merged to main branch

5. **🧊 Frozen**
   - Good ideas, not now
   - Future enhancements
   - Waiting for strategic decision

## Labels

### Priority
- 🔴 `priority: critical` - Blocks everything
- 🟠 `priority: high` - Important for current sprint
- 🟡 `priority: medium` - Nice to have
- 🟢 `priority: low` - Future consideration

### Type
- `type: infrastructure` - Docker, servers, deployment
- `type: schema` - Graph ontology design
- `type: skill` - New skill creation
- `type: integration` - External service connection
- `type: documentation` - README, guides, specs
- `type: bug` - Something broken
- `type: enhancement` - Improvement to existing feature

### Sprint
- `sprint: bootstrap` - Initial infrastructure setup
- `sprint: population` - Synthetic customer generation
- `sprint: pet-claims` - Insurance journey implementation
- `sprint: vr-interface` - MetaQuest 3 visualization (frozen)

### Assignment
- `assigned: claude` - AI agent task
- `assigned: peter` - Human review/decision
- `assigned: team` - Collaborative task

## Milestones

### M1: Bootstrap Complete (Week 1)
- [ ] Docker containers running
- [ ] Skills executing successfully
- [ ] AuraDB schema loaded
- [ ] GitHub repo initialized

### M2: Population System Live (Week 2)
- [ ] Postgres database on bunny server
- [ ] 10M synthetic NPCs generated
- [ ] Vector personalities implemented
- [ ] Integration with Willow tested

### M3: Pet Claims Demo (Week 3)
- [ ] Customer journey ontology implemented
- [ ] MSSQL data ingested
- [ ] Claims lifecycle tracked
- [ ] Demo ready for Claims Department

### M4: Self-Managing System (Week 4)
- [ ] Tasks stored as graph nodes
- [ ] Claude can query roadmap
- [ ] Autonomous skill creation working
- [ ] Brand evolution integrated

## Initial Issues to Create

### Bootstrap Sprint (WILL-001 to WILL-006)
```markdown
**WILL-001: Reorganize file structure**
- Labels: priority: critical, type: infrastructure, sprint: bootstrap
- Description: Move files to match docker-compose paths
- Assigned: claude

**WILL-002: Fix autumn BrandAsset**
- Labels: priority: low, type: bug, sprint: bootstrap
- Description: Logo URL syntax error in schema
- Assigned: claude

**WILL-003: Start Docker containers**
- Labels: priority: critical, type: infrastructure, sprint: bootstrap
- Description: docker-compose up -d --build
- Assigned: claude
- Blocked by: WILL-001

**WILL-004: Test get_skills()**
- Labels: priority: high, type: skill, sprint: bootstrap
- Description: Verify MCP can query skills
- Assigned: claude
- Blocked by: WILL-003

**WILL-005: Test hello_world execution**
- Labels: priority: high, type: skill, sprint: bootstrap
- Description: Execute hello_world via API
- Assigned: claude
- Blocked by: WILL-003

**WILL-006: Test retrieve_conversation_context**
- Labels: priority: high, type: skill, sprint: bootstrap
- Description: Query decisions by keyword
- Assigned: claude
- Blocked by: WILL-003
```

### Population Sprint (WILL-007 to WILL-011)
```markdown
**WILL-007: SSH to bunny server**
- Labels: priority: high, type: infrastructure, sprint: population
- Description: Verify access to 128GB Xeon
- Assigned: claude

**WILL-008: Design Population schema**
- Labels: priority: medium, type: schema, sprint: population
- Description: Postgres tables for NPCs
- Assigned: claude
- Blocked by: WILL-007

**WILL-009: Create Population generator**
- Labels: priority: medium, type: skill, sprint: population
- Description: Faker-based customer generator
- Assigned: claude
- Blocked by: WILL-008

**WILL-010: Generate 10M NPCs**
- Labels: priority: low, type: infrastructure, sprint: population
- Description: Run generator at scale
- Assigned: claude
- Blocked by: WILL-009

**WILL-011: Add vector embeddings**
- Labels: priority: low, type: enhancement, sprint: population
- Description: Personality vectors for similarity
- Assigned: claude
- Blocked by: WILL-009
```

### Pet Claims Sprint (WILL-012 to WILL-015)
```markdown
**WILL-012: Design Pet Claims sub-ontology**
- Labels: priority: high, type: schema, sprint: pet-claims
- Description: Customer journey graph structure
- Assigned: claude

**WILL-013: Implement journey schema**
- Labels: priority: high, type: schema, sprint: pet-claims
- Description: Jerry→Barry→Quote→Policy→Claim
- Assigned: claude
- Blocked by: WILL-012

**WILL-014: Connect MSSQL database**
- Labels: priority: medium, type: integration, sprint: pet-claims
- Description: Ingest real claims data
- Assigned: claude
- Status: BLOCKED (waiting for credentials)

**WILL-015: Accumulating Snapshot for Claims**
- Labels: priority: medium, type: schema, sprint: pet-claims
- Description: Track claim state changes
- Assigned: claude
- Blocked by: WILL-013
```

### GitHub Tasks (WILL-016 to WILL-019)
```markdown
**WILL-016: Initialize Git repo**
- Labels: priority: high, type: infrastructure, sprint: bootstrap
- Description: .gitignore, initial commit
- Assigned: claude

**WILL-017: Push to GitHub**
- Labels: priority: medium, type: infrastructure, sprint: bootstrap
- Description: github.com/Pass-The-Butter/willow
- Assigned: claude
- Blocked by: WILL-016

**WILL-018: Create GitHub Project board**
- Labels: priority: medium, type: documentation, sprint: bootstrap
- Description: Kanban with 5 columns
- Assigned: claude
- Status: IN PROGRESS

**WILL-019: Sync AuraDB to GitHub Issues**
- Labels: priority: low, type: integration, sprint: bootstrap
- Description: Task nodes → GitHub issues
- Assigned: claude
- Blocked by: WILL-018
```

### Frozen Tasks (WILL-020 to WILL-023)
```markdown
**WILL-020: Canva MCP integration**
- Labels: priority: low, type: integration
- Status: FROZEN (good idea, not now)

**WILL-021: VR interface (MetaQuest 3)**
- Labels: priority: low, type: enhancement, sprint: vr-interface
- Status: FROZEN (future enhancement)

**WILL-022: Pricing engine**
- Labels: priority: low, type: enhancement
- Status: FROZEN (using random prices for MVP)

**WILL-023: Process documents in graph**
- Labels: priority: low, type: schema
- Status: FROZEN (design structure first)
```

## Automation Rules

### When Issue is Created
- Auto-add to Backlog column
- Add "needs-triage" label

### When Issue is Assigned
- Move to Next Sprint if priority >= medium
- Remove "needs-triage" label

### When PR is Linked
- Move issue to In Progress
- Add "in-development" label

### When PR is Merged
- Move issue to Done
- Auto-close issue
- Add "deployed" label

## GitHub Actions (Future)

```yaml
# .github/workflows/sync-auradb-tasks.yml
name: Sync Tasks to AuraDB
on:
  issues:
    types: [opened, edited, closed, reopened]

jobs:
  sync:
    runs-on: ubuntu-latest
    steps:
      - name: Update Task Node in AuraDB
        run: |
          # Cypher query to create/update Task node
          # Mirror GitHub issue state to graph
```

## How This Works

1. **Peter creates GitHub issue** → Task appears in Backlog
2. **Peter moves to Next Sprint** → Task becomes queryable by Claude
3. **Claude queries AuraDB** → `MATCH (t:Task {status: 'todo'}) RETURN t`
4. **Claude completes work** → Updates task in graph
5. **Sync script runs** → GitHub issue moves to Done
6. **Both systems stay in sync** → Specification = Product

---

**The Meta Loop:**
- GitHub = Human interface
- AuraDB = Claude interface
- Tasks exist in both
- Changes propagate bidirectionally
- The roadmap manages itself 🌳
