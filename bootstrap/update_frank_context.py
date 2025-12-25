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

def update_frank_context():
    print("Connecting to AuraDB to update infrastructure context for Frank...")
    os.environ['SSL_CERT_FILE'] = certifi.where()
    os.environ['REQUESTS_CA_BUNDLE'] = certifi.where()
    
    driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))
    
    try:
        with driver.session() as session:
            # 1. Rename 'Win 11 PC' to 'Frank' and update specs
            print("Renaming 'Win 11 PC' to 'Frank'...")
            session.run("""
                MATCH (c:ComputeResource {name: 'Win 11 PC'})
                SET c.name = 'Frank',
                    c.hostname = 'frank',
                    c.role = 'AI Inference & Rendering',
                    c.description = 'Intel PC with RTX 3090 Ti running Ollama'
            """)
            
            # 2. Update Population Component Scale
            print("Updating Population Component scale to 100M...")
            session.run("""
                MATCH (pop:Component {name: 'Population'})
                SET pop.target_scale = '100,000,000 Entities',
                    pop.description = 'Entity generation and management (The People) - Target 100M'
            """)
            
            # 3. Ensure Frank is linked to the Project
            print("Ensuring Frank is linked...")
            session.run("""
                MATCH (p:Project {name: 'Willow'})
                MATCH (f:ComputeResource {name: 'Frank'})
                MERGE (p)-[:HAS_RESOURCE]->(f)
            """)

            print("✓ Infrastructure context updated: Frank is online.")
            
    except Exception as e:
        print(f"Error updating graph: {e}")
    finally:
        driver.close()

if __name__ == "__main__":
    update_frank_context()
