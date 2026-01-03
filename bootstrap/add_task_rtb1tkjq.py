#!/usr/bin/env python3
"""
Script to add Task node rtb1tkjq to Neo4j graph under Core domain.
Mission: GOPHER-rtb1tkjq - Connect Mongo Mission Log
"""
import os
from pathlib import Path
from neo4j import GraphDatabase
import certifi
from dotenv import load_dotenv

# Load .env from project root (override existing env vars)
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(env_path, override=True)

def add_task_node():
    """Add the rtb1tkjq task node to the Neo4j graph."""
    uri = os.getenv("NEO4J_URI")
    user = os.getenv("NEO4J_USER")
    password = os.getenv("NEO4J_PASSWORD")

    os.environ['SSL_CERT_FILE'] = certifi.where()

    if not all([uri, user, password]):
        raise ValueError("Missing Neo4j credentials. Check .env file.")

    driver = GraphDatabase.driver(uri, auth=(user, password))

    try:
        with driver.session() as session:
            # First, ensure the Core domain exists
            session.run("""
                MERGE (p:Project {name: "Willow"})
                MERGE (d:Domain {name: "Core"})
                MERGE (p)-[:HAS_DOMAIN]->(d)
            """)

            # Create the task node
            result = session.run("""
                MATCH (d:Domain {name: "Core"})
                MERGE (t:Task {
                    guid: "rtb1tkjq",
                    name: "Connect Mongo Mission Log",
                    mission_code: "GOPHER-rtb1tkjq",
                    status: "In Progress",
                    description: "Upgrade land_the_plane skill to store JSON health reports in MongoDB Atlas",
                    created_at: datetime()
                })
                MERGE (d)-[:HAS_TASK]->(t)
                RETURN t.guid as guid, t.name as name
            """)

            record = result.single()
            if record:
                print(f"✅ Task node created: {record['name']} (GUID: {record['guid']})")

            # Add specification details
            session.run("""
                MATCH (t:Task {guid: "rtb1tkjq"})
                MERGE (s:Specification {
                    task_guid: "rtb1tkjq",
                    database: "willow-mission-control",
                    collection: "flight_logs",
                    evidence_path: "artifacts/evidence/mongo_push_rtb1tkjq.json"
                })
                MERGE (t)-[:REQUIRES]->(s)
            """)

            print("✅ Specification node linked")

            # Add acceptance criteria
            session.run("""
                MATCH (t:Task {guid: "rtb1tkjq"})
                MERGE (c:TestCriteria {
                    task_guid: "rtb1tkjq",
                    criteria: "Successful landing report confirmed in MongoDB",
                    evidence: "mongo_push_rtb1tkjq.json file exists"
                })
                MERGE (t)-[:MUST_SATISFY]->(c)
            """)

            print("✅ Test criteria node linked")

            # Verify the task exists in the graph
            verify_result = session.run("""
                MATCH (d:Domain {name: "Core"})-[:HAS_TASK]->(t:Task {guid: "rtb1tkjq"})
                OPTIONAL MATCH (t)-[:REQUIRES]->(s:Specification)
                OPTIONAL MATCH (t)-[:MUST_SATISFY]->(c:TestCriteria)
                RETURN t.name as task,
                       t.status as status,
                       s.database as db,
                       c.criteria as criteria
            """)

            record = verify_result.single()
            if record:
                print("\n🎯 Task Node Verification:")
                print(f"  Task: {record['task']}")
                print(f"  Status: {record['status']}")
                print(f"  Database: {record['db']}")
                print(f"  Criteria: {record['criteria']}")

    finally:
        driver.close()

if __name__ == "__main__":
    print("🧠 Connecting to Neo4j Brain...")
    add_task_node()
    print("\n✅ Task rtb1tkjq successfully added to the graph!")
