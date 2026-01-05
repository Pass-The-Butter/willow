# Deep Research Agent Specification

> "Research like NotebookLM, publish to the Grapevine."

**Status**: Ready for PM Delegation  
**Priority**: High  
**Estimated Effort**: 4-6 hours  
**Cost**: $0-5/month (using free tiers)

---

## 📋 PROJECT DEFINITION (Meeseeks Format)

```yaml
PROJECT_DEFINITION:
  name: "Deep Research Agent"
  goal: "Build an autonomous research agent that accepts topics, conducts deep research including academic papers, and publishes structured reports to AuraDB (Grapevine) or Google Docs"
  constraints:
    - Use FREE APIs only (Gemini CLI, Brave Search 2000/mo, Semantic Scholar, arXiv)
    - Deploy on existing N8N (bunny:5678)
    - Store results in AuraDB (The Brain)
    - Trigger via Telegram bot
  deliverables:
    - N8N workflow: `bootstrap/deep_research_workflow.json`
    - AuraDB schema: ResearchTask, Source, Claim, ResearchReport nodes
    - Telegram integration for request/response
    - Test with sample query: "AI Agent Memory Architectures"
  acceptance_criteria:
    - [ ] Telegram message triggers research
    - [ ] Agent searches Brave, Semantic Scholar, arXiv
    - [ ] Agent uses Gemini API (2M context) for synthesis
    - [ ] Report published to AuraDB with citations
    - [ ] Telegram notification on completion
    - [ ] < $5/month running costs
  context:
    - Plan: `.github/prompts/plan-deepResearchAgent.prompt.md`
    - Resources: `RESOURCES.md` (AI/LLM Services section)
    - Infrastructure: N8N on bunny:5678, AuraDB credentials in .env
```

---

## 🎯 GOAL

Create a self-hosted "NotebookLM-style" research agent that:

1. **Accepts** a research topic via Telegram
2. **Searches** multiple sources (Brave web, Semantic Scholar papers, arXiv)
3. **Synthesizes** findings using Gemini API (2M token context)
4. **Publishes** structured report to AuraDB (Grapevine)
5. **Notifies** requester via Telegram with summary + link

---

## 🛠️ AVAILABLE RESOURCES

### AI APIs (from RESOURCES.md)

| API | Use In This Project | Cost |
|-----|---------------------|------|
| **Gemini API** | Main synthesis (2M context) | FREE (Google One) |
| **Gemini CLI** | Alternative: `gemini -p "query"` | 1000/day FREE |
| **Groq** | Intent classification, quick analysis | FREE tier |
| **OpenRouter** | Fallback for any model | Pay-per-token |

### Research APIs (FREE)

| API | Limit | Endpoint |
|-----|-------|----------|
| **Brave Search** | 2000/mo | `https://api.search.brave.com/res/v1/web/search` |
| **Semantic Scholar** | Unlimited | `https://api.semanticscholar.org/graph/v1/paper/search` |
| **arXiv** | Unlimited | `http://export.arxiv.org/api/query` |

### Infrastructure

- **N8N**: `http://bunny:5678` (workflow orchestration)
- **AuraDB**: `neo4j+s://e59298d2.databases.neo4j.io` (storage)
- **Telegram Bot**: `@Willow_AgileMesh_Bot` (trigger/notify)

---

## 📐 ARCHITECTURE

```
┌─────────────────────────────────────────────────────────────────┐
│                        DEEP RESEARCH AGENT                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────┐     ┌─────────────┐     ┌──────────────────┐     │
│  │ Telegram │────▶│   N8N       │────▶│ Research Sources │     │
│  │  Input   │     │  Workflow   │     │                  │     │
│  └──────────┘     └──────┬──────┘     │ • Brave Search   │     │
│                          │            │ • Semantic Scholar│     │
│                          ▼            │ • arXiv          │     │
│                   ┌──────────────┐    └────────┬─────────┘     │
│                   │   Gemini     │             │               │
│                   │   API        │◀────────────┘               │
│                   │  (2M ctx)    │                             │
│                   └──────┬───────┘                             │
│                          │                                      │
│                          ▼                                      │
│  ┌──────────┐     ┌──────────────┐     ┌──────────────────┐   │
│  │ Telegram │◀────│   AuraDB     │     │  ResearchReport  │   │
│  │  Notify  │     │  (Grapevine) │────▶│  Source, Claim   │   │
│  └──────────┘     └──────────────┘     │  nodes           │   │
│                                         └──────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📊 AURADB SCHEMA

```cypher
// ResearchTask - The request
CREATE (rt:ResearchTask {
  id: "research-001",
  topic: "AI Agent Memory Architectures",
  requested_by: "Peter",
  requested_at: datetime(),
  status: "in_progress",  // pending, in_progress, complete, failed
  telegram_chat_id: "123456"
})

// Source - Each reference found
CREATE (s:Source {
  id: "source-001",
  title: "MemGPT: Towards LLMs as Operating Systems",
  url: "https://arxiv.org/abs/2310.08560",
  type: "academic_paper",  // web_page, academic_paper, news
  authors: ["Charles Packer", "Sarah Wooders"],
  publication_date: date("2023-10-12"),
  tldr: "Hierarchical memory management for LLMs",
  relevance_score: 0.92,
  retrieved_at: datetime()
})

// Claim - Extracted insights
CREATE (c:Claim {
  id: "claim-001",
  text: "Hierarchical memory with main context and external storage improves long-term reasoning",
  confidence: 0.85,
  category: "architecture_pattern"
})

