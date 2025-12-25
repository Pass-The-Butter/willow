
import os
import certifi
from neo4j import GraphDatabase

# Load .env manually
with open('.env') as f:
    for line in f:
        if '=' in line and not line.startswith('#'):
            key, val = line.strip().split('=', 1)
            os.environ[key] = val

os.environ['SSL_CERT_FILE'] = certifi.where()

print("Connecting to:", os.getenv('NEO4J_URI'))

try:
    driver = GraphDatabase.driver(
        os.getenv('NEO4J_URI'),
        auth=(os.getenv('NEO4J_USER'), os.getenv('NEO4J_PASSWORD'))
    )
    with driver.session() as session:
        # Check for vector indexes specifically
        result = session.run("SHOW INDEXES YIELD name, type, entityType, labelsOrTypes, properties WHERE type = 'VECTOR'")
        
        indexes = list(result)
        if indexes:
            print(f"✅ FOUND {len(indexes)} VECTOR INDEXES:")
            for record in indexes:
                print(f"   - Name: {record['name']}")
                print(f"     Type: {record['type']}")
                print(f"     Labels: {record['labelsOrTypes']}")
                print(f"     Properties: {record['properties']}")
        else:
            print("❌ NO VECTOR INDEXES FOUND.")
            
    driver.close()
except Exception as e:
    print(f"❌ Connection or Query Failed: {e}")
