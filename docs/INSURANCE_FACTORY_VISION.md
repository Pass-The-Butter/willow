# The Insurance Factory Vision
**Collated from Willow Project Memory**
**Date**: 2026-01-03
**Status**: Living Vision Document

---

## Executive Summary

The **Insurance Factory** is Willow's core mission: a **fully autonomous insurance ecosystem simulation** where synthetic entities (NPCs) flow through realistic customer journeys, generating claims, requesting quotes, and interacting with policies—all underpinned by a living knowledge graph ontology.

**Key Innovation**: Unlike traditional insurance systems modeled around business silos (underwriting, claims, finance), the Insurance Factory is designed **customer-first**. The ontology emerges from the customer journey story itself.

---

## The Foundation Story: Jerry & Barry

The entire ontology is anchored to a single narrative:

### The Journey
1. **Jerry finds Barry** - A man adopts a Labrador puppy
2. **Jerry requests a quote** - Via Purely Pets Insurance website
3. **Jerry purchases a policy** - Lifetime cover, £7k vet fee limit
4. **Barry gets sick** - Hip dysplasia symptoms appear
5. **Jerry takes Barry to vet** - Diagnosis and treatment plan
6. **Vet diagnoses Barry** - Medical documentation created
7. **Jerry submits a claim** - Claim documents uploaded
8. **Claim is assessed** - Against policy rules and coverage limits
9. **Claim is paid** - Jerry receives reimbursement

### The Ontology Insight

**This story IS the schema.** Not business departments, not technical abstractions—the customer experience defines the graph structure:

```cypher
// The core relationships emerge from the story
(:Customer {name: "Jerry"})-[:FOUND]->(:Pet {name: "Barry"})
(:Customer)-[:REQUESTED]->(:Quote)
(:Quote)-[:FOR_PET]->(:Pet)
(:Quote)-[:CONVERTED_TO]->(:Policy)
(:Policy)-[:COVERS]->(:Pet)
(:Pet)-[:DIAGNOSED_WITH]->(:Condition {name: "Hip Dysplasia"})
(:Customer)-[:SUBMITTED]->(:Claim)
(:Claim)-[:AGAINST]->(:Policy)
(:Claim)-[:FOR_PET]->(:Pet)
(:Claim)-[:ASSESSED_BY]->(:Underwriter)
(:Claim)-[:RESULTED_IN]->(:Payment)
```

**Decision Captured in Brain**:
> "Build educational presentation with pet insurance narrative. Demonstrates SQL→Graph transformation using relatable customer journey story."

---

## The Population: 100 Million NPCs

### Scale & Realism

The Insurance Factory requires a **massive synthetic population** to enable realistic simulations:

- **Target Scale**: 100 Million entities (customers + pets)
- **Current Implementation**: Purely Pets Insurance product model
- **Data Store**: Postgres 15 + `pgvector` on Bunny (Xeon Server, 128GB RAM)

### Population Architecture

#### Customers (Primary Entities)
Aligned with **Purely Pets quote form** fields:
- Full Name, Email, Phone (UK mobile format)
- Address (UK format with postcodes)
- Date of Birth (18-80 years old)
- **Personality Vector** (384 dimensions for similarity search)
- **Marketing Segment** (cat person, dog person, multi-pet, etc.)

**Demographics (UK-Focused)**:
- Age distribution skewed 25-45 (typical pet owners)
- 30% of customers own pets (realistic UK rate)
- UK-specific: Valid postcodes, British addresses, en_GB locale

#### Pets (Linked Entities)
Aligned with **Purely Pets pet details** form:
- Pet Name, Species (Dog/Cat), Breed
- Date of Birth (0-15 years, insurance limit)
- Gender, Microchipped (70% rate, UK standard)
- Pre-existing Conditions (10-15% of pets)
- Acquired Date

**Realistic Constraints**:
- 60% dogs, 40% cats (UK ratio)
- Common UK breeds (Labrador, British Shorthair, etc.)
- Microchip rate matches UK statistics

