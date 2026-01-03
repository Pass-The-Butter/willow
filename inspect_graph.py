from core.clients.graph_client import GraphClient
import os

client = GraphClient(agent_id="inspector")
print("--- DOMAINS ---")
res = client.run("MATCH (n:Domain) RETURN keys(n) as k, n{.*} as props LIMIT 1")
print(res)

print("--- COMPONENTS ---")
res = client.run("MATCH (n:Component) RETURN keys(n) as k, n{.*} as props LIMIT 1")
print(res)

print("--- TASKS ---")
res = client.run("MATCH (n:Task) RETURN keys(n) as k, n{.*} as props LIMIT 1")
print(res)

client.close()
