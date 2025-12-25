
import os
import json
import certifi
from neo4j import GraphDatabase
from datetime import datetime

# Load .env manually to ensure we get the latest
env_vars = {}
try:
    with open('.env') as f:
        for line in f:
            if '=' in line and not line.strip().startswith('#'):
                k, v = line.strip().split('=', 1)
                env_vars[k] = v.strip()
except:
    pass

NEO4J_URI = env_vars.get('NEO4J_URI')
NEO4J_USER = env_vars.get('NEO4J_USER')
NEO4J_PASSWORD = env_vars.get('NEO4J_PASSWORD')

os.environ['SSL_CERT_FILE'] = certifi.where()

BACKUP_DIR = "backups"
TIMESTAMP = datetime.now().strftime("%Y%m%d_%H%M%S")
SNAPSHOT_DIR = f"{BACKUP_DIR}/snapshot_{TIMESTAMP}"


# Custom JSON Encoder for Neo4j types
class Neo4jEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, 'isoformat'):
            return obj.isoformat()
        return super().default(obj)

def backup_brain():
    print(f"🧠 Starting Brain Backup to {SNAPSHOT_DIR}...")
    
    if not os.path.exists(SNAPSHOT_DIR):
        os.makedirs(SNAPSHOT_DIR)
        
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
    
    try:
        with driver.session() as session:
            # 1. Backup Nodes
            print("   Exporting Nodes...")
            result = session.run("MATCH (n) RETURN n")
            with open(f"{SNAPSHOT_DIR}/nodes.jsonl", "w") as f:
                count = 0
                for record in result:
                    node = record['n']
                    # Serialize node with labels and properties
                    data = {
                        "id": node.element_id, # AuraDB uses string IDs
                        "labels": list(node.labels),
                        "properties": dict(node)
                    }
                    f.write(json.dumps(data, cls=Neo4jEncoder) + "\n")
                    count += 1
            print(f"   ✅ Saved {count} nodes.")

            # 2. Backup Relationships
            print("   Exporting Relationships...")
            # We explicitly return start/end identifiers. 
            # In neo4j 5+, elementId() works.
            result = session.run("""
                MATCH (a)-[r]->(b) 
                RETURN elementId(a) as start_id, 
                       elementId(b) as end_id, 
                       type(r) as type, 
                       properties(r) as props
            """)
            with open(f"{SNAPSHOT_DIR}/relationships.jsonl", "w") as f:
                count = 0
                for record in result:
                    data = {
                        "start_node": record['start_id'],
                        "end_node": record['end_id'],
                        "type": record['type'],
                        "properties": record['props']
                    }
                    f.write(json.dumps(data, cls=Neo4jEncoder) + "\n")
                    count += 1
            print(f"   ✅ Saved {count} relationships.")
            
    except Exception as e:
        print(f"❌ Backup Failed: {e}")
    finally:
        driver.close()
        
    print(f"🏁 Backup Complete. Location: {os.path.abspath(SNAPSHOT_DIR)}")

if __name__ == "__main__":
    backup_brain()
