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

def memorize_architecture():
    print("Connecting to AuraDB to memorize definitive architecture...")
    
    # SSL Config for Mac
    os.environ['SSL_CERT_FILE'] = certifi.where()
    os.environ['REQUESTS_CA_BUNDLE'] = certifi.where()
    
    driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))
    
    try:
        with driver.session() as session:
            # 1. Clear specific infrastructure nodes to avoid duplicates/conflicts
            # We are careful not to delete the whole graph, just the Infrastructure layer
            print("Cleaning up old infrastructure context...")
            session.run("""
                MATCH (n:Infrastructure) DETACH DELETE n
            """)
            
            # 2. Create the Definitive Architecture
            print("Memorizing new architecture...")
            session.run("""
                // --- The Brain (AuraDB) ---
                MERGE (aura:Infrastructure {name: 'AuraDB', type: 'Database'})
                SET aura.role = 'Memory & Ontology',
                    aura.description = 'The central brain containing the Graph Ontology and Agent Memory.',
                    aura.location = 'Cloud (Neo4j Aura)',
                    aura.status = 'Active'

                // --- The Vault (Bunny) ---
                MERGE (bunny:Infrastructure {name: 'Bunny', type: 'ComputeNode'})
                SET bunny.hostname = 'bunny',
                    bunny.hardware = 'Xeon Server',
                    bunny.specs = '128GB RAM',
                    bunny.os = 'Ubuntu',
                    bunny.role = 'Population Storage & Orchestration',
                    bunny.network_address = 'bunny' // Tailscale name

                MERGE (pg:Infrastructure {name: 'Postgres', type: 'Database'})
                SET pg.role = 'Population Store',
                    pg.capacity = '100M Entities',
                    pg.port = 5432
                
                MERGE (bunny)-[:HOSTS]->(pg)

                // --- The Muscle (Frank) ---
                MERGE (frank:Infrastructure {name: 'Frank', type: 'ComputeNode'})
                SET frank.hostname = 'frank',
                    frank.hardware = 'PC',
                    frank.os = 'Windows 11',
                    frank.role = 'Inference & Generation',
                    frank.network_address = 'frank' // Tailscale name

                MERGE (ollama:Infrastructure {name: 'Ollama', type: 'Service'})
                SET ollama.role = 'LLM Inference',
                    ollama.port = 11434,
                    ollama.models = ['llama3', 'mistral']
                
                MERGE (frank)-[:HOSTS]->(ollama)

                // --- The Architect (Mac Mini) ---
                MERGE (mac:Infrastructure {name: 'Mac Mini', type: 'Workstation'})
                SET mac.role = 'Controller & Development',
                    mac.os = 'macOS',
                    mac.location = 'Local'

                // --- The Network (Tailscale) ---
                MERGE (tailscale:Infrastructure {name: 'Tailscale', type: 'Network'})
                SET tailscale.role = 'Mesh Fabric',
                    tailscale.description = 'Secure connectivity between all nodes'

                // --- Relationships ---
                MERGE (mac)-[:CONTROLS]->(bunny)
                MERGE (mac)-[:CONTROLS]->(frank)
                MERGE (mac)-[:CONNECTS_VIA]->(tailscale)
                MERGE (bunny)-[:CONNECTS_VIA]->(tailscale)
                MERGE (frank)-[:CONNECTS_VIA]->(tailscale)
                
                // --- Logical Flow ---
                MERGE (frank)-[:GENERATES_DATA_FOR]->(pg)
                MERGE (ollama)-[:PROVIDES_INFERENCE_TO]->(mac)
                MERGE (aura)-[:STORES_MEMORY_FOR]->(mac)
            """)
            
            print("✓ Architecture memorized successfully.")
            
    except Exception as e:
        print(f"Error updating graph: {e}")
    finally:
        driver.close()

if __name__ == "__main__":
    memorize_architecture()
