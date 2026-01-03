#!/usr/bin/env python3
"""
Execute drift repairs to sync Willow's Brain with the Repo.
"""

import os
import sys
from pathlib import Path
from typing import Dict, Any
from neo4j import GraphDatabase
import certifi
from dotenv import load_dotenv

# Load environment
load_dotenv()

# Configuration
NEO4J_URI = os.getenv("NEO4J_URI", "neo4j+s://e59298d2.databases.neo4j.io")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")
REPO_ROOT = Path(__file__).parent.parent.parent  # Go up from core/skills/ to repo root

def get_driver():
    """Create Neo4j driver with SSL."""
    os.environ['SSL_CERT_FILE'] = certifi.where()
    return GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))


def register_skill(driver, skill_info: Dict[str, Any]) -> bool:
    """Register a skill in the Brain."""
    try:
        with driver.session() as session:
            result = session.run("""
                MERGE (s:Skill {name: $name})
                SET s.code_path = $code_path,
                    s.description = $description,
                    s.language = $language,
                    s.registered_at = datetime(),
                    s.source = 'drift_repair'
                RETURN s.name as name
            """, 
            name=skill_info['name'],
            code_path=skill_info['code_path'],
            description=skill_info['description'],
            language=skill_info['language'])
            
            record = result.single()
            if record:
                print(f"  ✅ Registered skill: {record['name']}")
                return True
    except Exception as e:
        print(f"  ❌ Failed to register {skill_info['name']}: {str(e)}")
        return False
    return False


def delete_orphaned_skill(driver, skill_name: str) -> bool:
    """Delete an orphaned skill node."""
    try:
        with driver.session() as session:
            result = session.run("""
                MATCH (s:Skill {name: $name})
                DETACH DELETE s
                RETURN count(s) as deleted
            """, name=skill_name)
            
            record = result.single()
            if record and record['deleted'] > 0:
                print(f"  ✅ Deleted orphaned skill: {skill_name}")
                return True
    except Exception as e:
        print(f"  ❌ Failed to delete {skill_name}: {str(e)}")
        return False
    return False


def delete_orphaned_component(driver, component_name: str) -> bool:
    """Delete an orphaned component node."""
    try:
        with driver.session() as session:
            result = session.run("""
                MATCH (c:Component {name: $name})
                DETACH DELETE c
                RETURN count(c) as deleted
            """, name=component_name)
            
            record = result.single()
            if record and record['deleted'] > 0:
                print(f"  ✅ Deleted orphaned component: {component_name}")
                return True
    except Exception as e:
        print(f"  ❌ Failed to delete {component_name}: {str(e)}")
        return False
    return False


def scan_skills_directory() -> list:
    """Scan core/skills directory for Python files."""
    skills_dir = REPO_ROOT / "core" / "skills"
    if not skills_dir.exists():
        return []
    
    skills = []
    for py_file in skills_dir.glob("*.py"):
        if py_file.name.startswith("_"):
            continue
            
        skill_name = py_file.stem
        relative_path = f"core/skills/{py_file.name}"
        
        # Try to extract description from file
        description = f"Skill: {skill_name}"
        try:
            with open(py_file, 'r', encoding='utf-8') as f:
                content = f.read()
                # Look for module docstring
                if '"""' in content:
                    start = content.find('"""')
                    end = content.find('"""', start + 3)
                    if end > start:
                        docstring = content[start+3:end].strip()
                        # Get first line as description
                        first_line = docstring.split('\n')[0].strip()
                        if first_line and len(first_line) > 10:
                            description = first_line
                elif "'''" in content:
                    start = content.find("'''")
                    end = content.find("'''", start + 3)
                    if end > start:
                        docstring = content[start+3:end].strip()
                        first_line = docstring.split('\n')[0].strip()
                        if first_line and len(first_line) > 10:
                            description = first_line
        except Exception as e:
            print(f"  Warning: Could not read {py_file.name}: {e}")
        
        skills.append({
            'name': skill_name,
            'code_path': relative_path,
            'description': description,
            'language': 'python'
        })
    
    return skills


def get_registered_skills(driver) -> set:
    """Get set of skill names already in Brain."""
    try:
        with driver.session() as session:
            result = session.run("MATCH (s:Skill) RETURN s.name as name")
            return {record['name'] for record in result}
    except Exception as e:
        print(f"Failed to query registered skills: {e}")
        return set()


def main():
    print("🔧 Executing Willow Drift Repairs")
    print("=" * 70)
    
    driver = get_driver()
    
    try:
        # 1. Delete orphaned skill node
        print("\n[1/4] Removing orphaned Skill node...")
        delete_orphaned_skill(driver, "query_my_tasks")
        
        # 2. Scan and register undocumented skills
        print("\n[2/4] Registering undocumented skills...")
        all_skills = scan_skills_directory()
        registered = get_registered_skills(driver)
        
        undocumented = [s for s in all_skills if s['name'] not in registered]
        print(f"  Found {len(undocumented)} skills to register")
        
        success_count = 0
        for skill in undocumented:
            if register_skill(driver, skill):
                success_count += 1
        
        print(f"  Registered {success_count}/{len(undocumented)} skills")
        
        # 3. Clean up orphaned components
        print("\n[3/4] Checking for orphaned components...")
        # Query for components with missing paths
        with driver.session() as session:
            result = session.run("""
                MATCH (c:Component)
                WHERE c.path IS NOT NULL OR c.location IS NOT NULL
                RETURN c.name as name, coalesce(c.path, c.location) as path
            """)
            
            for record in result:
                component_path = record['path']
                if component_path:
                    full_path = REPO_ROOT / component_path.lstrip('/')
                    if not full_path.exists():
                        print(f"  Found orphaned component: {record['name']}")
                        delete_orphaned_component(driver, record['name'])
        
        # 4. Add provenance to decisions (requires manual mapping)
        print("\n[4/4] Decisions without provenance...")
        with driver.session() as session:
            result = session.run("""
                MATCH (d:Decision)
                WHERE d.source_file IS NULL
                RETURN count(d) as count
            """)
            record = result.single()
            if record:
                count = record['count']
                print(f"  ⚠️  {count} decisions need source provenance")
                print("  This requires manual mapping to documentation")
                print("  (Run 'python3 bootstrap/update_*_context.py' scripts)")
        
        print("\n" + "=" * 70)
        print("✅ Repair execution complete!")
        print("\nRun 'python3 core/skills/detect_drift.py' to verify repairs")
        
    finally:
        driver.close()


if __name__ == "__main__":
    main()
