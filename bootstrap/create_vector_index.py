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

def create_vector_index():
    print("Connecting to AuraDB to create Vector Index...")
    os.environ['SSL_CERT_FILE'] = certifi.where()
    os.environ['REQUESTS_CA_BUNDLE'] = certifi.where()
    
    driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))
    
    try:
        with driver.session() as session:
            # Check if index exists (Neo4j 5.x syntax)
            print("Creating Vector Index 'willow_memory'...")
            
            # Create Vector Index for 'Memory' nodes (e.g., Idea, Decision, Insight)
            # Dimension: 1536 (Standard OpenAI/Nomic embedding size) or 1024 (Ollama/mxbai)
            # Let's assume 768 (nomic-embed-text v1.5) or 1024. 
            # Frank has 'nomic-embed-text', which is usually 768.
            
            session.run("""
                CREATE VECTOR INDEX willow_memory IF NOT EXISTS
                FOR (m:Memory)
                ON (m.embedding)
                OPTIONS {indexConfig: {
                    `vector.dimensions`: 768,
                    `vector.similarity_function`: 'cosine'
                }}
            """)
            
            # Also create one for 'Idea' nodes if we want to search them specifically
            session.run("""
                CREATE VECTOR INDEX willow_ideas IF NOT EXISTS
                FOR (i:Idea)
                ON (i.embedding)
                OPTIONS {indexConfig: {
                    `vector.dimensions`: 768,
                    `vector.similarity_function`: 'cosine'
                }}
            """)
            
            print("✓ Vector Indexes created (Dimensions: 768).")
            print("  - willow_memory (Label: Memory)")
            print("  - willow_ideas (Label: Idea)")
            
    except Exception as e:
        print(f"Error creating index: {e}")
    finally:
        driver.close()

if __name__ == "__main__":
    create_vector_index()
