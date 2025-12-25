# Willow Random Ideas & Future Enhancements

**Purpose**: Capture all brainstorm ideas so they don't get lost. These can be promoted to Tasks when ready.

**Status Key**:
- `concept` - Interesting idea, needs exploration
- `planned` - Scheduled for implementation (linked to Task)
- `adopted` - Being implemented now
- `frozen` - Good idea, not now
- `rejected` - Won't implement (with reason)

---

## 🤖 Distributed Agent Architecture

### Any Agent, Anywhere Can Work on Tasks
**Status**: `concept` | **Impact**: `high`

By storing tasks, decisions, and skills as graph nodes, any agent can query "what needs doing?" and execute autonomously:
- **GitHub PR agent** fixing WILL-001
- **AntiGravity Claude** implementing WILL-012
- **Cloud agent** watching email, updating Claim status
- **N8N workflow** generating birthday sprite for Doris

**Insight**: Graph-based specification enables distributed coordination without central orchestrator.

### Email-Triggered Claim Status Updates
**Status**: `concept` | **Impact**: `high`

Cloud agent monitors email inbox. When claim documents arrive:
1. Parse email for claim ID
2. Extract attachments
3. Update Claim node status in AuraDB
4. Trigger next workflow step
5. No human intervention required

**Example**: Vet sends diagnosis PDF → Claim moves from "info_requested" to "under_assessment"

### Personalized User Graphics Generation
**Status**: `concept` | **Impact**: `medium`

N8N workflow detects lifecycle events (birthday, anniversary, milestone):
1. Doris in Accounts turns 60
2. N8N agent generates custom birthday SVG sprite
3. Updates User node with `sprite_url`
4. Optional: Email notification with personalized graphic

**Example**: "Happy 60th Doris! Here's your special avatar 🎂"

### News-Based Proactive Marketing
**Status**: `concept` | **Impact**: `high` | **Added**: Dec 21, 2025

**Example: Slough Cat Strangler Returns**

Willow monitors news feeds (RSS, API, web scraping):
1. Detect event: "Slough Cat Strangler seen again"
2. Parse location: "Slough" → Postcode area "SL"
3. Parse threat: "Cat Strangler" → Species: Cat
4. Query graph:
   ```cypher
   MATCH (c:Customer)-[:OWNS]->(p:Pet {species: 'Cat'})
   WHERE c.postcode STARTS WITH 'SL'
   RETURN c.email, p.pet_name
   ```
5. Generate targeted campaign:
   - Subject: "Protect [PetName] - Slough Cat Strangler Alert"
   - Content: Safety tips + insurance coverage info
6. Suggest to marketing (or auto-send if pre-approved)

**Extensions**:
- Monitor vet alerts (disease outbreaks, recalls)
- Weather events (storms → travel insurance for pets)
- Local events (fireworks → anxiety coverage reminders)
- Legislative changes (microchip requirements, breed bans)

**Requirements**:
- News API integration (NewsAPI.org, Google News RSS)
- NLP for entity extraction (location, species, threat type)
- Geospatial query capability (postcode radius search)
- Marketing approval workflow (or auto-send whitelist)

---

## 🕶️ VR & Visualization

### MetaQuest 3 VR Graph Visualization
**Status**: `frozen` | **Impact**: `high` | **Related**: WILL-021

Render entire graph as walkable 3D space:
- Each entity has sprite model (e.g., `willow_tree.glb`)
- Spatial position: `{x, y, z}`
- Color, scale properties
- Real-time multi-user MMOG-style interface
- Navigate customer journey by walking through graph

**Use Cases**:
- Claims adjuster "walks" through claim dependencies
- Management sees system overview in 3D
- Training: New employees explore ontology spatially

### N8N Agents Generate SVG Sprites
**Status**: `concept` | **Impact**: `medium`

When entity created in graph, trigger workflow:
1. New `:Customer` node created
2. N8N webhook receives event
3. Local agent generates personalized SVG avatar
4. Upload to storage or embed in node
5. Update node: `sprite_svg` or `sprite_url`

**Example**:
```cypher
(:Customer {
  name: 'Jerry Smith',
  sprite_svg: '<svg>...custom avatar...</svg>',
  sprite_color: '#8B9D83'
})
```

### Real-Time Event Stream for VR Sync
**Status**: `concept` | **Impact**: `medium`

GraphEvent nodes capture all changes:
```cypher
(:GraphEvent {
  type: 'NODE_CREATED',
  entity_id: 'customer-12345',
  entity_type: 'Customer',
  timestamp: datetime(),
  visible_to: ['claims-dept', 'management']
})
```

VR clients subscribe via WebSocket → See changes live (MMOG-style).

### Every Entity Has 3D Sprite Model
**Status**: `concept` | **Impact**: `medium`

