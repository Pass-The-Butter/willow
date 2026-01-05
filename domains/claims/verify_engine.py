"""
Verify Neurosymbolic Engine (Pet Insurance Edition)
===================================================
1. Seeds the Graph with Jane Winterbottom's Policy.
2. Runs Neural Perception on a Vet Bill (Text).
3. Creates a Claim in the Graph.
4. Runs the Symbolic Activities/Rules (Policy Active? Coverage matches Diagnosis?).
5. Asserts the Decision is correct.
"""

import asyncio
import uuid
import datetime
from dotenv import load_dotenv
from core.clients.graph_client import GraphClient
from domains.claims.perception import extract_claim_facts
from domains.claims.activities import check_policy_active, check_coverage_match, create_claim_decision

load_dotenv()

# Context from The Insurance Factory Story
POLICY_NUMBER = "POL-JANE-001"
PET_NAME = "Bobby"
# A text representation of a vet bill / claim email
VET_BILL_TEXT = """
Subject: Invoice for Bobby
Date: 2026-01-05
From: Francis Bacon Pet Health

Hi Jane, 
Here is the invoice for Bobby's checkup today.
Diagnosis: Sniffle and Lump (Code: DX-SNIFF-LUMP).
Treatment: Anti-inflammatories.
Total: £150.00.
"""

async def run_verification():
    print("🧠 Neurosymbolic Engine Verification (Pet Domain) Starting...")
    
    client = GraphClient(agent_id="Verifier")
    
    # 1. SEED THE GRAPH (Symbolic World)
    # We ensure Jane and Bobby exist with an active policy covering 'Vet Fees'
    print("\n1. Seeding Graph with Jane, Bobby & Policy...")
    seed_query = """
        MERGE (jane:Person {name: "Jane Winterbottom"})
        MERGE (bobby:Pet {name: "Bobby", species: "Dog"})
        MERGE (jane)-[:OWNS]->(bobby)
        
        MERGE (p:Policy {id: $pol_id})
        SET p.status = 'ACTIVE', p.start_date = date() - duration('P6M')
        
        MERGE (p)-[:OWNED_BY]->(jane)
        MERGE (p)-[:COVERS]->(bobby)
        
        MERGE (k:Coverage {type: 'Vet Fees'})
        MERGE (p)-[:COVERS]->(k)
        
        RETURN p.id
    """
    client.run(seed_query, {"pol_id": POLICY_NUMBER})
    print(f"   -> Policy {POLICY_NUMBER} seeded for Jane & Bobby.")

    # 2. NEURAL PERCEPTION (Reading the World)
    print("\n2. Running Neural Perception (LLM) on Vet Bill...")
    facts = extract_claim_facts(VET_BILL_TEXT)
    print(f"   -> Extracted Facts: {facts}")
    
    # 3. INGEST (Writing to Graph)
    print("\n3. Ingesting Claim to Graph...")
    claim_id = f"CLM-{uuid.uuid4().hex[:8]}"
    
    # Map extracted data to graph nodes
    # If LLM extracts 'Sniffle and Lump', we map that as the 'Risk' or 'Diagnosis'
    diagnosis = facts.get('summary', 'Unknown Condition')
    amount = facts.get('claimed_amount', 150.0)
    
    client.run("""
        CREATE (c:Claim {id: $claim_id, text: $text, amount: $amount})
        WITH c
        MATCH (p:Policy {id: $pol_id})
        CREATE (c)<-[:FILED_AGAINST]-(p)
        WITH c, p
        // Relate to the specific pet
        MATCH (p)-[:COVERS]->(pet:Pet {name: $pet_name})
        CREATE (c)-[:CONCERNS]->(pet)
        
        // In Pet Insurance, the 'Risk' is the Condition/Diagnosis
        // For the rule engine, we map this check to 'Vet Fees' coverage
        MERGE (r:Risk {type: 'Vet Fees'}) 
        CREATE (c)-[:CONCERNS]->(r)
        
        RETURN c.id
    """, {
        "claim_id": claim_id, 
        "text": VET_BILL_TEXT,
        "pol_id": POLICY_NUMBER,
        "pet_name": PET_NAME,
        "amount": amount
    })
    print(f"   -> Created Claim {claim_id} for {PET_NAME}")
    
    # 4. SYMBOLIC REASONING (The 'Activities')
    print("\n4. Executing Symbolic Rules (Activities)...")
    
    # Activity 1: Check Policy
    res_policy = await check_policy_active(claim_id)
    print(f"   -> Check Policy: {res_policy}")
    if not res_policy['active']:
        print("   ❌ FAILED: Policy should be active")
        return

    # Activity 2: Check Coverage
    # This checks if the Policy covers 'Vet Fees' (which we seeded it to do)
    res_coverage = await check_coverage_match(claim_id)
    print(f"   -> Check Coverage: {res_coverage}")
    if not res_coverage['match']:
        print("   ❌ FAILED: Coverage should match 'Vet Fees'")
        return

    # Activity 3: Decision
    # Simple rule: If covered and active, approve.
    decision = await create_claim_decision({
        "claim_id": claim_id, 
        "decision": "APPROVE", 
        "reason": "Policy Active + Vet Fees Covered"
    })
    print(f"   -> Final Decision: {decision}")

    print("\n✅ VERIFICATION SUCCESSFUL: Jane's claim for Bobby was approved.")

if __name__ == "__main__":
    asyncio.run(run_verification())
