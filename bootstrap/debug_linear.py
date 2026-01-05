import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()
LINEAR_API_KEY = os.getenv("LINEAR_API_KEY")
LINEAR_API_URL = "https://api.linear.app/graphql"

def gql(query, variables=None):
    headers = {"Content-Type": "application/json", "Authorization": LINEAR_API_KEY}
    res = requests.post(LINEAR_API_URL, json={"query": query, "variables": variables}, headers=headers)
    print(f"Status: {res.status_code}")
    print(f"Response: {res.text}")

print("--- TRY 1: Filter by 'teams' ---")
q1 = """
query Projects {
  teams(first: 1) {
    nodes { id name }
  }
}
"""
# Get team ID first
gql(q1)

# Now try filter
# Replace with actual ID after run or just try general structure check
q2 = """
query Projects {
  projects(first: 1, filter: { teams: { id: { eq: "YOUR_TEAM_ID" } } }) {
    nodes { id name }
  }
}
"""
# I don't have the ID handy easily without parsing response.
# I'll just use the one from previous output/assumption or just list all projects and see structure.

print("--- TRY 2: List all and inspect ---")
q3 = """
query {
    projects(first: 2) {
        nodes {
            id
            name
            teams {
                nodes {
                    name
                }
            }
        }
    }
}
"""
gql(q3)
