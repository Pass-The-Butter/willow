#!/usr/bin/env python3
"""
Add source provenance to Decisions in the Brain.

This script links Decision nodes to their source documentation,
making the knowledge graph traceable and auditable.
"""

import os
from neo4j import GraphDatabase
import certifi
from dotenv import load_dotenv

# Load environment
load_dotenv()

# Configuration
NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")


def get_driver():
    """Create Neo4j driver with SSL."""
    os.environ['SSL_CERT_FILE'] = certifi.where()
    return GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))


def add_provenance_to_decisions(driver):
    """Add source_file to decisions based on their content/phase."""
    
    mappings = [
        # Task management decisions -> README.md
        {
            'pattern': 'roadmap as graph nodes',
            'source_file': 'README.md',
            'source_anchor': 'Task Management Architecture'
        },
        {
            'pattern': 'Dual kanban',
            'source_file': 'README.md',
            'source_anchor': 'Task Management Architecture'
        },
        {
            'pattern': 'Link Tasks to Decisions',
            'source_file': 'README.md',
            'source_anchor': 'Task Management Architecture'
        },
        # Jira integration -> MISSION_CONTROL.md
        {
            'pattern': 'Jira integration credentials',
            'source_file': 'MISSION_CONTROL.md',
            'source_anchor': 'Integration Points'
        },
        # Ontology decisions -> docs/POPULATION_SCHEMA_SPEC.md
        {
            'pattern': 'Pet defined as Insured Asset',
            'source_file': 'docs/POPULATION_SCHEMA_SPEC.md',
            'source_anchor': 'Ontology Design'
        },
        {
            'pattern': 'Policy node',
            'source_file': 'docs/POPULATION_SCHEMA_SPEC.md',
            'source_anchor': 'Schema Design'
        },
    ]
    
    updated_count = 0
    
    with driver.session() as session:
        # First, handle decisions with clear text patterns
        for mapping in mappings:
            result = session.run("""
                MATCH (d:Decision)
                WHERE d.text CONTAINS $pattern
                  AND d.source_file IS NULL
                SET d.source_file = $source_file,
                    d.source_anchor = $source_anchor,
                    d.provenance_added_at = datetime()
                RETURN count(d) as updated
            """, 
            pattern=mapping['pattern'],
            source_file=mapping['source_file'],
            source_anchor=mapping['source_anchor'])
            
            record = result.single()
            if record and record['updated'] > 0:
                count = record['updated']
                updated_count += count
                print(f"  ✅ Added provenance to {count} decision(s) matching '{mapping['pattern'][:30]}...'")
        
        # Handle decisions without text (likely need cleanup)
        result = session.run("""
            MATCH (d:Decision)
            WHERE d.text IS NULL
              AND d.rationale IS NULL
            RETURN count(d) as empty_decisions
        """)
        record = result.single()
        if record and record['empty_decisions'] > 0:
            count = record['empty_decisions']
            print(f"  ⚠️  Found {count} empty Decision node(s) (no text or rationale)")
            print("     Consider removing these with: MATCH (d:Decision) WHERE d.text IS NULL AND d.rationale IS NULL DETACH DELETE d")
        
        # Handle decisions by phase
        phase_mappings = {
            'ontology': 'docs/POPULATION_SCHEMA_SPEC.md',
            'infrastructure': 'MISSION_CONTROL.md',
            'architecture': 'README.md',
            'bootstrap': 'BIOS.md'
        }
        
        for phase, source_file in phase_mappings.items():
            result = session.run("""
                MATCH (d:Decision)
                WHERE d.phase = $phase
                  AND d.source_file IS NULL
                  AND d.text IS NOT NULL
                SET d.source_file = $source_file,
                    d.provenance_added_at = datetime()
                RETURN count(d) as updated
            """,
            phase=phase,
            source_file=source_file)
            
            record = result.single()
            if record and record['updated'] > 0:
                count = record['updated']
                updated_count += count
                print(f"  ✅ Added provenance to {count} decision(s) in phase '{phase}'")
    
    return updated_count


def clean_empty_decisions(driver):
    """Remove Decision nodes with no meaningful content."""
    with driver.session() as session:
        result = session.run("""
            MATCH (d:Decision)
            WHERE d.text IS NULL
              AND d.rationale IS NULL
            DETACH DELETE d
            RETURN count(d) as deleted
        """)
        
        record = result.single()
        if record and record['deleted'] > 0:
            count = record['deleted']
            print(f"  ✅ Removed {count} empty Decision node(s)")
            return count
    return 0


def main():
    print("📝 Adding Source Provenance to Decisions")
    print("=" * 70)
    
    driver = get_driver()
    
    try:
        print("\n[1/2] Mapping decisions to source documents...")
        updated = add_provenance_to_decisions(driver)
        print(f"\nUpdated {updated} decision(s) with source provenance")
        
        print("\n[2/2] Cleaning up empty decisions...")
        deleted = clean_empty_decisions(driver)
        if deleted > 0:
            print(f"Removed {deleted} empty decision(s)")
        else:
            print("No empty decisions to remove")
        
        print("\n" + "=" * 70)
        print("✅ Provenance update complete!")
        print("\nRun 'python3 core/skills/detect_drift.py' to verify")
        
    finally:
        driver.close()


if __name__ == "__main__":
    main()
