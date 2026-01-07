#!/usr/bin/env python3
"""
Willow Skill: Deep Research Agent
Conducts deep research on a topic using Brave Search, Semantic Scholar, and arXiv
Synthesizes findings with Gemini API and publishes to AuraDB
"""

import os
import json
import requests
from datetime import datetime
from typing import Dict, Any, List
from neo4j import GraphDatabase
from dotenv import load_dotenv

load_dotenv()

# Environment
NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USER = os.getenv("NEO4J_USER")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
BRAVE_API_KEY = os.getenv("BRAVE_API_KEY")

# API Endpoints
BRAVE_SEARCH_URL = "https://api.search.brave.com/res/v1/web/search"
SEMANTIC_SCHOLAR_URL = "https://api.semanticscholar.org/graph/v1/paper/search"
ARXIV_URL = "http://export.arxiv.org/api/query"
GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"


def brave_search(query: str, count: int = 5) -> List[Dict]:
    """Search the web using Brave Search API"""
    print(f"  🔍 Brave Search: {query}")
    try:
        response = requests.get(
            BRAVE_SEARCH_URL,
            headers={"X-Subscription-Token": BRAVE_API_KEY, "Accept": "application/json"},
            params={"q": query, "count": count}
        )
        response.raise_for_status()
        data = response.json()
        
        results = []
        for result in data.get("web", {}).get("results", []):
            results.append({
                "title": result.get("title", ""),
                "url": result.get("url", ""),
                "description": result.get("description", ""),
                "type": "web_page"
            })
        print(f"    ✅ Found {len(results)} web results")
        return results
    except Exception as e:
        print(f"    ⚠️  Brave Search error: {e}")
        return []


def semantic_scholar_search(query: str, limit: int = 5) -> List[Dict]:
    """Search academic papers using Semantic Scholar API"""
    print(f"  📚 Semantic Scholar: {query}")
    try:
        response = requests.get(
            SEMANTIC_SCHOLAR_URL,
            params={
                "query": query,
                "limit": limit,
                "fields": "title,authors,year,abstract,url,citationCount,tldr"
            }
        )
        response.raise_for_status()
        data = response.json()
        
        results = []
        for paper in data.get("data", []):
            results.append({
                "title": paper.get("title", ""),
                "url": paper.get("url", ""),
                "description": paper.get("tldr", {}).get("text", "") or paper.get("abstract", "")[:200],
                "authors": [a.get("name") for a in paper.get("authors", [])],
                "year": paper.get("year"),
                "citations": paper.get("citationCount", 0),
                "type": "academic_paper"
            })
        print(f"    ✅ Found {len(results)} papers")
        return results
    except Exception as e:
        print(f"    ⚠️  Semantic Scholar error: {e}")
        return []


def arxiv_search(query: str, max_results: int = 3) -> List[Dict]:
    """Search preprints using arXiv API"""
    print(f"  📄 arXiv: {query}")
    try:
        response = requests.get(
            ARXIV_URL,
            params={
                "search_query": f"all:{query}",
                "max_results": max_results,
                "sortBy": "relevance"
            }
        )
        response.raise_for_status()
        
        # Parse XML (simple approach)
        import xml.etree.ElementTree as ET
        root = ET.fromstring(response.content)
        ns = {"atom": "http://www.w3.org/2005/Atom"}
        
        results = []
        for entry in root.findall("atom:entry", ns):
            title = entry.find("atom:title", ns).text.strip() if entry.find("atom:title", ns) is not None else ""
            url = entry.find("atom:id", ns).text if entry.find("atom:id", ns) is not None else ""
            summary = entry.find("atom:summary", ns).text.strip()[:200] if entry.find("atom:summary", ns) is not None else ""
            
            results.append({
                "title": title,
                "url": url,
                "description": summary,
                "type": "preprint"
            })
        print(f"    ✅ Found {len(results)} arXiv papers")
        return results
    except Exception as e:
        print(f"    ⚠️  arXiv error: {e}")
        return []


def gemini_synthesize(query: str, sources: List[Dict]) -> Dict:
    """Synthesize research findings using Gemini API"""
    print(f"  🤖 Gemini: Synthesizing {len(sources)} sources...")
    
    # Build context from sources
    context = f"Research Query: {query}\n\nSources:\n"
    for i, source in enumerate(sources, 1):
        context += f"\n{i}. {source['title']} ({source['type']})\n"
        context += f"   URL: {source['url']}\n"
        context += f"   Summary: {source['description']}\n"
    
    prompt = f"""{context}

Based on these sources, provide a comprehensive research report on: {query}

Include:
1. Executive Summary (2-3 sentences)
2. Key Findings (3-5 bullet points)
3. Analysis (2-3 paragraphs)
4. Recommendations (if applicable)
5. Source Citations

Format as structured text."""
    
    try:
        response = requests.post(
            GEMINI_URL,
            headers={
                "Content-Type": "application/json",
                "X-goog-api-key": GEMINI_API_KEY
            },
            json={
                "contents": [{"parts": [{"text": prompt}]}]
            }
        )
        response.raise_for_status()
        
        result = response.json()
        report_text = result["candidates"][0]["content"]["parts"][0]["text"]
        
        print(f"    ✅ Generated {len(report_text)} character report")
        return {
            "full_content": report_text,
            "word_count": len(report_text.split()),
            "model_used": "gemini-2.0-flash"
        }
    except Exception as e:
        print(f"    ❌ Gemini error: {e}")
        return {
            "full_content": "Error generating report",
            "word_count": 0,
            "model_used": "gemini-2.0-flash",
            "error": str(e)
        }


