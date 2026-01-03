import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import the modular skill
try:
    from core.skills.land_the_plane import land_the_plane
except ImportError:
    # Fallback to allow running from different directories
    sys.path.append(os.path.join(os.path.dirname(__file__), '../../'))
    from core.skills.land_the_plane import land_the_plane

class FlightControllerAgent:
    """
    Experimental Agent Wrapper for automated system checks.
    Designed for future upgrading to Autogen 0.8+ (AgentChat) when API stabilizes.
    """
    def __init__(self):
        self.name = "Flight_Controller"
    
    def run_preflight_check(self):
        print(f"🚁 [{self.name}] Received Command: LAND THE PLANE")
        print(f"📋 [{self.name}] Initiating 'land_the_plane' skill sequence...")
        
        # Execute the skill
        results = land_the_plane()
        
        # Simple analysis
        all_systems_go = True
        
        # Check network
        if not all(v == 'Alive' for v in results['network'].values()):
            all_systems_go = False
        
        # Check services
        if not results['services'].get('bunny_docker_up'):
            all_systems_go = False
        
        if all_systems_go:
             print(f"✅ [{self.name}] SYSTEMS NOMINAL. Routine Completed.")
        else:
             print(f"⚠️ [{self.name}] ANOMALIES DETECTED. Review Report.")

if __name__ == "__main__":
    agent = FlightControllerAgent()
    agent.run_preflight_check()
