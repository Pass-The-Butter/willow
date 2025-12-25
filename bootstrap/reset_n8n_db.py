import paramiko
import sys

# Configuration
REMOTE_HOST = "bunny"
REMOTE_USER = "bunny"
REMOTE_PASS = "Chocolate1!"
REMOTE_DIR = "~/agilemesh/n8n_stack"

def run_wipe():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        print(f"Connecting to {REMOTE_USER}@{REMOTE_HOST}...")
        client.connect(REMOTE_HOST, username=REMOTE_USER, password=REMOTE_PASS)
        
        print(f"⚠️  WIPING Postgres Data at {REMOTE_DIR}/postgres-data ...")
        # Stop containers first to avoid locking
        client.exec_command("docker stop agilemesh-postgres agilemesh-n8n")
        
        # Delete data
        stdin, stdout, stderr = client.exec_command(f"rm -rf {REMOTE_DIR}/postgres-data")
        exit_status = stdout.channel.recv_exit_status()
        
        if exit_status == 0:
            print("✅ Data Wiped. Ready for clean deploy.")
        else:
            print(f"❌ Error wiping data: {stderr.read().decode()}")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    run_wipe()
