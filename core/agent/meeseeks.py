"""
The Meeseeks Squad.
"Existence is pain to a Meeseeks... until the task is done."

Implements the Research -> Do -> Check -> Land the Plane loop.
"""

import os
import json
from core.skills import manage_episodic_memory, manage_beads, client_graphiti
from core.utils.credentials import load_env_or_fail
import requests

# Load LLM Credentials
env = load_env_or_fail(["OPENAI_API_KEY"])
OPENAI_API_KEY = env["OPENAI_API_KEY"]

class Meeseeks:
    def __init__(self, role: str = "Assistant"):
        self.role = role
        self.session_id = f"meeseeks-{role}-{os.urandom(4).hex()}"
        print(f"👻 Meeseeks {self.session_id} spawned!")

    def log(self, content: str):
        """Log thoughts to Episodic Memory"""
        print(f"[{self.role}] {content}")
        manage_episodic_memory.add_turn(self.session_id, "assistant", content)

    def research(self, task_id: str):
        """Scout the graph for context"""
        self.log(f"Searching context for Task {task_id}...")
        # 1. Get recent episodes
        episodes = manage_episodic_memory.get_recent_context(self.session_id)
        # 2. Get temporal facts
        facts = client_graphiti.search_facts(f"Task {task_id}")
        
        return {
            "episodes": episodes,
            "facts": facts
        }

    def execute(self, plan: str):
        """Simulate execution (for now)"""
        self.log(f"Executing Plan: {plan[:50]}...")
        # In a real agent, this would call tools.
        return {"status": "success", "output": "Code written."}

    def check(self, execution_result: dict):
        """Verify the work"""
        self.log("Verifying work...")
        if execution_result["status"] == "success":
            return True
        return False

    def land_the_plane(self, task_id: str):
        """Consolidate memory and close task"""
        self.log("Landing the plane...")
        manage_beads.land_the_plane(task_id, f"Completed by {self.session_id}")

    def run_task(self, task_id: str):
        """The Main Loop"""
        try:
            # 1. Research
            context = self.research(task_id)
            
            # 2. Plan & Execute (Simple Mock)
            self.log(f"Context gathered. Generating plan...")
            plan = "Write the code."
            result = self.execute(plan)
            
            # 3. Check
            if self.check(result):
                # 4. Land the Plane
                self.land_the_plane(task_id)
                print(f"✨ Task {task_id} Complete! I can stop existing now.")
            else:
                self.log("❌ Verification failed. Retrying...")
                # Retry logic would go here
                
        except Exception as e:
            self.log(f"☠️ Helper died: {e}")

if __name__ == "__main__":
    # Test Run
    m = Meeseeks()
    # Create a dummy task to work on
    task = manage_beads.create_bead("Test Task", "A test for Meeseeks")
    if task.get("success"):
        m.run_task(task["bead_id"])
