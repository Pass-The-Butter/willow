import os
import certifi
from neo4j import GraphDatabase
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

URI = os.getenv("NEO4J_URI")
USER = os.getenv("NEO4J_USER")
PASSWORD = os.getenv("NEO4J_PASSWORD")

if not all([URI, USER, PASSWORD]):
    raise ValueError("Neo4j credentials not found in .env")

def log_bootstrap_decision():
    print("Logging Bootstrap Protocol to Graph...")
    os.environ['SSL_CERT_FILE'] = certifi.where()
    os.environ['REQUESTS_CA_BUNDLE'] = certifi.where()
    
    driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))
    
    try:
        with driver.session() as session:
            session.run("""
                MERGE (d:Decision {title: 'New Agent Bootstrap Protocol'})
                SET d.content = 'SESSION_BOOTSTRAP.md created as entry point for new agents. Provides step-by-step guide to query the graph and understand project state without full conversation history.',
                    d.category = 'Documentation',
                    d.status = 'Active',
                    d.date = date()
                
                MERGE (p:Project {name: 'Willow'})
                MERGE (d)-[:IMPROVES]->(p)
            """)
            print("✓ Bootstrap protocol logged to graph.")
            
    except Exception as e:
        print(f"Error: {e}")
    finally:
        driver.close()

if __name__ == "__main__":
    log_bootstrap_decision()
