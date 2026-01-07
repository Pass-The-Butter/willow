import os
import requests
from neo4j import GraphDatabase
from dotenv import load_dotenv
import certifi

load_dotenv()

NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USER = os.getenv("NEO4J_USER")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://frank:11434")

os.environ['SSL_CERT_FILE'] = certifi.where()

def get_embedding(text):
    response = requests.post(
        f"{OLLAMA_URL}/api/embeddings",
        json={"model": "nomic-embed-text", "prompt": text},
        timeout=10
    )
    return response.json()["embedding"]

def seed():
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
    
    memories = [
        {
            "title": "Quantum Computing Basics",
            "content": "Quantum computing uses qubits to perform calculations that are impossible for classical computers. It relies on superposition and entanglement.",
            "category": "Technology"
        },
        {
            "title": "Baking the Perfect Sourdough",
            "content": "To bake sourdough, you need a starter, flour, water, and salt. Long fermentation is key to the flavor and texture of the bread.",
            "category": "Cooking"
        },
        {
            "title": "Willow System Architecture",
            "content": "Willow uses a neurosymbolic architecture combining LLMs for perception and Neo4j for logical reasoning and memory.",
            "category": "Documentation"
        }
    ]

    with driver.session() as session:
        # Create Vector index if it doesn't exist (assuming 768 for nomic-embed-text)
        session.run("CREATE VECTOR INDEX willow_memory IF NOT EXISTS FOR (n:Memory) ON (n.embedding) OPTIONS {indexConfig: {`vector.dimensions`: 768, `vector.similarity_function`: 'cosine'}}")
        
        for mem in memories:
            embedding = get_embedding(mem["content"])
            session.run("""
                MERGE (m:Memory {title: $title})
                SET m.content = $content,
                    m.category = $category,
                    m.timestamp = datetime(),
                    m.embedding = $embedding
            """, title=mem["title"], content=mem["content"], category=mem["category"], embedding=embedding)
            print(f"Seeded: {mem['title']}")

    driver.close()

if __name__ == "__main__":
    seed()
