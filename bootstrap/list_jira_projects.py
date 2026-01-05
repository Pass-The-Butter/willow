import os
import requests
import base64
from dotenv import load_dotenv

load_dotenv()

JIRA_URL = os.getenv("JIRA_URL")
JIRA_USER = os.getenv("JIRA_USER")
JIRA_TOKEN = os.getenv("JIRA_TOKEN")

def get_auth_header():
    cred = f"{JIRA_USER}:{JIRA_TOKEN}"
    encoded = base64.b64encode(cred.encode("utf-8")).decode("utf-8")
    return {
        "Authorization": f"Basic {encoded}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

def list_projects():
    url = f"{JIRA_URL}/rest/api/3/project"
    response = requests.get(url, headers=get_auth_header())
    if response.status_code == 200:
        projects = response.json()
        print(f"Found {len(projects)} projects:")
        for p in projects:
            print(f" - Name: {p['name']}, Key: {p['key']}, ID: {p['id']}")
    else:
        print(f"Error: {response.status_code} - {response.text}")

if __name__ == "__main__":
    list_projects()
