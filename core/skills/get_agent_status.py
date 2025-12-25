"""
Willow Skill: Get Agent Status
Query the swarm status - which agents exist and what they're doing
"""

from neo4j import GraphDatabase
import os
import certifi

NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USER = os.getenv("NEO4J_USER")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")

def execute() -> dict:
    """
    Get the status of all agents in the swarm
    
    Returns:
        dict with agent list and their current assignments
    """
    os.environ['SSL_CERT_FILE'] = certifi.where()
    os.environ['REQUESTS_CA_BUNDLE'] = certifi.where()
    
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
    
    try:
        with driver.session() as session:
            # Get agents and their current tasks
            result = session.run("""
                MATCH (a:Agent)
                OPTIONAL MATCH (a)-[:ASSIGNED_TO]->(t:Task)
                WHERE t.status = 'In Progress'
                RETURN a.name as name,
                       a.role as role,
                       a.description as description,
                       collect(t.title) as current_tasks
                ORDER BY a.name
            """)
            
            agents = []
            for record in result:
                agents.append({
                    "name": record["name"],
                    "role": record["role"],
                    "description": record["description"],
                    "active_tasks": [t for t in record["current_tasks"] if t]
                })
            
            return {
                "success": True,
                "agents": agents,
                "count": len(agents)
            }
            
    except Exception as e:
        return {"success": False, "error": str(e)}
    finally:
        driver.close()
