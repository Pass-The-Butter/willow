#!/usr/bin/env python3
import os
from neo4j import GraphDatabase
import certifi
from dotenv import load_dotenv

load_dotenv()

NEO4J_URI = os.getenv("NEO4J_URI", "neo4j+s://e59298d2.databases.neo4j.io")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")

sidebar_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../domains/sidebar/src/content/docs/operations/kanban.md'))

def generate_kanban_report():
    os.environ['SSL_CERT_FILE'] = certifi.where()
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
    
    with driver.session() as session:
        result = session.run("""
            MATCH (t:Task)
            RETURN t.id as id, t.title as title, t.status as status, t.priority as priority, t.assigned_to as assigned_to
            ORDER BY 
                CASE t.status
                    WHEN 'in_progress' THEN 1
                    WHEN 'todo' THEN 2
                    WHEN 'blocked' THEN 3
                    WHEN 'complete' THEN 4
                    ELSE 5
                END,
                CASE t.priority
                    WHEN 'critical' THEN 1
                    WHEN 'high' THEN 2
                    WHEN 'medium' THEN 3
                    WHEN 'low' THEN 4
                    ELSE 5
                END
        """)
        tasks = list(result)
        
    driver.close()
    
    # Generate Markdown
    md = "---\ntitle: Kanban Board\ndescription: Current project task status from AuraDB\n---\n\n"
    md += "# 📋 Project Kanban Board\n\n"
    md += f"*Last updated: {os.popen('date').read().strip()}*\n\n"
    
    # Group by status
    statuses = ['in_progress', 'todo', 'blocked', 'complete', 'frozen']
    status_labels = {
        'in_progress': '🟡 In Progress',
        'todo': '⚪ To Do',
        'blocked': '🔴 Blocked',
        'complete': '🟢 Complete',
        'frozen': '❄️ Frozen'
    }
    
    for status in statuses:
        status_tasks = [t for t in tasks if t['status'].lower() == status]
        if not status_tasks:
            continue
            
        md += f"## {status_labels[status]}\n\n"
        md += "| ID | Task | Priority | Assignee |\n"
        md += "| :--- | :--- | :--- | :--- |\n"
        for t in status_tasks:
            md += f"| `{t['id']}` | {t['title']} | {t['priority']} | {t['assigned_to']} |\n"
        md += "\n"
        
    os.makedirs(os.path.dirname(sidebar_path), exist_ok=True)
    with open(sidebar_path, 'w') as f:
        f.write(md)
    print(f"Kanban report generated at: {sidebar_path}")

if __name__ == "__main__":
    generate_kanban_report()
