from core.clients.graph_client import GraphClient
import uuid
from datetime import datetime

def add_factory_data():
    client = GraphClient(agent_id="DataEnricher")
    
    print("🚀 Ingesting additional factory data scenarios...")

    scenarios = [
        {
            "customer": {"name": "Arthur Dent", "address": "155 Country Lane", "postcode": "SA1 1ZZ"},
            "pet": {"name": "Marvin", "species": "Dog", "breed": "Paranoid Android", "dob": "1978-01-01"},
            "policy": {"number": "POL-AD-42", "premium": 42.42},
            "vet": {"name": "The Restaurant at the End of the Universe", "location": "Magrathea"},
            "diagnosis": {"code": "DX-DEPRESSION", "desc": "Genuine People Personality"},
            "claim": {"ref": "CLM-AD-001", "status": "Passed", "amount": 420.00},
            "decision": {"outcome": "PASSED", "reason": "Policy covers existential dread."}
        },
        {
            "customer": {"name": "Ford Prefect", "address": "Betelgeuse 7", "postcode": "H2G 2"},
            "pet": {"name": "Zaphod", "species": "Cat", "breed": "Two-headed Ginger", "dob": "2020-05-10"},
            "policy": {"number": "POL-FP-6x9", "premium": 54.00},
            "vet": {"name": "Heart of Gold Vet Clinic", "location": "Deep Space"},
            "diagnosis": {"code": "DX-EGO", "desc": "Inflated Ego"},
            "claim": {"ref": "CLM-FP-002", "status": "Rejected", "amount": 1000.00},
            "decision": {"outcome": "REJECTED", "reason": "Self-inflicted injury via improbability drive."}
        },
        {
            "customer": {"name": "Tricia McMillan", "address": "Earth (Alpha)", "postcode": "LDN 1"},
            "pet": {"name": "Trillian", "species": "Mice", "breed": "White Mouse", "dob": "2023-12-01"},
            "policy": {"number": "POL-TM-MIKE", "premium": 12.50},
            "vet": {"name": "Slartibartfast Surgical", "location": "Norway"},
            "diagnosis": {"code": "DX-QUEST", "desc": "Questioning Reality"},
            "claim": {"ref": "CLM-TM-003", "status": "Pending", "amount": 250.00},
            "decision": {"outcome": "PENDING", "reason": "Waiting for the Ultimate Answer."}
        }
    ]

    for s in scenarios:
        query = """
        // Create Customer and Address
        MERGE (p:Person {name: $customer.name})
        MERGE (addr:Address {line1: $customer.address, postcode: $customer.postcode})
        MERGE (p)-[:LIVES_AT]->(addr)

        // Create Pet and Breed
        MERGE (pet:Pet {name: $pet.name, species: $pet.species, dob: $pet.dob})
        MERGE (breed:Breed {name: $pet.breed, species: $pet.species})
        MERGE (pet)-[:IS_BREED]->(breed)
        MERGE (p)-[:OWNS]->(pet)

        // Create Policy
        MERGE (pol:Policy {policy_number: $policy.number})
        SET pol.premium = $policy.premium
        MERGE (pol)-[:OWNED_BY]->(p)
        MERGE (pol)-[:COVERS]->(pet)

        // Create Vet and Diagnosis
        MERGE (vet:VetPractice {name: $vet.name, location: $vet.location})
        MERGE (diag:Diagnosis {code: $diagnosis.code})
        SET diag.description = $diagnosis.desc
        MERGE (pet)-[:VISITED]->(vet)
        MERGE (vet)-[:DIAGNOSED]->(diag)
        MERGE (diag)-[:FOR]->(pet)

        // Create Claim
        MERGE (c:Claim {reference_number: $claim.ref})
        SET c.status = $claim.status, c.amount = $claim.amount
        MERGE (c)-[:FILED_AGAINST]->(pol)
        MERGE (c)-[:CONCERNS]->(pet)  // Bridge relationship for visualization
        MERGE (c)-[:INVOLVES]->(pet)  // Ontology relationship
        MERGE (p)-[:SUBMITTED]->(c)

        // Create Decision
        MERGE (dec:Decision {id: $decision_id})
        SET dec.decision = $decision.outcome, dec.reason = $decision.reason, dec.timestamp = datetime()
        MERGE (dec)-[:DECIDED_ON]->(c)
        """
        
        try:
            client.run(query, parameters={
                "customer": s["customer"],
                "pet": s["pet"],
                "policy": s["policy"],
                "vet": s["vet"],
                "diagnosis": s["diagnosis"],
                "claim": s["claim"],
                "decision": s["decision"],
                "decision_id": str(uuid.uuid4())
            })
            print(f"   ✅ Ingested scenario for {s['customer']['name']}")
        except Exception as e:
            print(f"   ❌ Failed for {s['customer']['name']}: {e}")

if __name__ == "__main__":
    add_factory_data()