// ResearchReport - The final synthesis
CREATE (rr:ResearchReport {
  id: "report-001",
  title: "AI Agent Memory Architectures: State of the Art 2025",
  executive_summary: "...",
  full_content: "...",
  word_count: 2500,
  created_at: datetime(),
  model_used: "gemini-2.5-pro"
})

// Relationships
(rt)-[:PRODUCED]->(rr)
(rr)-[:CITES]->(s)
(rr)-[:CONTAINS_CLAIM]->(c)
(c)-[:EXTRACTED_FROM]->(s)
```

---

## 🔧 N8N WORKFLOW STRUCTURE

### Nodes Required:

1. **Telegram Trigger** - Listen for research requests
2. **Intent Classifier** (Groq) - Confirm this is a research request
3. **Create ResearchTask** - Log to AuraDB
4. **Parallel Search**:
   - Brave Search API (web)
   - Semantic Scholar API (papers)
   - arXiv API (preprints)
5. **Aggregate Sources** - Combine and dedupe
6. **Gemini Synthesis** - 2M context analysis
7. **Extract Claims** - Parse structured insights
8. **Store Report** - Write to AuraDB
9. **Telegram Notify** - Send summary to requester

### Workflow JSON Location:
`bootstrap/deep_research_workflow.json`

---

## 🔑 REQUIRED SECRETS

Add to N8N credentials or `.env`:

| Secret | Source | Status |
|--------|--------|--------|
| `GEMINI_API_KEY` | https://aistudio.google.com/apikey | ⏳ Needed |
| `BRAVE_API_KEY` | https://brave.com/search/api/ | ⏳ Needed |
| `NEO4J_URI` | Already in .env | ✅ |
| `NEO4J_PASSWORD` | Already in .env | ✅ |
| `TELEGRAM_BOT_TOKEN` | Already in .env | ✅ |

---

## 📝 IMPLEMENTATION STEPS

### Phase 1: Setup (30 mins)
1. [ ] Get Gemini API key from AI Studio
2. [ ] Get Brave Search API key (free tier)
3. [ ] Add credentials to N8N

### Phase 2: Schema (30 mins)
1. [ ] Deploy AuraDB schema (ResearchTask, Source, Claim, ResearchReport)
2. [ ] Test with sample nodes
3. [ ] Create indexes for search

### Phase 3: N8N Workflow (2-3 hours)
1. [ ] Create Telegram trigger node
2. [ ] Add Groq intent classifier
3. [ ] Build Brave Search integration
4. [ ] Build Semantic Scholar integration  
5. [ ] Build arXiv integration
6. [ ] Add Gemini synthesis node (HTTP Request to API)
7. [ ] Add AuraDB write nodes
8. [ ] Add Telegram notification node
9. [ ] Test end-to-end

### Phase 4: Testing (1 hour)
1. [ ] Test: "What is the top AI Agent Memory Architecture?"
2. [ ] Verify sources are diverse (web + papers)
3. [ ] Verify report is stored in AuraDB
4. [ ] Verify Telegram notification works
5. [ ] Check cost (should be $0)

---

## 🧪 TEST CRITERIA

```gherkin
Feature: Deep Research Agent

Scenario: Research AI Memory Architectures
  Given I send "@Willow_AgileMesh_Bot research: AI Agent Memory Architectures"
  When the agent processes my request
  Then I should receive an acknowledgment within 10 seconds
  And the agent should search at least 3 sources
  And a ResearchReport node should be created in AuraDB
  And I should receive a summary on Telegram within 5 minutes
  And the report should cite at least 5 sources
  And the cost should be $0

Scenario: Handle Invalid Request
  Given I send "@Willow_AgileMesh_Bot hello"
  When the agent classifies the intent
  Then it should NOT trigger a research workflow
  And should respond with a helpful message
```

---

## 🎯 SUCCESS METRICS

| Metric | Target |
|--------|--------|
| Response time (ack) | < 10 seconds |
| Full report time | < 5 minutes |
| Sources per report | ≥ 5 |
| Monthly cost | ≤ $5 |
| Academic paper ratio | ≥ 30% of sources |

---

## 📎 RELATED DOCUMENTS

- **Implementation Plan**: [.github/prompts/plan-deepResearchAgent.prompt.md](../../.github/prompts/plan-deepResearchAgent.prompt.md)
- **Resources Registry**: [RESOURCES.md](../../RESOURCES.md)
- **PM Agent Spec**: [PROJECT_MANAGER_AGENT.md](PROJECT_MANAGER_AGENT.md)
- **Economical Agent Pattern**: [ECONOMICAL_AGENT_SPEC.md](ECONOMICAL_AGENT_SPEC.md)

---

## 🤖 PM DELEGATION COMMAND

To delegate this to a Meeseeks PM Agent:

```
Use the meeseeks-pm-deep-research agent with this project definition:

PROJECT: Deep Research Agent
GOAL: Build autonomous research agent on N8N that searches web + academic sources, 
      synthesizes with Gemini (2M context), publishes to AuraDB
SPEC: docs/specs/DEEP_RESEARCH_AGENT_SPEC.md
PLAN: .github/prompts/plan-deepResearchAgent.prompt.md
BUDGET: $0-5/month
TIMELINE: 4-6 hours
```

---

**Created**: 2025-01-05  
**Author**: Captain Willow  
**Status**: Ready for Implementation
