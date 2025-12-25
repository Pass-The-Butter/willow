import os
import certifi
from neo4j import GraphDatabase
from dotenv import load_dotenv

# Load Environment
load_dotenv()
os.environ['SSL_CERT_FILE'] = certifi.where()

# Neo4j Config
URI = os.getenv('NEO4J_URI', "neo4j+s://e59298d2.databases.neo4j.io")
USER = os.getenv('NEO4J_USER', "neo4j")
PASS = os.getenv('NEO4J_PASSWORD', "c2U7h1mwvmYn2k2cr_Fp9EaUrZaLZdEQ3_Cawt6zvyU")

def backup_file(filepath, doc_name):
    # Read Content
    try:
        with open(filepath, 'r') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Error: File {filepath} not found.")
        return

    # Upload to Brain
    driver = GraphDatabase.driver(URI, auth=(USER, PASS))
    with driver.session() as session:
        session.run("""
            MERGE (d:SystemDoc {name: $name})
            SET d.content = $content, 
                d.updated_at = datetime(),
                d.path = $path
            RETURN d.name as name
        """, name=doc_name, content=content, path=filepath)
        print(f"✅ Backed up {doc_name} to the Brain.")
    driver.close()

if __name__ == "__main__":
    # Backup BIOS
    backup_file("/Volumes/Delila/dev/Willow/BIOS.md", "BIOS.md")
    # Backup Task
    backup_file("/Users/peter/.gemini/antigravity/brain/6310b00a-5063-4ce3-93f6-9ee7a0c1539b/task.md", "task.md")
    # Backup Plan
    backup_file("/Users/peter/.gemini/antigravity/brain/6310b00a-5063-4ce3-93f6-9ee7a0c1539b/implementation_plan.md", "implementation_plan.md")
    # Backup Env
    backup_file("/Volumes/Delila/dev/Willow/.env", ".env")
