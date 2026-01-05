#!/usr/bin/env python3
"""
Willow Linear Sync (The Architect)
Wipes the board and reconstructs it with proper hierarchy (Phases -> Projects).
"""

import os
import re
import sys
import requests
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

LINEAR_API_KEY = os.getenv("LINEAR_API_KEY")
LINEAR_API_URL = "https://api.linear.app/graphql"

if not LINEAR_API_KEY:
    print("❌ Error: LINEAR_API_KEY not found in .env")
    sys.exit(1)

def gql_request(query, variables=None):
    headers = {"Content-Type": "application/json", "Authorization": LINEAR_API_KEY}
    response = requests.post(LINEAR_API_URL, json={"query": query, "variables": variables}, headers=headers)
    if response.status_code != 200:
        print(f"❌ API Error: {response.text}")
        return None
    return response.json()

def get_team():
    query = """
    query {
      teams {
        nodes {
          id
          name
        }
      }
    }
    """
    res = gql_request(query)
    teams = res.get('data', {}).get('teams', {}).get('nodes', [])
    if not teams:
        return None
    # Prefer "Willow", else first
    willow = next((t for t in teams if 'Willow' in t['name']), teams[0])
    return willow

def get_all_issues(team_id):
    query = """
    query Issues($teamId: ID!) {
      issues(first: 250, filter: { team: { id: { eq: $teamId } } }) {
        nodes {
          id
          title
        }
      }
    }
    """
    res = gql_request(query, {"teamId": team_id})
    return res.get('data', {}).get('issues', {}).get('nodes', [])

def get_all_projects(team_id):
    # Fetch all projects, we will filter by team in Python to be safe/avoid API schema issues
    query = """
    query Projects {
      projects(first: 100) {
        nodes {
          id
          name
          teams {
            nodes {
              id
            }
          }
        }
      }
    }
    """
    res = gql_request(query)
    all_projects = res.get('data', {}).get('projects', {}).get('nodes', [])
    
    # Filter by team_id
    team_projects = []
    for p in all_projects:
        t_nodes = p.get('teams', {}).get('nodes', [])
        for t in t_nodes:
            if t['id'] == team_id:
                team_projects.append(p)
                break
    return team_projects

def delete_issue(issue_id):
    query = """
    mutation IssueDelete($id: String!) {
      issueDelete(id: $id) {
        success
      }
    }
    """
    gql_request(query, {"id": issue_id})

def delete_project(project_id):
    query = """
    mutation ProjectDelete($id: String!) {
      projectDelete(id: $id) {
        success
      }
    }
    """
    gql_request(query, {"id": project_id})

def create_project(team_id, name, description="Imported from Willow task.md"):
    query = """
    mutation ProjectCreate($teamId: String!, $name: String!, $description: String) {
      projectCreate(input: { teamIds: [$teamId], name: $name, description: $description }) {
        success
        project {
          id
          name
        }
      }
    }
    """
    res = gql_request(query, {"teamId": team_id, "name": name, "description": description})
    return res.get('data', {}).get('projectCreate', {}).get('project') 

def get_workflow_states(team_id):
    query = """
    query States($teamId: ID!) {
      workflowStates(filter: { team: { id: { eq: $teamId } } }) {
        nodes {
          id
          name
          type
        }
      }
    }
    """
    res = gql_request(query, {"teamId": team_id})
    return res.get('data', {}).get('workflowStates', {}).get('nodes', [])

def create_issue_full(team_id, title, project_id=None, state_id=None):
    query = """
    mutation IssueCreate($teamId: String!, $title: String!, $projectId: String, $stateId: String) {
      issueCreate(input: {
        teamId: $teamId
        title: $title
        projectId: $projectId
        stateId: $stateId
      }) {
        success
        issue {
          id
          title
          url
        }
      }
    }
    """
    variables = {
        "teamId": team_id,
        "title": title,
        "projectId": project_id,
    }
    if state_id:
        variables["stateId"] = state_id
        
    res = gql_request(query, variables)
    return res.get('data', {}).get('issueCreate', {}).get('issue')

