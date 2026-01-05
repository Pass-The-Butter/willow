
import sys
import os
from dotenv import load_dotenv

# Add repo root to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '../../'))

try:
    from core.skills import manage_change
except ImportError:
    # Try importing assuming run from CWD=repo_root
    try:
        from core.skills import manage_change
    except ImportError as e:
        print(f"❌ Critical Error: Could not import core.skills.manage_change: {e}")
        print(f"sys.path: {sys.path}")
        sys.exit(1)

class ChangeManagerAgent:
    """
    Change Manager Agent
    Responsible for synchronizing state and notifying stakeholders of finalized work.
    """
    def __init__(self):
        self.name = "Change_Manager"

    def finalize_changes(self, summary: str):
        print(f"🤖 [{self.name}] Processing Finalization Request...")
        print(f"📝 Summary: {summary}")
        
        manage_change.execute(summary)
        print(f"✅ [{self.name}] Process Complete.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python core/agents/change_manager.py '<summary_of_changes>'")
        sys.exit(1)
        
    agent = ChangeManagerAgent()
    agent.finalize_changes(sys.argv[1])
