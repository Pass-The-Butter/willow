# Plan: Custom Deep Research Agent for Willow

Build a self-hosted NotebookLM-like research agent using existing infrastructure (N8N, Ollama, AuraDB) plus free academic APIs. Accepts research topics via Telegram/webhook, performs recursive web + academic paper research, synthesizes findings with reasoning LLM, and publishes to the Grapevine (AuraDB) with implementation recommendations.

---

## 🆕 OPTION 0: Gemini API with 2M Context Window (Recommended)

**Reality Check**: The NotebookLM Enterprise API requires Google Workspace Enterprise. However, with **Google One AI Premium** (Gemini Advanced), you can replicate NotebookLM's core functionality using the **Gemini API** directly.

### Why This Works

NotebookLM is essentially Gemini + RAG + Document Ingestion. With Gemini API:
- **2 million token context window** = Upload entire PDFs, papers, codebases
- **Native RAG capabilities** = Query uploaded sources like NotebookLM
- **Same underlying model** = Gemini 1.5 Pro / 2.0

### Access Methods

| Method | Cost | Setup |
|--------|------|-------|
| **Google AI Studio** | Free tier + Pay-as-you-go | [aistudio.google.com](https://aistudio.google.com) |
| **Gemini API** | Free daily quota, then ~$0.00025/1K tokens | API key from AI Studio |
| **Vertex AI** | $300 free trial | Google Cloud Console |

### Quick Start: Gemini API for Research

```python
import google.generativeai as genai

genai.configure(api_key="YOUR_GEMINI_API_KEY")

# Use Gemini 1.5 Pro with 2M context window
model = genai.GenerativeModel('gemini-1.5-pro')

# Upload research sources (PDFs, papers, etc.)
sources = [
    genai.upload_file("paper1.pdf"),
    genai.upload_file("paper2.pdf"),
    genai.upload_file("blog_post.txt"),
]

# Research query with all sources as context
response = model.generate_content([
    *sources,
    """You are a research synthesis expert. Analyze these sources about 
    'AI Agent Memory Architectures' and provide:
    
    1. Executive Summary
    2. Key Findings (with citations to source documents)
    3. Comparison of Approaches
    4. Implementation Recommendations for our N8N + AuraDB stack
    5. Gaps in the research
    """
])

print(response.text)
```

### N8N Integration Architecture

```
Telegram/Webhook → N8N (Bunny)
                       ↓
         [Gather Sources via Free APIs]
         • Brave Search API → Web content
         • Semantic Scholar API → Academic papers
         • arXiv API → Preprints
                       ↓
         [Upload to Gemini API]
         • 2M token context window
         • All sources in single prompt
                       ↓
         [Gemini Synthesis]
         • Deep analysis across all sources
         • Citations and cross-references
         • Implementation recommendations
                       ↓
    [Publish to AuraDB + Telegram notify]
```

### Alternative: Google Drive Bridge to NotebookLM

If you want to use the actual NotebookLM UI:

```
N8N → Gather sources → Format as Google Docs → Upload to Google Drive folder
                                                        ↓
                              NotebookLM (synced to that folder) auto-ingests
                                                        ↓
                              Manual interaction or use browser automation
```

Tools for this approach:
- **[Apify to NotebookLM](https://github.com/doveretepergkhb/apify-to-notebooklm)** - Scrapes web data, formats to Google Docs
- **Google Drive API** - Programmatically add files to synced folder

### Discovery Engine API (Enterprise-Grade)

For more advanced RAG with structured data:

```python
# Google Cloud Discovery Engine (Vertex AI Search)
# Powers NotebookLM's enterprise backend
# $300 free trial available

from google.cloud import discoveryengine

client = discoveryengine.SearchServiceClient()

# Create a data store, upload documents, then search
response = client.search(
    serving_config="projects/YOUR_PROJECT/locations/global/dataStores/YOUR_STORE/servingConfigs/default",
    query="best practices for graph-based memory in AI agents",
)
```

---

## OPTION 1: Build Custom Research Agent (No Google Dependency)

## Architecture

```
Telegram/Webhook → N8N (Bunny) → Ollama (Frank) + Free APIs → AuraDB (Grapevine)
                       ↓
              [Query Expansion]     ← Ollama llama3 (FREE)
                       ↓
         [Parallel: Web + Academic Search]
         • Brave Search API (2000/mo FREE)
         • Semantic Scholar (unlimited FREE - 214M papers, TLDR summaries)
         • arXiv API (unlimited FREE)
                       ↓
              [Extract Claims]      ← Ollama mistral (FREE)
                       ↓
           [Depth Loop Check]       ← Recursive self-trigger
                       ↓
           [Final Synthesis]        ← OpenAI GPT-4 (~$0.20/report)
                       ↓
    [Publish to AuraDB + Telegram notify]
```

## Cost Summary

| Resource | Monthly Cost |
|----------|-------------|
| Brave Search (2000 free queries) | $0 |
| Semantic Scholar API | $0 |
| arXiv API | $0 |
| Ollama on Frank | $0 |
| OpenAI for synthesis (~100 reports) | ~$10-30 |
| N8N (self-hosted on Bunny) | $0 |
| AuraDB (existing) | Existing cost |
| **Total** | **~$10-30/month** |

## Implementation Steps

### Phase 1: API Setup (Day 1)
- [ ] Get Brave Search API key at https://brave.com/search/api/ (free tier: 2000/mo)
- [ ] Optionally get Tavily API key at https://tavily.com (backup, 1000/mo free)
- [ ] Test Semantic Scholar API (no key needed for basic usage)
- [ ] Add credentials to N8N on Bunny

### Phase 2: AuraDB Schema (Day 2)
- [ ] Deploy ResearchTask node type (tracks research jobs)
- [ ] Deploy Source node type (web/academic results)
- [ ] Deploy Claim node type (extracted facts)
- [ ] Deploy ResearchReport node type (final output)
- [ ] Create vector index for semantic search on Sources
- [ ] Test CRUD operations

### Phase 3: N8N Workflow (Days 3-4)
- [ ] Create `Deep Research Agent` workflow on Bunny
- [ ] Build webhook trigger endpoint `/webhook/research`
- [ ] Build query expansion node (HTTP to Ollama on Frank)
- [ ] Build parallel search nodes (Brave + Semantic Scholar + arXiv)
- [ ] Build source storage node (Neo4j create Source nodes)
- [ ] Build claim extraction node (Ollama mistral)
- [ ] Build depth check + self-trigger for recursion
- [ ] Build synthesis node (OpenAI GPT-4)
- [ ] Build AuraDB publish node (create ResearchReport)
- [ ] Build Telegram notification node

### Phase 4: Integration (Day 5)
- [ ] Add Telegram `/research <topic>` command handler
- [ ] Connect to existing Telegram bot workflow
- [ ] Test end-to-end flow with sample topic
- [ ] Add error handling and retry logic
- [ ] Document usage in BIOS or README

## AuraDB Schema (Cypher)

```cypher
// ResearchTask - The request/job
CREATE (rt:ResearchTask {
  id: apoc.create.uuid(),
  topic: "Graph RAG architectures for enterprise",
  status: "pending", // pending, searching, enriching, synthesizing, complete, failed
  depth: 0,
  max_depth: 3,
  breadth: 5,
  created_at: datetime(),
  updated_at: datetime(),
  triggered_by: "telegram", // telegram, api, schedule
  requestor: "Captain"
})

// Source - Raw search results
CREATE (s:Source {
  id: apoc.create.uuid(),
  type: "academic", // academic, web, arxiv
  title: "Paper title",
  url: "https://...",
  abstract: "...",
  snippet: "...",
  citation_count: 150,
  publication_date: date("2024-06-15"),
  pdf_url: "https://...",
  tldr: "AI-generated summary",
  relevance_score: 0.92,
  created_at: datetime()
})

// Claim - Extracted facts from sources
CREATE (c:Claim {
  id: apoc.create.uuid(),
  statement: "GraphRAG reduces hallucinations by 40%",
  confidence: 0.85,
  supporting_quote: "...",
  created_at: datetime()
})

// ResearchReport - Final output
CREATE (rr:ResearchReport {
  id: apoc.create.uuid(),
  title: "Deep Research: Graph RAG Architectures",
  executive_summary: "...",
  methodology: "Web search + Academic paper analysis",
  findings: "...", // Markdown formatted
  recommendations: "...",
  implementation_plan: "...",
  limitations: "...",
  sources_count: 25,
  academic_sources_count: 12,
  total_citations: 450,
  created_at: datetime(),
  published_to: "auradb"
})

// Relationships
CREATE (rt)-[:HAS_SOURCE]->(s)
CREATE (s)-[:SUPPORTS]->(c)
CREATE (rt)-[:PRODUCED]->(rr)
CREATE (parent:ResearchTask)-[:SPAWNED]->(child:ResearchTask)
CREATE (rr)-[:CITES]->(s)
CREATE (p:Project {name: 'Willow'})-[:HAS_RESEARCH]->(rr)
```

## N8N Workflow Nodes (Skeleton)

```json
{
  "name": "Deep Research Agent",
  "nodes": [
    {
      "name": "Research Trigger",
      "type": "n8n-nodes-base.webhook",
      "parameters": {
        "httpMethod": "POST",
        "path": "research"
      }
    },
    {
      "name": "Create ResearchTask",
      "type": "n8n-nodes-base.neo4j",
      "parameters": {
        "query": "CREATE (rt:ResearchTask {id: randomUUID(), topic: $topic, status: 'pending', depth: $depth, max_depth: $max_depth, created_at: datetime()}) RETURN rt"
      }
    },
    {
      "name": "Query Expansion (Ollama)",
      "type": "n8n-nodes-base.httpRequest",
      "parameters": {
        "url": "http://frank:11434/api/generate",
        "method": "POST",
        "body": {
          "model": "llama3",
          "prompt": "Generate 5 diverse search queries for: {{ $json.topic }}. Include academic and practical angles. Return as JSON array of strings.",
          "stream": false
        }
      }
    },
    {
      "name": "Brave Web Search",
      "type": "n8n-nodes-base.httpRequest",
      "parameters": {
        "url": "https://api.search.brave.com/res/v1/web/search",
        "headers": { "X-Subscription-Token": "{{ $env.BRAVE_API_KEY }}" },
        "qs": { "q": "{{ $json.query }}", "count": 10 }
      }
    },
    {
      "name": "Semantic Scholar Search",
      "type": "n8n-nodes-base.httpRequest",
      "parameters": {
        "url": "https://api.semanticscholar.org/graph/v1/paper/search",
        "qs": {
          "query": "{{ $json.query }}",
          "fields": "title,abstract,tldr,openAccessPdf,citationCount,year,authors",
          "limit": 10
        }
      }
    },
    {
      "name": "arXiv Search",
      "type": "n8n-nodes-base.httpRequest",
      "parameters": {
        "url": "http://export.arxiv.org/api/query",
        "qs": { "search_query": "all:{{ $json.query }}", "max_results": 10 }
      }
    },
    {
      "name": "Extract Claims (Ollama)",
      "type": "n8n-nodes-base.httpRequest",
      "parameters": {
        "url": "http://frank:11434/api/generate",
        "method": "POST",
        "body": {
          "model": "mistral",
          "prompt": "Extract key claims from: {{ $json.content }}. Return as JSON array with statement and confidence.",
          "stream": false
        }
      }
    },
    {
      "name": "Synthesize (OpenAI)",
      "type": "n8n-nodes-base.openAi",
      "parameters": {
        "model": "gpt-4",
        "messages": [
          { "role": "system", "content": "You are a research synthesis expert. Create a comprehensive report with: Executive Summary, Key Findings, Implementation Recommendations, Limitations, and Citations." },
          { "role": "user", "content": "Topic: {{ $json.topic }}\n\nSources:\n{{ $json.sources }}\n\nClaims:\n{{ $json.claims }}" }
        ]
      }
    },
    {
      "name": "Publish to AuraDB",
      "type": "n8n-nodes-base.neo4j",
      "parameters": {
        "query": "MATCH (rt:ResearchTask {id: $task_id}) CREATE (rr:ResearchReport { ... }) CREATE (rt)-[:PRODUCED]->(rr) WITH rr MATCH (p:Project {name: 'Willow'}) CREATE (p)-[:HAS_RESEARCH]->(rr)"
      }
    },
    {
      "name": "Telegram Notify",
      "type": "n8n-nodes-base.telegram",
      "parameters": {
        "chatId": "{{ $env.TELEGRAM_CHAT_ID }}",
        "text": "🔬 Research Complete: {{ $json.title }}\n\n{{ $json.executive_summary }}"
      }
    }
  ]
}
```

## Configuration Options

| Parameter | Default | Description |
|-----------|---------|-------------|
| `depth` | 2 | How many recursive search rounds |
| `breadth` | 5 | Queries per round |
| `max_sources` | 50 | Cap on total sources |
| `include_academic` | true | Search Semantic Scholar + arXiv |
| `include_web` | true | Search Brave |
| `synthesis_model` | gpt-4 | Model for final report |

**Estimated time**: Depth=2, Breadth=5 → 15-20 minutes per report

## Open Questions

1. **Gemini API key available?** Get from [AI Studio](https://aistudio.google.com) - should be free with Google One AI Premium
2. **Rate limiting?** Semantic Scholar is 1 RPS. Gemini API has daily free quota - check limits.
3. **PDF extraction?** Gemini can read PDFs directly via `genai.upload_file()` - no separate extraction needed!
4. **Prior research search?** Query AuraDB for existing ResearchReports on similar topics before starting?
5. **Audio output?** If needed, add Google Cloud TTS or ElevenLabs as final step

---

## OPTION 2: Local NotebookLM Clone (Fully Offline)

**Repo**: [W-X-Dai/notebooklm](https://github.com/W-X-Dai/notebooklm)

Uses Ollama + local TTS to create podcast-style research outputs. Good for complete offline operation on Frank.

**Requirements**: Ollama with gpt-oss:20B model, VibeVoice TTS

---

## Recommendation Matrix

| Requirement | Option 0 (Gemini API) | Option 1 (Custom N8N) | Option 2 (Local Clone) |
|-------------|------------------------|------------------------|------------------------|
| **Setup Complexity** | Low (API key only) | High (full workflow) | High (models + TTS) |
| **Ongoing Cost** | ~$0-5/mo (free tier + overflow) | ~$10-30/mo | $0 (electricity) |
| **Academic Paper Access** | Via gathered sources | Native Semantic Scholar | Manual PDF upload |
| **Synthesis Quality** | Excellent (Gemini 1.5 Pro) | Good (GPT-4) | Good (Ollama) |
| **Context Window** | 2M tokens! | Limited by API | Limited by VRAM |
| **Offline Capable** | No | Partial (Ollama steps) | Yes |
| **Audio Output** | No (use TTS separately) | No | Yes (TTS) |
| **Your Control** | Medium | Full | Full |

**Recommended Path**:
1. **Option 0 (Gemini API)** - Best balance of capability vs effort. Use 2M context window to replicate NotebookLM.
2. **Option 1 (Custom N8N)** - If you want full control and to avoid Google dependency
3. **Option 2** - For fully offline scenarios

---

## Next Steps

1. [ ] Get Gemini API key from [Google AI Studio](https://aistudio.google.com)
2. [ ] Test with a simple research query using the Python code above
3. [ ] Get Brave Search API key for source gathering
4. [ ] Build N8N workflow: Telegram → Gather Sources → Gemini API → AuraDB
5. [ ] Add Telegram notification for completed research

