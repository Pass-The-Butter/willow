from temporalio import activity
from core.clients.graph_client import GraphClient

@activity.defn
async def check_policy_active(claim_id: str) -> dict:
    activity.logger.info(f"Checking policy for {claim_id}...")
    
    # Connect to Brain
    client = GraphClient(agent_id="TemporalWorker")
    
    # Basic Query: Find a policy linked to the claim (or mocked by ID pattern for now if graph incomplete)
    # Architecture: (:Claim {id: claim_id})<-[:FILED_AGAINST]-(:Policy)
    cypher = """
        MATCH (c:Claim {id: $claim_id})<-[:FILED_AGAINST]-(p:Policy)
        RETURN p.id as policy_id, p.status as status
    """
    results = client.run(cypher, {"claim_id": claim_id})
    
    if not results:
        # Fallback for prototype: If claim_id mentions a policy, assume it exists for testing
        activity.logger.warning(f"No policy found in graph for {claim_id}. Using heuristic.")
        return {"active": "OneDayInsurance" in claim_id, "policy_id": "UNKNOWN"}

    policy = results[0]
    is_active = (policy['status'] == 'ACTIVE')
    
    return {"active": is_active, "policy_id": policy['policy_id']}

@activity.defn
async def check_coverage_match(claim_id: str) -> dict:
    activity.logger.info(f"Checking coverage for {claim_id}...")
    client = GraphClient(agent_id="TemporalWorker")
    
    # Query: Does the Policy cover the Risk Type associated with the Claim?
    cypher = """
        MATCH (c:Claim {id: $claim_id})-[:CONCERNS]->(r:Risk)
        MATCH (c)<-[:FILED_AGAINST]-(p:Policy)
        MATCH (p)-[:COVERS]->(k:Coverage)
        WHERE k.type = r.type
        RETURN k.type as coverage
    """
    results = client.run(cypher, {"claim_id": claim_id})
    
    match = len(results) > 0
    return {"match": match, "coverage_type": results[0]['coverage'] if match else None}

@activity.defn
async def assess_fraud_risk(claim_id: str) -> dict:
    activity.logger.info(f"Assessing fraud for {claim_id}...")
    # For now, simplistic rule: If amount > 10000 and created < 1 day after policy start
    # We will just use a deterministic hash for the prototype
    
    is_fraud = "FRAUD" in claim_id
    score = 0.95 if is_fraud else 0.1
    return {"score": score}

@activity.defn
async def create_claim_decision(details: dict) -> dict:
    activity.logger.info(f"Recording decision for {details['claim_id']}: {details['decision']}")
    client = GraphClient(agent_id="TemporalWorker")
    
    cypher = """
        MATCH (c:Claim {id: $claim_id})
        CREATE (d:Decision {
            decision: $decision,
            reason: $reason,
            timestamp: datetime()
        })
        CREATE (d)-[:DECIDED_ON]->(c)
        RETURN elementId(d) as id
    """
    client.run(cypher, {
        "claim_id": details['claim_id'],
        "decision": details['decision'],
        "reason": details['reason']
    })
    
    return {
        "status": "RECORDED", 
        "decision": details["decision"], 
        "reason": details["reason"]
    }
