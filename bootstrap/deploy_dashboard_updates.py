import subprocess
import os

def run(cmd):
    print(f"Executing: {cmd}")
    return subprocess.run(cmd, shell=True)

BUNNY = "bunny"
LOCAL_DIR = "/Volumes/Delila/dev/Willow/domains/interface"
REMOTE_DIR = "~/agilemesh/domains/interface"

print("🚀 Deploying Dashboard updates to Bunny...")

# 1. Create remote dir
run(f"ssh {BUNNY} 'mkdir -p {REMOTE_DIR}/templates'")

# 2. Upload app.py and requirements
run(f"scp {LOCAL_DIR}/app.py {BUNNY}:{REMOTE_DIR}/")
run(f"scp {LOCAL_DIR}/requirements.txt {BUNNY}:{REMOTE_DIR}/")

# 3. Upload templates
run(f"scp {LOCAL_DIR}/templates/*.html {BUNNY}:{REMOTE_DIR}/templates/")

# 4. Upload Dockerfile
run(f"scp {LOCAL_DIR}/Dockerfile {BUNNY}:{REMOTE_DIR}/")

# 5. Build and Restart on Bunny
print("🔨 Rebuilding container on Bunny...")
build_cmd = (
    f"ssh {BUNNY} 'cd {REMOTE_DIR} && "
    f"docker build -t willow-dashboard . && "
    f"docker stop dashboard || true && "
    f"docker rm dashboard || true && "
    f"docker run -d --name dashboard "
    f"--network willow_willow-network "
    f"-p 5001:5001 "
    f"-e PG_HOST=willow-population-db "
    f"-e PG_DB=population "
    f"-e PG_USER=n8n "
    f"-e PG_PASS=willowdev123 "
    f"-e TELEGRAM_BOT_TOKEN=8215056046:AAHWB34BIBIPwWhH7ogmGUY7G-cdZWPo04I "
    f"willow-dashboard'"
)
run(build_cmd)

print("✅ Dashboard deployed and running at http://bunny/board")
