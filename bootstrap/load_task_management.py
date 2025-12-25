#!/usr/bin/env python3
"""
Load task management schema into AuraDB
Creates Task, Sprint nodes with relationships
"""

from neo4j import GraphDatabase
import certifi
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# AuraDB connection details
URI = os.getenv("NEO4J_URI", "neo4j+s://e59298d2.databases.neo4j.io")
USER = os.getenv("NEO4J_USER", "neo4j")
PASSWORD = os.getenv("NEO4J_PASSWORD")

if not PASSWORD:
    raise ValueError("NEO4J_PASSWORD environment variable not set")

def load_task_schema():
    """Load task management schema into AuraDB"""

    os.environ['SSL_CERT_FILE'] = certifi.where()
    os.environ['REQUESTS_CA_BUNDLE'] = certifi.where()

    driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))

    print("Reading task management schema...")
    # Adjusted path for when script is run from bootstrap/ directory
    schema_path = os.path.join(os.path.dirname(__file__), '../schemas/task-management.cypher')
    with open(schema_path, 'r') as f:
        schema_content = f.read()

    # Split into statements
    statements = []
    current_statement = []

    for line in schema_content.split('\n'):
        line = line.strip()

        # Skip empty lines and comment-only lines
        if not line or line.startswith('//'):
            continue

        # Remove inline comments
        if '//' in line:
            line = line.split('//')[0].strip()

        current_statement.append(line)

        # Check if statement ends with semicolon
        if line.endswith(';'):
            stmt = ' '.join(current_statement).rstrip(';')
            if stmt:
                statements.append(stmt)
            current_statement = []

    # Add last statement if no trailing semicolon
    if current_statement:
        stmt = ' '.join(current_statement)
        if stmt:
            statements.append(stmt)

    print(f"Found {len(statements)} statements to execute")

    # First, add new Decision nodes for task management meta-decisions
    meta_decisions = [
        {
            'text': 'Store roadmap as graph nodes (Tasks, Sprints)',
            'rationale': 'The specification IS the product. Claude can query its own roadmap, making task management introspectable.',
            'suggested_by': 'Peter',
            'phase': 'meta-system'
        },
        {
            'text': 'Dual kanban: GitHub Projects + AuraDB Tasks',
            'rationale': 'GitHub for human agents, AuraDB for Claude. Both stay in sync. Redundancy and appropriate interfaces.',
            'suggested_by': 'Peter',
            'phase': 'meta-system'
        },
        {
            'text': 'Link Tasks to Decisions that motivated them',
            'rationale': 'Traceability from "why" to "what". Every task has a decision lineage.',
            'suggested_by': 'Claude',
            'phase': 'meta-system'
        }
    ]

    print("\nAdding meta-decisions about task management...")
    with driver.session() as session:
        for decision in meta_decisions:
            query = """
            CREATE (d:Decision {
                text: $text,
                rationale: $rationale,
                suggested_by: $suggested_by,
                phase: $phase,
                made_at: datetime(),
                confidence: 'high'
            })
            RETURN d.text as text
            """
            result = session.run(query, decision)
            print(f"  ✓ Created: {result.single()['text'][:60]}...")

    # Execute task schema statements
    print("\nLoading task management schema...")
    with driver.session() as session:
        for i, statement in enumerate(statements, 1):
            try:
                print(f"  Executing statement {i}/{len(statements)}...", end='')
                result = session.run(statement)
                result.consume()
                print(" ✓")
            except Exception as e:
                print(f" ✗ Failed: {str(e)[:100]}")

    # Verify what was created
    print("\nVerifying task management nodes...")
    with driver.session() as session:
        # Count tasks by status
        result = session.run("""
            MATCH (t:Task)
            RETURN t.status as status, count(t) as count
            ORDER BY count DESC
        """)
        print("\nTasks by status:")
        for record in result:
            print(f"  {record['status']}: {record['count']}")

        # Count sprints
        result = session.run("MATCH (s:Sprint) RETURN count(s) as count")
        sprint_count = result.single()['count']
        print(f"\nSprints created: {sprint_count}")

        # Show critical path
        result = session.run("""
            MATCH (t:Task {priority: 'critical'})
            RETURN t.id as id, t.title as title, t.status as status
            ORDER BY t.id
        """)
        print("\nCritical path tasks:")
        for record in result:
            print(f"  [{record['status']}] {record['id']}: {record['title']}")

    driver.close()
    print("\n✓ Task management system loaded!")

if __name__ == "__main__":
    load_task_schema()
