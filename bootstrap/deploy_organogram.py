"""
Deploy Organogram to AuraDB
Executes organogram.cypher statements one by one
"""

from neo4j import GraphDatabase
import certifi
import os
import re

os.environ['SSL_CERT_FILE'] = certifi.where()

NEO4J_URI = "neo4j+s://e59298d2.databases.neo4j.io"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "c2U7h1mwvmYn2k2cr_Fp9EaUrZaLZdEQ3_Cawt6zvyU"

def parse_cypher_file(filepath):
    """Parse Cypher file into executable statements"""
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Remove comments
    content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
    
    # Split by semicolons
    statements = [s.strip() for s in content.split(';') if s.strip()]
    
    return statements

def deploy():
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
    
    statements = parse_cypher_file('schemas/organogram.cypher')
    
    print(f"Found {len(statements)} statements to execute\n")
    
    with driver.session() as session:
        for i, stmt in enumerate(statements, 1):
            try:
                session.run(stmt)
                # Extract first line for summary
                first_line = stmt.split('\n')[0][:60]
                print(f"✓ {i:2d}. {first_line}...")
            except Exception as e:
                print(f"✗ {i:2d}. Failed: {e}")
                print(f"   Statement: {stmt[:100]}...")
    
    driver.close()
    print("\n✅ Organogram deployment complete!")

if __name__ == "__main__":
    deploy()
