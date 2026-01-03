"""
Willow Graph Client
===================
The official client for accessing the Brain via the Gateway.
Replaces direct neo4j.GraphDatabase usage for Agents.

Usage:
    from core.clients.graph_client import GraphClient
    client = GraphClient(agent_id="my-agent")
    results = client.run("MATCH (n) RETURN n")
"""

import os
import requests
from typing import List, Dict, Any, Optional

# Default Gateway URL (internal Docker alias)
GATEWAY_URL = os.getenv("WILLOW_GATEWAY_URL", "http://bunny:8001")
# Fallback for local dev if bunny not resolved, use localhost
if "localhost" in os.getenv("NEO4J_URI", ""): # Heuristic
    GATEWAY_URL = "http://localhost:8001"

class GraphClient:
    def __init__(self, agent_id: str, gateway_url: str = None):
        self.agent_id = agent_id
        self.gateway_url = gateway_url or GATEWAY_URL
        self.endpoint = f"{self.gateway_url}/query"

    def run(self, cypher: str, parameters: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """
        Execute a Cypher query via the Gateway.
        
        Args:
            cypher: The query string
            parameters: Query parameters
            
        Returns:
            List of records (dicts)
            
        Raises:
            Exception: If policy violation or DB error
        """
        payload = {
            "cypher": cypher,
            "params": parameters or {},
            "agent_id": self.agent_id
        }
        
        try:
            response = requests.post(self.endpoint, json=payload, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    return data.get("data", [])
                else:
                    raise Exception(f"Gateway Error: {data.get('message')}")
            
            elif response.status_code == 403:
                raise Exception(f"Policy Violation: {response.json().get('message')}")
            
            else:
                raise Exception(f"HTTP {response.status_code}: {response.text}")

        except requests.RequestException as e:
            raise Exception(f"Connection Failed to Gateway at {self.gateway_url}: {e}")

    def close(self):
        # No persistent connection to close for HTTP
        pass
