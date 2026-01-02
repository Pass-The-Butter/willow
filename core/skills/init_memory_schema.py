"""
Willow Memory Schema Initialization
Applies constraints and indexes for:
1. Episodic Memory (Session, Turn, Summary)
2. Beads Task Graph (Task, Epic)
3. Semantic Memory (Policy, Skill)
"""

from neo4j import GraphDatabase
import os
import certifi
from core.utils.credentials import get_neo4j_auth

# Load environment
NEO4J_URI, NEO4J_AUTH = get_neo4j_auth()
NEO4J_USER = NEO4J_AUTH[0]
NEO4J_PASSWORD = NEO4J_AUTH[1]

os.environ['SSL_CERT_FILE'] = certifi.where()

def run_schema_updates():
    if not NEO4J_URI:
        print("❌ Error: NEO4J_URI not set.")
        return

    print(f"🔌 Connecting to Brain at {NEO4J_URI}...")
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

    queries = [
        # --- Episodic Memory (Neo4j Native) ---
        "CREATE CONSTRAINT session_id_unique IF NOT EXISTS FOR (s:Session) REQUIRE s.id IS UNIQUE",
        "CREATE INDEX turn_timestamp IF NOT EXISTS FOR (t:Turn) ON (t.timestamp)",
        
        # --- Beads Task Graph (The "Beads") ---
        "CREATE CONSTRAINT task_id_unique IF NOT EXISTS FOR (t:Task) REQUIRE t.id IS UNIQUE",
        "CREATE INDEX task_status IF NOT EXISTS FOR (t:Task) ON (t.status)",
        "CREATE INDEX task_priority IF NOT EXISTS FOR (t:Task) ON (t.priority)",
        
        # --- Semantic Memory ---
        "CREATE CONSTRAINT policy_name_unique IF NOT EXISTS FOR (p:Policy) REQUIRE p.name IS UNIQUE",
        "CREATE CONSTRAINT skill_name_unique IF NOT EXISTS FOR (s:Skill) REQUIRE s.name IS UNIQUE",
        
        # --- Vector Indexes (for GraphRAG) ---
        # Note: Vector indexes usually require specific creation syntax depending on version, 
        # but we'll assume standard procedure or use the Python wrapper later.
        # This placeholder is just a reminder.
    ]

    try:
        with driver.session() as session:
            for q in queries:
                print(f"   Executing: {q}")
                session.run(q)
        print("✅ Schema Initialization Complete.")
    except Exception as e:
        print(f"❌ Error applying schema: {e}")
    finally:
        driver.close()

if __name__ == "__main__":
    run_schema_updates()