def save_to_auradb(query: str, sources: List[Dict], report: Dict) -> str:
    """Save research task, sources, and report to AuraDB"""
    print(f"  💾 Saving to AuraDB...")
    
    import certifi
    os.environ['SSL_CERT_FILE'] = certifi.where()
    
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
    
    try:
        with driver.session() as session:
            # Create ResearchTask
            task_result = session.run("""
                CREATE (rt:ResearchTask {
                    id: randomUUID(),
                    topic: $topic,
                    requested_by: 'System',
                    requested_at: datetime(),
                    status: 'complete',
                    source_count: $source_count
                })
                RETURN rt.id as task_id
            """, topic=query, source_count=len(sources))
            
            task_id = task_result.single()["task_id"]
            
            # Create Sources
            for source in sources:
                session.run("""
                    MATCH (rt:ResearchTask {id: $task_id})
                    CREATE (s:Source {
                        id: randomUUID(),
                        title: $title,
                        url: $url,
                        type: $type,
                        description: $description,
                        retrieved_at: datetime()
                    })
                    MERGE (rt)-[:USED_SOURCE]->(s)
                """, task_id=task_id, **source)
            
            # Create ResearchReport
            session.run("""
                MATCH (rt:ResearchTask {id: $task_id})
                CREATE (rr:ResearchReport {
                    id: randomUUID(),
                    title: $title,
                    full_content: $content,
                    word_count: $word_count,
                    created_at: datetime(),
                    model_used: $model
                })
                MERGE (rt)-[:PRODUCED]->(rr)
            """, 
                task_id=task_id,
                title=f"Research Report: {query}",
                content=report["full_content"],
                word_count=report["word_count"],
                model=report["model_used"]
            )
            
            print(f"    ✅ Saved task {task_id}")
            return task_id
    except Exception as e:
        print(f"    ⚠️  AuraDB save failed: {e}")
        # Save to local file as fallback
        task_id = f"local-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        filename = f"research_report_{task_id}.json"
        with open(filename, 'w') as f:
            json.dump({
                "task_id": task_id,
                "query": query,
                "sources": sources,
                "report": report,
                "timestamp": datetime.now().isoformat()
            }, f, indent=2)
        print(f"    💾 Saved locally as {filename}")
        return task_id
    finally:
        driver.close()


def execute(query: str, max_sources: int = 10) -> Dict[str, Any]:
    """
    Execute deep research on a topic
    
    Args:
        query: Research topic or question
        max_sources: Maximum number of sources to gather (default: 10)
    
    Returns:
        dict with task_id, sources, report, and status
    """
    print("=" * 60)
    print(f"🔬 DEEP RESEARCH AGENT")
    print("=" * 60)
    print(f"Query: {query}\n")
    
    # Gather sources from multiple APIs
    print("📊 Gathering sources...")
    sources = []
    sources.extend(brave_search(query, count=5))
    sources.extend(semantic_scholar_search(query, limit=5))
    sources.extend(arxiv_search(query, max_results=3))
    
    # Dedupe by URL
    seen_urls = set()
    unique_sources = []
    for source in sources:
        if source["url"] not in seen_urls:
            seen_urls.add(source["url"])
            unique_sources.append(source)
    
    sources = unique_sources[:max_sources]
    print(f"\n✅ Collected {len(sources)} unique sources\n")
    
    # Synthesize with Gemini
    print("🧠 Synthesizing report...")
    report = gemini_synthesize(query, sources)
    
    # Save to AuraDB
    print("\n💾 Storing results...")
    task_id = save_to_auradb(query, sources, report)
    
    print("\n" + "=" * 60)
    print("✅ RESEARCH COMPLETE")
    print("=" * 60)
    
    return {
        "success": True,
        "task_id": task_id,
        "source_count": len(sources),
        "report_word_count": report["word_count"],
        "report_preview": report["full_content"][:200] + "...",
        "model_used": report["model_used"]
    }


if __name__ == "__main__":
    import sys
    query = sys.argv[1] if len(sys.argv) > 1 else "AI Agent Memory Architectures"
    result = execute(query)
    print(f"\n📋 Task ID: {result['task_id']}")
    print(f"📚 Sources: {result['source_count']}")
    print(f"📄 Report: {result['report_word_count']} words")
