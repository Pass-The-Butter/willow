#!/usr/bin/env python3
"""
Willow Repository Sync Skill
Synchronizes the local repository with GitHub origin.
"""

import subprocess
import sys
import os

def run_command(cmd):
    print(f"Executing: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
        return False, result.stderr
    return True, result.stdout

def main():
    print("🚀 [Repo Sync] Starting synchronization...")
    
    # 1. Fetch latest
    success, _ = run_command(["git", "fetch", "origin"])
    if not success: return
    
    # 2. Add all changes
    success, _ = run_command(["git", "add", "."])
    if not success: return
    
    # 3. Commit
    commit_msg = "feat: Implement Deep Research Agent, update population schema, and synchronize repo state"
    success, output = run_command(["git", "commit", "-m", commit_msg])
    if not success:
        if "nothing to commit" in output:
            print("Already in sync.")
        else:
            return
            
    # 4. Push
    success, _ = run_command(["git", "push", "origin", "main"])
    if success:
        print("✅ [Repo Sync] Successfully pushed to origin main.")
    else:
        print("❌ [Repo Sync] Push failed.")

if __name__ == "__main__":
    main()