#### Quotes & Policies
Generated interactions tracking customer behavior:
- Cover Type (Lifetime 60%, Time Limited 30%, Accident Only 10%)
- Excess Amount (£0, £99, £149, £199)
- Vet Fee Limit (£2k, £4k, £7k, £12k)
- Premium calculations
- Status tracking (generated → accepted → expired)

### Generation Strategy

**Phase 1: Faker + UK Locale**
```python
from faker import Faker
fake = Faker('en_GB')  # UK postcodes, addresses, phone numbers

# Generate demographics
customer = {
    'full_name': fake.name(),
    'email': fake.email(),
    'phone_mobile': fake.phone_number(),
    'postcode': fake.postcode(),
    'date_of_birth': fake.date_of_birth(min_age=18, max_age=80)
}
```

**Phase 2: Ollama Integration** (Local LLM on Frank - RTX 3090Ti)
- Generate personality vectors via embeddings
- Semantic traits: "cat lover", "urban dweller", "gym enthusiast"
- Enable similarity search for marketing segmentation

**Decision from Brain**:
> "Local Ollama agent for bulk NPC generation. RTX 3090 Ti handles Faker-based generation of 10M NPCs. Saves Claude credits, faster parallel generation."

### Vector-Powered Marketing

**Use Case**: Find similar customers via personality vectors
```sql
-- Find 100 customers most similar to customer #12345
SELECT * FROM customers
ORDER BY personality_vector <-> (
    SELECT personality_vector FROM customers WHERE id = 12345
)
LIMIT 100;
```

**Applications**:
- Cat lovers → New cat insurance products
- Allergy sufferers → Hypoallergenic pet food partnerships
- Geographic clustering → Local event marketing
- Behavioral patterns → Churn prediction

---

## Event-Driven Intelligence

### News-Based Proactive Marketing

**Example: Slough Cat Strangler Returns**

The Factory monitors external events and triggers intelligent responses:

1. **Detect Event**: News feed reports "Slough Cat Strangler seen again"
2. **Parse Context**:
   - Location: "Slough" → Postcode area "SL"
   - Threat: "Cat Strangler" → Species: Cat
3. **Query Population**:
   ```cypher
   MATCH (c:Customer)-[:OWNS]->(p:Pet {species: 'Cat'})
   WHERE c.postcode STARTS WITH 'SL'
   RETURN c.email, p.pet_name
   ```
4. **Generate Campaign**:
   - Subject: "Protect [PetName] - Slough Cat Strangler Alert"
   - Content: Safety tips + insurance coverage info
5. **Execute**: Auto-send or route to marketing approval

### Event Sources

- **News APIs**: Disease outbreaks, product recalls, local incidents
- **Weather Events**: Storms → Travel insurance for pets
- **Legislative Changes**: Microchip requirements, breed bans
- **Vet Alerts**: Health warnings, safety notices
- **Calendar Events**: Policy renewals, pet birthdays

### Email Inbox Automation

Cloud agent monitors shared inbox:
- **Claim documents from vets** → Extract claim ID, parse attachments, update Claim node status
- **Customer responses** → Info requests automatically processed
- **Partner communications** → Reinsurance updates trigger workflow changes

**No human intervention required** for routine processing.

---

## Distributed Agent Architecture

### Any Agent, Anywhere

**Core Principle**: By storing tasks, decisions, and skills as graph nodes, **any agent** can query "what needs doing?" and execute autonomously.

**Agent Types**:
- **Claude Sonnet 4.5** (Orchestration, reasoning, architecture)
- **Local Ollama** (RTX 3090Ti for bulk generation)
- **GitHub PR agents** (Automated code fixes)
- **N8N workflows** (Sprite generation, email monitoring)
- **Cloud agents** (Email watchers, news scrapers)

**Example Workflows**:
1. **Doris turns 60** → N8N generates birthday SVG sprite → Updates User node
2. **Claim documents arrive via email** → Cloud agent extracts, updates Claim status → Triggers assessment
3. **News: Vet recall** → Scraper detects → Queries affected pets → Marketing campaign auto-generated

