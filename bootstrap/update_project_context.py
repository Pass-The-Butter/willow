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

def update_project_context():
    print("Connecting to AuraDB to update project context...")
    os.environ['SSL_CERT_FILE'] = certifi.where()
    os.environ['REQUESTS_CA_BUNDLE'] = certifi.where()
    
    driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))
    
    try:
        with driver.session() as session:
            # Update Project node with Jira URL
            print("Updating Project node with Jira URL...")
            session.run("""
                MATCH (p:Project {name: 'Willow'})
                SET p.jira_url = 'https://agilemeshnet.atlassian.net/jira/projects?selectedProjectType=software%2Cbusiness'
            """)
            
            # Create a Tool/Service node for Jira
            print("Creating Jira Service node...")
            session.run("""
                MERGE (jira:Service {name: 'Jira'})
                SET jira.url = 'https://agilemeshnet.atlassian.net/jira/projects?selectedProjectType=software%2Cbusiness',
                    jira.type = 'Project Management',
                    jira.description = 'Agile Meshnet Jira Board'
                
                WITH jira
                MATCH (p:Project {name: 'Willow'})
                MERGE (p)-[:USES_SERVICE]->(jira)
            """)
            
            print("✓ Project context updated in graph.")
            
    except Exception as e:
        print(f"Error updating graph: {e}")
    finally:
        driver.close()

if __name__ == "__main__":
    update_project_context()
