#!/usr/bin/env python3
"""
Load Willow bootstrap schema into AuraDB
"""

from neo4j import GraphDatabase
import certifi
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# AuraDB connection details
URI = os.getenv("NEO4J_URI", "neo4j+s://e59298d2.databases.neo4j.io")
USER = os.getenv("NEO4J_USER", "neo4j")
PASSWORD = os.getenv("NEO4J_PASSWORD")

if not PASSWORD:
    raise ValueError("NEO4J_PASSWORD environment variable not set")

def load_schema(schema_file: str):
    """Load and execute Cypher schema file"""

    # Read schema file
    print(f"Reading schema from {schema_file}...")
    with open(schema_file, 'r') as f:
        schema_content = f.read()

    # Split into individual statements (separated by semicolons)
    # Filter out comments and empty lines
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

    print(f"Found {len(statements)} Cypher statements")

    # Connect to AuraDB
    print(f"Connecting to AuraDB at {URI}...")

    # Set SSL cert file environment variable for Python
    os.environ['SSL_CERT_FILE'] = certifi.where()
    os.environ['REQUESTS_CA_BUNDLE'] = certifi.where()

    driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))

    try:
        with driver.session() as session:
            # Execute each statement
            for i, statement in enumerate(statements, 1):
                try:
                    print(f"Executing statement {i}/{len(statements)}...")
                    result = session.run(statement)
                    result.consume()  # Consume result to ensure execution
                    print(f"  ✓ Statement {i} completed")
                except Exception as e:
                    print(f"  ✗ Statement {i} failed: {e}")
                    # Continue with other statements

        # Verify what was created
        print("\nVerifying schema load...")
        with driver.session() as session:
            result = session.run("MATCH (n) RETURN labels(n)[0] as type, count(n) as count ORDER BY count DESC")
            print("\nNode counts by type:")
            for record in result:
                print(f"  {record['type']}: {record['count']}")

        print("\n✓ Schema loaded successfully!")

    finally:
        driver.close()

if __name__ == "__main__":
    schema_file = "schemas/willow-bootstrap.cypher"
    load_schema(schema_file)