**Insight from Brain**:
> "Graph-based specification enables distributed agent coordination without central orchestrator."

---

## The Living Ontology

### Spec-Driven Architecture

**Fundamental Principle**: The Graph (Spec + Memory) is the source of truth. Code is a **projection**.

```
┌──────────────────────────────────────┐
│     AuraDB (The Brain)               │
│                                      │
│  - Ontology (Entities & Relations)   │
│  - Skills (Capabilities as Nodes)    │
│  - Decisions (Why we built things)   │
│  - Tasks (What needs doing)          │
│  - Memory (Episodic + Semantic)      │
└──────────┬───────────────────────────┘
           │
           │ Projects to...
           ↓
┌──────────────────────────────────────┐
│   Code, Schemas, Documentation       │
│   (Generated from graph)             │
└──────────────────────────────────────┘
```

### Three Memory Pillars

| Pillar | Technology | Purpose | Example |
|--------|-----------|---------|---------|
| **Episodic** | Neo4j `:Session`, `:Turn` | "What did we say?" | Conversation logs linked to tasks |
| **Beads** | Neo4j `:Bead` | "What am I doing?" | Task state management, work units |
| **Graphiti** | Docker Service (Bunny) | "What happened?" | Temporal events, entity interactions |

### Self-Describing System

**Skills stored as graph nodes**:
```cypher
(:Skill {
  name: 'hello_world',
  language: 'python',
  code_path: '/core/skills/hello_world.py',
  mcp_compatible: true,
  description: 'First skill - proves the system works'
})
```

**Any agent can query**: "What can I do?"
```cypher
MATCH (s:Skill) RETURN s.name, s.description
```

**System becomes introspectable and self-aware.**

---

## The Organogram Pattern

### Hierarchical Context Scoping

Project structure as a **corporate organogram**:

```
Willow (CEO)
│
├── Population Domain (VP of Data)
│   ├── Generator (Manager)
│   │   ├── Faker Integration (Task)
│   │   ├── Ollama Integration (Task)
│   │   └── Batch Processing (Task)
│   │
│   └── Schema (Manager)
│       ├── Customer Table (Task)
│       └── Pet Table (Task)
│
├── Interface Domain (VP of UX)
│   └── Web App (Manager)
│       ├── Landing Page (Task)
│       └── Quote Form (Task)
│
└── Core Domain (VP of Engineering)
    ├── Skills (Manager)
    └── Ontology (Manager)
```

### Just Enough Context

When agent says: **"Work on Population → Generator → Faker Integration"**

System queries:
```cypher
MATCH (root:Project {name: "Willow"})
  -[:HAS_DOMAIN]->(domain:Domain {name: "Population"})
  -[:HAS_COMPONENT]->(component:Component {name: "Generator"})
  -[:HAS_TASK]->(task:Task {name: "Faker Integration"})
MATCH (task)-[:REQUIRES]->(spec:Specification)
MATCH (task)-[:DEPENDS_ON]->(dep:Task)
RETURN task, spec, dep
```

**Agent receives**:
- Task description
- Parent component spec
- Dependencies
- Acceptance criteria

**Agent does NOT receive**: Interface specs, other domains, unrelated context

**Minimal context loading** = Efficient agent operation

---

## VR & Visualization (Future State)

### MetaQuest 3 Graph Walkthrough

**Vision**: Render entire graph as walkable 3D space

- Each entity has sprite model (`customer.glb`, `dog_labrador.glb`)
- Spatial position: `{x, y, z}`
- Real-time multi-user MMOG-style interface
- **Navigate customer journey by walking through the graph**

**Use Cases**:
- Claims adjuster "walks" through claim dependencies
- Management sees system overview in 3D
- Training: New employees explore ontology spatially
- Customer presentations: Show Jerry & Barry's journey visually

### Sprite Generation Pipeline