All nodes can have visualization metadata:
```cypher
(:Pet {
  name: 'Barry',
  sprite_model: 'dog_labrador.glb',
  sprite_position: {x: 10.5, y: 0, z: -3.2},
  sprite_scale: 1.0,
  sprite_color: '#FFD700'
})
```

**Models needed**:
- Customer → humanoid avatar
- Pet → species-specific (dog, cat)
- Claim → document icon
- Policy → contract icon
- Vet → building model
- Skill → tool icon

---

## 👥 Population & NPCs

### NPCs as Evolving Sims Characters
**Status**: `concept` | **Impact**: `medium`

Population starts with basic demographics (Faker). Over time:
- NPCs develop personalities based on interactions
- Life events update graph (marriage, pet adoption, moving)
- Vector personalities evolve
- Behavioral patterns emerge

**Example**: Customer who files many small claims → Personality vector shifts toward "risk-averse" cluster

### Infinite Library Pattern for NPC Creation
**Status**: `rejected` | **Impact**: `low`

**Idea**: Create NPCs on-demand when needed (like Borges' Library of Babel)

**Challenge**: Need to know global distributions before creation
- "What % of population has nut allergies?"
- "How many cat owners in Manchester?"

**Rejection reason**: Pre-generating 10M NPCs simpler for MVP. Allows realistic distributions and immediate querying.

### Vector Similarity for Marketing
**Status**: `planned` | **Impact**: `high` | **Related**: WILL-011

Find similar customers via personality vectors:
- Cat lovers for new cat insurance product
- Allergy sufferers for hypoallergenic pet food partner
- Political views for brand alignment messaging
- Geographic clustering for local events

**Query example**:
```sql
SELECT * FROM customers
ORDER BY personality_vector <-> (SELECT personality_vector FROM customers WHERE id = 12345)
LIMIT 100;
```

Returns 100 customers most similar to customer #12345.

---

## 🎨 Brand & Design

### Canva MCP for Autonomous Brand Evolution
**Status**: `frozen` | **Impact**: `medium` | **Related**: WILL-020

Claude queries BrandAsset nodes, requests new themes:
1. System detects Christmas approaching
2. Claude: "I need a winter/Christmas theme"
3. Canva MCP creates design
4. New BrandAsset node created
5. UI updates automatically

**Brand becomes self-evolving** based on context (seasons, campaigns, events).

### Brand Evolution Timeline
**Status**: `concept` | **Impact**: `low`

BrandAsset nodes linked via relationships:
```cypher
(:BrandAsset {season: 'autumn_v1', created_at: '2025-09-01'})
  -[:EVOLVED_FROM]->
(:BrandAsset {season: 'autumn_v2', created_at: '2025-10-15'})
  -[:EVOLVED_FROM]->
(:BrandAsset {season: 'autumn_v3', created_at: '2025-11-20'})
```

Historical brand audit trail. Design lineage tracking.

---

## 🛠️ Skill System

### Skill-Creation-Skill (Meta-Skill)
**Status**: `concept` | **Impact**: `high`

A skill that writes new skills:
1. Claude identifies need: "I need a skill to calculate premium discounts"
2. Executes `create_skill` meta-skill
3. Generates Python code for new skill
4. Saves to `/skills/calculate_discount.py`
5. Creates Skill node in graph
6. New skill immediately available

**Self-modifying system.**

### Skills Linked via CREATED_BY
**Status**: `concept` | **Impact**: `low`

Track skill genealogy:
```cypher
(:Skill {name: 'create_skill'})
  -[:CREATED]->
(:Skill {name: 'calculate_discount_v1'})
  -[:CREATED]->
(:Skill {name: 'calculate_discount_v2'})
```

Meta-insight into system evolution.

---

## 📊 Ontology & Data Modeling

### Department ACLs (Palantir/Timbr Strategy)
**Status**: `concept` | **Impact**: `high`

Same graph, different security scopes:
- **Claims Dept**: Sees customer journey, claims, payments
- **Underwriting**: Sees risk models, policy terms, exclusions
- **Vets**: Sees treatments, diagnoses, medical history
- **Marketing**: Sees customer segments, preferences, vectors

**Implementation**: AuraDB role-based access control (RBAC)

### Process Documents as Graph Nodes
**Status**: `frozen` | **Impact**: `medium` | **Related**: WILL-023

Store policy documents in graph:
```cypher
(:AssessmentRule {
  title: 'Hip Dysplasia Coverage Rule',
  content: 'Claims for hip dysplasia are covered if...',
  applies_to: 'dogs',
  effective_date: '2025-01-01'
})

(:Claim)-[:ASSESSED_USING]->(:AssessmentRule)
```

Or separate knowledge graph with cross-references.

**Queryable policy**: "What rules apply to this claim?"

### Multi-Graph Architecture
**Status**: `concept` | **Impact**: `low`

Separate graphs for different domains:
- **Main Willow graph**: Operations (customers, claims, policies)
- **Knowledge graph**: Rules, processes, documentation
- **Audit graph**: Historical changes, compliance logs
- **Archive graph**: Closed claims, expired policies

**Tradeoff**: Complexity vs. performance. Start with single graph + ACLs.

### Customer Journey Story Defines Ontology
**Status**: `adopted` | **Impact**: `high` | **Related**: WILL-012, WILL-013

Rather than business-first modeling (policies → claims → payments), design around customer experience:

**The Story**:
1. Jerry finds Barry (dog)
2. Jerry requests quote
3. Jerry purchases policy
4. Barry gets sick
5. Jerry takes Barry to vet
6. Vet diagnoses Barry
7. Jerry submits claim
8. Claim assessed
9. Claim paid

**This story IS the schema.** Customer-first design.

---

## 🏗️ Infrastructure

### Google Cloud Run for Serverless API
**Status**: `concept` | **Impact**: `low`

Deploy Willow API as serverless container:
- Auto-scaling based on demand
- Pay-per-use (no idle costs)
- Triggered by graph events or HTTP

**Note**: Docker-based API sufficient for MVP. Cloud Run for production scale.

### Local Ollama for Bulk Generation
**Status**: `adopted` | **Impact**: `high` | **Related**: WILL-009, WILL-010

RTX 3090 Ti runs Ollama locally via Tailscale:
- Handles Faker-based generation of 10M NPCs
- Parallel generation (multi-GPU if available)
- Saves Claude credits
- Faster than cloud-based generation

**Agent architecture**:
```
Claude Sonnet 4.5 (orchestration)
    ↓
Local Ollama Agent (RTX 3090 Ti)
    ↓
Population DB (Postgres)
```

### Sora Integration for VR
**Status**: `frozen` | **Impact**: `low`

Use Sora (OpenAI video gen) for dynamic VR visualizations:
- Generate animated customer journeys
- Claim flow videos
- Training simulations

**Note**: Cool but not MVP critical. Explore after VR interface proven.

---

## 🔔 Event-Driven Ideas

### News Feed Integration
**Status**: `concept` | **Impact**: `high`

Monitor external data sources:
- **News APIs**: Google News, NewsAPI.org
- **Vet alerts**: Disease outbreaks, product recalls
- **Weather**: Storms, extreme heat (travel insurance for pets)
- **Legislation**: Microchip laws, breed restrictions

**Trigger workflows**:
- Proactive customer communication
- Risk model updates
- Marketing campaigns
- Underwriting policy changes

### Email Inbox Monitoring
**Status**: `concept` | **Impact**: `high`

Cloud agent watches shared inbox:
- Claim documents from vets
- Customer responses to info requests
- Partner communications (reinsurance, providers)

**Auto-process**:
- Extract claim ID from subject
- Parse attachments (PDFs, images)
- Update Claim node status
- Trigger next workflow step

### Calendar/Date-Based Triggers
**Status**: `concept` | **Impact**: `medium`

N8N workflows triggered by dates:
- Policy renewals approaching → Send reminder email
- Pet birthdays → Marketing opportunity
- Employee milestones (Doris turns 60) → Personalized graphics
- Seasonal brand changes → Switch to winter theme

---

## 📝 Promotion Path: Idea → Task

When random idea is ready for implementation:

1. **Update status**: `concept` → `planned`
2. **Create Task node**:
   ```cypher
   CREATE (t:Task {
     id: 'WILL-XXX',
     title: 'Implement [Idea Title]',
     status: 'todo',
     priority: 'medium'
   })
   CREATE (idea:RandomIdea)-[:IMPLEMENTED_BY_TASK]->(t)
   ```
3. **Link to Sprint**
4. **Add to GitHub Project board**

---

## 🔍 Query Examples

### Show all high-impact ideas still in concept phase
```cypher
MATCH (r:RandomIdea {potential_impact: 'high', status: 'concept'})
RETURN r.title, r.description;
```

### Find ideas by category
```cypher
MATCH (r:RandomIdea {category: 'vr-interface'})
RETURN r.title, r.status;
```

### Show adopted ideas and their implementing tasks
```cypher
MATCH (r:RandomIdea {status: 'adopted'})-[:IMPLEMENTED_BY_TASK]->(t:Task)
RETURN r.title, t.id, t.status;
```

### Ideas that became insights
```cypher
MATCH (r:RandomIdea)-[:INSPIRED_INSIGHT]->(i:Insight)
RETURN r.title, i.text;
```

---

## 🌳 Meta-Insight

**The specification IS the product.**

By capturing ideas as graph nodes:
- Nothing gets lost
- Ideas are queryable
- Can be linked to decisions, tasks, insights
- Promotion path is clear (concept → planned → task)
- Any agent can discover and implement ideas

**This document lives in both**:
- `/docs/RANDOM_IDEAS.md` (human readable)
- AuraDB as RandomIdea nodes (machine queryable)

---

**Last Updated**: December 21, 2025
**Total Ideas**: 21+
**Status**: Living document - add ideas as they emerge! 🌳
