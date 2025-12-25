import os
import certifi
from neo4j import GraphDatabase
import re

# AuraDB connection details
URI = "neo4j+s://e59298d2.databases.neo4j.io"
USER = "neo4j"
PASSWORD = "c2U7h1mwvmYn2k2cr_Fp9EaUrZaLZdEQ3_Cawt6zvyU"

HANDOFF_FILE = "/Volumes/Delila/dev/Willow/Willow_Persitant_HANDOFF_Memory.md"

def parse_handoff_and_ingest():
    print(f"Reading memory from {HANDOFF_FILE}...")
    with open(HANDOFF_FILE, 'r') as f:
        content = f.read()

    # Connect to AuraDB
    os.environ['SSL_CERT_FILE'] = certifi.where()
    os.environ['REQUESTS_CA_BUNDLE'] = certifi.where()
    driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))

    session_id = "claude-code-handoff-2025-12-21"

    try:
        with driver.session() as session:
            # 1. Create ConversationSession for this handoff
            print("Creating ConversationSession node...")
            session.run("""
                MERGE (s:ConversationSession {session_id: $sid})
                SET s.platform = 'Claude Code',
                    s.started_at = datetime(),
                    s.summary = 'Handoff from Claude Desktop to Claude Code',
                    s.type = 'handoff'
            """, sid=session_id)

            # 2. Extract and create Decision nodes
            # Looking for "## Achitecture Decision: ..." or specific decision blocks if formatted
            # The file format is a bit free-text, so we'll extract key known decisions if strict parsing is hard,
            # or treat the whole file as a 'Memory' artifact.
            
            # Let's store the entire content as a Document node first
            print("Storing Handoff Document...")
            session.run("""
                MERGE (d:Document {path: $path})
                SET d.content = $content,
                    d.type = 'handoff_memory',
                    d.ingested_at = datetime()
                
                WITH d
                MATCH (s:ConversationSession {session_id: $sid})
                MERGE (s)-[:INCLUDES_DOCUMENT]->(d)
            """, path=HANDOFF_FILE, content=content, sid=session_id)

            # 3. Extract Tasks?
            # We could parse "Task 1.1", etc., but maybe just linking the document is enough for now.
            # The prompt asks to "continue to create the agent memory".
            
            print("✓ Memory ingested successfully.")

    finally:
        driver.close()

if __name__ == "__main__":
    parse_handoff_and_ingest()
