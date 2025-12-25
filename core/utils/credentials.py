"""
Willow Credentials Manager
Centralized credential loading for all agents and skills
"""

import os
from typing import Dict

def load_env() -> Dict[str, str]:
    """
    Load environment variables from .env file
    
    Returns:
        dict of environment variables
    """
    env_path = os.path.join(os.path.dirname(__file__), '../../.env')
    
    credentials = {}
    
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if line and '=' in line and not line.startswith('#'):
                key, val = line.split('=', 1)
                credentials[key] = val
                os.environ[key] = val
    
    return credentials


def get_neo4j_credentials() -> tuple:
    """
    Get Neo4j connection credentials
    
    Returns:
        (uri, username, password)
    """
    if not os.getenv('NEO4J_URI'):
        load_env()
    
    return (
        os.getenv('NEO4J_URI'),
        os.getenv('NEO4J_USER'),
        os.getenv('NEO4J_PASSWORD')
    )


def get_postgres_credentials() -> dict:
    """
    Get PostgreSQL connection credentials
    
    Returns:
        dict with host, port, database, user, password
    """
    if not os.getenv('PG_HOST'):
        load_env()
    
    return {
        'host': os.getenv('PG_HOST', 'bunny'),
        'port': os.getenv('PG_PORT', '5432'),
        'database': os.getenv('PG_DB', 'population'),
        'user': os.getenv('PG_USER', 'willow'),
        'password': os.getenv('PG_PASS', 'willowdev123')
    }


def get_ssh_credentials() -> dict:
    """
    Get SSH connection details
    
    Returns:
        dict with frank and bunny connection strings
    """
    if not os.getenv('SSH_FRANK_HOST'):
        load_env()
    
    return {
        'frank': {
            'host': os.getenv('SSH_FRANK_HOST', 'frank'),
            'user': os.getenv('SSH_FRANK_USER', 'peter'),
            'connection': f"{os.getenv('SSH_FRANK_USER', 'peter')}@{os.getenv('SSH_FRANK_HOST', 'frank')}"
        },
        'bunny': {
            'host': os.getenv('SSH_BUNNY_HOST', 'bunny'),
            'user': os.getenv('SSH_BUNNY_USER', 'bunny'),
            'connection': f"{os.getenv('SSH_BUNNY_USER', 'bunny')}@{os.getenv('SSH_BUNNY_HOST', 'bunny')}"
        }
    }


def get_n8n_credentials() -> dict:
    """
    Get N8N webhook credentials
    
    Returns:
        dict with auth and webhook details
    """
    if not os.getenv('N8N_BASIC_AUTH_USER'):
        load_env()
    
    return {
        'auth_active': os.getenv('N8N_BASIC_AUTH_ACTIVE', 'true') == 'true',
        'user': os.getenv('N8N_BASIC_AUTH_USER', 'willow'),
        'password': os.getenv('N8N_BASIC_AUTH_PASSWORD', 'willowdev123'),
        'webhook_url': os.getenv('N8N_WEBHOOK_URL', '')
    }


def get_telegram_credentials() -> dict:
    """
    Get Telegram bot credentials
    
    Returns:
        dict with bot token and chat ID
    """
    if not os.getenv('TELEGRAM_BOT_TOKEN'):
        load_env()
    
    return {
        'bot_token': os.getenv('TELEGRAM_BOT_TOKEN', ''),
        'chat_id': os.getenv('TELEGRAM_CHAT_ID', '')
    }


def verify_all_credentials() -> dict:
    """
    Verify all credential sets are available
    
    Returns:
        dict with status of each credential type
    """
    load_env()
    
    status = {
        'neo4j': all([
            os.getenv('NEO4J_URI'),
            os.getenv('NEO4J_USER'),
            os.getenv('NEO4J_PASSWORD')
        ]),
        'postgres': all([
            os.getenv('PG_HOST'),
            os.getenv('PG_USER'),
            os.getenv('PG_PASS')
        ]),
        'ssh': all([
            os.getenv('SSH_FRANK_HOST'),
            os.getenv('SSH_BUNNY_HOST')
        ]),
        'n8n': bool(os.getenv('N8N_BASIC_AUTH_USER')),
        'telegram': bool(os.getenv('TELEGRAM_BOT_TOKEN'))
    }
    
    return status


if __name__ == "__main__":
    """Test credential loading"""
    print("=" * 80)
    print("🔐 WILLOW CREDENTIALS MANAGER TEST")
    print("=" * 80)
    
    status = verify_all_credentials()
    
    print("\n✅ Credential Status:")
    for service, available in status.items():
        icon = "✅" if available else "⚠️ "
        print(f"   {icon} {service.upper()}: {'Available' if available else 'Not configured'}")
    
    print("\n📋 Connection Details:")
    
    neo4j = get_neo4j_credentials()
    print(f"\n   Neo4j (AuraDB):")
    print(f"      URI: {neo4j[0][:40]}...")
    print(f"      User: {neo4j[1]}")
    
    pg = get_postgres_credentials()
    print(f"\n   PostgreSQL (Bunny):")
    print(f"      Host: {pg['host']}:{pg['port']}")
    print(f"      Database: {pg['database']}")
    print(f"      User: {pg['user']}")
    
    ssh = get_ssh_credentials()
    print(f"\n   SSH Connections:")
    print(f"      Frank: {ssh['frank']['connection']}")
    print(f"      Bunny: {ssh['bunny']['connection']}")
    
    print("\n" + "=" * 80)
    print("✅ CREDENTIALS LOADED SUCCESSFULLY")
    print("=" * 80)
