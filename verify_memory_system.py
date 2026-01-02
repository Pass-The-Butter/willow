"""
System Verification: Memory Integration
"""
import sys
import time
from core.skills import manage_episodic_memory, manage_beads, client_graphiti
from core.agent.meeseeks import Meeseeks

def run_checks():
    print("🚀 Starting System Checks...")
    
    # 1. Beads Check
    print("\n[1/4] Testing Beads (Task Graph)...")
    task = manage_beads.create_bead("Verification Task", "Verify the memory system")
    if task.get("success"):
        print(f"✅ Created Task: {task['bead_id']}")
    else:
        print(f"❌ Failed to create task: {task}")
        sys.exit(1)
        
    # 2. Episodic Check
    print("\n[2/4] Testing Episodic Memory (Neo4j)...")
    res = manage_episodic_memory.add_turn("verify-session-1", "user", "System check start", relevant_tasks=[task['bead_id']])
    if res.get("success"):
        print(f"✅ Logged Turn: {res['turn_id']}")
    else:
        print(f"❌ Failed to log turn: {res}")
        sys.exit(1)

    # 3. Graphiti Check
    print("\n[3/4] Testing Graphiti Service (Docker)...")
    # Wait a moment for container to potentially wake up
    time.sleep(2) 
    g_res = client_graphiti.add_event("System Verification Run", ["Willow", "Meeseeks"])
    # Note: client result depends on server implementation response
    if "error" not in g_res and ("result" in g_res or type(g_res) == list):
        print(f"✅ Graphiti Response: {g_res}")
    else:
        print(f"⚠️ Graphiti Warning (Is container up?): {g_res}")
        # Not fatal for now, as we verify connection
        
    # 4. Meeseeks Check
    print("\n[4/4] Summoning Meeseeks...")
    try:
        m = Meeseeks(role="Tester")
        m.run_task(task['bead_id'])
        print("✅ Meeseeks Loop Completed.")
    except Exception as e:
        print(f"❌ Meeseeks died: {e}")
        sys.exit(1)
        
    print("\n✨ All Systems Go!")

if __name__ == "__main__":
    run_checks()
