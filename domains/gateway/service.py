"""
Willow Graph Gateway Service
============================
The implementation of the Constitution.
Acts as the middleware between Agents and AuraDB.

Enforces:
1. No Direct DB Access (Agents verify via this API)
2. Policy Checks (No DELETE, etc.)
3. Provenance Logging

Run with: python domains/gateway/service.py
"""

import os
import sys
from pathlib import Path
from flask import Flask, request, jsonify
from neo4j import GraphDatabase
from dotenv import load_dotenv
import certifi
from datetime import datetime, date, time

# Fix path to import sibling modules
REPO_ROOT = Path(__file__).parent.parent.parent
sys.path.append(str(REPO_ROOT))

# Import Policy
from domains.gateway.policy import PolicyEnforcer

# Load environment
load_dotenv(REPO_ROOT / '.env')

app = Flask(__name__)
policy = PolicyEnforcer()

# Database Connection (Privileged)
NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USER = os.getenv("NEO4J_USER")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")

if not NEO4J_URI:
    print("CRITICAL: NEO4J_URI not set")
    sys.exit(1)

# Initialize Driver
os.environ['SSL_CERT_FILE'] = certifi.where()
driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

def serialize(obj):
    """Recursively serialize objects to JSON-compatible types"""
    if hasattr(obj, 'iso_format'):
        return obj.iso_format()
    if isinstance(obj, (datetime, date, time)):
        return obj.isoformat()
    if isinstance(obj, dict):
        return {k: serialize(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [serialize(i) for i in obj]
    return obj

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "active", "service": "willow-gateway", "version": "2026.1"})

@app.route('/query', methods=['POST'])
def execute_query():
    """
    Execute a Cypher query.
    Payload: {
        "cypher": "MATCH (n) RETURN n",
        "params": {},
        "agent_id": "agent-name"
    }
    """
    data = request.json
    cypher = data.get('cypher', '')
    params = data.get('params', {})
    agent_id = data.get('agent_id', 'anonymous')

    # 1. Enforce Policy
    check = policy.check_query(cypher)
    if not check['allowed']:
        print(f"🚫 BLOCKED query from {agent_id}: {check['reason']}")
        return jsonify({
            "error": "Policy Violation",
            "message": check['reason'],
            "success": False
        }), 403

    # 2. Execute (Privileged)
    try:
        results = []
        with driver.session() as session:
            # We use the transaction context
            result = session.run(cypher, parameters=params)
            
            # Serialize results (basic implementation)
            # Graph objects (Nodes/Relationships) are not JSON serializable by default
            # We assume queries return basic types or we map them.
            # A full graph proxy needs robust serialization.
            # For now, we return list of dicts (records)
            keys = result.keys()
            for record in result:
                # Convert record to dict, handling complex types if needed
                # (Skipping complex graph object serialization for MVP - assume explicitly returned properties)
                # If query returns Node, this might fail serialization. Agents should RETURN n.prop
                results.append(serialize(dict(record)))
                
        return jsonify({
            "success": True,
            "data": results,
            "meta": {"agent": agent_id, "policy_check": "passed"}
        })

    except Exception as e:
        print(f"❌ Execution Error: {e}")
        return jsonify({
            "error": "Database Error",
            "message": str(e),
            "success": False
        }), 500

if __name__ == "__main__":
    print("🌳 Willow Gateway starting on port 8001...")
    print("🔒 Holding the Keys to the Kingdom")
    app.run(host='0.0.0.0', port=8001)