**N8N Workflow**:
1. New `:Customer` node created in graph
2. Webhook triggers N8N
3. Local agent generates personalized SVG avatar
4. Upload to storage or embed in node property
5. Update node: `sprite_svg` or `sprite_url`

**Every entity becomes visually renderable.**

---

## The Current State (2026-01-03)

### What's Built

✅ **Infrastructure**:
- Bunny (Xeon Server) running Docker services
- AuraDB (Neo4j Cloud) as Brain
- Tailscale mesh network
- N8N workflow automation

✅ **Ontology**:
- Bootstrap schema loaded
- Organogram structure defined
- Task management system active
- Decision/Insight nodes captured

✅ **Specifications**:
- Population schema aligned to Purely Pets
- Customer journey ontology designed
- Skills framework established

### What's Next

🔧 **Immediate (Population Reset)**:
1. Upgrade `population-db` to `pgvector/pgvector:pg15`
2. Apply `correct_schema.sql` (customers, pets, quotes)
3. Rewrite `remote_generator.py` for Purely Pets alignment
4. Generate initial 1M NPCs for validation
5. Verify quote form integration

🔧 **Short-Term (Factory Operations)**:
1. Implement event-driven claim processing
2. Build news feed integration
3. Create email inbox monitoring
4. Deploy N8N sprite generation workflows
5. Enable vector similarity marketing queries

🔧 **Long-Term (Complete Vision)**:
1. Scale to 100M NPCs
2. VR interface on MetaQuest 3
3. Multi-agent swarm coordination
4. Self-evolving brand system (Canva integration)
5. Full autonomous operations

---

## The Meta-Insight

### Why This Matters

**Traditional Insurance Systems**:
- Modeled around business departments (silos)
- Schema designed by DBAs, not customer experience
- Agents are external bolted-on tools
- Memory is fragmented (logs, databases, wikis)
- Changes require human coordination

**The Insurance Factory**:
- Modeled around **customer journey** (Jerry & Barry's story)
- Schema **emerges from** the narrative
- Agents **are native citizens** of the graph
- Memory is **unified** in the ontology (Brain/Diary/Eyes)
- Changes are **autonomous** via distributed agents

### The Specification IS the Product

By capturing the vision, decisions, tasks, and ontology **as graph nodes**:
- Nothing gets lost
- Everything is queryable
- Any agent can discover context
- System is self-documenting
- Evolution is traceable

**Willow doesn't just simulate insurance—it embodies it.**

---

## References from Brain

### Key Decisions
1. "Use Docker MCP for full stack autonomy"
2. "Store conversational memory in AuraDB alongside domain data"
3. "Skills stored as graph nodes"
4. "Build educational presentation with pet insurance narrative"
5. "Spec-Driven Architecture - Graph is source of truth"
6. "Customer journey story defines ontology"

### Related Documents
- [BIOS.md](../BIOS.md) - Bootstrap protocol
- [POPULATION_SCHEMA_SPEC.md](POPULATION_SCHEMA_SPEC.md) - Purely Pets alignment
- [ORGANOGRAM_VISION.md](ORGANOGRAM_VISION.md) - Hierarchical task structure
- [WILLOW_STRATEGIC_OVERVIEW.md](../WILLOW_STRATEGIC_OVERVIEW.md) - System architecture
- [Willow_Architecture_Focus_2026.pdf](../Willow_Architecture_Focus_2026.pdf) - Memory sync architecture
- [RANDOM_IDEAS.md](RANDOM_IDEAS.md) - Future enhancements

### Infrastructure
- **Bunny**: `ssh bunny@bunny` (Xeon Server, 128GB RAM)
- **AuraDB**: Neo4j Cloud Knowledge Graph
- **Frank**: Windows 11 + RTX 3090Ti (Ollama inference)
- **Tailscale**: Mesh network overlay

---

**Status**: Vision Documented
**Next Action**: Share with team for alignment validation
**Maintained By**: Willow Project Manager (Ontology)

🌳 **To the Moon!** 🚀
