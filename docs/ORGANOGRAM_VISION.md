# Willow Organogram Vision

**Date**: 2025-12-22  
**Author**: Chief Officer  
**Status**: Vision Document

---

## Core Concept: The Living Organogram

Willow's project structure exists as a **hierarchical graph** in AuraDB, mirroring a corporate organogram where:

- **Root Node**: Project Vision (CEO level)
- **Branch Nodes**: Major features/domains (C-Suite: Population, Interface, Core)
- **Leaf Nodes**: Specific tasks/components (Individual Contributors)

**Key Insight**: When you say "I'm working on Population → Generator → Faker Integration", the system:
1. Traverses to that node in the graph
2. Loads **only the context relevant to that branch**
3. Provides test criteria from parent nodes
4. Reports completion back up the hierarchy

---

## The Organogram Structure

```
Willow (Root)
│
├── Population Domain (VP of Data)
│   ├── Generator (Manager)
│   │   ├── Faker Integration (Task)
│   │   ├── Ollama Integration (Task)
│   │   └── Batch Processing (Task)
│   │
│   ├── Schema (Manager)
│   │   ├── Customer Table (Task)
│   │   ├── Pet Table (Task)
│   │   └── Quote Table (Task)
│   │
│   └── Quality Assurance (Manager)
│       ├── Data Validation (Task)
│       └── Volume Testing (Task)
│
├── Interface Domain (VP of UX)
│   ├── Web App (Manager)
│   │   ├── Landing Page (Task)
│   │   ├── Quote Form (Task)
│   │   └── Dashboard (Task)
│   │
│   └── API (Manager)
│       ├── REST Endpoints (Task)
│       └── WebSocket Events (Task)
│
└── Core Domain (VP of Engineering)
    ├── Skills (Manager)
    │   ├── Memory Search (Task)
    │   ├── Infrastructure Query (Task)
    │   └── Population Check (Task)
    │
    └── Ontology (Manager)
        ├── Schema Design (Task)
        └── Graph Deployment (Task)
```

---

## How It Works

### 1. Context Scoping by Node Position

When you say: **"Let's work on Population → Generator → Faker Integration"**

The system:
```cypher
// Find the node
MATCH (root:Project {name: "Willow"})
      -[:HAS_DOMAIN]->(domain:Domain {name: "Population"})
      -[:HAS_COMPONENT]->(component:Component {name: "Generator"})
      -[:HAS_TASK]->(task:Task {name: "Faker Integration"})

// Get relevant context (parent specs, sibling dependencies)
MATCH (task)-[:REQUIRES]->(spec:Specification)
MATCH (task)-[:DEPENDS_ON]->(dep:Task)
MATCH (component)-[:DEFINED_BY]->(schema:Schema)

RETURN task, spec, dep, schema
```

**Result**: Agent gets:
- Faker Integration task description
- Generator component spec (parent context)
- Schema dependencies (what data structure to follow)
- Sibling tasks (what else needs to align)

**NOT Loaded**: Interface specs, Core ontology details, other domains.

---

### 2. Test-Before-Merge Protocol

Each node has **acceptance criteria** defined by its parent:

```cypher
(:Task {name: "Faker Integration"})
  -[:MUST_SATISFY]->(:TestCriteria {
    validation: "Generate 1000 customers with UK postcodes",
    performance: "Complete in under 60 seconds",
    quality: "Zero NULL fields in required columns"
  })
```

**Workflow**:
1. Agent works on task with scoped context
2. Runs tests defined in `TestCriteria`
3. If pass → Report to Project Manager (parent node)
4. If fail → Log blocker, request help from C-Suite (root)

---

### 3. Hierarchical Knowledge Flow

**Downward**: Requirements, specs, acceptance criteria  
**Upward**: Completions, blockers, RFCs (Request for Comment)

```
CEO (User/Chief Officer)
  ↓ (Strategic direction)
Project Manager (Sprint orchestration)
  ↓ (Task assignment + scoped context)
Feature Agent (Implementation)
  ↑ (Completion report + test results)
Project Manager (Integration check)
  ↑ (Sprint summary + deployment status)
CEO (Approval/Next directive)
```

---

## Proposed Systems

### 1. **Agent Diary System**

Each agent logs their work in the graph as `:DiaryEntry` nodes:

```cypher
CREATE (entry:DiaryEntry {
  agent: "Feature Agent #42",
  timestamp: datetime(),
  task: "Population → Generator → Faker Integration",
  status: "In Progress",
  notes: "Implemented UK postcode generation. Need to verify distribution."
})

// Link to task
MATCH (task:Task {name: "Faker Integration"})
CREATE (task)-[:HAS_DIARY_ENTRY]->(entry)
```

