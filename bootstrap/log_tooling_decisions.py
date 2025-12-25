import os
import certifi
from neo4j import GraphDatabase
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# AuraDB connection details
URI = os.getenv("NEO4J_URI")
USER = os.getenv("NEO4J_USER")
PASSWORD = os.getenv("NEO4J_PASSWORD")

if not all([URI, USER, PASSWORD]):
    raise ValueError("Neo4j credentials not found in .env")

def log_tooling_decisions():
    print("Connecting to AuraDB to log Tooling Decisions...")
    os.environ['SSL_CERT_FILE'] = certifi.where()
    os.environ['REQUESTS_CA_BUNDLE'] = certifi.where()
    
    driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))
    
    try:
        with driver.session() as session:
            print("Logging Decisions...")
            
            # Decision 1: Framework = N8N
            session.run("""
                MERGE (d:Decision {title: 'Swarm Orchestration Framework'})
                SET d.choice = 'N8N',
                    d.reason = 'Visual workflow management, runs locally on Bunny, integrates with Graph events.',
                    d.status = 'Adopted',
                    d.date = date()
                
                MERGE (tech:Technology {name: 'N8N'})
                MERGE (d)-[:CHOOSES]->(tech)
            """)
            
            # Decision 2: Inference = Hybrid (Ollama First)
            session.run("""
                MERGE (d:Decision {title: 'Inference Cost Strategy'})
                SET d.choice = 'Hybrid (Local First)',
                    d.reason = 'Use Frank (Ollama) for bulk/routine tasks (Free). Use Cloud (OpenAI/Anthropic) only for high-level reasoning if needed.',
                    d.status = 'Adopted',
                    d.date = date()
                
                MERGE (tech1:Technology {name: 'Ollama'})
                MERGE (tech2:Technology {name: 'OpenAI API'})
                MERGE (d)-[:CHOOSES]->(tech1)
                MERGE (d)-[:CONSIDERS]->(tech2)
            """)
            
            print("✓ Tooling decisions logged.")
            
    except Exception as e:
        print(f"Error logging decisions: {e}")
    finally:
        driver.close()

if __name__ == "__main__":
    log_tooling_decisions()
