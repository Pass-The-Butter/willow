import os
import certifi
from neo4j import GraphDatabase

# AuraDB connection details (reusing from load_schema.py)
URI = "neo4j+s://e59298d2.databases.neo4j.io"
USER = "neo4j"
PASSWORD = "c2U7h1mwvmYn2k2cr_Fp9EaUrZaLZdEQ3_Cawt6zvyU"

def fix_brand_asset():
    print("Connecting to AuraDB...")
    os.environ['SSL_CERT_FILE'] = certifi.where()
    os.environ['REQUESTS_CA_BUNDLE'] = certifi.where()
    
    driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))
    
    try:
        with driver.session() as session:
            print("Fixing autumn BrandAsset...")
            # The issue might be related to how the URL was stored or the previous load failed for this node.
            # We will merge (create if not exists) and update the property.
            query = """
            MERGE (b:BrandAsset {season: 'autumn'})
            SET b.logo_url = 'https://www.canva.com/d/r1GY4_LfcJpg1xA',
                b.active = true,
                b.description = 'Minimalist geometric willow tree - autumn palette'
            RETURN b
            """
            result = session.run(query)
            record = result.single()
            if record:
                print("✓ Autumn BrandAsset fixed/verified.")
            else:
                print("✗ Failed to fix Autumn BrandAsset.")
                
    finally:
        driver.close()

if __name__ == "__main__":
    fix_brand_asset()
