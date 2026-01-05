import os
import sys
from datetime import datetime
from neo4j import GraphDatabase
import certifi

# Add valid path to Willow root so we can import dependencies if needed, 
# though this script is standalone.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Load env vars safely
def load_env():
    env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
    if os.path.exists(env_path):
        with open(env_path, 'r') as f:
            for line in f:
                if '=' in line and not line.startswith('#'):
                    key, value = line.strip().split('=', 1)
                    if not os.environ.get(key):
                        os.environ[key] = value

load_env()

# Connection details
URI = os.getenv("NEO4J_URI")
USER = os.getenv("NEO4J_USER")
PASSWORD = os.getenv("NEO4J_PASSWORD")
os.environ['SSL_CERT_FILE'] = certifi.where()

def verify_business_ontology():
    driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))

    story_data = {
        "customer": {
            "name": "Jane Winterbottom",
            "address": "76 Acaicia Drive",
            "postcode": "XXX XXX"
        },
        "pet": {
            "name": "Bobby",
            "species": "Dog",
            "breed": "Cocker Spaniel",
            "purchase_date": "2024-02-14"
        },
        "policy": {
            "insurer": "Affinity",
            "premium": 24.37,
            "policy_number": "POL-JANE-001"
        },
        "vet": {
            "name": "Francis Bacon Pet Health",
            "location": "Wossit"
        },
        "diagnosis": {
            "description": "Sniffle and Lump",
            "code": "DX-SNIFF-LUMP"
        },
        "claim": {
            "reference": "CLM-BOBBY-001",
            "status": "Passed"
        }
    }

    print("🚀 Starting Business Ontology Verification...")

    with driver.session() as session:
        # 1. Apply Schema
        print("\n1. Applying Schema Constraints...")
        with open(os.path.join(os.path.dirname(__file__), 'business_ontology.cypher'), 'r') as f:
            cypher_commands = f.read().split(';')
            for cmd in cypher_commands:
                if cmd.strip():
                    try:
                        session.run(cmd)
                    except Exception as e:
                        print(f"   Warning applying constraint: {e}")
        print("   ✅ Schema applied.")

        # 2. Ingest Story Data (The Jane Winterbottom Narrative)
        print("\n2. Ingesting Story Data...")
        ingest_query = """
        // Create Customer and Address
        MERGE (jane:Person {name: $customer_name})
        MERGE (addr:Address {line1: $address_line1, postcode: $address_postcode})
        MERGE (jane)-[:LIVES_AT]->(addr)

        // Create Pet and Breed
        MERGE (bobby:Pet {name: $pet_name, species: $pet_species, purchase_date: $pet_purchase_date})
        MERGE (breed:Breed {name: $pet_breed, species: $pet_species})
        MERGE (bobby)-[:IS_BREED]->(breed)
        MERGE (jane)-[:OWNS]->(bobby)

        // Create Policy, Insurer, Underwriter
        MERGE (policy:Policy {policy_number: $policy_number, premium: $policy_premium})
        MERGE (insurer:Insurer {name: $insurer_name})
        MERGE (policy)-[:INSURED_BY]->(insurer)
        MERGE (policy)-[:OWNED_BY]->(jane)
        MERGE (policy)-[:COVERS]->(bobby)

        // Create Vet, Visit, Diagnosis
        MERGE (vet:VetPractice {name: $vet_name, location: $vet_location})
        MERGE (diag:Diagnosis {code: $diag_code, description: $diag_desc})
        MERGE (bobby)-[:VISITED]->(vet)
        MERGE (vet)-[:DIAGNOSED]->(diag)
        MERGE (diag)-[:FOR]->(bobby)

        // Create Claim
        MERGE (claim:Claim {reference_number: $claim_ref, status: $claim_status})
        MERGE (claim)-[:FILED_AGAINST]->(policy)
        MERGE (claim)-[:INVOLVES]->(bobby)
        MERGE (jane)-[:SUBMITTED]->(claim)

        // Create Assessments/Interactions (Simulated)
        MERGE (anne:Person {name: "Anne Farraday", role: "Assessor"})
        MERGE (willow:Agent {name: "Willow", role: "Research Agent"})
        MERGE (anne)-[:ASSESSED]->(claim)
        MERGE (willow)-[:RESEARCHED]->(diag)

        RETURN jane, bobby, policy, claim
        """
        
        session.run(ingest_query, 
            customer_name=story_data["customer"]["name"],
            address_line1=story_data["customer"]["address"],
            address_postcode=story_data["customer"]["postcode"],
            pet_name=story_data["pet"]["name"],
            pet_species=story_data["pet"]["species"],
            pet_breed=story_data["pet"]["breed"],
            pet_purchase_date=story_data["pet"]["purchase_date"],
            policy_number=story_data["policy"]["policy_number"],
            policy_premium=story_data["policy"]["premium"],
            insurer_name=story_data["policy"]["insurer"],
            vet_name=story_data["vet"]["name"],
            vet_location=story_data["vet"]["location"],
            diag_code=story_data["diagnosis"]["code"],
            diag_desc=story_data["diagnosis"]["description"],
            claim_ref=story_data["claim"]["reference"],
            claim_status=story_data["claim"]["status"]
        )
        print("   ✅ Story data ingested.")

        # 3. Verify Story Retrieval
        print("\n3. Verifying Graph Structure...")
        
        # Test 1: Find Jane's Pet
        result = session.run("""
            MATCH (p:Person {name: "Jane Winterbottom"})-[:OWNS]->(pet:Pet)
            RETURN pet.name as pet_name, pet.species as species
        """)
        record = result.single()
        if record and record['pet_name'] == "Bobby":
            print("   ✅ Verified: Jane owns Bobby.")
        else:
            print("   ❌ Failed: Jane does not own Bobby.")

        # Test 2: Find Claim for Bobby
        result = session.run("""
            MATCH (claim:Claim)-[:INVOLVES]->(pet:Pet {name: "Bobby"})
            RETURN claim.reference_number as ref, claim.status as status
        """)
        record = result.single()
        if record and record['status'] == "Passed":
            print(f"   ✅ Verified: Claim {record['ref']} for Bobby is Passed.")
        else:
            print("   ❌ Failed: No passed claim found for Bobby.")

        # Test 3: Find Willow's Contribution
        result = session.run("""
            MATCH (a:Agent {name: "Willow"})-[:RESEARCHED]->(d:Diagnosis)
            RETURN d.description as diagnosis
        """)
        record = result.single()
        if record and record['diagnosis'] == "Sniffle and Lump":
            print("   ✅ Verified: Willow researched the 'Sniffle and Lump'.")
        else:
            print("   ❌ Failed: Willow did not research the diagnosis.")

    driver.close()
    print("\n✨ Verification Complete!")

if __name__ == "__main__":
    verify_business_ontology()
