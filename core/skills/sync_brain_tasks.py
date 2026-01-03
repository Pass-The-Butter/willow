#!/usr/bin/env python3
import os
import re
from neo4j import GraphDatabase
import certifi
from dotenv import load_dotenv

load_dotenv()

NEO4J_URI = os.getenv("NEO4J_URI", "neo4j+s://e59298d2.databases.neo4j.io")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")

def parse_markdown_tasks(md_path):
    tasks = []
    if not os.path.exists(md_path):
        return tasks
        
    with open(md_path, 'r') as f:
        content = f.read()
        
    # Match tasks like: - [x] Task Title <!-- id: 123 -->
    # Or: - [/] **Phase 1: Title** <!-- id: 1 -->
    lines = content.split('\n')
    for line in lines:
        match = re.search(r'^\s*-\s*\[([\s/xX])\]\s*(.*?)(?:\s*<!--\s*id:\s*(\d+)\s*-->)?$', line)
        if match:
            status_char = match.group(1).lower()
            title = match.group(2).strip()
            # Remove markdown bolding if present
            title = re.sub(r'^\*\*(.*?)\*\*$', r'\1', title)
            local_id = match.group(3)
            
            status = 'todo'
            if status_char == 'x':
                status = 'complete'
            elif status_char == '/':
                status = 'in_progress'
                
            tasks.append({
                'title': title,
                'status': status,
                'local_id': local_id
            })
    return tasks

def sync_to_brain(tasks):
    os.environ['SSL_CERT_FILE'] = certifi.where()
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
    
    with driver.session() as session:
        for task in tasks:
            print(f"Syncing: {task['title']} ({task['status']})")
            
            # 1. Try to find by title (case insensitive-ish)
            query = """
            MATCH (t:Task)
            WHERE t.title = $title OR t.title CONTAINS $title
            RETURN t.id as id, t.title as actual_title
            LIMIT 1
            """
            result = session.run(query, title=task['title'])
            record = result.single()
            
            if record:
                print(f"  -> Found existing task: {record['id']} ({record['actual_title']})")
                # Update status
                session.run("""
                    MATCH (t:Task {id: $id})
                    SET t.status = $status, t.updated_at = datetime()
                """, id=record['id'], status=task['status'])
            else:
                # 2. Extract WILL-XXX ID if it was in the title or if we can generate one
                # For now, let's just create a new one if it's not "Phase"
                if "Phase" in task['title']:
                    print(f"  -> Skipping Phase node creation for now: {task['title']}")
                    continue
                    
                print(f"  -> Task not found, creating new node...")
                # Generate a temporary ID or use a hash
                import uuid
                new_id = f"WILL-{uuid.uuid4().hex[:4].upper()}"
                
                session.run("""
                    CREATE (t:Task {
                        id: $id,
                        title: $title,
                        status: $status,
                        assigned_to: 'claude',
                        created_at: datetime(),
                        source: 'task.md'
                    })
                """, id=new_id, title=task['title'], status=task['status'])
                print(f"  -> Created {new_id}")
                
    driver.close()

if __name__ == "__main__":
    import sys
    task_file = sys.argv[1] if len(sys.argv) > 1 else '/Volumes/Delila/dev/Willow/task.md'
    print(f"Reading tasks from: {task_file}")
    tasks = parse_markdown_tasks(task_file)
    print(f"Parsed {len(tasks)} tasks.")
    sync_to_brain(tasks)
    print("Sync complete.")
