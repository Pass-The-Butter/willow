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

def update_infrastructure_context():
    print("Connecting to AuraDB to update infrastructure context...")
    os.environ['SSL_CERT_FILE'] = certifi.where()
    os.environ['REQUESTS_CA_BUNDLE'] = certifi.where()
    
    driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))
    
    try:
        with driver.session() as session:
            # 1. Ensure Component and Resource exist and are linked
            print("Linking Population Component to Xeon Server...")
            session.run("""
                MERGE (pop:Component {name: 'Population'})
                ON CREATE SET 
                    pop.path = '/domains/population',
                    pop.description = 'Entity generation and management (The People)',
                    pop.store = 'postgres',
                    pop.status = 'planned'
                
                MERGE (xeon:ComputeResource {name: 'Xeon Server'})
                ON CREATE SET 
                    xeon.role = 'Population Host',
                    xeon.os = 'Ubuntu',
                    xeon.specs = '128GB RAM',
                    xeon.network = 'Tailscale',
                    xeon.hostname = 'bunny'
                
                MERGE (pop)-[:HOSTED_ON]->(xeon)
            """)
            
            # 2. Document the Decision
            print("Documenting the architectural decision...")
            session.run("""
                MERGE (d:Decision {title: 'Host Population DB on Xeon Server'})
                SET d.description = 'The Population Database (Postgres+pgvector) requires significant RAM for 10M+ entities. The Xeon Server (bunny) has 128GB RAM, making it the suitable host.',
                    d.status = 'approved',
                    d.date = datetime(),
                    d.impact = 'high',
                    d.domain = 'Infrastructure'
                
                WITH d
                MATCH (xeon:ComputeResource {name: 'Xeon Server'})
                MERGE (d)-[:AFFECTS]->(xeon)
                
                WITH d
                MATCH (pop:Component {name: 'Population'})
                MERGE (d)-[:CONCERNS]->(pop)
                
                WITH d
                MATCH (p:Project {name: 'Willow'})
                MERGE (p)-[:HAS_DECISION]->(d)
            """)
            
            print("✓ Infrastructure context updated in graph.")
            
    except Exception as e:
        print(f"Error updating graph: {e}")
    finally:
        driver.close()

if __name__ == "__main__":
    update_infrastructure_context()
