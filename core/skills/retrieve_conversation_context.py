"""
Willow Skill: Retrieve Conversation Context
Query decisions and context from graph based on keywords
"""

from typing import Optional, List
from neo4j import GraphDatabase
import os

NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "willowdev123")

def execute(keyword: str, depth: int = 2, limit: int = 10) -> dict:
    """
    Query decisions and insights from the graph based on keyword

    Args:
        keyword: Search term to find in decisions/insights
        depth: How many relationship hops to traverse (default: 2)
        limit: Maximum results to return (default: 10)

    Returns:
        dict with matching decisions, insights, and related context
    """
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

    # Build query with depth baked in (Cypher doesn't support param in path length)
    query = f"""
    MATCH (d:Decision)
    WHERE d.text CONTAINS $keyword OR d.rationale CONTAINS $keyword
    OPTIONAL MATCH path = (d)-[*1..{depth}]-(related)
    WITH d, collect(DISTINCT related) as related_nodes
    RETURN d.text as decision,
           d.rationale as rationale,
           d.made_at as made_at,
           d.suggested_by as suggested_by,
           [node in related_nodes | labels(node)[0] + ': ' + coalesce(node.name, node.text, 'unknown')] as related
    LIMIT $limit
    """

    try:
        with driver.session() as session:
            result = session.run(query, {
                "keyword": keyword,
                "limit": limit
            })

            decisions = []
            for record in result:
                decisions.append({
                    "decision": record["decision"],
                    "rationale": record["rationale"],
                    "made_at": str(record["made_at"]) if record["made_at"] else None,
                    "suggested_by": record["suggested_by"],
                    "related": record["related"]
                })

            driver.close()

            return {
                "success": True,
                "keyword": keyword,
                "count": len(decisions),
                "decisions": decisions,
                "skill": "retrieve_conversation_context"
            }

    except Exception as e:
        driver.close()
        return {
            "success": False,
            "error": str(e),
            "skill": "retrieve_conversation_context"
        }

if __name__ == "__main__":
    # Test the skill
    result = execute("Docker")
    print(result)
