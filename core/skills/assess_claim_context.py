import os
from typing import Dict, Any, List
from core.clients.graph_client import GraphClient
from datetime import datetime

class ClaimAssessorEnrichment:
    """
    Assessor Enrichment Skill (Phase 11/13).
    Summarizes claim context and assesses relevance of unstructured data (Apollo-1 model).
    """
    
    def __init__(self, agent_id: str = "ClaimsAssessor"):
        self.client = GraphClient(agent_id=agent_id)
    
    def get_claim_summary(self, claim_ref: str) -> Dict[str, Any]:
        """Fetches the full story for a claim from the Brain."""
        # Robust query: handles multiple possible reference properties
        query = """
            MATCH (c:Claim)
            WHERE c.reference_number = $ref OR c.id = $ref
            OPTIONAL MATCH (c)-[:FILED_AGAINST]->(pol:Policy)-[:OWNED_BY]->(p:Person)
            OPTIONAL MATCH (c)-[:CONCERNS]->(pet:Pet)
            OPTIONAL MATCH (pet)-[:VISITED]->(vet:VetPractice)-[:DIAGNOSED]->(d:Diagnosis)
            RETURN properties(c) as claim, 
                   properties(pol) as policy, 
                   properties(p) as customer, 
                   properties(pet) as pet, 
                   collect(DISTINCT {vet: vet.name, diagnosis: d.description, code: d.code}) as history
        """
        results = self.client.run(query, parameters={"ref": claim_ref})
        if not results:
            return {"error": f"Claim {claim_ref} not found in the Brain."}
        
        record = results[0]
        return {
            "claim": record['claim'],
            "policy": record['policy'] or {},
            "customer": record['customer'] or {},
            "pet": record['pet'] or {},
            "medical_history": record['history']
        }

    def assess_unstructured_relevance(self, claim_ref: str, raw_note: str) -> Dict[str, Any]:
        """
        Simulates the Apollo-1 Neurosymbolic assessment.
        In production, this would use a Claude 3.5 Sonnet call to classify relevance.
        """
        summary = self.get_claim_summary(claim_ref)
        if "error" in summary:
            return summary

        # Mock Relevance Logic (Symbolic + Neural Simulation)
        # We look for keywords that bridge the history to the note.
        pet_name = summary['pet'].get('name', '').lower()
        hist_codes = [h['code'].lower() for h in summary['medical_history'] if h['code']]
        
        relevance_score = 0.1 # Baseline
        reasons = []

        if pet_name in raw_note.lower():
            relevance_score += 0.4
            reasons.append(f"Direct mention of pet name: {pet_name}")
        
        if any(code in raw_note.lower() for code in hist_codes):
            relevance_score += 0.5
            reasons.append("Reference to existing diagnosis code in historical vet records.")

        if "previous vet" in raw_note.lower() or "medical records" in raw_note.lower():
            relevance_score += 0.3
            reasons.append("Contextual mention of medical history acquisition.")

        return {
            "claim_ref": claim_ref,
            "relevance_score": min(relevance_score, 1.0),
            "relevance_summary": "HIGH" if relevance_score > 0.7 else "MEDIUM" if relevance_score > 0.4 else "LOW",
            "findings": reasons,
            "original_note": raw_note,
            "system_instruction": "Neurosymbolic Apollo-1: Enrich claim with these findings if score > 0.5"
        }

    def log_assessor_adjustment(self, claim_ref: str, step_id: str, human_adjustment: str):
        """
        Records a human-in-the-loop adjustment for the Apollo-1 refactoring loop.
        """
        self.client.run("""
            MATCH (c:Claim)
            WHERE c.reference_number = $ref OR c.id = $ref
            CREATE (c)-[:ADJUSTED_BY_HUMAN]->(a:Adjustment {
                timestamp: datetime(),
                step: $step,
                adjustment: $adj,
                type: 'Apollo-1 Feedback'
            })
        """, parameters={"ref": claim_ref, "step": step_id, "adj": human_adjustment})
        print(f"✅ Logged adjustment for {claim_ref} at step {step_id}.")

if __name__ == "__main__":
    # Test
    enricher = ClaimAssessorEnrichment()
    ref = "CLM-AHMED-001"
    print(f"Testing enrichment for {ref}...")
    # Seed specific note that should trigger matches
    test_note = "Ahmed's pet had a DX-GASTRO-01 diagnosis previously. Looking into it."
    assessment = enricher.assess_unstructured_relevance(ref, test_note)
    print(f"Relevance: {assessment['relevance_summary']} ({assessment['relevance_score']})")
    for f in assessment['findings']:
        print(f" - {f}")
    
    enricher.log_assessor_adjustment(ref, "Step_3_Enrichment", "Validated Slough vet history manually.")
