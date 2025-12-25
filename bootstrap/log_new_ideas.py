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

def log_new_ideas():
    print("Connecting to AuraDB to log new ideas...")
    os.environ['SSL_CERT_FILE'] = certifi.where()
    os.environ['REQUESTS_CA_BUNDLE'] = certifi.where()
    
    driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))
    
    try:
        with driver.session() as session:
            # 1. Update Project Jira URL
            print("Updating Project Jira URL...")
            session.run("""
                MATCH (p:Project {name: 'Willow'})
                SET p.jira_url = 'https://agilemeshnet.atlassian.net/jira/software/projects/SCRUM/boards/1'
                WITH p
                MATCH (s:Service {name: 'Jira'})
                SET s.url = 'https://agilemeshnet.atlassian.net/jira/software/projects/SCRUM/boards/1'
            """)

            # 2. Log Idea: Google Maps Integration
            print("Logging Idea: Google Maps Integration...")
            session.run("""
                MERGE (i:Idea {title: 'Google Maps Integration'})
                SET i.description = 'Use Google Maps API to visualize the population distribution. Requires valid UK postcodes for accurate plotting.',
                    i.source = 'Frank (User)',
                    i.status = 'planned',
                    i.date = datetime(),
                    i.domain = 'Interface'
                
                WITH i
                MATCH (p:Project {name: 'Willow'})
                MERGE (p)-[:HAS_IDEA]->(i)
            """)

            # 3. Log Idea: UK Synthetic Postcodes
            print("Logging Idea: UK Synthetic Postcodes...")
            session.run("""
                MERGE (i:Idea {title: 'Use UK Synthetic/Special Postcodes'})
                SET i.description = 'Use special non-geographic postcodes (e.g., XM4 5HQ, BX1 1LT, XX area) or known landmarks (SW1A 1AA) for testing to avoid affecting real residential data.',
                    i.source = 'Arch-Willow (Research)',
                    i.status = 'implemented',
                    i.date = datetime(),
                    i.domain = 'Population'
                
                WITH i
                MATCH (p:Project {name: 'Willow'})
                MERGE (p)-[:HAS_IDEA]->(i)
            """)

            # 4. Log Idea: PurelyPets Ontology
            print("Logging Idea: PurelyPets Ontology...")
            session.run("""
                MERGE (i:Idea {title: 'Reverse Engineer PurelyPets Ontology'})
                SET i.description = 'Model the graph schema based on the PurelyPets quote flow. Key entities: Pet (Name, Species, Breed, DOB, Cost, Neutered), Owner, Policy.',
                    i.source = 'Frank (User)',
                    i.status = 'planned',
                    i.date = datetime(),
                    i.domain = 'Ontology'
                
                WITH i
                MATCH (p:Project {name: 'Willow'})
                MERGE (p)-[:HAS_IDEA]->(i)
            """)
            
            print("✓ Ideas logged in graph.")
            
    except Exception as e:
        print(f"Error updating graph: {e}")
    finally:
        driver.close()

if __name__ == "__main__":
    log_new_ideas()
