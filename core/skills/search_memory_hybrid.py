"""
Willow Skill: Hybrid Memory Search
Implements full GraphRAG pattern: Vector entry point + Graph traversal for context
"""

from typing import Optional
from neo4j import GraphDatabase
import os
import certifi
import requests

NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USER = os.getenv("NEO4J_USER")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://frank:11434")

def execute(query: str, limit: int = 5, traverse_depth: int = 2) -> dict:
    """
    GraphRAG Hybrid Search:
    1. Use vector similarity to find entry points
    2. Traverse graph relationships to gather context
    3. Return enriched results with connected knowledge
    
    Args:
        query: The search query text
        limit: Maximum number of entry points (default: 5)
        traverse_depth: How many hops to traverse for context (default: 2)
    
    Returns:
        dict with memories and their connected context (decisions, components, agents)
    """
    os.environ['SSL_CERT_FILE'] = certifi.where()
    os.environ['REQUESTS_CA_BUNDLE'] = certifi.where()
    
    try:
        # Step 1: Vector Search (Fuzzy Entry Point)
        response = requests.post(
            f"{OLLAMA_URL}/api/embeddings",
            json={"model": "nomic-embed-text", "prompt": query},
            timeout=10
        )
        query_embedding = response.json()["embedding"]
        
        driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
        
        with driver.session() as session:
            # Step 2: Vector search + Graph traversal (GraphRAG Core)
            result = session.run(f"""
                CALL db.index.vector.queryNodes('willow_memory', $limit, $embedding)
                YIELD node, score
                
                // Now traverse from each found node to gather context
                CALL {{
                    WITH node
                    MATCH path = (node)-[*1..{traverse_depth}]-(connected)
                    RETURN node, 
                           collect(DISTINCT labels(connected)[0]) as connected_types,
                           collect(DISTINCT connected.name) as connected_names
                }}
                
                RETURN node.title as title,
                       node.content as content,
                       node.category as category,
                       node.timestamp as timestamp,
                       score,
                       connected_types,
                       connected_names
                ORDER BY score DESC
            """, limit=limit, embedding=query_embedding)
            
            memories = []
            for record in result:
                memories.append({
                    "title": record["title"],
                    "content": record["content"],
                    "category": record["category"],
                    "timestamp": str(record["timestamp"]),
                    "similarity": round(record["score"], 3),
                    "context": {
                        "types": list(set(record["connected_types"])),
                        "entities": list(set([n for n in record["connected_names"] if n]))
                    }
                })
            
            driver.close()
            
            return {
                "success": True,
                "query": query,
                "method": "GraphRAG (Vector + Traversal)",
                "results": memories,
                "count": len(memories)
            }
            
    except Exception as e:
        return {"success": False, "error": str(e), "query": query}
