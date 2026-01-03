from core.clients.graph_client import GraphClient
import os

client = GraphClient(agent_id="inspector")

print("Checking Population -> Quality Assurance...")
res = client.run("""
    MATCH (d:Domain {name: 'Population'})-[:HAS_COMPONENT]->(c:Component {name: 'Quality Assurance'})
    RETURN d.name, c.name
""")
print(res)

print("Linking Task if needed...")
# We use the Task with title 'Reorganize file structure to match docker-compose'
# And Component 'Quality Assurance'
res = client.run("""
    MATCH (c:Component {name: 'Quality Assurance'})
    MATCH (t:Task {title: 'Reorganize file structure to match docker-compose'})
    MERGE (c)-[:HAS_TASK]->(t)
    RETURN c.name, t.title
""")
print("Linked:", res)

client.close()
