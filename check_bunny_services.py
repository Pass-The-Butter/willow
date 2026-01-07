
import paramiko
import os
from dotenv import load_dotenv

load_dotenv()

HOST = "bunny"
USER = "bunny"
# Using password from .env for security, though hardcoded in remote_deploy.py was seen
PASS = os.getenv("SSH_BUNNY_PASSWORD", "Chocolate1!")

def check_services():
    print(f"Connecting to {HOST}...")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(HOST, username=USER, password=PASS)
        print("✓ Connected.")
        
        # Check all containers
        stdin, stdout, stderr = ssh.exec_command("docker ps -a --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'")
        print("\n--- Container Status on Bunny ---")
        print(stdout.read().decode())
        
        # Check specifically for graphiti logs if it's not Up
        stdin, stdout, stderr = ssh.exec_command("docker logs willow-graphiti")
        print("\n--- Willow Graphiti Logs ---")
        print(stdout.read().decode()[-1000:]) # Last 1000 chars

    except Exception as e:
        print(f"Error: {e}")
    finally:
        ssh.close()

if __name__ == "__main__":
    check_services()
