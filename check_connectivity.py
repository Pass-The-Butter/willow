from core.clients.graph_client import GraphClient
import os

client = GraphClient(agent_id="inspector")

print("Checking HAS_TASK count...")
res = client.run("MATCH (c:Component)-[:HAS_TASK]->(t:Task) RETURN count(t) as cnt")
print(res)

print("Checking Task neighbors...")
res = client.run("MATCH (t:Task)-[r]-(n) RETURN type(r), labels(n) LIMIT 5")
print(res)

client.close()
