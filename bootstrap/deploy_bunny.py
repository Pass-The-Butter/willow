
import os
import sys
import paramiko
from scp import SCPClient
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()


# Configuration
REMOTE_HOST = "bunny"
REMOTE_USER = "bunny"
REMOTE_PASS = os.getenv("SSH_BUNNY_PASSWORD")
REMOTE_DIR = "agilemesh" # Relative to home
REPO_ROOT = Path(__file__).parent.parent

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
    else:
        out = stdout.read().decode().strip()
        if out: print(out)
        return True

def sync_path(scp, local_path, remote_base):
    """Sync a file or directory to remote base"""
    if not os.path.exists(local_path):
        print(f"⚠️ Skipping missing path: {local_path}")
        return

    name = os.path.basename(local_path)
    remote_dest = f"{remote_base}/{name}"
    
    print(f"Syncing {name}...")
    try:
        scp.put(local_path, remote_base, recursive=True)
    except Exception as e:
        print(f"❌ Sync failed for {name}: {e}")


def ensure_docker_compose(client):
    """Ensure docker-compose binary exists on remote"""
    print("Checking for docker-compose...")
    # Check if we can run it globally
    if run_command(client, "which docker-compose"):
        return "docker-compose"
    
    # Check if we can run docker compose plugin
    stdin, stdout, stderr = client.exec_command("docker compose version")
    if stdout.channel.recv_exit_status() == 0:
        return "docker compose"
        
    # Check local binary
    local_bin = f"{REMOTE_DIR}/docker-compose"
    if run_command(client, f"test -f {local_bin}"):
        return f"./docker-compose"
        
    # Download it
    print("⚠️ docker-compose not found. Downloading standalone binary...")
    # Using v2.29.1
    url = "https://github.com/docker/compose/releases/download/v2.29.1/docker-compose-linux-x86_64"
    run_command(client, f"curl -L {url} -o {local_bin}")
    run_command(client, f"chmod +x {local_bin}")
    return f"./docker-compose"

def deploy():
    if not REMOTE_PASS:
        print("❌ SSH_BUNNY_PASSWORD env var not set")
        sys.exit(1)

    client = create_ssh_client()
    scp = SCPClient(client.get_transport())

    try:
        # 1. Prepare Remote Directory
        print("Preparing remote directory...")
        run_command(client, f"mkdir -p {REMOTE_DIR}")
        
        # 2. Create optimized tarball locally
        print("Creating deployment package (filtering node_modules, etc)...")
        
        # Prepare escaped .env for Docker Compose
        with open(REPO_ROOT / ".env", 'r') as f:
            env_content = f.read()
            
        # Escape $ in NEO4J_PASSWORD for Docker Compose (replace $ with $$)
        # We only want to target the specific line to be safe
        lines = env_content.splitlines()
        new_lines = []
        for line in lines:
            if line.startswith("NEO4J_PASSWORD="):
                key, val = line.split("=", 1)
                # Escape $ to $$
                val_escaped = val.replace("$", "$$")
                new_lines.append(f"{key}={val_escaped}")
            else:
                new_lines.append(line)
        
        with open(REPO_ROOT / ".env.deploy", 'w') as f:
            f.write("\n".join(new_lines) + "\n")
            
        # Tar command (renaming .env.deploy to .env using -s for Mac bsdtar if available, or just include it and mv on remote)
        # Using simple include and remote mv to be cross-platform safe regarding tar flags
        tar_cmd = [
            "tar", 
            "--exclude='node_modules'", 
            "--exclude='__pycache__'", 
            "--exclude='.git'", 
            "--exclude='.DS_Store'",
            "--exclude='.venv'",
            "-czf", "deploy_package.tar.gz",
            "docker-compose.yml", ".env.deploy", "core", "domains", "infrastructure", "Inbox"
        ]
        # Run tar command locally
        import subprocess
        subprocess.check_call(" ".join(tar_cmd), shell=True, cwd=str(REPO_ROOT))
        
        # 3. Upload Tarball
        print(f"Uploading deployment package to {REMOTE_DIR}...")
        scp.put(str(REPO_ROOT / "deploy_package.tar.gz"), REMOTE_DIR)
        
        # 4. Extract on Remote
        print("Extracting package on remote...")
        run_command(client, f"tar -xzf {REMOTE_DIR}/deploy_package.tar.gz -C {REMOTE_DIR}")
        
        # Move .env.deploy to .env
        run_command(client, f"mv {REMOTE_DIR}/.env.deploy {REMOTE_DIR}/.env")
        
        # 5. Ensure Docker Compose
        compose_cmd_prefix = ensure_docker_compose(client)
        print(f"Using compose command: {compose_cmd_prefix}")
        
        # 6. Docker Compose Up (Gateway Only)
        print("🚀 Launching Gateway Service...")
        
        # If using ./docker-compose, we must be in the dir
        # We deploy gateway, dashboard, and proxy to ensure visualization is live
        cmd = f"cd {REMOTE_DIR} && {compose_cmd_prefix} up -d --build willow-gateway dashboard proxy"
        
        run_command(client, cmd)
        
        print("\n✅ Deployment Command Sent!")
        print("⏳ Verifying Health...")
        run_command(client, "curl -I http://localhost:8001/health || echo 'Health check failed'")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Local Tar creation failed: {e}")
    finally:
        scp.close()
        client.close()
        # Cleanup local tar and temp env
        if os.path.exists(str(REPO_ROOT / "deploy_package.tar.gz")):
            os.remove(str(REPO_ROOT / "deploy_package.tar.gz"))
        if os.path.exists(str(REPO_ROOT / ".env.deploy")):
            os.remove(str(REPO_ROOT / ".env.deploy"))

if __name__ == "__main__":
    deploy()

