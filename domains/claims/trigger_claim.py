import asyncio
import sys
import os
import uuid

# Ensure root in path
sys.path.append(os.getcwd())

from core.orchestration.client import TemporalClient
from domains.claims.playbooks import InstantPropertyClaimWorkflow

async def main():
    if len(sys.argv) < 2:
        print("Usage: python trigger_claim.py <claim_id_suffix>")
        print("Example: python trigger_claim.py CLM-TEST-001")
        return

    claim_id = sys.argv[1]
    
    print(f"Triggering workflow for {claim_id}...")
    try:
        client = await TemporalClient.connect()
        
        # Unique workflow ID to allow re-runs
        workflow_id = f"claim-workflow-{claim_id}-{uuid.uuid4().hex[:4]}"

        handle = await client.start_workflow(
            InstantPropertyClaimWorkflow.run,
            claim_id,
            id=workflow_id,
            task_queue="claims-task-queue",
        )

        print(f"Workflow started. ID: {handle.id}")
        print(f"Waiting for result...")

        result = await handle.result()
        print(f"Workflow completed! Result: {result}")

    except Exception as e:
        print(f"Failed to run workflow: {e}")

if __name__ == "__main__":
    asyncio.run(main())
