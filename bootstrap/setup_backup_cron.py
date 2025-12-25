
import os
import sys

def setup_cron():
    cwd = os.getcwd()
    script_path = os.path.join(cwd, "bootstrap/backup_brain.py")
    python_path = sys.executable
    
    # 0 3 * * * = Run at 3 AM every day
    cron_command = f"0 3 * * * cd {cwd} && {python_path} {script_path} >> {cwd}/backups/backup.log 2>&1"
    
    print(f"📅 Setting up daily backup at 3 AM...")
    print(f"   Command: {cron_command}")
    
    try:
        # Check if already exists
        code = os.system("crontab -l | grep -q 'backup_brain.py'")
        if code == 0:
            print("✅ Backup cron job already exists.")
        else:
            # Append new job
            # Use a safe way to append: list current, append, pipe to crontab
            cmd = f"(crontab -l 2>/dev/null; echo '{cron_command}') | crontab -"
            os.system(cmd)
            print("✅ Daily backup scheduled successfully.")
            
    except Exception as e:
        print(f"❌ Failed to set cron: {e}")

if __name__ == "__main__":
    setup_cron()
