import paramiko
import sys

# Configuration
REMOTE_HOST = "bunny"
REMOTE_USER = "bunny"
REMOTE_PASS = "Chocolate1!"

def run_debug():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        print(f"Connecting to {REMOTE_USER}@{REMOTE_HOST}...")
        client.connect(REMOTE_HOST, username=REMOTE_USER, password=REMOTE_PASS)
        
        # 1. Inspect Env
        print("\n🔍 Checking Environment Variables...")
        stdin, stdout, stderr = client.exec_command("docker inspect agilemesh-n8n | grep -E 'WEBHOOK_URL|N8N_HOST|PROTOCOL|PORT'")
        print(stdout.read().decode())
        
        # 2. Check Logs for Tunnel
        print("\n📜 Checking Logs for Tunnel URL...")
        stdin, stdout, stderr = client.exec_command("docker logs agilemesh-n8n --tail 50")
        logs = stdout.read().decode()
        print(logs)
        
        if "Tunnel URL:" in logs:
            print("\n✅ Tunnel detected in logs!")
        else:
            print("\n❌ No Tunnel URL found in recent logs.")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    run_debug()
