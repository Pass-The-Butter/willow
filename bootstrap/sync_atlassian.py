#!/usr/bin/env python3
"""
Willow Jira Sync (Professional PM Edition)
"The Architect"
Wipes the board and reconstructs it with proper hierarchy (Epics -> Tasks) and Statuses.
"""

import os
import re
import sys
import json
import base64
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

JIRA_URL = os.getenv("JIRA_URL")
JIRA_USER = os.getenv("JIRA_USER")
JIRA_TOKEN = os.getenv("JIRA_TOKEN")
PROJECT_KEY = "WILLOW"

if not JIRA_URL:
    print("❌ Error: JIRA_URL not set.")
    sys.exit(1)

def get_auth_header():
    cred = f"{JIRA_USER}:{JIRA_TOKEN}"
    encoded = base64.b64encode(cred.encode("utf-8")).decode("utf-8")
    return {
        "Authorization": f"Basic {encoded}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

def get_issue_types():
    """Fetch available issue types to find IDs for 'Epic' and 'Task'"""
    url = f"{JIRA_URL}/rest/api/3/issuetype/project?projectId={get_project_id()}"
    # Fallback to global if project specific fails or isn't supported easily
    # Actually simpler: search for the project first to get ID
    return {}

def get_project_id():
    url = f"{JIRA_URL}/rest/api/3/project/{PROJECT_KEY}"
    response = requests.get(url, headers=get_auth_header())
    if response.status_code == 200:
        return response.json()['id']
    return None

def resolve_issue_types(project_id):
    """Get the correct IDs for Epic and Task in this project"""
    # Try project specific
    url = f"{JIRA_URL}/rest/api/3/project/{PROJECT_KEY}"
    response = requests.get(url, headers=get_auth_header())
    
    types = {'Epic': None, 'Task': None}
    
    if response.status_code == 200:
        found_types = response.json().get('issueTypes', [])
        for t in found_types:
            if t['name'] == 'Epic':
                types['Epic'] = t['id']
            elif t['name'] == 'Task':
                types['Task'] = t['id']
                
    # If Task is missing, just grab the first one that isn't Epic? No, rely on defaults.
    return types

def get_all_issues():
    """Fetch ALL existing issues in the project using (Correct) GET Search"""
    url = f"{JIRA_URL}/rest/api/3/search"
    jql = f"project = {PROJECT_KEY}"
    
    issues = []
    start_at = 0
    while True:
        params = {
            "jql": jql,
            "fields": "id,key",
            "maxResults": 100,
            "startAt": start_at
        }
        
        response = requests.get(url, headers=get_auth_header(), params=params)
        
        if response.status_code != 200:
            print(f"❌ Failed to fetch issues: {response.text}")
            break
            
        data = response.json()
        batch = data.get("issues", [])
        if not batch:
            break
            
        issues.extend(batch)
        start_at += len(batch)
        if start_at >= data.get("total", 0):
            break
            
    return issues

def delete_issue(issue_key):
    """Delete an issue by key"""
    url = f"{JIRA_URL}/rest/api/3/issue/{issue_key}"
    response = requests.delete(url, headers=get_auth_header())
    return response.status_code in [204, 200]

def create_issue(title, issue_type_id, parent_key=None, description_text="Imported from Willow task.md", labels=None):
    """Create a new issue in Jira"""
    url = f"{JIRA_URL}/rest/api/3/issue"
    
    description = {
        "type": "doc",
        "version": 1,
        "content": [{"type": "paragraph", "content": [{"type": "text", "text": description_text}]}]
    }
    
    fields = {
        "project": {"key": PROJECT_KEY},
        "summary": title,
        "description": description,
        "issuetype": {"id": issue_type_id}
    }
    
    if parent_key:
        # parent field is used in Team-managed projects for Epic link, and Subtasks
        fields["parent"] = {"key": parent_key}
        
    if labels:
        fields["labels"] = labels
    
    payload = {"fields": fields}
    
    response = requests.post(url, headers=get_auth_header(), json=payload)
    if response.status_code == 201:
        return response.json()
    else:
        # Fallback: Maybe "parent" field isn't supported for this issue type structure (Classic Project)?
        # Or Epic Name is required?
        err = response.text
        if "Epic Name" in err and parent_key is None: # Likely Classic Project Epic
             # Try adding custom field for Epic Name? We don't know the ID.
             # Easier fallback: Create as TASK instead of Epic.
             print(f"  ⚠️  Failed to create Epic '{title}', falling back to standard Task. (Error: {err[:100]}...)")
             # Recursion guard/fallback
             if parent_key is None and issue_type_id: # Assume we tried Epic 
                  # Find Task ID - hacky, we pass it in usually. 
                  # Just retry without specifying ID (let Jira pick default) or use known Task ID if we had one.
                  # For now, just return None so we can log failure.
                  pass
                  
        print(f"  ❌ Failed to create '{title}' (TypeID: {issue_type_id}, Parent: {parent_key}): {response.status_code} - {response.text}")
        return None

def get_transitions(issue_id):
    """Get available transitions for an issue"""
    url = f"{JIRA_URL}/rest/api/3/issue/{issue_id}/transitions"
    response = requests.get(url, headers=get_auth_header())
    if response.status_code == 200:
        return response.json().get("transitions", [])
    return []

def transition_issue(issue_id, target_status):
    """Transition issue to target status name"""
    transitions = get_transitions(issue_id)
    
    target_transition = None
    for t in transitions:
        t_name = t['name'].lower()
        to_status = t['to']['name'].lower()
        target = target_status.lower()
        
        if target in t_name or target in to_status:
            target_transition = t
            break
            
    if not target_transition:
        return False
        
    url = f"{JIRA_URL}/rest/api/3/issue/{issue_id}/transitions"
    payload = {"transition": {"id": target_transition['id']}}
    
    response = requests.post(url, headers=get_auth_header(), json=payload)
    return response.status_code == 204

def parse_md_tasks(md_file):
    """
    Parse tasks. Returns list of dict.
    """
    tasks = []
    if not os.path.exists(md_file):
        return tasks
        
    with open(md_file, 'r') as f:
        current_phase_idx = 0
        
        for line in f:
            line_stripped = line.strip()
            
            # Detect Phase (Bold headers in list items)
            phase_match = re.search(r'^-\s*\[([ /x])\]\s*\*\*(.+?)\*\*', line_stripped)
            if phase_match:
                status_char = phase_match.group(1)
                title = phase_match.group(2).strip()
                current_phase_idx += 1
                
                status = "To Do"
                if status_char == "/": status = "In Progress"
                elif status_char == "x": status = "Done"
                
                tasks.append({
                    'title': title, 
                    'status': status, 
                    'is_phase': True, 
                    'phase_id': current_phase_idx
                })
                continue

            # Detect Items
            item_match = re.search(r'^\s*-\s*\[([ /x])\]\s*(.+?)(?:\s*<!--.*-->)?$', line)
            if item_match and not phase_match:
                status_char = item_match.group(1)
                title = item_match.group(2).strip()
                
                status = "To Do"
                if status_char == "/": status = "In Progress"
                elif status_char == "x": status = "Done"
                
                tasks.append({
                    'title': title, 
                    'status': status, 
                    'is_phase': False,
                    'phase_id': current_phase_idx
                })

    return tasks

def main():
    print(f"🏗️  Willow Jira 'Architect' Protocol Initiated...")
    print(f"   Target: {JIRA_URL} (Project: {PROJECT_KEY})")
    
    # 0. DISCOVER TYPES
    print("🔍 Discovering Project Metadata...")
    proj_id = get_project_id()
    if not proj_id:
        print("❌ Could not get Project ID. Check credentials.")
        return
        
    type_map = resolve_issue_types(proj_id)
    epic_id = type_map.get('Epic')
    task_id = type_map.get('Task')
    print(f"   Types Found: Epic={epic_id}, Task={task_id}")
    
    if not task_id:
        print("❌ Could not find 'Task' issue type. Aborting to be safe.")
        return

    # 1. NUKE EXISTING
    print("WARNING: Deleting ALL issues in project to start fresh (Clean Slate)...")
    issues = get_all_issues()
    print(f"Found {len(issues)} existing issues to delete.")
    
    for i, issue in enumerate(issues):
        print(f"[{i+1}/{len(issues)}] Deleting {issue['key']}...")
        delete_issue(issue['key'])
        
    print("✨ Board cleared.")
    
    # 2. PARSE TASK.MD
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    task_file = os.path.join(repo_root, 'task.md')
    tasks = parse_md_tasks(task_file)
    print(f"📖 Parsed {len(tasks)} tasks.")
    
    # 3. CONSTRUCT HIERARCHY
    current_epic_key = None
    current_epic_phase_id = 0
    created_count = 0
    
    for t in tasks:
        display_title = t['title']
        
        # Determine Type and Parent
        if t['is_phase']:
            # Try to create as Epic
            target_type = epic_id if epic_id else task_id
            parent = None # Epics have no parent
            labels = ["Willow-Phase"]
            
            print(f"🏛️  Creating Epic: [{t['status']}] {display_title}")
            
        else:
            # Create as Task
            target_type = task_id
            # Link to parent if we are in the same phase group
            if t['phase_id'] == current_epic_phase_id and current_epic_key:
                parent = current_epic_key
            else:
                parent = None # Orphan task?
            
            labels = [f"Phase-{t['phase_id']}"]
            print(f"   🧱 Creating Task: [{t['status']}] {display_title} (Parent: {parent})")

        # Execute Create
        result = create_issue(display_title, target_type, parent, labels=labels)
        
        # fallback: if Epic failed (maybe Classic project fields needed), create as Task with no parent
        if t['is_phase'] and not result and epic_id:
            print("   ⚠️  Epic creation failed. Retrying as standard Task...")
            target_type = task_id
            result = create_issue(display_title, target_type, None, labels=labels)

        if result:
            key = result['key']
            issue_id = result['id']
            created_count += 1
            
            # Update Context for children
            if t['is_phase']:
                current_epic_key = key
                current_epic_phase_id = t['phase_id']
            
            # Handle Status
            if t['status'] != "To Do":
                if t['status'] == "In Progress":
                    transition_issue(issue_id, "In Progress")
                elif t['status'] == "Done":
                     if not transition_issue(issue_id, "Done"):
                        transition_issue(issue_id, "In Progress")
                        transition_issue(issue_id, "Done")
                        
    print(f"🎉 Architecture Complete. {created_count} items built.")

if __name__ == "__main__":
    main()
