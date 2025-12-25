#!/usr/bin/env python3
"""Test all Willow system connections"""
import os
import certifi
import psycopg2
from neo4j import GraphDatabase

os.environ['SSL_CERT_FILE'] = certifi.where()

# Load .env
print("=" * 80)
print("🔍 WILLOW CONNECTION AUDIT")
print("=" * 80)

with open('.env') as f:
    for line in f:
        if '=' in line and not line.startswith('#'):
            key, val = line.strip().split('=', 1)
            os.environ[key] = val

print("\n✅ .env loaded")
print(f"   NEO4J_URI: {os.getenv('NEO4J_URI')[:30]}...")
print(f"   NEO4J_USER: {os.getenv('NEO4J_USER')}")
print(f"   POSTGRES_USER: {os.getenv('POSTGRES_USER')}")
print(f"   POSTGRES_DB: {os.getenv('POSTGRES_DB')}")

# Test Neo4j
print("\n" + "=" * 80)
print("Testing Neo4j (AuraDB - The Brain)...")
print("=" * 80)
try:
    driver = GraphDatabase.driver(
        os.getenv('NEO4J_URI'),
        auth=(os.getenv('NEO4J_USER'), os.getenv('NEO4J_PASSWORD'))
    )
    with driver.session() as session:
        result = session.run("MATCH (p:Project {name: 'Willow'}) RETURN p.name as name")
        record = result.single()
        if record:
            print(f"✅ Neo4j connected!")
            print(f"   Project: {record['name']}")
            
            # Count domains
            result = session.run("MATCH (d:Domain) RETURN count(d) as count")
            count = result.single()['count']
            print(f"   Domains: {count}")
            
            # Count tasks
            result = session.run("MATCH (t:Task) RETURN count(t) as count")
            count = result.single()['count']
            print(f"   Tasks: {count}")
            
            # Count messages
            result = session.run("MATCH (m:Message) WHERE m.read = false RETURN count(m) as count")
            count = result.single()['count']
            print(f"   Unread messages: {count}")
        else:
            print("⚠️  Neo4j connected but no Willow project found")
    driver.close()
except Exception as e:
    print(f"❌ Neo4j connection failed: {e}")

# Test PostgreSQL (Bunny)
print("\n" + "=" * 80)
print("Testing PostgreSQL (Bunny - Population DB)...")
print("=" * 80)
try:
    conn = psycopg2.connect(
        host="bunny",
        port="5432",
        dbname=os.getenv('POSTGRES_DB'),
        user=os.getenv('POSTGRES_USER'),
        password=os.getenv('POSTGRES_PASSWORD')
    )
    cur = conn.cursor()
    
    # Get table counts
    cur.execute("""
        SELECT 'customers' as table_name, count(*) as count FROM customers
        UNION ALL
        SELECT 'pets', count(*) FROM pets
        UNION ALL
        SELECT 'quotes', count(*) FROM quotes
    """)
    
    print("✅ PostgreSQL connected!")
    for row in cur.fetchall():
        print(f"   {row[0]}: {row[1]:,} records")
    
    cur.close()
    conn.close()
except Exception as e:
    print(f"❌ PostgreSQL connection failed: {e}")

# Test SSH connections
print("\n" + "=" * 80)
print("Testing SSH Connections...")
print("=" * 80)
import subprocess

# Test Frank
try:
    result = subprocess.run(
        ["ssh", "peter@frank", "hostname"],
        capture_output=True,
        text=True,
        timeout=5
    )
    if result.returncode == 0:
        print(f"✅ SSH to Frank: {result.stdout.strip()}")
    else:
        print(f"❌ SSH to Frank failed: {result.stderr}")
except Exception as e:
    print(f"❌ SSH to Frank failed: {e}")

# Test Bunny
try:
    result = subprocess.run(
        ["ssh", "bunny@bunny", "hostname"],
        capture_output=True,
        text=True,
        timeout=5
    )
    if result.returncode == 0:
        print(f"✅ SSH to Bunny: {result.stdout.strip()}")
    else:
        print(f"❌ SSH to Bunny failed: {result.stderr}")
except Exception as e:
    print(f"❌ SSH to Bunny failed: {e}")

print("\n" + "=" * 80)
print("✅ CONNECTION AUDIT COMPLETE")
print("=" * 80)
