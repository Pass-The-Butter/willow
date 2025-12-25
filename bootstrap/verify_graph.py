import os
import certifi
from neo4j import GraphDatabase
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# AuraDB connection details
URI = os.getenv("NEO4J_URI", "neo4j+s://e59298d2.databases.neo4j.io")
USER = os.getenv("NEO4J_USER", "neo4j")
PASSWORD = os.getenv("NEO4J_PASSWORD")

if not PASSWORD:
    raise ValueError("NEO4J_PASSWORD environment variable not set")

def verify_graph_structure():
    print("Connecting to AuraDB...")
    os.environ['SSL_CERT_FILE'] = certifi.where()
    os.environ['REQUESTS_CA_BUNDLE'] = certifi.where()
    
    driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))
    
    try:
        with driver.session() as session:
            print("\n=== Project Structure ===")
            result = session.run("""
                MATCH (p:Project)-[:HAS_COMPONENT]->(c:Component)
                RETURN p.name as Project, c.name as Component, c.description as Description, c.store as Store
                ORDER BY c.name
            """)
            for record in result:
                store_info = f" [Store: {record['Store']}]" if record['Store'] else ""
                print(f"Project: {record['Project']} -> Component: {record['Component']}{store_info}")
                print(f"  Description: {record['Description']}")
                
            print("\n=== Specifications ===")
            result = session.run("""
                MATCH (c:Component)-[:DEFINED_BY]->(s:Specification)
                RETURN c.name as Component, s.name as Spec
            """)
            # Note: We haven't linked granular specs yet, just the big Handoff doc to the Project
            # Let's check the Project level specs
            result_proj = session.run("""
                MATCH (p:Project)-[:HAS_SPEC]->(s:Specification)
                RETURN p.name as Project, s.name as Spec, substring(s.content, 0, 50) as Snippet
            """)
            for record in result_proj:
                print(f"Project: {record['Project']} has Spec: '{record['Spec']}'")
                
            print("\n=== Skills ===")
            result = session.run("""
                MATCH (c:Component)-[:PROVIDES_CAPABILITY]->(s:Skill)
                RETURN c.name as Component, s.name as Skill
            """)
            for record in result:
                print(f"Component: {record['Component']} -> Skill: {record['Skill']}")

            print("\n=== Infrastructure ===")
            result = session.run("""
                MATCH (r:ComputeResource)
                RETURN r.name as Name, r.role as Role, r.specs as Specs
            """)
            for record in result:
                print(f"Resource: {record['Name']} ({record['Specs']}) - {record['Role']}")


    finally:
        driver.close()

if __name__ == "__main__":
    verify_graph_structure()
