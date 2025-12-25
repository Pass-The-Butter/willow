import paramiko
import time

# Configuration
HOST = "bunny"
USER = "bunny"
PASS = "Chocolate1!"

def execute_remote_command(ssh, command, description):
    print(f"[{description}] Running: {command}")
    stdin, stdout, stderr = ssh.exec_command(command)
    exit_status = stdout.channel.recv_exit_status()
    out = stdout.read().decode().strip()
    err = stderr.read().decode().strip()
    
    if exit_status == 0:
        print(f"✓ Success: {out[:100]}...")
        return True, out
    else:
        print(f"✗ Failed: {err}")
        return False, err

def setup_population_server():
    print(f"Connecting to {HOST} as {USER}...")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(HOST, username=USER, password=PASS)
        print("✓ Connected via SSH.")
        
        # 1. System Info
        execute_remote_command(ssh, "uname -a", "Checking System Info")
        execute_remote_command(ssh, "free -h", "Checking Memory")
        
        # 2. Check Docker
        success, _ = execute_remote_command(ssh, "docker --version", "Checking Docker")
        if not success:
            print("Docker not found. Installing...")
            # Install Docker
            cmds = [
                "echo '{0}' | sudo -S apt-get update".format(PASS),
                "echo '{0}' | sudo -S apt-get install -y docker.io".format(PASS),
                "echo '{0}' | sudo -S systemctl start docker".format(PASS),
                "echo '{0}' | sudo -S systemctl enable docker".format(PASS),
                "echo '{0}' | sudo -S usermod -aG docker {1}".format(PASS, USER)
            ]
            for cmd in cmds:
                s, o = execute_remote_command(ssh, cmd, "Installing Docker components")
                if not s:
                     print("Failed to install/configure Docker")
                     return
            print("✓ Docker installed and configured.")
            
        else:
            print("✓ Docker is installed.")
            
        # 3. Check/Deploy Postgres Container
        success, out = execute_remote_command(ssh, "echo '{0}' | sudo -S docker ps -a | grep willow-population-db".format(PASS), "Checking for DB container")
        
        if success and "Up" in out:
             print("! Population DB already running.")
        else:
             print("Deploying Population DB...")
             # Remove if exists but stopped
             if out:
                 execute_remote_command(ssh, "echo '{0}' | sudo -S docker rm -f willow-population-db".format(PASS), "Cleaning old container")
                 
             # Run new container with pgvector (using ankane/pgvector image)
             run_cmd = (
                 "echo '{0}' | sudo -S docker run -d "
                 "--name willow-population-db "
                 "-p 5432:5432 "
                 "-e POSTGRES_USER=willow "
                 "-e POSTGRES_PASSWORD=willowdev123 "
                 "-e POSTGRES_DB=population "
                 "-v population_data:/var/lib/postgresql/data "
                 "--restart always "
                 "ankane/pgvector:latest"
             ).format(PASS)
             s, o = execute_remote_command(ssh, run_cmd, "Starting Postgres+pgvector")
             if s:
                 print("✓ Population DB deployed on Xeon Server!")
                 time.sleep(5) # Wait for startup
             else:
                 print("✗ Failed to deploy DB.")

    except Exception as e:
        print(f"Connection Failed: {e}")
    finally:
        ssh.close()

if __name__ == "__main__":
    setup_population_server()
