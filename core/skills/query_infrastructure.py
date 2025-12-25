"""
Willow Skill: Query Infrastructure Status
Get real-time status of all infrastructure nodes (Frank, Bunny, Mac)
"""

from typing import Optional
from neo4j import GraphDatabase
import os
import certifi
import subprocess

NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USER = os.getenv("NEO4J_USER")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")

def execute(node_name: Optional[str] = None) -> dict:
    """
    Query the infrastructure status from the graph and optionally ping the node
    
    Args:
        node_name: Optional specific node to check (Frank, Bunny, Mac)
    
    Returns:
        dict with infrastructure status and connectivity info
    """
    os.environ['SSL_CERT_FILE'] = certifi.where()
    os.environ['REQUESTS_CA_BUNDLE'] = certifi.where()
    
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
    
    try:
        with driver.session() as session:
            query = """
                MATCH (i:Infrastructure)
                WHERE $node_name IS NULL OR i.name = $node_name
                OPTIONAL MATCH (i)-[:HOSTS]->(s)
                RETURN i.name as name, 
                       i.role as role, 
                       i.status as status,
                       i.network_address as address,
                       collect(s.name) as services
            """
            
            results = session.run(query, node_name=node_name)
            
            nodes = []
            for record in results:
                node = {
                    "name": record["name"],
                    "role": record["role"],
                    "status": record["status"],
                    "address": record["address"],
                    "services": record["services"]
                }
                
                # Try to ping if it's a network node
                if record["address"]:
                    try:
                        result = subprocess.run(
                            ["ping", "-c", "1", "-W", "1", record["address"]], 
                            capture_output=True,
                            timeout=2
                        )
                        node["reachable"] = result.returncode == 0
                    except:
                        node["reachable"] = "unknown"
                
                nodes.append(node)
            
            return {
                "success": True,
                "nodes": nodes,
                "count": len(nodes)
            }
            
    except Exception as e:
        return {"success": False, "error": str(e)}
    finally:
        driver.close()
