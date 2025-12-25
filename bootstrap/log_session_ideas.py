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

def log_session_ideas():
    print("Connecting to AuraDB to log session ideas...")
    os.environ['SSL_CERT_FILE'] = certifi.where()
    os.environ['REQUESTS_CA_BUNDLE'] = certifi.where()
    
    driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))
    
    try:
        with driver.session() as session:
            print("Logging ideas...")
            
            # Idea 1: Autonomous Population Agent on Frank
            session.run("""
                MERGE (i:Idea {title: 'Autonomous Population Agent on Frank'})
                SET i.description = 'Spin up a dedicated agent instance on Frank to manage population generation autonomously, separate from the main controller.',
                    i.status = 'Proposed',
                    i.source = 'User Session',
                    i.category = 'Architecture'
                
                MERGE (c:Component {name: 'Population'})
                MERGE (i)-[:RELATES_TO]->(c)
            """)
            print("✓ Logged: Autonomous Population Agent")

            # Idea 2: Fake Website for Population
            session.run("""
                MERGE (i:Idea {title: 'Population Showcase Website'})
                SET i.description = 'Create a fake website on agilemesh.net to display the generated population and their quotes/stories.',
                    i.status = 'Proposed',
                    i.source = 'User Session',
                    i.category = 'Frontend'
                
                MERGE (c:Component {name: 'Interface'})
                MERGE (i)-[:RELATES_TO]->(c)
            """)
            print("✓ Logged: Population Showcase Website")

            # Idea 3: Website Hosting Strategy
            session.run("""
                MERGE (i:Idea {title: 'Website Hosting Strategy'})
                SET i.description = 'Determine where to host the showcase website. Options: Bunny (Docker/Nginx), GitHub Pages, or External.',
                    i.status = 'Pending Analysis',
                    i.source = 'User Session',
                    i.category = 'Infrastructure'
                
                MERGE (infra:Infrastructure {name: 'Bunny'})
                MERGE (i)-[:CONSIDERS]->(infra)
            """)
            print("✓ Logged: Website Hosting Strategy")
            
    except Exception as e:
        print(f"Error logging ideas: {e}")
    finally:
        driver.close()

if __name__ == "__main__":
    log_session_ideas()
