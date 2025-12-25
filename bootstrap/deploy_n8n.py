
import os
import sys
import paramiko
import time

# Configuration
REMOTE_HOST = "bunny"
REMOTE_USER = "bunny"
REMOTE_PASS = "Chocolate1!"
REMOTE_DIR = "~/agilemesh/n8n_stack"

# N8N Configuration
domain = "n8n.agilemesh.net"
webhook_url = f"https://{domain}/"

# Load env vars for deployment
from dotenv import load_dotenv
load_dotenv()
pg_pass = os.getenv("POSTGRES_PASSWORD", "n8n_password_secure_123")
n8n_pass = os.getenv("N8N_BASIC_AUTH_PASSWORD", "willowdev123")

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
        print(f"❌ Error (Exit {exit_status}): {err}")
        return False
    return True

def deploy():
    client = create_ssh_client()
    
    try:
        # 1. Prepare Directories
        run_command(client, f"mkdir -p {REMOTE_DIR}/n8n-data")
        run_command(client, f"mkdir -p {REMOTE_DIR}/postgres-data")
        
        # 2. Network
        print("\n🌐 Creating Docker Network...")
        run_command(client, "docker network create agilemesh || true")
        
        # 3. Deploy PostgreSQL (for N8N)
        print("\n🐘 Deploying PostgreSQL...")
        run_command(client, "docker stop agilemesh-postgres || true")
        run_command(client, "docker rm agilemesh-postgres || true")
        
        pg_cmd = (
            f"docker run -d --name agilemesh-postgres "
            f"--restart unless-stopped "
            f"--network agilemesh "
            f"-e POSTGRES_USER=n8n "
            f"-e POSTGRES_PASSWORD={pg_pass} " 
            f"-e POSTGRES_DB=n8n "
            f"-v {REMOTE_DIR}/postgres-data:/var/lib/postgresql/data "
            f"postgres:15-alpine"
        )
        if not run_command(client, pg_cmd):
            print("❌ PostgreSQL failed to start!")
            return

        print("Waiting 10s for Postgres to initialize...")
        time.sleep(10)

        # 4. Deploy N8N
        print("\n⚡ Deploying N8N...")
        run_command(client, "docker stop agilemesh-n8n || true")
        run_command(client, "docker rm agilemesh-n8n || true")

        n8n_cmd = (
            f"docker run -d --name agilemesh-n8n "
            f"--restart unless-stopped "
            f"--network agilemesh "
            f"-p 5678:5678 "
            f"-e N8N_BASIC_AUTH_ACTIVE=true "
            f"-e N8N_BASIC_AUTH_USER=willow "
            f"-e N8N_BASIC_AUTH_PASSWORD={n8n_pass} "
            f"-e GENERIC_TIMEZONE=Europe/London "
            f"-e DB_TYPE=postgresdb "
            f"-e DB_POSTGRESDB_HOST=agilemesh-postgres "
            f"-e DB_POSTGRESDB_PORT=5432 "
            f"-e DB_POSTGRESDB_DATABASE=n8n "
            f"-e DB_POSTGRESDB_USER=n8n "
            f"-e DB_POSTGRESDB_PASSWORD={pg_pass} "
            f"-v {REMOTE_DIR}/n8n-data:/home/node/.n8n "
            f"n8nio/n8n:latest "
            f"n8n start --tunnel"
        )
        
        if run_command(client, n8n_cmd):
            print("\n✅ N8N Deployment Complete!")
            print(f"🌍 Access: http://{REMOTE_HOST}:5678")
            print("   Login: willow / willowdev123")
        else:
            print("❌ N8N failed to start.")

    finally:
        client.close()

if __name__ == "__main__":
    deploy()
