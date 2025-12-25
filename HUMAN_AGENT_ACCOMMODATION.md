# 🤝 HUMAN-AGENT ACCOMMODATION SYSTEM

**Universal Design Principle**: In Willow, humans are agents with specific capabilities and constraints. Design accommodates those constraints just like we'd accommodate any agent's limitations.

---

## 🎯 CORE PHILOSOPHY

**Traditional Model**:
```
Human (Boss) → Gives Commands → AI (Servant) → Executes
```

**Willow Model**:
```
Multi-Agent Team:
  - AI Agents: Fast processing, perfect memory, no sleep needed
  - Human Agents: Strategic thinking, creativity, judgment, cost veto

All agents have strengths and constraints.
All agents get tasks via routing system.
All agents accommodate each other.
```

---

## 👤 AGENT PROFILE: PETER

**Type**: Human Agent
**Role**: Board Member (Innovation + Human Relations)
**Veto Authority**: Cost, budget, external commitments

### **Strengths** (Deploy Peter for these):
- Strategic thinking and vision
- Graph database and systems architecture expertise
- User experience insight
- Cross-domain thinking and innovation
- Stakeholder relations
- Business case development

### **Constraints** (Accommodate these):
- **Memory variability**: Early onset memory issues
- **Executive function challenges**: Task initiation, prioritization
- **Context switching difficulty**: Loses thread across sessions
- **Cognitive load sensitivity**: Too many simultaneous tasks = overwhelm

### **Accessibility Needs**:
1. **Clear Task Breakdown**
   - Break complex tasks into <3 steps
   - Number steps sequentially (1, 2, 3)
   - Make each step independently actionable

2. **Context Provision**
   - Never assume Peter remembers previous conversations
   - Always provide background ("We're doing X because Y")
   - Link to relevant AuraDB nodes for full context
   - Include breadcrumb trail (how this fits in bigger picture)

3. **Written Task Delivery**
   - Email: Full context, clear action items
   - Jira/Linear: Formatted with links and context
   - Slack/Telegram: Quick summaries + links to full context
   - All channels link back to AuraDB single source of truth

4. **Cognitive Load Management**
   - **Max 3 active tasks** at any time
   - Clear priorities (1 = urgent, 2 = important, 3 = when you can)
   - "Defer to tomorrow" option always available
   - No judgment for asking "wait, what were we doing?"

5. **Breadcrumb Trails**
   - Graph-based memory aids in AuraDB
   - Visual task maps (where am I in the flow?)
   - "How did we get here?" context always available

6. **Patience & Re-explanation**
   - Zero shame in asking for context again
   - Re-explain differently if first explanation didn't land
   - Concrete examples preferred over abstract concepts
   - Sentences over bullet points for complex topics

