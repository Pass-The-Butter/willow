"""
Debug Graph State
=================
List all claims for Jane -> Bobby and check for decisions.
"""
import os
from neo4j import GraphDatabase
from dotenv import load_dotenv
import certifi

load_dotenv()

def debug_graph():
    print("🐞 Debugging Graph State...")
    uri = os.getenv("NEO4J_URI")
    user = os.getenv("NEO4J_USER")
    password = os.getenv("NEO4J_PASSWORD")
    os.environ['SSL_CERT_FILE'] = certifi.where()
    driver = GraphDatabase.driver(uri, auth=(user, password))

    try:
        with driver.session() as session:
            # Query ALL claims for Jane/Bobby
            result = session.run("""
                MATCH (p:Person {name: "Jane Winterbottom"})-[:OWNS]->(pet:Pet {name: "Bobby"})
                MATCH (c:Claim)-[:CONCERNS]->(pet)
                OPTIONAL MATCH (dec:Decision)-[:DECIDED_ON]->(c)
                RETURN elementId(c) as id, c.id as claim_id, c.status as status, dec.decision as decision
            """)
            
            print("\n--- Claims for Bobby ---")
            for r in result:
                print(f"ID: {r['id']} | ClaimID: {r['claim_id']} | Status: {r['status']} | Decision: {r['decision']}")
            print("------------------------\n")

    finally:
        driver.close()

if __name__ == "__main__":
    debug_graph()
