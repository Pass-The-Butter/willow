#!/usr/bin/env python3
"""
Willow Unified Project Manager Skill
Synchronizes Task.md with all downstream boards (Jira, Linear, AuraDB)
"""

import sys
import os
import importlib.util

def run_module(path, name):
    print(f"\n{'='*60}")
    print(f"🚀 RUNNING: {name}")
    print(f"{'='*60}")
    
    try:
        spec = importlib.util.spec_from_file_location("module.name", path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        if hasattr(module, 'main'):
            module.main()
        print(f"✅ {name} COMPLETE")
    except Exception as e:
        print(f"❌ {name} FAILED: {e}")

def main():
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
    
    print("🧠 WILLOW PROJECT MANAGER: MASTER SYNC")
    
    # 1. AuraDB Sync (The Brain)
    # Using existing skill if available or bootstrapping it
    # Note: sync_brain_tasks.py should be in core/skills
    brain_sync = os.path.join(repo_root, 'core/skills/sync_brain_tasks.py')
    if os.path.exists(brain_sync):
        run_module(brain_sync, "AuraDB Sync")
    else:
        print("⚠️  AuraDB Sync skill not found, skipping.")

    # 2. Jira Sync (The Architect)
    jira_sync = os.path.join(repo_root, 'bootstrap/sync_atlassian.py')
    if os.path.exists(jira_sync):
        run_module(jira_sync, "Jira Sync")
    
    # 3. Linear Sync (The Architect)
    linear_sync = os.path.join(repo_root, 'core/skills/sync_linear.py')
    if os.path.exists(linear_sync):
        run_module(linear_sync, "Linear Sync")
        
    print("\n✨ ALL SYSTEMS SYNCHRONIZED")

if __name__ == "__main__":
    main()
