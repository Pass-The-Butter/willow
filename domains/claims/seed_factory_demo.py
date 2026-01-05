"""
Seed Factory Demo Data
======================
Populates the graph with the "Happy Path" story for the Insurance Factory visualization.
Story: Jane Winterbottom -> Bobby (Pet) -> Vet Visit (Sniffle) -> Claim -> Automated Approval.
"""

import os
import uuid
from dotenv import load_dotenv
from core.clients.graph_client import GraphClient

load_dotenv()

def seed_factory_data():
    print("🌱 Seeding Insurance Factory Demo Data...")
    client = GraphClient(agent_id="FactorySeeder")

    # Clear existing demo data?
    # NOTE: Graph Gateway Policy forbids DELETE. We rely on MERGE to update existing nodes.
    print("   Skipping cleanup (DELETE forbidden). Using MERGE to update entities...")

    print("   Creating new story entities...")
    
    # The Full Story Query
    query = """
    // 1. The Actors
    MERGE (jane:Person {name: "Jane Winterbottom", id: "P-JANE-001"})
    MERGE (bobby:Pet {name: "Bobby", species: "Dog", breed: "Cocker Spaniel"})
    MERGE (jane)-[:OWNS]->(bobby)

    // 2. The Policy (Active & Covering Vet Fees)
    MERGE (pol:Policy {policy_number: "POL-JANE-001"})
    SET pol.status = 'ACTIVE', pol.start_date = date() - duration('P6M')
    MERGE (pol)-[:OWNED_BY]->(jane)
    MERGE (pol)-[:COVERS]->(bobby)
    MERGE (cov:Coverage {type: "Vet Fees"})
    MERGE (pol)-[:COVERS]->(cov)

    // 3. The Vet Visit
    MERGE (vet:VetPractice {name: "Francis Bacon Pet Health", location: "Wossit"})
    MERGE (visit:Visit {date: date()})
    MERGE (bobby)-[:VISITED]->(vet)
    
    // 4. The Diagnosis
    MERGE (diag:Diagnosis {code: "DX-SNIFF-LUMP", description: "Sniffle and Lump"})
    MERGE (vet)-[:DIAGNOSED]->(diag)
    MERGE (diag)-[:FOR]->(bobby)

    // 5. The Claim
    MERGE (c:Claim {id: $claim_id})
    SET c.amount = 150.00,
        c.status = 'PAID',
        c.description = "Vet bill for Sniffle/Lump"
    
    MERGE (jane)-[:SUBMITTED]->(c)
    MERGE (c)-[:CONCERNS]->(bobby)
    MERGE (c)-[:FILED_AGAINST]->(pol)
    MERGE (c)-[:BASED_ON]->(diag)
    
    // 6. The Decision (Neurosymbolic Result)
    // We assume one decision per claim for this demo
    MERGE (d:Decision {claim_id: $claim_id}) 
    SET d.decision = 'APPROVE',
        d.reason = 'Policy Active + Vet Fees Covered',
        d.timestamp = datetime()
    
    MERGE (d)-[:DECIDED_ON]->(c)
    
    // Return IDs for verification
    RETURN jane.name, bobby.name, c.id, d.decision
    """
    
    claim_id = f"CLM-{uuid.uuid4().hex[:8].upper()}"
    
    results = client.run(query, {"claim_id": claim_id})
    
    if results:
        print(f"✅ Seeded successfully!")
        print(f"   Claim ID: {results[0]['c.id']}")
        print(f"   Decision: {results[0]['d.decision']}")
    else:
        print("❌ Seeding failed to return results.")

if __name__ == "__main__":
    seed_factory_data()
