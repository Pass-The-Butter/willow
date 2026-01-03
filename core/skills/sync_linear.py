import os
import re
import requests
import sys
from dotenv import load_dotenv

load_dotenv()

LINEAR_API_KEY = os.getenv("LINEAR_API_KEY")
LINEAR_API_URL = "https://api.linear.app/graphql"

def get_teams():
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
    headers = {"Content-Type": "application/json", "Authorization": LINEAR_API_KEY}
    response = requests.post(LINEAR_API_URL, json={"query": query}, headers=headers)
    return response.json()

def get_issues(team_id):
    query = """
    query Issues($teamId: ID!) {
      issues(filter: { team: { id: { eq: $teamId } } }) {
        nodes {
          id
          title
        }
      }
    }
    """
    variables = {"teamId": team_id}
    headers = {"Content-Type": "application/json", "Authorization": LINEAR_API_KEY}
    response = requests.post(LINEAR_API_URL, json={"query": query, "variables": variables}, headers=headers)
    return response.json()

def create_issue(title, team_id, description=None):
    query = """
    mutation IssueCreate($title: String!, $teamId: String!, $description: String) {
      issueCreate(input: {
        title: $title
        teamId: $teamId
        description: $description
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
        "title": title,
        "teamId": team_id,
        "description": description
    }
    headers = {"Content-Type": "application/json", "Authorization": LINEAR_API_KEY}
    response = requests.post(LINEAR_API_URL, json={"query": query, "variables": variables}, headers=headers)
    return response.json()

def parse_tasks(md_file):
    tasks = []
    if not os.path.exists(md_file):
        return tasks
        
    with open(md_file, 'r') as f:
        for line in f:
            # Match unchecked tasks: - [ ] Task Name <!-- id: 123 -->
            match = re.search(r'^\s*-\s*\[\s*\]\s*(.+?)(?:\s*<!--.*-->)?$', line)
            if match:
                tasks.append(match.group(1).strip())
    return tasks

def main():
    if not LINEAR_API_KEY:
        print("Error: LINEAR_API_KEY not found in .env")
        return

    # 1. Get Task File Path
    task_file = sys.argv[1] if len(sys.argv) > 1 else '/Volumes/Delila/dev/Willow/task.md'
    print(f"Reading tasks from: {task_file}")

    # 2. Get Team ID (Willow or first available)
    teams_data = get_teams()
    teams = teams_data.get('data', {}).get('teams', {}).get('nodes', [])
    if not teams:
        print("Error: No Linear teams found.")
        return
    
    willow_team = next((t for t in teams if 'Willow' in t['name']), teams[0])
    print(f"Syncing to Linear Team: {willow_team['name']} ({willow_team['id']})")

    # 3. Get Existing Issues to avoid duplicates
    issues_data = get_issues(willow_team['id'])
    existing_titles = {issue['title'] for issue in issues_data.get('data', {}).get('issues', {}).get('nodes', [])}
    print(f"Found {len(existing_titles)} existing issues in Linear.")

    # 4. Parse Tasks
    tasks = parse_tasks(task_file)
    print(f"Found {len(tasks)} pending tasks in local task file.")

    # 5. Create Issues
    created_count = 0
    skipped_count = 0
    for t in tasks:
        if t in existing_titles:
            print(f"Skipping (already exists): {t}")
            skipped_count += 1
            continue
            
        print(f"Creating issue: {t}...")
        res = create_issue(t, willow_team['id'], description="Imported from Willow task.md")
        if res.get('data', {}).get('issueCreate', {}).get('success'):
            issue = res['data']['issueCreate']['issue']
            print(f"  -> Created {issue['title']} ({issue['url']})")
            created_count += 1
        else:
            print(f"  -> Failed: {res}")
            
    print(f"\nSync complete: {created_count} created, {skipped_count} skipped.")

if __name__ == "__main__":
    main()
