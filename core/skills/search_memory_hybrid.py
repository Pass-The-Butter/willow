"""
Willow Skill: Hybrid Memory Search (Augmented)
Implements true Hybrid Retrieval: BM25 (Keyword) + Vector (Semantic) + Graph Traversal
"""

from typing import Optional, List, Dict
from neo4j import GraphDatabase
import os
import certifi
import requests
from dotenv import load_dotenv

load_dotenv()

NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USER = os.getenv("NEO4J_USER")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://frank:11434")

def ensure_indexes(driver):
    """Ensure Fulltext Index exists for BM25 with error handling if it already exists."""
    with driver.session() as session:
        # Check if index exists first to avoid error
        result = session.run("SHOW INDEXES WHERE name = 'willow_memory_fulltext'")
        if result.peek() is None:
            session.run("""
                CREATE FULLTEXT INDEX willow_memory_fulltext
                FOR (n:Memory) ON EACH [n.title, n.content, n.category]
            """)

def reciprocal_rank_fusion(vector_results, bm25_results, k=60):
    """
    Combine results using RRF.
    Score = 1 / (k + rank)
    """
    scores = {}
    
    # Process Vector Results
    for rank, item in enumerate(vector_results):
        node_id = item['id']
        scores[node_id] = scores.get(node_id, 0) + (1 / (k + rank + 1))
        scores[node_id + "_data"] = item # Store data
        
    # Process BM25 Results
    for rank, item in enumerate(bm25_results):
        node_id = item['id']
        scores[node_id] = scores.get(node_id, 0) + (1 / (k + rank + 1))
        if node_id + "_data" not in scores:
            scores[node_id + "_data"] = item

    # Sort by fused score
    fused = []
    for node_id, score in scores.items():
        if "_data" in str(node_id): continue
        data = scores[node_id + "_data"]
        data['fused_score'] = score
        fused.append(data)
    
    return sorted(fused, key=lambda x: x['fused_score'], reverse=True)

def execute(query: str, limit: int = 5, traverse_depth: int = 2) -> dict:
    """
    Hybrid Search Execution:
    1. Vector Search (Ollama Embedding -> Neo4j Vector Index)
    2. BM25 Search (Neo4j Fulltext Index)
    3. RRF Fusion
    4. Graph Traversal for Context
    """
    # Fix SSL Context for requests on some Macs
    os.environ['SSL_CERT_FILE'] = certifi.where()
    
    try:
        driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
        ensure_indexes(driver)
        
        # 1. Generate Embedding
        response = requests.post(
            f"{OLLAMA_URL}/api/embeddings",
            json={"model": "nomic-embed-text", "prompt": query},
            timeout=10
        )
        if response.status_code != 200:
            # Fallback if Ollama is down - rely only on BM25?
            # For now, just raise
            raise Exception(f"Ollama Error: {response.text}")
            
        embedding = response.json().get("embedding")
        if not embedding:
            raise Exception("No embedding returned from Ollama")

        with driver.session() as session:
            # 2. Vector Search
            try:
                vector_res = session.run("""
                    CALL db.index.vector.queryNodes('willow_memory', $limit, $embedding)
                    YIELD node, score
                    RETURN elementId(node) as id, node.title as title, node.content as content, 
                           node.category as category, toString(node.timestamp) as timestamp, score as vector_score
                """, limit=limit * 2, embedding=embedding)
                vector_hits = [dict(r) for r in vector_res]
            except Exception as e:
                print(f"Vector search failed (maybe index missing): {e}")
                vector_hits = []
            
            # 3. BM25 Search
            try:
                # Lucene query syntax: handle spaces
                lucene_query = f"{query}" # Simple pass-through
                
                bm25_res = session.run("""
                    CALL db.index.fulltext.queryNodes("willow_memory_fulltext", $search_term, {limit: $limit})
                    YIELD node, score
                    RETURN elementId(node) as id, node.title as title, node.content as content,
                           node.category as category, toString(node.timestamp) as timestamp, score as bm25_score
                """, search_term=lucene_query, limit=limit * 2)
                
                bm25_hits = [dict(r) for r in bm25_res]
            except Exception as e:
                 print(f"BM25 search failed (maybe index missing): {e}")
                 bm25_hits = []
            
            # 4. Fusion
            fused_results = reciprocal_rank_fusion(vector_hits, bm25_hits)[:limit]
            
            # 5. Context Traversal (for top results only)
            final_output = []
            for item in fused_results:
                # Get context for this specific node
                ctx_res = session.run(f"""
                    MATCH (n) WHERE elementId(n) = $id
                    MATCH path = (n)-[*1..{traverse_depth}]-(connected)
                    RETURN collect(DISTINCT labels(connected)[0]) as types,
                           collect(DISTINCT connected.name) as names
                """, id=item['id'])
                
                ctx = ctx_res.single()
                item['context'] = {
                    "types": ctx['types'] if ctx else [],
                    "entities": [n for n in ctx['names'] if n] if ctx else []
                }
                final_output.append(item)
            
            driver.close()
            return {
                "success": True,
                "query": query,
                "method": "Hybrid RRF (Vector + BM25)",
                "results": final_output,
                "count": len(final_output)
            }

    except Exception as e:
        return {"success": False, "error": str(e), "query": query}
