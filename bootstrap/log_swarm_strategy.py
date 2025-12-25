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

def log_swarm_strategy():
    print("Connecting to AuraDB to log Swarm Strategy...")
    os.environ['SSL_CERT_FILE'] = certifi.where()
    os.environ['REQUESTS_CA_BUNDLE'] = certifi.where()
    
    driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))
    
    try:
        with driver.session() as session:
            print("Creating Agent Nodes...")
            
            # 1. Define the Agents
            session.run("""
                MERGE (pm:Agent {name: 'Project Manager'})
                SET pm.role = 'Orchestration',
                    pm.description = 'Maintains the vision and assigns tasks.'
                
                MERGE (arch:Agent {name: 'Arch-Willow'})
                SET arch.role = 'Architecture',
                    arch.description = 'System design and ontology management.'
                
                MERGE (dev:Agent {name: 'Dev-Willow'})
                SET dev.role = 'Implementation',
                    dev.description = 'Coding and deployment.'
                
                MERGE (frank:Agent {name: 'Frank-Willow'})
                SET frank.role = 'Generation',
                    frank.description = 'Population synthesis.'
            """)
            
            # 2. Link to Strategy
            session.run("""
                MERGE (s:Strategy {name: 'Agent Swarm'})
                SET s.description = 'Hub-and-Spoke model using GraphRAG for shared memory.'
                
                WITH s
                MATCH (a:Agent)
                MERGE (a)-[:IMPLEMENTS]->(s)
            """)
            
            print("✓ Swarm Strategy logged to Graph.")
            
    except Exception as e:
        print(f"Error logging strategy: {e}")
    finally:
        driver.close()

if __name__ == "__main__":
    log_swarm_strategy()
