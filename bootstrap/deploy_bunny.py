
import os
import sys
import paramiko
from scp import SCPClient

# Configuration
REMOTE_HOST = "bunny"
REMOTE_USER = "bunny"
REMOTE_PASS = "Chocolate1!"
REMOTE_DIR = "~/agilemesh"
LOCAL_INTERFACE_DIR = "domains/interface"

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

def copy_files(client):
    print("Copying files...")
    scp = SCPClient(client.get_transport())
    
    # Create directories first
    run_command(client, f"mkdir -p {REMOTE_DIR}/website/templates")
    run_command(client, f"mkdir -p {REMOTE_DIR}/docs/procedures")
    
    # Copy files
    try:
        scp.put(f"{LOCAL_INTERFACE_DIR}/app.py", f"{REMOTE_DIR}/website/app.py")
        
        # SCP doesn't support wildcard upload easily with paramiko scp usually, 
        # but recursive directory put works.
        # Let's put the templates dir contents one by one or put the whole dir
        # We'll assume local structure matches remote needs
        
        # Upload templates individually to be safe or use recursive put of directory
        # scp.put(f"{LOCAL_INTERFACE_DIR}/templates", f"{REMOTE_DIR}/website/", recursive=True)
        # However, scp paths can be tricky. Let's list local files.
        
        templates = os.listdir(f"{LOCAL_INTERFACE_DIR}/templates")
        for t in templates:
            scp.put(f"{LOCAL_INTERFACE_DIR}/templates/{t}", f"{REMOTE_DIR}/website/templates/{t}")

        # Copy SOP
        scp.put("docs/procedures/HOW_TO_ROTATE_NEO4J_PASSWORD.md", f"{REMOTE_DIR}/docs/procedures/HOW_TO_ROTATE_NEO4J_PASSWORD.md")
        
    except Exception as e:
        print(f"❌ SCP Error: {e}")
    finally:
        scp.close()

def create_docker_compose(client):
    print("Generating docker-compose.yml...")
    
    # Load .env
    env_vars = {}
    try:
        with open('.env') as f:
            for line in f:
                if '=' in line and not line.strip().startswith('#'):
                    k, v = line.strip().split('=', 1)
                    env_vars[k] = v.strip()
    except:
        pass
                
    neo4j_uri = env_vars.get('NEO4J_URI', '')
    neo4j_user = env_vars.get('NEO4J_USER', '')
    neo4j_password = env_vars.get('NEO4J_PASSWORD', '')
    
    # Docker Compose Content
    dc_content = f"""
version: '3.8'

services:
  website:
    image: python:3.11-slim
    container_name: agilemesh-website
    restart: unless-stopped
    working_dir: /app
    ports:
      - "8000:5001"
    environment:
      - FLASK_APP=app.py
      - FLASK_ENV=production
      - NEO4J_URI={neo4j_uri}
      - NEO4J_USER={neo4j_user}
      - NEO4J_PASSWORD={neo4j_password}
      - PG_HOST=bunny
      - PG_PORT=5432
      - PG_DB=population
      - PG_USER=willow
      - PG_PASS=willowdev123
    volumes:
      - ./website:/app
      - ./docs:/docs
    command: >
      sh -c "pip install -q flask neo4j psycopg2-binary python-dotenv certifi &&
             python app.py"
    extra_hosts:
      - "bunny:host-gateway"
"""
    # Write remote file using cat
    # Use single quotes for EOF to avoid variable expansion by shell, but needed for python f-string
    # We escape $ if needed (none here except inside env vars which are resolved by python)
    
    cmd = f"cat > {REMOTE_DIR}/docker-compose.yml <<'EOF'\n{dc_content}\nEOF"
    run_command(client, cmd)

def deploy():
    client = create_ssh_client()
    
    # Load .env locally
    env_vars = {}
    try:
        with open('.env') as f:
            for line in f:
                if '=' in line and not line.strip().startswith('#'):
                    k, v = line.strip().split('=', 1)
                    env_vars[k] = v.strip()
    except:
        pass
                
    neo4j_uri = env_vars.get('NEO4J_URI', '')
    neo4j_user = env_vars.get('NEO4J_USER', '')
    neo4j_password = env_vars.get('NEO4J_PASSWORD', '')

    try:
        copy_files(client)
        # create_docker_compose still useful for structure if user fixes docker later, 
        # but let's just skip it if we know we are using run, or keep it.
        # We can pass vars to create_docker_compose if we wanted, but let's leave that function distinct if it works.
        # Actually create_docker_compose had its own env loading.
        
        # Redefine run_docker_compose to use local vars if needed or just try running commands
        
        print("Restarting Docker services...")
        
        def run_docker_compose():
            # Try v2
            if run_command(client, f"cd {REMOTE_DIR} && docker compose down"):
                if run_command(client, f"cd {REMOTE_DIR} && docker compose up -d"):
                    return True
            # Try v1
            if run_command(client, f"cd {REMOTE_DIR} && docker-compose down"):
                if run_command(client, f"cd {REMOTE_DIR} && docker-compose up -d"):
                    return True
            return False

        if not run_docker_compose():
            print("⚠️ Docker Compose unavailable. Falling back to direct 'docker run'...")
            
            # Clean up existing
            run_command(client, "docker stop agilemesh-website || true")
            run_command(client, "docker rm agilemesh-website || true")
            
            # Construct long docker run command
            # Note: We need to pass all env vars manually
            cmd = (
                f"docker run -d --name agilemesh-website "
                f"--restart unless-stopped "
                f"-p 8000:5001 "
                f"-w /app "
                f"-v {REMOTE_DIR}/website:/app "
                f"-v {REMOTE_DIR}/docs:/docs "
                f"-e FLASK_APP=app.py "
                f"-e FLASK_ENV=production "
                f"-e NEO4J_URI='{neo4j_uri}' "
                f"-e NEO4J_USER='{neo4j_user}' "
                f"-e NEO4J_PASSWORD='{neo4j_password}' "
                f"-e PG_HOST=bunny "
                f"-e PG_PORT=5432 "
                f"-e PG_DB=population "
                f"-e PG_USER=willow "
                f"-e PG_PASS=willowdev123 "
                f"--add-host bunny:host-gateway "
                f"python:3.11-slim "
                f"sh -c 'pip install -q flask neo4j psycopg2-binary python-dotenv certifi && python app.py'"
            )
            
            if not run_command(client, cmd):
                print("❌ 'docker run' failed too!")
                return
        
        print("\n✅ Deployment to Bunny Complete!")
        print(f"🌍 Access: http://{REMOTE_HOST}:8000/board")
        
    finally:
        client.close()

if __name__ == "__main__":
    deploy()
