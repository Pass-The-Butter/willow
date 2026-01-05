from datetime import timedelta
from temporalio import workflow

# Import our activities (even if they are just mocked for now)
# We use string names in execution, but need types for type hinting if desired
with workflow.unsafe.imports_passed_through():
    from domains.claims.activities import (
        check_policy_active,
        check_coverage_match,
        assess_fraud_risk,
        create_claim_decision
    )

@workflow.defn
class InstantPropertyClaimWorkflow:
    @workflow.run
    async def run(self, claim_id: str) -> dict:
        """
        Orchestrates an 'Instant Property Claim'.
        Step 1: check policy
        Step 2: check coverage
        Step 3: assess fraud
        Step 4: decide
        """
        workflow.logger.info(f"Starting claim assessment for {claim_id}")

        # 1. Check Policy Active
        policy_status = await workflow.execute_activity(
            check_policy_active,
            claim_id,
            start_to_close_timeout=timedelta(seconds=5),
        )
        if not policy_status["active"]:
            return await self._deny_claim(claim_id, "Policy inactive")

        # 2. Check Coverage Match
        coverage_status = await workflow.execute_activity(
            check_coverage_match,
            claim_id,
            start_to_close_timeout=timedelta(seconds=5),
        )
        if not coverage_status["match"]:
            return await self._deny_claim(claim_id, "No applicable coverage")

        # 3. Assess Fraud
        fraud_result = await workflow.execute_activity(
            assess_fraud_risk,
            claim_id,
            start_to_close_timeout=timedelta(seconds=10),
        )
        if fraud_result["score"] > 0.5:
             # In a real system, this might route to a human
             return await self._deny_claim(claim_id, "High fraud risk")

        # 4. If we got here, Approve
        decision = await workflow.execute_activity(
            create_claim_decision,
            {"claim_id": claim_id, "decision": "APPROVE", "reason": "All checks passed"},
            start_to_close_timeout=timedelta(seconds=5),
        )

        return decision

    async def _deny_claim(self, claim_id: str, reason: str) -> dict:
        """Helper to create a denial decision."""
        return await workflow.execute_activity(
            create_claim_decision,
            {"claim_id": claim_id, "decision": "DENY", "reason": reason},
            start_to_close_timeout=timedelta(seconds=5),
        )
