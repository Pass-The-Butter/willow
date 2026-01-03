from core.clients.graph_client import GraphClient
import os

client = GraphClient(agent_id="test-lister")
results = client.run("""
    MATCH (t:Task)
    OPTIONAL MATCH (t)<-[:HAS_TASK]-(c)
    RETURN t{.*}, labels(c) as parent_labels, c.name as parent_name
    LIMIT 5
""")
for r in results:
    print(r)
client.close()