def parse_md_tasks(md_file):
    tasks = []
    if not os.path.exists(md_file):
        return tasks
        
    with open(md_file, 'r') as f:
        current_phase_name = None
        
        for line in f:
            line_stripped = line.strip()
            
            # Detect Phase 
            phase_match = re.search(r'^-\s*\[([ /x])\]\s*\*\*(.+?)\*\*', line_stripped)
            if phase_match:
                current_phase_name = phase_match.group(2).strip()
                continue # We don't make an issue for the Phase, we make a PROJECT

            # Detect Item
            item_match = re.search(r'^\s*-\s*\[([ /x])\]\s*(.+?)(?:\s*<!--.*-->)?$', line)
            if item_match and not phase_match:
                status_char = item_match.group(1)
                title = item_match.group(2).strip()
                
                status = "Todo" # Linear default
                if status_char == "/": status = "In Progress"
                elif status_char == "x": status = "Done"
                
                tasks.append({
                    'title': title, 
                    'status': status, 
                    'phase': current_phase_name
                })
    return tasks

def main():
    print("🏗️  Willow Linear 'Architect' Protocol Initiated...")
    
    # 0. SETUP
    team = get_team()
    if not team:
        print("❌ Error: No Linear team found.")
        return
    print(f"   Target Team: {team['name']}")
    
    # Get States Mapping
    print("   Mapping Workflow States...")
    states = get_workflow_states(team['id'])
    
    # Map 'To Do', 'In Progress', 'Done' to IDs
    # Linear standard names: "Todo" "In Progress" "Done"
    state_map = {}
    for s in states:
        state_map[s['name']] = s['id']
        # Also map type for fallbacks
        if s['type'] == 'unstarted': state_map['Todo'] = s['id']
        elif s['type'] == 'started' and 'In Progress' not in state_map: state_map['In Progress'] = s['id']
        elif s['type'] == 'completed' and 'Done' not in state_map: state_map['Done'] = s['id']
        elif s['type'] == 'canceled': state_map['Canceled'] = s['id']

    # 1. NUKE EVERYTHING
    print("⚠️  CLEAN SLATE PROTOCOL: Deleting all existing projects and issues...")
    
    # Delete Issues
    issues = get_all_issues(team['id'])
    print(f"   Found {len(issues)} issues to delete.")
    for i, issue in enumerate(issues):
        print(f"   [{i+1}/{len(issues)}] Deleting {issue['title']}...")
        delete_issue(issue['id'])
        
    # Delete Projects
    projects = get_all_projects(team['id'])
    print(f"   Found {len(projects)} projects to delete.")
    for i, proj in enumerate(projects):
        print(f"   [{i+1}/{len(projects)}] Deleting Project {proj['name']}...")
        delete_project(proj['id'])
        
    print("✨ Linear Board Cleared.")

    # 2. PARSE TASKS
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
    task_file = os.path.join(repo_root, 'task.md')
    tasks = parse_md_tasks(task_file)
    print(f"📖 Parsed {len(tasks)} tasks.")

    # 3. RECONSTRUCT
    # Cache created projects: name -> id
    created_projects = {}
    
    count = 0
    for t in tasks:
        phase = t['phase']
        
        # Create Project if new
        if phase and phase not in created_projects:
            print(f"🏛️  Creating Project: {phase}")
            proj = create_project(team['id'], phase)
            if proj:
                created_projects[phase] = proj['id']
            else:
                print(f"   ❌ Failed to create project: {phase}")
                
        # Create Issue
        proj_id = created_projects.get(phase)
        status_id = state_map.get(t['status']) 
        
        # Fallback for status "Todo" vs "To Do" mismatch
        if not status_id and t['status'] == "Todo": status_id = state_map.get("To Do")
        
        print(f"   🧱 [{t['status']}] {t['title']}")
        issue = create_issue_full(team['id'], t['title'], proj_id, status_id)
        if issue:
            count += 1
            
    print(f"🎉 Protocol Complete. {count} issues created across {len(created_projects)} projects.")

if __name__ == "__main__":
    main()