**Query for context**:
```cypher
// Get recent work on this task
MATCH (task:Task {name: "Faker Integration"})-[:HAS_DIARY_ENTRY]->(entries:DiaryEntry)
WHERE entries.timestamp > datetime() - duration('P7D')  // Last 7 days
RETURN entries ORDER BY entries.timestamp DESC
```

---

### 2. **RFC (Request for Comment) System**

Agents propose changes/ideas as `:RFC` nodes:

```cypher
CREATE (rfc:RFC {
  id: "RFC-001",
  title: "Switch from Faker to custom UK address generator",
  author: "Generator Agent",
  rationale: "Faker UK postcodes lack proper geographic distribution",
  status: "Open",
  created: datetime()
})

// Link to affected component
MATCH (component:Component {name: "Generator"})
CREATE (component)-[:HAS_RFC]->(rfc)

// Tag decision-makers
MATCH (pm:Agent {role: "Project Manager"})
CREATE (rfc)-[:NEEDS_REVIEW_BY]->(pm)
```

**Workflow**:
1. Agent creates RFC when encountering design decision
2. PM or Chief Officer reviews
3. RFC status: `Open` → `Approved` / `Rejected` / `Needs Discussion`
4. Approved RFCs become new tasks in organogram

---

### 3. **Intra-Team Messaging**

Agents leave `:Message` nodes for async communication:

```cypher
CREATE (msg:Message {
  from: "Generator Agent",
  to: "Schema Agent",
  subject: "Pet breeds list validation",
  body: "Your pet breeds schema has 150 entries. My generator uses 10. Align?",
  timestamp: datetime(),
  status: "Unread"
})

// Link to relevant context
MATCH (task_from:Task {name: "Faker Integration"}),
      (task_to:Task {name: "Pet Table"})
CREATE (task_from)-[:SENT_MESSAGE]->(msg)-[:TARGETS]->(task_to)
```

**Query unread messages**:
```cypher
MATCH (me:Agent {name: "Schema Agent"})<-[:TARGETS]-(:Message {status: "Unread"})-[:SENT_MESSAGE]-(sender)
RETURN sender, msg
```

---

## Implementation Plan

### Phase 1: Graph Schema (WILL-020)
Create Cypher schema for organogram:
- `:Project`, `:Domain`, `:Component`, `:Task` nodes
- `:HAS_DOMAIN`, `:HAS_COMPONENT`, `:HAS_TASK` relationships
- `:TestCriteria`, `:Specification` linked to tasks

### Phase 2: Context Retrieval Skill (WILL-021)
```python
# core/skills/get_task_context.py
def execute(task_path: str) -> dict:
    """
    task_path: "Population → Generator → Faker Integration"
    Returns: {
      "task": {...},
      "parent_specs": [...],
      "dependencies": [...],
      "acceptance_criteria": {...}
    }
    """
```

### Phase 3: Diary & RFC Skills (WILL-022)
- `log_diary_entry.execute(task, notes)`
- `create_rfc.execute(title, rationale)`
- `send_message.execute(to_agent, subject, body)`

### Phase 4: PM Agent Integration (WILL-023)
PM Agent queries organogram to:
- Assign tasks to sub-agents with scoped context
- Check test criteria before merging
- Review RFCs and respond to messages

---

## Benefits

✅ **Minimal Context Loading**: Agents only see their branch of the tree  
✅ **Clear Accountability**: Each node has an owner (agent/team)  
✅ **Traceability**: Diary entries show who did what, when  
✅ **Collaborative**: RFCs and messages enable async coordination  
✅ **Scalable**: Tree grows as project complexity increases  
✅ **Testable**: Acceptance criteria enforced at each level  

---

## Example Session

**User**: "Let's work on the landing page."

**System**:
```
→ Traversing organogram...
→ Found: Willow → Interface → Web App → Landing Page
→ Loading context:
  - Parent spec: Interface Domain requirements
  - Dependencies: None
  - Acceptance criteria: Mobile responsive, <2s load time
→ Relevant files: domains/interface/templates/index.html

Ready to work on Landing Page task.
```

**Agent**: (Works on task, runs tests)

**System**:
```
→ Tests passed ✅
→ Logging to diary: "Landing page created with responsive design"
→ Reporting to PM Agent...
→ PM Agent: Task marked complete. Moving to next: Quote Form.
```

---

## Notes for Implementation

1. **Start Small**: Manually create organogram for Population domain first
2. **Validate Pattern**: Test context scoping with one task
3. **Automate**: Build skills for diary/RFC/messaging
4. **Expand**: Grow tree as new features are added

**Next Steps**:
- Create `schemas/organogram.cypher` with base structure
- Implement `get_task_context.py` skill
- Test with "Population → Generator" branch
- Roll out to PM Agent

---

**Vision Status**: Captured. Ready to seed into graph.
