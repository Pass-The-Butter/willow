import os
import sys
from datetime import datetime
from neo4j import GraphDatabase
import certifi

# Add valid path to Willow root
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

# Load env vars
def load_env():
    env_path = os.path.join(os.path.dirname(__file__), '..', '..', '.env')
    if os.path.exists(env_path):
        with open(env_path, 'r') as f:
            for line in f:
                if '=' in line and not line.startswith('#'):
                    key, value = line.strip().split('=', 1)
                    if not os.environ.get(key):
                        os.environ[key] = value

load_env()

URI = os.getenv("NEO4J_URI")
USER = os.getenv("NEO4J_USER")
PASSWORD = os.getenv("NEO4J_PASSWORD")
os.environ['SSL_CERT_FILE'] = certifi.where()

def diarise_request():
    driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))

    diary_note = """
    User requested construction of the initial Business Ontology based on the 'Purely Pets' narrative (Jane Winterbottom).
    Analysis completed in `domains/claims/ontology_vision.md`.
    Schema implemented in `schemas/business_ontology.cypher`.
    Verified successfully with `schemas/verify_business_ontology.py`.
    Key entities: Person, Pet, Policy, Claim, VetPractice.
    This sets the foundation for the Claims Assessment process.
    """

    task_name = "Business Ontology Construction"

    with driver.session() as session:
        # Find the task and add the entry
        result = session.run("""
            MATCH (t:Task {name: $task_name})
            CREATE (t)-[:HAS_DIARY_ENTRY]->(d:DiaryEntry {
                agent: "Antigravity",
                timestamp: datetime(),
                status: "Complete",
                notes: $notes
            })
            RETURN t.name as task, elementId(d) as diary_id
        """, task_name=task_name, notes=diary_note)
        
        record = result.single()
        if record:
            print(f"✅ Diarised request for task: {record['task']}")
        else:
            print(f"⚠️  Task '{task_name}' not found. Ensure sync_brain_tasks.py ran successfully.")
            # Fallback: Attach to Project if task not found
            session.run("""
                MATCH (p:Project {name: "Willow"})
                CREATE (p)-[:HAS_DIARY_ENTRY]->(d:DiaryEntry {
                    agent: "Antigravity",
                    timestamp: datetime(),
                    status: "Milestone",
                    notes: $notes
                })
            """, notes="[Fallback] " + diary_note)
            print("   (Attached to Project 'Willow' instead)")

    driver.close()

if __name__ == "__main__":
    diarise_request()
