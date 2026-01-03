import subprocess
import os

def run(cmd):
    print(f"Executing: {cmd}")
    return subprocess.run(cmd, shell=True)

BUNNY = "bunny"
LOCAL_DIR = "/Volumes/Delila/dev/Willow/domains/sidebar"
REMOTE_DIR = "~/agilemesh/domains/sidebar"

print("🚀 Deploying Sidebar (Mission Control) updates to Bunny...")

# 1. Sync source files (excluding node_modules)
run(f"rsync -avz --exclude 'node_modules' --exclude '.git' {LOCAL_DIR}/ {BUNNY}:{REMOTE_DIR}/")

# 2. Rebuild and Restart on Bunny
print("🔨 Rebuilding sidebar container on Bunny...")
# Sidebar serves at root via proxy, named 'sidebar'
cmd = (
    f"ssh {BUNNY} 'cd {REMOTE_DIR} && "
    f"docker build -t willow-sidebar . && "
    f"docker stop sidebar || true && "
    f"docker rm sidebar || true && "
    f"docker run -d --name sidebar "
    f"--network willow_willow-network "
    f"willow-sidebar'"
)
run(cmd)

print("✅ Mission Control deployed at http://bunny/")
