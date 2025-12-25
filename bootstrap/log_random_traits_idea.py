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

def log_random_traits_idea():
    print("Connecting to AuraDB to log Random Traits idea...")
    os.environ['SSL_CERT_FILE'] = certifi.where()
    os.environ['REQUESTS_CA_BUNDLE'] = certifi.where()
    
    driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))
    
    try:
        with driver.session() as session:
            # Log the Idea
            print("Logging Idea: Random Traits based on UK Stats...")
            session.run("""
                MERGE (i:Idea {title: 'Enrich Population with UK Statistics'})
                SET i.description = 'Add random traits like color blindness (4.5%) and hobbies (Knitting, Gardening) to the population vectors. Useful for targeted advertising simulation.',
                    i.source = 'Frank (User)',
                    i.status = 'implemented',
                    i.date = datetime(),
                    i.domain = 'Population'
                
                WITH i
                MATCH (pop:Component {name: 'Population'})
                MERGE (i)-[:ENHANCES]->(pop)
                
                WITH i
                MATCH (p:Project {name: 'Willow'})
                MERGE (p)-[:HAS_IDEA]->(i)
            """)
            
            print("✓ Idea logged in graph.")
            
    except Exception as e:
        print(f"Error updating graph: {e}")
    finally:
        driver.close()

if __name__ == "__main__":
    log_random_traits_idea()
