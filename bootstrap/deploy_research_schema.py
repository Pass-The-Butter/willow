#!/usr/bin/env python3
"""
Deploy Deep Research Agent Schema to AuraDB
Creates: ResearchTask, Source, Claim, ResearchReport nodes and indexes
"""

import os
from neo4j import GraphDatabase
from dotenv import load_dotenv

load_dotenv()

NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")

SCHEMA_CYPHER = """
// ============================================
// DEEP RESEARCH AGENT SCHEMA
// ============================================

// Constraints for unique IDs
CREATE CONSTRAINT research_task_id IF NOT EXISTS
FOR (rt:ResearchTask) REQUIRE rt.id IS UNIQUE;

CREATE CONSTRAINT source_id IF NOT EXISTS
FOR (s:Source) REQUIRE s.id IS UNIQUE;

CREATE CONSTRAINT claim_id IF NOT EXISTS
FOR (c:Claim) REQUIRE c.id IS UNIQUE;

CREATE CONSTRAINT research_report_id IF NOT EXISTS
FOR (rr:ResearchReport) REQUIRE rr.id IS UNIQUE;

// Indexes for common queries
CREATE INDEX research_task_status IF NOT EXISTS
FOR (rt:ResearchTask) ON (rt.status);

CREATE INDEX research_task_topic IF NOT EXISTS
FOR (rt:ResearchTask) ON (rt.topic);

CREATE INDEX source_type IF NOT EXISTS
FOR (s:Source) ON (s.type);

CREATE INDEX claim_category IF NOT EXISTS
FOR (c:Claim) ON (c.category);
"""

def deploy_schema():
    """Deploy the research agent schema to AuraDB"""
    print("=" * 60)
    print("📊 DEPLOYING DEEP RESEARCH AGENT SCHEMA")
    print("=" * 60)
    
    if not all([NEO4J_URI, NEO4J_PASSWORD]):
        print("❌ Missing NEO4J_URI or NEO4J_PASSWORD in .env")
        return False
    
    print(f"\n📍 Connecting to: {NEO4J_URI[:40]}...")
    
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
    
    try:
        with driver.session() as session:
            # Deploy constraints and indexes
            for statement in SCHEMA_CYPHER.strip().split(';'):
                statement = statement.strip()
                if statement and not statement.startswith('//'):
                    print(f"\n▶ Executing: {statement[:60]}...")
                    try:
                        session.run(statement)
                        print("  ✅ Done")
                    except Exception as e:
                        if "already exists" in str(e).lower():
                            print("  ⚠️  Already exists (skipping)")
                        else:
                            print(f"  ❌ Error: {e}")
            
            # Create sample ResearchTask for testing
            print("\n📝 Creating sample ResearchTask node...")
            session.run("""
                MERGE (rt:ResearchTask {id: 'sample-research-001'})
                SET rt.topic = 'AI Agent Memory Architectures',
                    rt.requested_by = 'System',
                    rt.requested_at = datetime(),
                    rt.status = 'sample',
                    rt.description = 'Sample task for testing schema'
                RETURN rt
            """)
            print("  ✅ Sample ResearchTask created")
            
            # Verify schema
            print("\n🔍 Verifying schema...")
            result = session.run("""
                CALL db.constraints() YIELD name
                WHERE name CONTAINS 'research' OR name CONTAINS 'source' 
                   OR name CONTAINS 'claim' OR name CONTAINS 'report'
                RETURN name
            """)
            constraints = [r['name'] for r in result]
            print(f"  ✅ Constraints: {len(constraints)}")
            for c in constraints:
                print(f"     - {c}")
            
            result = session.run("""
                CALL db.indexes() YIELD name
                WHERE name CONTAINS 'research' OR name CONTAINS 'source' 
                   OR name CONTAINS 'claim' OR name CONTAINS 'report'
                RETURN name
            """)
            indexes = [r['name'] for r in result]
            print(f"  ✅ Indexes: {len(indexes)}")
            for i in indexes:
                print(f"     - {i}")
            
            print("\n" + "=" * 60)
            print("✅ DEEP RESEARCH AGENT SCHEMA DEPLOYED SUCCESSFULLY")
            print("=" * 60)
            return True
            
    except Exception as e:
        print(f"\n❌ Failed: {e}")
        return False
    finally:
        driver.close()


if __name__ == "__main__":
    deploy_schema()
