import os
import sys
import paramiko
from dotenv import load_dotenv

# Load env vars
load_dotenv()
pg_pass = os.getenv("POSTGRES_PASSWORD", "willowdev123")
openai_key = os.getenv("OPENAI_API_KEY", "")

# Configuration
REMOTE_HOST = "bunny"
REMOTE_USER = "bunny"
REMOTE_PASS = "Chocolate1!" # TODO: Use Key in future
REMOTE_DIR = "~/agilemesh/memory_stack"

def create_ssh_client():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        print(f"Connecting to {REMOTE_USER}@{REMOTE_HOST}...")
        client.connect(REMOTE_HOST, username=REMOTE_USER, password=REMOTE_PASS)
        return client
    except Exception as e:
        print(f"❌ Failed to connect: {e}")
        sys.exit(1)

def run_command(client, command):
    print(f"Running: {command}")
    stdin, stdout, stderr = client.exec_command(command)
    exit_status = stdout.channel.recv_exit_status()
    if exit_status != 0:
        err = stderr.read().decode().strip()
        print(f"❌ Error: {err}")
        return False
    return True

def deploy():
    client = create_ssh_client()
    
    try:
        # 1. Prepare
        run_command(client, f"mkdir -p {REMOTE_DIR}/zep-data")
        
        # 2. Deploy Zep (Docker)
        print("\n🧠 Deploying Zep (Memory Layer)...")
        run_command(client, "docker stop agilemesh-zep || true")
        run_command(client, "docker rm agilemesh-zep || true")
        
        # Zep needs an LLM to function (for embedding/summarization). 
        # We'll pass the OpenAI Key from .env or rely on local NLP if configured (complex).
        # For simplicity, we use OpenAI for the 'Graphiti' style intelligence Zep offers.
        
        cmd = (
            f"docker run -d --name agilemesh-zep "
            f"--restart unless-stopped "
            f"--network agilemesh "
            f"-p 8001:8000 "  # Host:8001 -> Container:8000 (Dashboard is 8000)
            f"-e ZEP_OPENAI_API_KEY={openai_key} "
            f"-e ZEP_STORE_TYPE=postgres "
            f"-e ZEP_POSTGRES_URI='postgres://n8n:{pg_pass}@agilemesh-postgres:5432/n8n' " # Re-using N8N's Postgres for now to save resources? Or separate? 
            # Better to use separate DB or separate DB name. Let's use 'zep' DB.
            # But we need to create it first.
            f"-v {REMOTE_DIR}/zep-data:/app/data "
            f"ghcr.io/getzep/zep:latest"
        )
        
        # Wait! Zep needs its own DB or at least a DB to connect to.
        # Let's add a step to create 'zep' database in our existing Postgres container.
        create_db_cmd = f"docker exec agilemesh-postgres psql -U n8n -c 'CREATE DATABASE zep;'"
        run_command(client, create_db_cmd)
        
        # Now update URI
        zep_cmd = (
            f"docker run -d --name agilemesh-zep "
            f"--restart unless-stopped "
            f"--network agilemesh "
            f"-p 8001:8000 "
            f"-e ZEP_OPENAI_API_KEY={openai_key} "
            f"-e ZEP_STORE_TYPE=postgres "
            f"-e ZEP_POSTGRES_URI='postgres://n8n:{pg_pass}@agilemesh-postgres:5432/zep' "
            f"-e ZEP_NLP_MODEL_TYPE=openai " 
            f"-v {REMOTE_DIR}/zep-data:/app/data "
            f"ghcr.io/getzep/zep:latest"
        )

        if run_command(client, zep_cmd):
            print("\n✅ Zep Memory Layer Deployed!")
            print(f"🌍 API Access: http://{REMOTE_HOST}:8001")
            print(f"🔗 Internal Network: http://agilemesh-zep:8000")
        
    finally:
        client.close()

if __name__ == "__main__":
    deploy()
