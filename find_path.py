from core.clients.graph_client import GraphClient
import os

client = GraphClient(agent_id="test-lister")
results = client.run("""
    MATCH (d:Domain)-[:HAS_COMPONENT]->(c:Component)-[:HAS_TASK]->(t:Task)
    RETURN d.name + ' → ' + c.name + ' → ' + t.name as path
    LIMIT 1
""")
if results:
    print(results[0]['path'])
else:
    print("NO_PATH_FOUND")
client.close()
