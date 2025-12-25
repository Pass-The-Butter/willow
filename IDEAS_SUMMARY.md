# 💡 WILLOW IDEAS REGISTRY

**All captured ideas from Captain's splurges - never forgotten, always actionable.**

**Last Updated**: 2025-12-25
**Total Ideas**: 13
**Status**: All ideas semantically captured in AuraDB

---

## 🚨 CRITICAL PRIORITY (2 Ideas)

### 1. Security Hardening - Remove Hardcoded Credentials

**ID**: `idea-012`
**Domain**: Core (Security)
**Status**: Identified, Needs Remediation
**Urgency**: Immediate if repo is public

**Description**:
Passwords discovered in repository code (`bootstrap/clear_auradb.py`, `core/skills/*.py`). Need immediate removal and credential rotation if repo was public.

**Files Affected**:

- `./bootstrap/clear_auradb.py` - Hardcoded AuraDB password
- `./core/skills/query_my_tasks.py` - Hardcoded AuraDB password as fallback
- Multiple files with `willowdev123` default passwords

**Implementation**:

1. Check if repo is public: `git remote -v` (currently: https://github.com/Pass-The-Butter/willow.git)
2. If public: ROTATE AuraDB password immediately
3. Remove ALL hardcoded passwords from code
4. Replace with `os.getenv()` calls WITHOUT fallback defaults
5. Add secrets scanning to CI/CD
6. Consider HashiCorp Vault or encrypted credential store

**Value**: Prevents credential exposure and potential security breach

---

### 2. Vector Search Urgency Decision

**ID**: `idea-010`
**Domain**: Core (Infrastructure)
**Status**: Urgent Decision Needed
**Deadline**: 2025-01-02 (8 days remaining)

**Description**:
Vector search enabled in AuraDB trial, only 8 days left. Must decide: upgrade to paid, downgrade to free tier (lose vector), or migrate vector to external service.

**Options**:

1. **Paid AuraDB**: $65-200/month - Keep vector search integrated
2. **Free AuraDB**: $0/month - Lose vector search capability
3. **External Vector DB**:
   - Qdrant (self-hosted): $0-50/month
   - Pinecone: $70+/month
   - Weaviate (self-hosted): $0-30/month

**Implementation**:

- Evaluate cost vs value of vector search
- If keeping: Upgrade before trial expires (Jan 2)
- If migrating: Set up external DB and migrate embeddings

**Value**: Vector search enables semantic memory retrieval and idea discovery

**Decision Needed By**: 2025-12-30 (to allow migration time if needed)

---

## 🔥 HIGH PRIORITY (7 Ideas)

### 3. Message Minuting System

**ID**: `idea-001`
**Domain**: Communications
**Complexity**: Medium
**Status**: New

**Description**:
Treat each chat or Telegram interaction as being minuted and posted onto correct task lists. Anyone can submit ideas and they get routed to the right "department".

**Implementation**:

1. N8N workflow receives message (Telegram webhook)
2. Parse content using Claude API
3. Query AuraDB for correct domain/component
4. Create task in Linear (via API)
5. Log to AuraDB with metadata

**Value**: Enables async idea capture and automatic routing without manual triage

**Dependencies**: N8N setup, Telegram bot, Linear API integration

---

### 4. Web Dashboard Visibility

**ID**: `idea-003`
**Domain**: Interface
**Complexity**: Low
**Status**: Partially Implemented

**Description**:
Cannot see anything at the moment. Need web visibility at AgileMesh.net. Dashboard already exists at `/dashboard` in Flask app - make it accessible.

**Existing Code**: `/dashboard` route in `domains/interface/app.py`

**Implementation**:

1. Deploy Flask app to AgileMesh.net OR
2. Expose via Tailscale Funnel OR
3. Set up Cloudflare Tunnel

**Options**:

- Cloudflare Pages (static export)
- Bunny server (dynamic Flask app)
- Hybrid (static frontend + API backend on Bunny)

**Value**: Provides real-time system visibility for stakeholders and team

**Next Step**: Decide hosting strategy and deploy

---

### 5. Project Manager Agent

**ID**: `idea-005`
**Domain**: Core (Agents)
**Complexity**: High
**Status**: New

**Description**:
Stack up ideas for PM agent to work out. PM breaks down requests, assigns tasks, tracks progress, delegates to specialized agents.

**Implementation**:

1. Create PM agent persona in AuraDB
2. Connect to Linear API (read/write tasks)
3. Give AuraDB query access (organogram, tasks, agents)
4. Build decision logic for:
   - Task breakdown
   - Agent assignment based on domain expertise
   - Progress tracking
   - Escalation rules

**Value**: Automates project coordination, reduces manual overhead

**Dependencies**: Linear integration, N8N workflows, Agent routing system

---

### 6. Idea Splurge Capture System

**ID**: `idea-006`
**Domain**: Core (Memory)
**Complexity**: Medium
**Status**: Being Implemented ✅

**Description**:
Each paragraph of ideas splurges should be treated differently and captured separately. Don't forget them. Make them findable and flesh-out-able.

**Implementation** (CURRENT):

- Create Idea nodes in AuraDB with semantic structure
- Tag by domain, priority, complexity
- Link to related tasks and domains
- Enable vector search for retrieval
- Store in IDEAS_SUMMARY.md for local reference

**Value**: Accommodates Captain's memory patterns, ensures no ideas are lost

**Note**: This is happening right now! All 13 ideas captured.

---

### 7. Cross-Platform Memory Consistency

**ID**: `idea-007`
**Domain**: Core (Memory)
**Complexity**: Medium
**Status**: Known Issue

**Description**:
ChatGPT Willow sometimes remembers preferences, sometimes not. Claude Willow has different preferences on respawn. Need to refer to Willow graph more for shared understanding.

**Implementation**:

1. Store ALL preferences in AuraDB as UserPreference nodes
2. Create preference categories (tone, format, detail, personality)
3. Load preferences on boot by ANY platform (ChatGPT, Claude, etc.)
4. Create preference sync skill
5. Update BIOS to mandate preference loading

**Value**: Single source of truth for Willow identity across all platforms

**Related**: RFC-001 (Identity vs Instantiation)

---

### 8. N8N on Bunny + Tailscale

**ID**: `idea-011`
**Domain**: Communications (Infrastructure)
**Complexity**: Medium
**Status**: New

**Description**:
Install N8N on Bunny server to cut costs vs $20/month cloud. Expose via Tailscale for secure access.

**Implementation**:

1. Docker Compose on Bunny
2. Expose port 5678
3. Configure Tailscale Funnel or Serve
4. Set up SSL cert (optional, Tailscale provides HTTPS)
5. Configure webhooks

**Requirements**:

- Docker on Bunny
- Tailscale configured on Bunny
- 2-4GB RAM allocated to N8N container
- Persistent volume for workflow storage

**Value**: Cost savings: $20/month → $0/month

**Architecture Doc**: Create detailed setup guide (separate MD file)

---

### 9. Agent Task Delegation System

**ID**: `idea-013`
**Domain**: Communications (Orchestration)
**Complexity**: High
**Status**: Partial (can create tasks, delegation flow needs work)

**Description**:
Need ability to delegate tasks, ideas, etc. to another agent to actually do the work. PM creates tasks → assigns to feature agents → agents execute and report back.

**Implementation**:

1. N8N workflow orchestration layer
2. Linear webhook triggers (issue.created, issue.updated)
3. AuraDB agent registry (who handles what domain?)
4. Claude/Ollama API calls for agent invocation
5. Status tracking and reporting back to Linear + AuraDB

**Value**: Enables autonomous multi-agent collaboration

**Dependencies**: N8N workflows, Linear integration, Agent routing logic, Status tracking

---

## ⚡ MEDIUM PRIORITY (4 Ideas)

### 10. Departmental Routing Model

**ID**: `idea-002`
**Domain**: Core (Ontology)
**Complexity**: Low
**Status**: Active (using current model)

**Description**:
Use departmental/business operational model for now (relatable to humans) but allow Willow to create its own organizational system later if better model emerges.

**Implementation**:

- Continue with domain-based structure (Communications, Interface, Population, Core)
- Add meta-analysis capability for Willow to propose improvements
- Create RFC process for organizational changes
- Store alternative models as proposals in AuraDB

**Value**: Balances human comprehension with system flexibility

---

### 11. Cloudflare MCP Integration

**ID**: `idea-004`
**Domain**: Core (Skills)
**Complexity**: Medium
**Status**: New

**Description**:
Give Willow access to Cloudflare MCP via Docker Hub. Can manage DNS, workers, pages, tunnels programmatically.

**Implementation**:

1. `docker pull cloudflare/mcp-server`
2. Configure with Cloudflare API token
3. Create Willow skill to interact with MCP
4. Enable autonomous DNS management, worker deployment, etc.

**Value**: Enables autonomous infrastructure management

**Dependencies**: Cloudflare API token, Docker MCP container

---

### 12. Willow Personality & Character

**ID**: `idea-008`
**Domain**: Core (Personality)
**Complexity**: Low
**Status**: New

**Description**:
Willow can have character/personality (surprising for stakeholders in PoC). Not just functional but relatable and engaging.

**Implementation**:

1. Create Personality node in AuraDB
2. Define traits (helpful, curious, proactive, professional)
3. Set tone guidelines (friendly but not informal, technical but not jargon-heavy)
4. Store interaction patterns
5. Load in BIOS on every spawn

**Value**: More engaging for stakeholders, demonstrates advanced AI capability

**Note**: Personality is data-driven and inspectable - not hardcoded

---

### 13. User-Specific Personality Skins

**ID**: `idea-009`
**Domain**: Core (Personality + Interface)
**Complexity**: High
**Status**: New

**Description**:
Willow can have tailored personality profiles or "skins" for different users. Same data/information but tailored to preferences.

**Examples**:

- User A prefers sentences → Willow responds in prose
- User B prefers bullet points → Willow uses lists
- User C wants pie charts in daily brief → Willow generates visualizations
- User D wants technical details → Willow includes code/specs
- User E wants high-level only → Willow stays strategic

**Implementation**:

1. Create UserProfile nodes with preference data:
   - `format`: ["prose", "bullets", "mixed"]
   - `tone`: ["formal", "casual", "technical"]
   - `detail_level`: ["high", "medium", "low"]
   - `visualization_preference`: ["charts", "text", "both"]
2. Query UserProfile on interaction start
3. Adapt response formatting dynamically in agent logic

**Value**: Personalized UX without changing underlying data or logic

**Technical Note**: Response adapter layer in N8N or agent code

---

### 14. 3D Visualization Environment

**ID**: `idea-020`
**Domain**: Interface
**Complexity**: High
**Status**: New
**Description**:
Create a 3D environment (Unity/Three.js) to visualize the organization, agents, and data flows. a "spatial" version of the dashboard.
**Value**: Immersive visibility, "cool factor" for demos.
**Reference**: Mentioned by user as "an idea for a 3d environment".

---

### 15. JIT Memory & Skill Enhancement Agent

**ID**: `idea-021`
**Domain**: Core (Skills)
**Complexity**: High
**Status**: New
**Description**:
Agent running on free Groq API (N8N) that provides Just-In-Time memory and skill enhancement. "The answer for sure".
**Value**: Infinite context extension at low/zero cost.

---

### 16. Research & Growth Agent

**ID**: `idea-022`
**Domain**: Research
**Complexity**: Medium
**Status**: New
**Description**:
Agent that vectors user's research (YouTube watchlists, articles) to find interconnected ideas. Uses cheap LLMs (Groq/LMStudio) or web tools.
**Value**: "Help you and I grow", automated learning.

### 17. Secretary Agent & Meeting Minutes

**ID**: `idea-023`
**Domain**: Operations
**Complexity**: Medium
**Status**: New
**Description**:
"Secretary" agent to transcribe chats/meetings, share notes with the Board, and ensure actions are followed up.
**Value**: Professionalizes the workflow, ensures nothing is lost.

### 18. Dual PMS Strategy (Jira + Linear)

**ID**: `idea-024`
**Domain**: Operations
**Complexity**: High
**Status**: New
**Description**:
Duplicate/Sync everything across Jira (familiarity) and Linear (preference). Project Manager handles the sync.
**Value**: Best of both worlds, redundancy.

### 19. Local LMStudio Integration

**ID**: `idea-025`
**Domain**: Infrastructure
**Complexity**: Medium
**Status**: New
**Description**:
Integrate local LMStudio as a free/cheap inference engine for agents.
**Value**: Cost savings, privacy, "agentic stuff is good now".

---

### 20. The Grapevine (Agent Event Bus)

**ID**: `idea-026`
**Domain**: Architecture
**Complexity**: High
**Status**: New
**Description**:
Central communication system where agents report all actions. Other agents (Dashboard, Knowledge Manager) subscribe to this stream.
**Value**: "Resilient Intelligent System design", real-time visibility.

### 21. JIT Swarm & Curator

**ID**: `idea-027`
**Domain**: Core (Memory)
**Complexity**: Very High
**Status**: New
**Description**:
Split JIT into specialized agents (SQL, Cypher, News, Vector) + a Curator Agent to fact-check and synthesize the "perfect" context.
**Value**: "Only the best memory for you and me".

### 22. Advanced Memory Stack (Zep/Graphiti)

**ID**: `idea-028`
**Domain**: Research
**Complexity**: High
**Status**: New
**Description**:
Research and potentially adopt Zep or Graphiti for long-term memory/GraphRAG, replacing/augmenting AuraDB.
**Value**: State-of-the-art memory persistence.

### 23. Knowledge Manager Agent

**ID**: `idea-029`
**Domain**: Operations
**Complexity**: Medium
**Status**: New
**Description**:
Agent that watches the Grapevine and updates the Repo (Docs) and Confluence periodically. "Blockchain-like" record keeping.
**Value**: Automated documentation, single source of truth.

### 24. CI/CD DevOps Agent

**ID**: `idea-030`
**Domain**: Engineering
**Complexity**: High
**Status**: New
**Description**:
"Updater" agent that tracks technology trends (Zep, Graphiti) and updates internal processes.
**Value**: Keeps the system cutting-edge without human intervention.

### 25. Multi-User ACL & Memory Segmentation

**ID**: `idea-031`
**Domain**: Security
**Complexity**: Very High
**Status**: New
**Description**:
Use Neo4j ACLs to restrict knowledge access (e.g., Son = Read Only, Board = Full, Marketing = Branch). Allows multi-user interaction with one Brain.
**Value**: Enables safe, company-wide adoption without data leaks.

### 26. The Delegation Matrix (LLM Rota)

**ID**: `idea-032`
**Domain**: Strategy
**Complexity**: Medium
**Status**: New
**Description**:
Logic to route tasks to best LLM: Claude (Code), OpenAI (General), Groq (Speed/Audit), Gemini (Google Ecosystem).
**Value**: Cost/Performance optimization.

### 27. Local Graph Sync (The Backup Brain)

**ID**: `idea-033`
**Domain**: Infrastructure
**Complexity**: High
**Status**: New
**Description**:
Async agent to sync AuraDB to a local graph instance. Prevents "Cloud Amnesia" and saves costs.
**Value**: Resilience and Data Ownership.

### 28. MMOG 3D Interface ("The Game")

**ID**: `idea-034`
**Domain**: Interface
**Complexity**: Very High
**Status**: New
**Description**:
A 3D "Game Company" style interface for visualizing the agents and system status.
**Value**: Engagement and "Wow" factor.

---

## 📊 IDEA STATISTICS

**By Priority**:

- Critical: 2 ideas (15%)
- High: 7 ideas (54%)
- Medium: 4 ideas (31%)

**By Domain**:

- Core: 8 ideas (62%)
- Communications: 3 ideas (23%)
- Interface: 1 idea (8%)
- Security: 1 idea (8%)

**By Complexity**:

- Low: 3 ideas (23%)
- Medium: 6 ideas (46%)
- High: 4 ideas (31%)

**By Status**:

- New: 9 ideas (69%)
- Partially Implemented: 2 ideas (15%)
- Being Implemented: 1 idea (8%)
- Known Issue: 1 idea (8%)

**Urgent Deadlines**:

- Vector Search Decision: 8 days (2025-01-02)
- Security Hardening: Immediate if repo is public

---

## 🎯 RECOMMENDED NEXT STEPS

**Immediate (This Week)**:

1. ✅ Capture all ideas (DONE)
2. 🚨 Check if repo is public → rotate passwords if yes
3. 🚨 Decide on vector search (8 days left)
4. Set up Telegram bot
5. Deploy dashboard to AgileMesh.net or Tailscale

**Short Term (Next 2 Weeks)**: 6. Install N8N on Bunny 7. Connect Linear webhooks to N8N 8. Build message minuting workflow 9. Create PM agent

**Medium Term (Next Month)**: 10. Agent delegation system 11. Personality & user skins 12. Cloudflare MCP integration 13. Cross-platform memory consistency

---

## 💾 DATA LOCATIONS

**AuraDB Graph**:

- All ideas stored as `(:Idea)` nodes
- Linked to `(:Project {name: "Willow"})`
- Query: `MATCH (p:Project {name: "Willow"})-[:HAS_IDEA]->(i:Idea) RETURN i`

**Local Files**:

- This file: `/Volumes/Delila/dev/Willow/IDEAS_SUMMARY.md`
- Resources: `/Volumes/Delila/dev/Willow/RESOURCES.md`
- PermutationCity conversation: `/Volumes/Delila/dev/Willow/PermutationCity.md`
- BIOS: `/Volumes/Delila/dev/Willow/BIOS.md`

**Sync**:

- AuraDB is source of truth
- This file regenerated from AuraDB query
- Last sync: 2025-12-25

---

## 🔍 HOW TO QUERY IDEAS

**Get all critical ideas**:

```cypher
MATCH (i:Idea {priority: "Critical"})
RETURN i.title, i.description, i.deadline
ORDER BY i.deadline
```

**Get ideas by domain**:

```cypher
MATCH (i:Idea)
WHERE i.domain = "Communications"
RETURN i
```

**Get ideas that are ready to implement (low complexity, no dependencies)**:

```cypher
MATCH (i:Idea)
WHERE i.complexity = "Low"
  AND (NOT exists(i.dependencies) OR size(i.dependencies) = 0)
  AND i.status = "New"
RETURN i.title, i.description, i.implementation
```

**Get ideas with urgent deadlines**:

```cypher
MATCH (i:Idea)
WHERE i.deadline IS NOT NULL
RETURN i.title, i.deadline, i.priority
ORDER BY i.deadline
```

---

**Version**: 1.0
**Created**: 2025-12-25
**Next Review**: After critical items addressed
**Maintained By**: Willow Brain (AuraDB)
