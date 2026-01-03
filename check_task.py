from core.clients.graph_client import GraphClient
import os

client = GraphClient(agent_id="test-lister")
results = client.run("""
    MATCH (t:Task {title: "Deploy Gateway to `bunny` and verify health."})
    OPTIONAL MATCH (d:Domain)-[:HAS_COMPONENT]->(c:Component)-[:HAS_TASK]->(t)
    RETURN t.title, c.name, d.name
""")
for r in results:
    print(r)
client.close()
