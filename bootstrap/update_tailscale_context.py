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

def update_tailscale_context():
    print("Connecting to AuraDB to update Tailscale context...")
    os.environ['SSL_CERT_FILE'] = certifi.where()
    os.environ['REQUESTS_CA_BUNDLE'] = certifi.where()
    
    driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))
    
    try:
        with driver.session() as session:
            # 1. Create Tailscale Technology Node
            print("Creating Tailscale Technology node...")
            session.run("""
                MERGE (ts:Technology {name: 'Tailscale'})
                SET ts.description = 'Mesh VPN for secure device connectivity',
                    ts.features = ['Mesh Network', 'ACLs', 'SSH', 'Serve', 'Funnel'],
                    ts.documentation = '/infrastructure/tailscale_integration.md'
            """)
            
            # 2. Link Project to Tailscale
            print("Linking Project to Tailscale...")
            session.run("""
                MATCH (p:Project {name: 'Willow'})
                MATCH (ts:Technology {name: 'Tailscale'})
                MERGE (p)-[:USES_TECHNOLOGY]->(ts)
            """)
            
            # 3. Link Infrastructure to Tailscale
            print("Linking Infrastructure to Tailscale...")
            session.run("""
                MATCH (ts:Technology {name: 'Tailscale'})
                MATCH (c:ComputeResource)
                MERGE (c)-[:CONNECTED_VIA]->(ts)
            """)
            
            # 4. Log Research as Insight
            print("Logging Research Insight...")
            session.run("""
                MERGE (i:Insight {title: 'Tailscale MCP Potential'})
                SET i.description = 'No official Tailscale MCP exists, but one can be built using the Tailscale API to manage ACLs and devices programmatically.',
                    i.date = datetime(),
                    i.domain = 'Infrastructure'
                
                WITH i
                MATCH (ts:Technology {name: 'Tailscale'})
                MERGE (i)-[:RELATED_TO]->(ts)
                
                WITH i
                MATCH (p:Project {name: 'Willow'})
                MERGE (p)-[:HAS_INSIGHT]->(i)
            """)

            print("✓ Tailscale context updated in graph.")
            
    except Exception as e:
        print(f"Error updating graph: {e}")
    finally:
        driver.close()

if __name__ == "__main__":
    update_tailscale_context()
