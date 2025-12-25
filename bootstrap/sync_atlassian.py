import os
from atlassian import Jira, Confluence
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

JIRA_URL = os.getenv("JIRA_URL")
JIRA_USER = os.getenv("JIRA_USER")
JIRA_TOKEN = os.getenv("JIRA_TOKEN")

if not all([JIRA_URL, JIRA_USER, JIRA_TOKEN]):
    raise ValueError("Jira credentials not found in .env")

def sync_to_atlassian():
    print("Connecting to Atlassian...")
    jira = Jira(
        url=JIRA_URL,
        username=JIRA_USER,
        password=JIRA_TOKEN,
        cloud=True
    )
    
    confluence = Confluence(
        url=JIRA_URL,
        username=JIRA_USER,
        password=JIRA_TOKEN,
        cloud=True
    )

    # 1. Create Jira Epic
    print("Creating/Checking Jira Epic...")
    # Simple check or create logic
    epic_summary = "Willow Infrastructure Bootstrap"
    project_key = "SCRUM" # Assuming SCRUM based on the board URL provided
    
    # Create Epic
    try:
        epic = jira.issue_create(
            fields={
                "project": {"key": project_key},
                "summary": epic_summary,
                "description": "Bootstrapping the Willow autonomous agent system, including Neo4j, Postgres, and Tailscale integration.",
                "issuetype": {"name": "Epic"}
            }
        )
        print(f"✓ Created Epic: {epic['key']}")
        epic_key = epic['key']
    except Exception as e:
        print(f"Could not create Epic (might already exist or wrong project key): {e}")
        epic_key = None

    # 2. Create Tasks linked to Epic
    tasks = [
        {"summary": "Deploy Population Generator to Frank", "description": "Run the remote_generator.py on the Windows node."},
        {"summary": "Integrate Tailscale SSH", "description": "Configure ACLs and SSH trust between Arch-Willow and Frank."},
        {"summary": "Ingest Hello World Data", "description": "Verify data flow from Postgres to Neo4j."}
    ]

    if epic_key:
        for task in tasks:
            try:
                jira.issue_create(
                    fields={
                        "project": {"key": project_key},
                        "summary": task["summary"],
                        "description": task["description"],
                        "issuetype": {"name": "Task"},
                        "parent": {"key": epic_key}
                    }
                )
                print(f"✓ Created Task: {task['summary']}")
            except Exception as e:
                print(f"Failed to create task {task['summary']}: {e}")

    # 3. Sync Documentation to Confluence
    # We need a space key. Let's try 'SCRUM' or 'DS' or find one.
    # For now, we'll list spaces to find a valid one.
    print("Finding Confluence Space...")
    spaces = confluence.get_all_spaces(start=0, limit=5, expand=None)
    space_key = None
    if spaces['results']:
        space_key = spaces['results'][0]['key']
        print(f"Using Space: {space_key}")
    
    if space_key:
        docs_to_sync = [
            {"title": "Captain Willow Certificate", "path": "CAPTAIN_WILLOW.md"},
            {"title": "Tailscale Integration Guide", "path": "infrastructure/tailscale_integration.md"}
        ]

        for doc in docs_to_sync:
            try:
                with open(doc['path'], 'r') as f:
                    content = f.read()
                
                # Convert Markdown to HTML (Basic) or just wrap in macro
                # Confluence API prefers storage format (XHTML). 
                # We'll wrap in a code block or simple pre for now to ensure it uploads, 
                # as full MD-to-XHTML conversion is complex without a library.
                html_content = f"<p><strong>Auto-synced from Willow Repository</strong></p><pre>{content}</pre>"
                
                confluence.create_page(
                    space=space_key,
                    title=doc['title'],
                    body=html_content,
                    parent_id=None,
                    type='page',
                    representation='storage',
                    editor='v2'
                )
                print(f"✓ Created Page: {doc['title']}")
            except Exception as e:
                print(f"Failed to create page {doc['title']} (might already exist): {e}")

if __name__ == "__main__":
    sync_to_atlassian()
