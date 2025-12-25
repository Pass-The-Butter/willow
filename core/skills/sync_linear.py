import os
import re
import requests
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
    with open(md_file, 'r') as f:
        for line in f:
            # Match unchecked tasks: - [ ] Task Name <!-- id: 123 -->
            match = re.match(r'^\s*-\s*\[\s*\]\s*(.+?)(?:\s*<!--.*-->)?$', line)
            if match:
                tasks.append(match.group(1).strip())
    return tasks

def main():
    if not LINEAR_API_KEY:
        print("Error: LINEAR_API_KEY not found in .env")
        return

    # 1. Get Team ID (Willow or first available)
    teams_data = get_teams()
    teams = teams_data.get('data', {}).get('teams', {}).get('nodes', [])
    if not teams:
        print("Error: No Linear teams found.")
        return
    
    willow_team = next((t for t in teams if 'Willow' in t['name']), teams[0])
    print(f"Syncing to Linear Team: {willow_team['name']} ({willow_team['id']})")

    # 2. Parse Tasks
    task_file = '/Users/peter/.gemini/antigravity/brain/6310b00a-5063-4ce3-93f6-9ee7a0c1539b/task.md'
    if not os.path.exists(task_file):
         print(f"Task file not found: {task_file}")
         return
         
    tasks = parse_tasks(task_file)
    print(f"Found {len(tasks)} pending tasks in task.md")

    # 3. Create Issues
    for t in tasks:
        print(f"Creating issue: {t}...")
        res = create_issue(t, willow_team['id'], description="Imported from Willow Brain task.md")
        if res.get('data', {}).get('issueCreate', {}).get('success'):
            issue = res['data']['issueCreate']['issue']
            print(f"  -> Created {issue['title']} ({issue['url']})")
        else:
            print(f"  -> Failed: {res}")

if __name__ == "__main__":
    main()
