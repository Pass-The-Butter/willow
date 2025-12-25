import paramiko
import os

# Configuration
HOST = "bunny"
USER = "bunny"
PASS = "Chocolate1!"
SCHEMA_FILE = "domains/population/schema.sql"

def deploy_schema():
    print(f"Reading schema from {SCHEMA_FILE}...")
    with open(SCHEMA_FILE, 'r') as f:
        schema_sql = f.read()

    print(f"Connecting to {HOST}...")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(HOST, username=USER, password=PASS)
        
        # Escape single quotes for the shell command
        # We will write the schema to a temp file on the remote host first to avoid quoting hell
        print("Copying schema to remote host...")
        sftp = ssh.open_sftp()
        remote_path = "/tmp/schema.sql"
        sftp.put(SCHEMA_FILE, remote_path)
        sftp.close()
        
        print("Executing schema on Postgres container...")
        # Command to run psql inside the container using the file we just copied
        # We need to copy the file FROM the host TO the container first
        
        cmd_copy = f"echo '{PASS}' | sudo -S docker cp {remote_path} willow-population-db:/tmp/schema.sql"
        stdin, stdout, stderr = ssh.exec_command(cmd_copy)
        exit_status = stdout.channel.recv_exit_status()
        if exit_status != 0:
            print(f"Error copying to container: {stderr.read().decode()}")
            return

        cmd_exec = f"echo '{PASS}' | sudo -S docker exec -i willow-population-db psql -U willow -d population -f /tmp/schema.sql"
        stdin, stdout, stderr = ssh.exec_command(cmd_exec)
        exit_status = stdout.channel.recv_exit_status()
        
        if exit_status == 0:
            print("✓ Schema successfully deployed to Population DB!")
            print(stdout.read().decode())
        else:
            print(f"✗ Failed to deploy schema: {stderr.read().decode()}")

    except Exception as e:
        print(f"Connection Failed: {e}")
    finally:
        ssh.close()

if __name__ == "__main__":
    deploy_schema()
