import asyncio
import sys
import os

# Ensure the project root is in the python path
sys.path.append(os.getcwd())

from temporalio.worker import Worker
from core.orchestration.client import TemporalClient

# Import domains to register their workflows/activities
# We will add imports dynamically here as we build domains
from domains.claims.playbooks import InstantPropertyClaimWorkflow
from domains.claims.activities import (
    check_policy_active,
    check_coverage_match,
    assess_fraud_risk,
    create_claim_decision
)

async def run_worker():
    """
    Starts the Temporal Worker.
    This worker will listen to the 'claims-task-queue' (and others in future).
    """
    print("Starting Willow Temporal Worker...")
    
    # 1. Connect to Temporal
    client = await TemporalClient.connect()

    # 2. Create Worker
    # We will register workflows and activities here
    worker = Worker(
        client,
        task_queue="claims-task-queue",
        workflows=[
            InstantPropertyClaimWorkflow,
        ],
        activities=[
            check_policy_active,
            check_coverage_match,
            assess_fraud_risk,
            create_claim_decision,
        ],
    )

    print("Worker started. Listening on 'claims-task-queue'...")
    await worker.run()

if __name__ == "__main__":
    try:
        asyncio.run(run_worker())
    except KeyboardInterrupt:
        print("\nWorker stopped by user.")
    except Exception as e:
        print(f"Worker failed: {e}")
        # Keep terminal open if needed to see error
        # import time; time.sleep(5)
