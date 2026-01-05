"""
Verify Factory Backend Logic
============================
Simulates the /api/factory/story endpoint logic using direct Neo4j Driver (mirroring app.py).
"""
import os
from neo4j import GraphDatabase
from dotenv import load_dotenv
import certifi

load_dotenv()

def verify_backend_logic():
    print("🔬 Verifying Factory Backend Logic (Direct Driver)...")
    
    uri = os.getenv("NEO4J_URI")
    user = os.getenv("NEO4J_USER")
    password = os.getenv("NEO4J_PASSWORD")
    
    # Configure SSL like app.py
    os.environ['SSL_CERT_FILE'] = certifi.where()
    
    driver = GraphDatabase.driver(uri, auth=(user, password))
    
    try:
        with driver.session() as session:
            # EXACT Query from app.py
            query = """
                MATCH (p:Person)-[:OWNS]->(pet:Pet)<-[:CONCERNS]-(c:Claim)-[:FILED_AGAINST]->(pol:Policy)
                OPTIONAL MATCH (pet)-[:VISITED]->(vet:VetPractice)-[:DIAGNOSED]->(d:Diagnosis)
                OPTIONAL MATCH (dec:Decision)-[:DECIDED_ON]->(c)
                RETURN p, pet, c, pol, vet, d, dec
                ORDER BY elementId(c) DESC
                LIMIT 1
            """
            
            result = session.run(query)
            record = result.single()
            
            if not record:
                print("❌ No results found! Query failed.")
                return
            
            # Simulate app.py extraction
            p = record['p']
            pet = record['pet']
            dec = record['dec']
            
            print(f"✅ Query returned data for: {p.get('name')} & {pet.get('name')}")
            
            # Check Decision
            if dec:
                print(f"✅ Decision Found: {dec.get('decision')} (Reason: {dec.get('reason')})")
            else:
                print("❌ Decision NOT found in result!")

            # Check Diagnosis
            d = record.get('d')
            if d:
                print(f"✅ Diagnosis Found: {d.get('code')}")
            else:
                print("⚠️  Diagnosis NOT found (Optional match failed or null)")

    except Exception as e:
        print(f"❌ Verification Failed: {e}")
    finally:
        driver.close()

if __name__ == "__main__":
    verify_backend_logic()
