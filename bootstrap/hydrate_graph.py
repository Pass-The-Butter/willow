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

HANDOFF_FILE = "/Volumes/Delila/dev/Willow/Willow_Persitant_HANDOFF_Memory.md"
BOOTSTRAP_SCHEMA = "core/ontology/willow-bootstrap.cypher"

def load_bootstrap_schema(session):
    print(f"Loading bootstrap schema from {BOOTSTRAP_SCHEMA}...")
    try:
        with open(BOOTSTRAP_SCHEMA, 'r') as f:
            schema_content = f.read()
            
        # Better simple parser: split by semicolon, then clean up each statement
        raw_statements = schema_content.split(';')
        
        for i, raw_stmt in enumerate(raw_statements):
            # Remove comments (lines starting with //) and empty lines
            lines = [line for line in raw_stmt.split('\n') if line.strip() and not line.strip().startswith('//')]
            stmt = '\n'.join(lines).strip()
            
            if stmt:
                try:
                    session.run(stmt)
                except Exception as e:
                    print(f"Warning running statement {i}: {e}")
        print("✓ Bootstrap schema loaded.")
    except FileNotFoundError:
        print(f"Schema file {BOOTSTRAP_SCHEMA} not found via relative path.")

def hydrate_memory(session):
    print(f"Hydrating memory from {HANDOFF_FILE}...")
    try:
        with open(HANDOFF_FILE, 'r') as f:
            content = f.read()

        # Ingest the Handoff Document as a Specification Source
        session.run("""
            MERGE (spec:Specification {name: 'Claude Code Handoff'})
            SET spec.content = $content,
                spec.type = 'handoff_memory',
                spec.ingested_at = datetime()
            
            // Link to Project
            WITH spec
            MATCH (proj:Project {name: 'Willow'})
            MERGE (proj)-[:HAS_SPEC]->(spec)
        """, content=content)
        
        print("✓ Handoff memory ingested as Specification.")
        
    except FileNotFoundError:
        print(f"Handoff file {HANDOFF_FILE} not found.")

def hydrate_infrastructure_spec(session):
    # Ingest Infrastructure Inventory
    infra_spec_path = "infrastructure/inventory.md"
    try:
        with open(infra_spec_path, 'r') as f:
            content = f.read()
            
        session.run("""
            MERGE (spec:Specification {name: 'Infrastructure Inventory'})
            SET spec.content = $content,
                spec.type = 'infrastructure_map',
                spec.ingested_at = datetime()
            
            // Link to Project
            WITH spec
            MATCH (p:Project {name: 'Willow'})
            MERGE (p)-[:HAS_SPEC]->(spec)
        """, content=content)
        print("✓ Infrastructure Inventory ingested.")
    except FileNotFoundError:
        print(f"Spec file {infra_spec_path} not found.")

def hydrate_story_specs(session):
    # Ingest Jerry & Barry Story
    story_path = "domains/population/story_jerry_barry.md"
    try:
        with open(story_path, 'r') as f:
            content = f.read()
            
        session.run("""
            MERGE (spec:Specification {name: 'Story: Jerry & Barry'})
            SET spec.content = $content,
                spec.type = 'user_story',
                spec.ingested_at = datetime()
            
            // Link to Project
            WITH spec
            MATCH (p:Project {name: 'Willow'})
            MERGE (p)-[:HAS_SPEC]->(spec)
        """, content=content)
        print("✓ Story Spec 'Jerry & Barry' ingested.")
    except FileNotFoundError:
        print(f"Spec file {story_path} not found.")

def hydrate_domain_specs(session):
    # Ingest Population Spec
    pop_spec_path = "domains/population/specification.md"
    try:
        with open(pop_spec_path, 'r') as f:
            content = f.read()
            
        session.run("""
            MERGE (spec:Specification {name: 'Population Specification'})
            SET spec.content = $content,
                spec.type = 'domain_spec',
                spec.ingested_at = datetime()
            
            // Link to Component
            WITH spec
            MATCH (c:Component {name: 'Population'})
            MERGE (c)-[:DEFINED_BY]->(spec)
        """, content=content)
        print("✓ Population Spec ingested.")
    except FileNotFoundError:
        print(f"Spec file {pop_spec_path} not found.")

def main():
    print("Connecting to AuraDB...")
    os.environ['SSL_CERT_FILE'] = certifi.where()
    os.environ['REQUESTS_CA_BUNDLE'] = certifi.where()
    
    driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))
    
    try:
        with driver.session() as session:
            # 1. Load the Ontology (Project, Components, etc.)
            load_bootstrap_schema(session)
            
            # 2. Hydrate the Memory (The Spec)
            hydrate_memory(session)
            
            # 3. Hydrate Domain Specs
            hydrate_domain_specs(session)
            
            # 4. Hydrate Infrastructure
            hydrate_infrastructure_spec(session)
            
            # 5. Hydrate Stories
            hydrate_story_specs(session)
            
            print("\nVerification:")
            result = session.run("MATCH (n:Component) RETURN n.name")
            print("Components found:", [r['n.name'] for r in result])
            
    finally:
        driver.close()

if __name__ == "__main__":
    main()
