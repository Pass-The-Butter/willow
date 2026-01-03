from core.clients.graph_client import GraphClient
import os

client = GraphClient(agent_id="inspector")

print("--- DOMAIN RELATIONSHIPS ---")
res = client.run("MATCH (n:Domain)-[r]->(m) RETURN type(r) as rel, labels(m) as target LIMIT 5")
print(res)

print("--- COMPONENT RELATIONSHIPS ---")
res = client.run("MATCH (n:Component)-[r]->(m) RETURN type(r) as rel, labels(m) as target LIMIT 5")
print(res)

print("--- TASK PARENTS ---")
res = client.run("MATCH (n:Task)<-[r]-(p) RETURN labels(p) as parent, type(r) as rel LIMIT 5")
print(res)

client.close()
