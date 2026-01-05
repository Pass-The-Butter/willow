from temporalio import activity
import asyncio

# In future, these will use GraphClient to read/write from Neo4j

@activity.defn
async def check_policy_active(claim_id: str) -> dict:
    activity.logger.info(f"Checking policy for {claim_id}...")
    # Simulate DB lookup
    # Mocking: Claims starting with 'CLM-VALID' are valid
    is_active = True
    if "INVALID-POL" in claim_id:
        is_active = False
    
    return {"active": is_active, "policy_id": "POL-12345"}

@activity.defn
async def check_coverage_match(claim_id: str) -> dict:
    activity.logger.info(f"Checking coverage for {claim_id}...")
    # Mock result
    return {"match": True, "coverage_type": "Property Damage"}

@activity.defn
async def assess_fraud_risk(claim_id: str) -> dict:
    activity.logger.info(f"Assessing fraud for {claim_id}...")
    # Mock result
    # In reality, this would call an ML model or check graph patterns
    is_fraud = False
    if "FRAUD" in claim_id:
        is_fraud = True
        
    return {"score": 0.9 if is_fraud else 0.05}

@activity.defn
async def create_claim_decision(details: dict) -> dict:
    activity.logger.info(f"Recording decision for {details['claim_id']}: {details['decision']}")
    # This would write the (:Decision) node to Neo4j
    return {
        "status": "RECORDED", 
        "decision": details["decision"], 
        "reason": details["reason"]
    }
