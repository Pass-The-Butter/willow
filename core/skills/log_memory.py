"""
Willow Skill: Log Memory to Graph
Store decisions, ideas, insights, or general memories in the knowledge graph
Implements GraphRAG pattern: stores unstructured text + vector embedding + structured links
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

def execute(
    content: str,
    memory_type: str = "Memory",
    title: Optional[str] = None,
    category: Optional[str] = None,
    relates_to: Optional[str] = None,
    generate_embedding: bool = True
) -> dict:
    """
    Log a memory, decision, idea, or insight to the graph with vector embedding
    
    Args:
        content: The text content to store
        memory_type: Type of memory (Memory, Decision, Idea, Insight)
        title: Optional title for the memory
        category: Optional category (Architecture, Frontend, Backend, etc)
        relates_to: Optional component/entity name to link to
        generate_embedding: Whether to generate vector embedding (default: True)
    
    Returns:
        dict with success status and created node info
    """
    os.environ['SSL_CERT_FILE'] = certifi.where()
    os.environ['REQUESTS_CA_BUNDLE'] = certifi.where()
    
    # Generate embedding if requested (GraphRAG: Unstructured Memory)
    embedding = None
    if generate_embedding:
        try:
            response = requests.post(
                f"{OLLAMA_URL}/api/embeddings",
                json={"model": "nomic-embed-text", "prompt": content},
                timeout=10
            )
            embedding = response.json()["embedding"]
        except:
            pass  # Continue without embedding if Frank is unreachable
    
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
    
    try:
        with driver.session() as session:
            # Create the memory node with embedding (GraphRAG: Hybrid Storage)
            result = session.run(f"""
                CREATE (m:{memory_type})
                SET m.content = $content,
                    m.title = $title,
                    m.category = $category,
                    m.timestamp = datetime(),
                    m.status = 'Active',
                    m.embedding = $embedding
                RETURN m
            """, content=content, title=title or content[:50], category=category, embedding=embedding)
            
            node = result.single()
            
            # Link to related entity if specified (GraphRAG: Structured Links)
            if relates_to:
                session.run(f"""
                    MATCH (m:{memory_type}), (e)
                    WHERE m.content = $content 
                      AND (e.name = $relates_to OR e.title = $relates_to)
                    MERGE (m)-[:RELATES_TO]->(e)
                """, content=content, relates_to=relates_to)
            
            return {
                "success": True,
                "type": memory_type,
                "title": title or content[:50],
                "message": f"{memory_type} logged to graph",
                "has_embedding": embedding is not None
            }
            
    except Exception as e:
        return {"success": False, "error": str(e)}
    finally:
        driver.close()