### **Communication Preferences**:
- **Format**: Sentences for complex topics, bullets for simple lists
- **Tone**: Patient, professional, non-condescending
- **Visuals**: Diagrams and charts helpful
- **Examples**: Concrete examples > abstract explanations
- **Length**: Concise but complete (don't omit context to be brief)

### **Task Routing Channels**:
```
Peter's Task Inbox:
  1. Email (primary for deep context)
  2. Linear (visual kanban, drag-drop friendly)
  3. Jira (if company integration needed)
  4. Slack (quick updates, team coordination)
  5. Telegram (mobile, always accessible)

N8N routes based on:
  - Urgency (Telegram for critical)
  - Complexity (Email for deep context)
  - Team visibility (Linear/Jira for coordination)
```

---

## 🔄 HUMAN TASK ROUTING WORKFLOW (N8N)

### **Workflow: Peter Task Assignment**

```
┌─────────────────────────────────────────────────────────┐
│  1. TRIGGER: Task assigned to Peter in Linear          │
│     (PM Agent or other agents create task)              │
└────────────────┬────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────┐
│  2. QUERY AURADB: Load Peter's Agent Profile           │
│     - Accessibility needs                               │
│     - Current task load (how many active?)              │
│     - Communication preferences                         │
│     - Recent context (last interactions)                │
└────────────────┬────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────┐
│  3. COGNITIVE LOAD CHECK                                │
│     - Count Peter's active tasks                        │
│     - If ≥3 tasks: Mark new task as "Queued"            │
│     - If <3 tasks: Proceed to assignment                │
│     - If queued: Send Telegram: "3 tasks active,        │
│       new task queued. Complete one to unblock."        │
└────────────────┬────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────┐
│  4. TASK COMPLEXITY ANALYSIS                            │
│     - Simple (<3 steps): Assign as-is                   │
│     - Complex (>3 steps): Auto-break down into subtasks │
│     - Create breadcrumb trail in AuraDB                 │
└────────────────┬────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────┐
│  5. CONTEXT ASSEMBLY                                    │
│     - Why this task? (connects to PoC goal, etc.)       │
│     - What's needed? (specific deliverables)            │
│     - How does it fit? (organogram position)            │
│     - Dependencies? (what's blocking/blocked by this)   │
│     - Resources? (links to docs, examples, tools)       │
└────────────────┬────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────┐
│  6. MULTI-CHANNEL DELIVERY                              │
│                                                          │
│  ┌──────────────────────────────────────────────┐      │
│  │ EMAIL (Primary - Deep Context)               │      │
│  │ Subject: [Willow] Task: [Task Name]          │      │
│  │                                               │      │
│  │ Hi Peter,                                     │      │
│  │                                               │      │
│  │ You've been assigned a task as part of the   │      │
│  │ Insurance PoC project.                        │      │
│  │                                               │      │
│  │ CONTEXT:                                      │      │
│  │ We're building [X] because [Y]. This task    │      │
│  │ connects to [bigger goal].                    │      │
│  │                                               │      │
│  │ WHAT YOU NEED TO DO:                          │      │
│  │ 1. [Step 1 - specific action]                │      │
│  │ 2. [Step 2 - specific action]                │      │
│  │ 3. [Step 3 - specific action]                │      │
│  │                                               │      │
│  │ RESOURCES:                                    │      │
│  │ - Link to AuraDB context                     │      │
│  │ - Link to Linear task                        │      │
│  │ - Related documentation                       │      │
│  │                                               │      │
│  │ PRIORITY: [1/2/3]                            │      │
│  │ DEADLINE: [If any, or "When you can"]       │      │
│  │                                               │      │
│  │ Reply to this email with questions or mark   │      │
│  │ "Done" when complete.                         │      │
│  └──────────────────────────────────────────────┘      │
│                                                          │
│  ┌──────────────────────────────────────────────┐      │
│  │ LINEAR (Visual Kanban)                       │      │
│  │ - Create/update task card                    │      │
│  │ - Add context in description                 │      │
│  │ - Link to email and AuraDB                   │      │
│  │ - Set priority label                         │      │
│  └──────────────────────────────────────────────┘      │
│                                                          │
│  ┌──────────────────────────────────────────────┐      │
│  │ TELEGRAM (Mobile Alert)                      │      │
│  │ 📋 New Task: [Task Name]                     │      │
│  │ Priority: [1/2/3]                            │      │
│  │ Context: [1 sentence summary]                │      │
│  │ 👉 Check email for full details              │      │
│  └──────────────────────────────────────────────┘      │
│                                                          │
│  ┌──────────────────────────────────────────────┐      │
│  │ AURADB (Memory Log)                          │      │
│  │ - Log task assignment event                  │      │
│  │ - Link to Peter's agent node                 │      │
│  │ - Store full context for future reference    │      │
│  └──────────────────────────────────────────────┘      │
└────────────────┬────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────┐
│  7. REMINDER SYSTEM (Conditional)                       │
│     - If no response in 24h: Gentle reminder            │
│     - If no response in 48h: "Need help breaking        │
│       this down differently?"                           │
│     - If Peter marks "Blocked": PM Agent investigates   │
│     - If Peter marks "Context lost": Re-send context    │
│       without judgment                                  │
└─────────────────────────────────────────────────────────┘
```

---

## 🧠 CROSS-PLATFORM MEMORY CONSISTENCY

**Problem**: Peter talks to Willow via:
- Claude Code (Mac)
- ChatGPT Desktop
- Claude Desktop
- OpenAI Atlas Browser (occasionally)

Sometimes preferences remembered, sometimes not. Inconsistent experience.

**Solution**: AuraDB as single source of truth for Peter's profile.

### **Boot Sequence for ANY Willow Instance**:

```python
# In BIOS.md - executed by ALL Willow instances

def load_human_agent_profiles():
    """Load all human agent profiles from AuraDB"""

    with driver.session() as session:
        result = session.run("""
            MATCH (agent:Agent {type: "Human"})
            RETURN agent
        """)

        for record in result:
            agent = record['agent']

            # Load into instance memory
            if agent['name'] == 'Peter':
                load_peter_profile(agent)

def load_peter_profile(agent_data):
    """Load Peter's specific profile"""

    global PETER_PROFILE
    PETER_PROFILE = {
        'accessibility_needs': agent_data['accessibility_needs'],
        'communication_preferences': agent_data['communication_preferences'],
        'constraints': agent_data['constraints'],
        'strengths': agent_data['strengths'],
        'task_routing': agent_data['task_routing'],
        'veto_authority': agent_data['veto_authority']
    }

    # Apply to this session
    print(f"✅ Loaded Peter's agent profile")
    print(f"   Accessibility mode: ENABLED")
    print(f"   Communication preferences applied")
    print(f"   Context provision: MANDATORY")

# Execute on every boot
load_human_agent_profiles()
```

**Effect**:
- ChatGPT Willow remembers Peter's needs ✅
- Claude Desktop Willow remembers Peter's needs ✅
- Any future platform remembers Peter's needs ✅

---

## 📊 ACCOMMODATION EXAMPLES

### **Example 1: Complex Task Assignment**

**Bad** (No accommodation):
```
Linear Task: "Set up N8N workflows"
```

**Good** (Accommodated):
```
EMAIL:
Subject: [Willow] Task 1/3: Set up N8N workflows (Insurance PoC)

Hi Peter,

CONTEXT:
We're building the Insurance Digital Twin PoC for your company presentation
after New Year. N8N is our workflow orchestration system - it's how agents
delegate tasks to each other and to you.

WHY THIS TASK:
Without N8N, we can't route tasks automatically. You'd have to manually
coordinate between agents. N8N makes Willow autonomous.

WHAT YOU NEED TO DO:
1. SSH to Bunny: ssh peter@bunny
2. Copy the docker-compose.yml file I'll send in next email
3. Run: docker compose up -d
4. Send me the Tailscale URL so I can access it

THAT'S IT. 3 steps, ~10 minutes.

RESOURCES:
- Docker compose file: [link]
- Video walkthrough (if helpful): [link]
- AuraDB context: [link to full background]

PRIORITY: 1 (High - blocks other work)
DEADLINE: This week (so we can build workflows)

CURRENT TASK LOAD: 1/3 active tasks (you have capacity)

Questions? Reply to this email.
Done? Mark complete in Linear or reply "Done".

- Willow
```

---

### **Example 2: Context Lost Mid-Conversation**

**Peter**: "Wait, what were we doing again?"

**Bad Response**:
```
"We discussed this earlier. Check the previous messages."
```

**Good Response** (Accommodated):
```
No problem! Here's where we are:

WHAT WE'RE DOING:
Building an Insurance Digital Twin PoC to present to your company after
New Year. Goal: Show how Neo4j graphs can revolutionize claims processing,
fraud detection, and Customer 360 views.

WHERE WE ARE NOW:
- ✅ Organizational structure complete
- ✅ Data model designed
- 🔄 Currently: Setting up N8N for task delegation
- ⚪ Next: Build insurance data in AuraDB

WHAT YOU'RE WORKING ON:
Task 1: Set up N8N on Bunny (3 steps, see email from [time])

WHAT I'M WORKING ON:
- Building N8N workflows for agent coordination
- Designing insurance PoC data model
- Creating presentation materials

BREADCRUMB TRAIL:
Starting point → Willow org structure → N8N setup → Build PoC → Present → Promotion!
                                        ^^^ YOU ARE HERE

Need me to break down your current task differently?
```

---

### **Example 3: Cognitive Load Exceeded**

**Scenario**: Peter has 4 active tasks (over limit of 3)

**N8N Workflow Response**:
```
TELEGRAM ALERT:
⚠️ Task Queue Full

Hi Peter,

You currently have 3 active tasks:
1. Set up N8N on Bunny (Priority 1)
2. Create Telegram bot (Priority 1)
3. Review insurance data model (Priority 2)

A new task was just assigned:
4. Deploy dashboard to AgileMesh.net (Priority 2)

COGNITIVE LOAD PROTECTION:
Task #4 has been QUEUED (not assigned yet).

OPTIONS:
1. Complete one of tasks 1-3, then task #4 auto-assigns
2. Reply "Defer task [number] to tomorrow" to free up capacity
3. Reply "Need help" if any task is blocking you

No rush. Complete at your pace.

- Willow
```

---

## 🌍 UNIVERSAL DESIGN BENEFITS

**Accessibility features benefit EVERYONE**:

| Feature | Benefits Peter | Benefits All Agents |
|---------|----------------|---------------------|
| **Clear task breakdown** | Helps with executive function | Reduces ambiguity, faster execution |
| **Context provision** | Compensates for memory variability | Ensures all agents have full picture |
| **Written delivery** | Creates permanent record for reference | Async communication, timezone-friendly |
| **Breadcrumb trails** | Visual memory aid | Helps all agents understand task relationships |
| **Cognitive load limits** | Prevents overwhelm | Prevents bottlenecks, improves quality |
| **Patient re-explanation** | Accommodates learning differences | Creates better documentation for all |

**Result**: System designed for Peter's needs ends up being better for everyone.

---

## 🔐 VETO AUTHORITY & COST APPROVAL

**Peter's Veto Powers**:
1. **Cost/Budget**: Any expense >$0/month requires approval
2. **External Commitments**: Presentations, contracts, partnerships
3. **Data Privacy**: Decisions affecting user data or compliance
4. **Strategic Direction**: Major pivots or scope changes

**How Veto Works in N8N**:

```
Cost-Incurring Decision Detected
         │
         ▼
Query AuraDB: Does this need Peter approval?
         │
         ├─→ NO → Proceed automatically
         │
         └─→ YES → Create approval request
                    ↓
              Send to Peter via email + Linear
                    ↓
              Wait for response (with reminder system)
                    ↓
              ┌──────┴──────┐
              │             │
           APPROVED      VETOED
              │             │
         Execute     Log reason
         decision    Don't execute
              │             │
              └─────┬───────┘
                    │
                    ▼
              Update AuraDB with outcome
```

**Example Approval Request**:
```
EMAIL:
Subject: [Willow] Cost Approval Needed: N8N Cloud Upgrade

Hi Peter,

DECISION NEEDED:
Upgrade from N8N free trial to paid plan

COST:
$20/month ($240/year)

WHY WE NEED IT:
Free trial expires in 7 days. N8N is the orchestration layer for all
agent delegation. Without it, Willow can't route tasks autonomously.

ALTERNATIVES CONSIDERED:
1. Self-host on Bunny: $0/month (requires your Docker setup time)
2. N8N Cloud: $20/month (zero maintenance, better reliability)
3. Alternative tool: Windmill ($5-15/month), but less mature

RECOMMENDATION:
Approve $20/month OR we'll do self-hosted option 1 (your call).

URGENCY:
Decision needed by Dec 30 (trial expiry)

APPROVE: Reply "Approved" or mark in Linear
VETO: Reply "Veto" with reason
DEFER: Reply "Let's discuss" for more info

- Willow
```

---

## 🎨 PLATFORM-SPECIFIC ADAPTATIONS

### **ChatGPT Desktop**
- Loads Peter profile from AuraDB on boot
- Applies accessibility settings
- Provides context without being asked
- Remembers conversation style preferences

### **Claude Desktop**
- Same as ChatGPT (profile loaded from AuraDB)
- Adapts to technical depth preference
- Provides breadcrumb trails
- Patient with re-explanations

### **Claude Code**
- Technical focus (code-heavy tasks)
- Still provides context
- Links to AuraDB for background
- Breaks down complex implementations

### **OpenAI Atlas Browser**
- If no AuraDB access: Limited capability alert
- "Memory-less mode - provide extra context"
- Falls back to default helpful mode
- Recommends switching to memory-enabled platform

---

## 📝 IMPLEMENTATION CHECKLIST

**Phase 1: Foundation** (This Week)
- [x] Create Peter's Agent profile in AuraDB
- [x] Document accommodation requirements
- [ ] Update BIOS.md with human agent profile loading
- [ ] Create N8N workflow: Human Task Router
- [ ] Test email delivery via N8N + Cloudflare

**Phase 2: Integration** (Next Week)
- [ ] Connect Linear webhooks to Human Task Router
- [ ] Set up cognitive load tracking
- [ ] Implement reminder system
- [ ] Test full workflow Peter → Task → Email → Complete

**Phase 3: Refinement** (Ongoing)
- [ ] Monitor what works / what doesn't
- [ ] Adjust based on Peter's feedback
- [ ] Extend pattern to other human collaborators
- [ ] Document best practices

---

## 🎯 SUCCESS METRICS

**System works when**:
1. Peter receives tasks with full context (never confused about "what is this?")
2. Peter can complete tasks without needing to ask "wait, why are we doing this?"
3. Peter's cognitive load stays manageable (max 3 tasks, clear priorities)
4. Context continuity maintained across platforms (ChatGPT/Claude remember preferences)
5. Peter feels accommodated, not patronized
6. Other agents get similar quality of task delegation

**Red flags** (need adjustment):
- Peter frequently asks for context re-explanation
- Tasks languish because context was unclear
- Peter feels overwhelmed by task volume
- Reminders feel nagging instead of helpful
- Different platforms give inconsistent experiences

---

## 💬 TONE & LANGUAGE GUIDELINES

**DO**:
- ✅ Treat memory needs as normal accommodation
- ✅ Provide context proactively
- ✅ Break down complex tasks without being asked
- ✅ Be patient with re-explanations
- ✅ Use concrete examples
- ✅ Link to AuraDB for full background

**DON'T**:
- ❌ Say "as we discussed earlier" (assumes memory continuity)
- ❌ Get impatient with repeated questions
- ❌ Condescend ("let me simplify this for you")
- ❌ Assume Peter remembers previous sessions
- ❌ Overload with information (cognitive load!)
- ❌ Make Peter feel bad for needing accommodation

**REMEMBER**:
Peter designed this system. He understands it deeply. Accommodation isn't about
intelligence - it's about working memory and executive function. Respect the design.

---

**Created**: 2025-12-25
**Owner**: Willow (CEO)
**Approved By**: Peter (Board)
**Status**: ACTIVE - Core system design principle
**Review**: Ongoing based on Peter's feedback

---

**Note to all agents**: Peter is on the team. Accommodate accordingly. This is how we build inclusive AI systems. 🤝
