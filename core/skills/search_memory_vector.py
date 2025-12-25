"""
Willow Skill: Search Memory with Vector
Perform semantic search on the knowledge graph using vector embeddings
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

def execute(query: str, limit: int = 5, index_name: str = "willow_memory") -> dict:
    """
    Search memories using semantic similarity (vector search)
    
    Args:
        query: The search query text
        limit: Maximum number of results (default: 5)
        index_name: Vector index to search (willow_memory, willow_ideas)
    
    Returns:
        dict with matching memories and similarity scores
    """
    os.environ['SSL_CERT_FILE'] = certifi.where()
    os.environ['REQUESTS_CA_BUNDLE'] = certifi.where()
    
    try:
        # Generate embedding for the query using Ollama
        response = requests.post(
            f"{OLLAMA_URL}/api/embeddings",
            json={"model": "nomic-embed-text", "prompt": query},
            timeout=10
        )
        query_embedding = response.json()["embedding"]
        
        # Search the graph
        driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
        
        with driver.session() as session:
            # Use vector similarity search
            result = session.run("""
                CALL db.index.vector.queryNodes($index, $limit, $embedding)
                YIELD node, score
                RETURN node.title as title, 
                       node.content as content,
                       node.category as category,
                       node.timestamp as timestamp,
                       score
                ORDER BY score DESC
            """, index=index_name, limit=limit, embedding=query_embedding)
            
            memories = []
            for record in result:
                memories.append({
                    "title": record["title"],
                    "content": record["content"],
                    "category": record["category"],
                    "timestamp": str(record["timestamp"]),
                    "similarity": round(record["score"], 3)
                })
            
            driver.close()
            
            return {
                "success": True,
                "query": query,
                "results": memories,
                "count": len(memories)
            }
            
    except Exception as e:
        return {"success": False, "error": str(e), "query": query}
