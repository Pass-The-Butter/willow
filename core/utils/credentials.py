"""
Centralized Credential Management for Willow.
Usage:
    from core.utils.credentials import load_env_or_fail
    env = load_env_or_fail(["NEO4J_URI", "OPENAI_API_KEY"])
    neo4j_uri = env["NEO4J_URI"]
"""

import os
from dotenv import load_dotenv
import sys

def load_env_or_fail(required_keys: list = []) -> dict:
    """
    Load .env file and validate required keys exist.
    Returns dictionary of found keys.
    Exits program if keys are missing.
    """
    # Find .env properly - looking in current and parent dirs
    # Assuming running from root or one level deep
    dotenv_path = os.path.join(os.getcwd(), '.env')
    if not os.path.exists(dotenv_path):
        # Try going up one level
        dotenv_path = os.path.join(os.path.dirname(os.getcwd()), '.env')
    
    load_dotenv(dotenv_path)
    
    missing = []
    found = {}
    
    for key in required_keys:
        val = os.getenv(key)
        if not val:
            missing.append(key)
        else:
            found[key] = val
            
    if missing:
        print(f"❌ CRITICAL ERROR: Missing required environment variables: {', '.join(missing)}")
        print(f"   Please ensure .env file at {dotenv_path} contains these keys.")
        sys.exit(1)
        
    return found

def get_neo4j_auth():
    env = load_env_or_fail(["NEO4J_URI", "NEO4J_USER", "NEO4J_PASSWORD"])
    return (env["NEO4J_URI"], (env["NEO4J_USER"], env["NEO4J_PASSWORD"]))
