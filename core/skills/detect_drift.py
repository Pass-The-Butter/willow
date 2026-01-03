"""
Willow Skill: Detect Drift
==========================
The first self-diagnostic capability for Willow.

This skill compares the state of the repository (markdown docs, code files)
against the knowledge stored in the Brain (AuraDB Neo4j). It detects:

1. Facts in graph with no corresponding source in repo (orphaned nodes)
2. Content in repo not reflected in graph (missing nodes)
3. Mismatches where both exist but content has diverged

This is the foundational capability for the Memory Bus architecture.
It proves the drift problem exists before we build sync solutions.

HISTORY:
--------
2026-01-03: Created by Willow PM (Ontology) based on Architecture Focus 2026.
            This represents Willow's FIRST autonomous self-improvement based on
            its own research into the sync problem between Semantic Memory (graph)
            and Procedural Memory (code/docs).

ARCHITECTURE CONTEXT:
--------------------
From Willow_Architecture_Focus_2026.pdf:
- Pain point: KG (semantic) drifting from docs/code (procedural)
- Solution: Event -> Normalize -> Decide -> Project pattern
- This skill is the "Drift Scanner" described in Section 7

The drift detector is the prerequisite for all sync capabilities.
You cannot fix drift without first detecting it.

Author: Willow Project Manager (Ontology Domain)
"""

import os
import re
import hashlib
from pathlib import Path
from typing import Optional, List, Dict, Any
from datetime import datetime
from neo4j import GraphDatabase
import certifi
from dotenv import load_dotenv

# Load environment first
load_dotenv()

# Configuration
NEO4J_URI = os.getenv("NEO4J_URI", "neo4j+s://e59298d2.databases.neo4j.io")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")

# Repository root (relative to this file's location)
REPO_ROOT = Path(__file__).parent.parent.parent

# Key documents to track for drift detection
TRACKED_DOCUMENTS = [
    "BIOS.md",
    "README.md",
    "MISSION_CONTROL.md",
    "docs/ORGANOGRAM_VISION.md",
    "docs/POPULATION_SCHEMA_SPEC.md",
    "docs/PROJECT_MANAGER_AGENT.md",
    "docs/INSURANCE_FACTORY_VISION.md",
    "docs/RANDOM_IDEAS.md",
]


def extract_markdown_anchors(filepath: Path) -> List[Dict[str, Any]]:
    """
    Extract headings from a markdown file as stable anchors.

    Each heading becomes a potential "fact source" that should have
    corresponding knowledge in the Brain.

    Returns list of dicts with:
    - anchor: The heading text (normalized for comparison)
    - level: Heading level (1-6)
    - line_number: Where it appears in the file
    - content_hash: Hash of content under this heading (for drift detection)
    """
    anchors = []

    if not filepath.exists():
        return anchors

    try:
        content = filepath.read_text(encoding='utf-8')
        lines = content.split('\n')

        current_heading = None
        current_content = []
        current_line = 0

        for i, line in enumerate(lines, 1):
            # Match markdown headings
            heading_match = re.match(r'^(#{1,6})\s+(.+)$', line)

            if heading_match:
                # Save previous heading's content
                if current_heading:
                    content_text = '\n'.join(current_content).strip()
                    content_hash = hashlib.md5(content_text.encode()).hexdigest()[:8]
                    anchors.append({
                        'anchor': current_heading,
                        'level': current_level,
                        'line_number': current_line,
                        'content_hash': content_hash,
                        'content_preview': content_text[:100] + '...' if len(content_text) > 100 else content_text
                    })

                # Start new heading
                current_level = len(heading_match.group(1))
                current_heading = heading_match.group(2).strip()
                current_line = i
                current_content = []
            elif current_heading:
                current_content.append(line)

        # Don't forget the last heading
        if current_heading:
            content_text = '\n'.join(current_content).strip()
            content_hash = hashlib.md5(content_text.encode()).hexdigest()[:8]
            anchors.append({
                'anchor': current_heading,
                'level': current_level,
                'line_number': current_line,
                'content_hash': content_hash,
                'content_preview': content_text[:100] + '...' if len(content_text) > 100 else content_text
            })

    except Exception as e:
        print(f"Error reading {filepath}: {e}")

    return anchors


def query_brain_decisions() -> List[Dict[str, Any]]:
    """
    Query all Decision nodes from the Brain.

    Decisions are the primary way knowledge is captured in the graph.
    They should correspond to content in documentation.
    """
    os.environ['SSL_CERT_FILE'] = certifi.where()
    os.environ['REQUESTS_CA_BUNDLE'] = certifi.where()

    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

    decisions = []

    try:
        with driver.session() as session:
            result = session.run("""
                MATCH (d:Decision)
                OPTIONAL MATCH (d)-[:SOURCE_FROM]->(source)
                RETURN d.text as text,
                       d.rationale as rationale,
                       d.phase as phase,
                       d.made_at as made_at,
                       d.source_file as source_file,
                       d.source_anchor as source_anchor,
                       labels(source) as source_labels
            """)

            for record in result:
                decisions.append({
                    'text': record['text'],
                    'rationale': record['rationale'],
                    'phase': record['phase'],
                    'made_at': str(record['made_at']) if record['made_at'] else None,
                    'source_file': record['source_file'],
                    'source_anchor': record['source_anchor'],
                    'has_provenance': bool(record['source_file'] or record['source_anchor'])
                })
    finally:
        driver.close()

    return decisions


def query_brain_skills() -> List[Dict[str, Any]]:
    """
    Query all Skill nodes and check if their code_path exists.
    """
    os.environ['SSL_CERT_FILE'] = certifi.where()

    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

    skills = []

    try:
        with driver.session() as session:
            result = session.run("""
                MATCH (s:Skill)
                RETURN s.name as name,
                       s.code_path as code_path,
                       s.description as description,
                       s.language as language
            """)

            for record in result:
                code_path = record['code_path']
                file_exists = False

                if code_path:
                    # Normalize path (remove leading slash if present)
                    normalized_path = code_path.lstrip('/')
                    full_path = REPO_ROOT / normalized_path
                    file_exists = full_path.exists()

                skills.append({
                    'name': record['name'],
                    'code_path': code_path,
                    'description': record['description'],
                    'language': record['language'],
                    'file_exists': file_exists
                })
    finally:
        driver.close()

    return skills


def query_brain_components() -> List[Dict[str, Any]]:
    """
    Query Component nodes and check if their paths exist.
    """
    os.environ['SSL_CERT_FILE'] = certifi.where()

    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

    components = []

    try:
        with driver.session() as session:
            result = session.run("""
                MATCH (c:Component)
                WHERE c.path IS NOT NULL OR c.location IS NOT NULL
                RETURN c.name as name,
                       c.path as path,
                       c.location as location,
                       c.description as description
            """)

            for record in result:
                path = record['path'] or record['location']
                path_exists = False

                if path:
                    normalized_path = path.lstrip('/')
                    full_path = REPO_ROOT / normalized_path
                    path_exists = full_path.exists()

                components.append({
                    'name': record['name'],
                    'path': path,
                    'description': record['description'],
                    'path_exists': path_exists
                })
    finally:
        driver.close()

    return components


def find_undocumented_skills() -> List[Dict[str, Any]]:
    """
    Find Python files in core/skills that are NOT registered in the Brain.
    """
    os.environ['SSL_CERT_FILE'] = certifi.where()

    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

    # Get all skills from Brain
    brain_skills = set()
    try:
        with driver.session() as session:
            result = session.run("MATCH (s:Skill) RETURN s.name as name")
            for record in result:
                brain_skills.add(record['name'])
    finally:
        driver.close()

    # Scan skills directory
    skills_dir = REPO_ROOT / 'core' / 'skills'
    undocumented = []

    if skills_dir.exists():
        for py_file in skills_dir.glob('*.py'):
            if py_file.name.startswith('__'):
                continue

            skill_name = py_file.stem
            if skill_name not in brain_skills:
                undocumented.append({
                    'name': skill_name,
                    'file': str(py_file.relative_to(REPO_ROOT)),
                    'reason': 'File exists but no Skill node in Brain'
                })

    return undocumented


def execute(
    verbose: bool = False,
    check_decisions: bool = True,
    check_skills: bool = True,
    check_components: bool = True,
    check_documents: bool = True
) -> Dict[str, Any]:
    """
    Execute the drift detection scan.

    Args:
        verbose: Include detailed information in output
        check_decisions: Check Decision nodes for provenance
        check_skills: Check Skill nodes against filesystem
        check_components: Check Component nodes against filesystem
        check_documents: Scan tracked documents for untracked content

    Returns:
        Comprehensive drift report
    """

    report = {
        'timestamp': datetime.now().isoformat(),
        'skill': 'detect_drift',
        'success': True,
        'summary': {},
        'drift_detected': False,
        'details': {}
    }

    issues = []

    # 1. Check Decisions for provenance
    if check_decisions:
        decisions = query_brain_decisions()
        decisions_without_provenance = [d for d in decisions if not d['has_provenance']]

        report['details']['decisions'] = {
            'total': len(decisions),
            'with_provenance': len(decisions) - len(decisions_without_provenance),
            'without_provenance': len(decisions_without_provenance),
            'items_without_provenance': decisions_without_provenance if verbose else [d['text'][:50] for d in decisions_without_provenance]
        }

        if decisions_without_provenance:
            issues.append(f"{len(decisions_without_provenance)} Decision(s) have no source provenance")

    # 2. Check Skills against filesystem
    if check_skills:
        skills = query_brain_skills()
        orphaned_skills = [s for s in skills if s['code_path'] and not s['file_exists']]

        undocumented = find_undocumented_skills()

        report['details']['skills'] = {
            'total_in_brain': len(skills),
            'orphaned': len(orphaned_skills),  # In brain but file missing
            'undocumented': len(undocumented),  # In repo but not in brain
            'orphaned_items': orphaned_skills if verbose else [s['name'] for s in orphaned_skills],
            'undocumented_items': undocumented if verbose else [s['name'] for s in undocumented]
        }

        if orphaned_skills:
            issues.append(f"{len(orphaned_skills)} Skill(s) reference missing files")
        if undocumented:
            issues.append(f"{len(undocumented)} skill file(s) not registered in Brain")

    # 3. Check Components against filesystem
    if check_components:
        components = query_brain_components()
        orphaned_components = [c for c in components if c['path'] and not c['path_exists']]

        report['details']['components'] = {
            'total': len(components),
            'orphaned': len(orphaned_components),
            'orphaned_items': orphaned_components if verbose else [c['name'] for c in orphaned_components]
        }

        if orphaned_components:
            issues.append(f"{len(orphaned_components)} Component(s) reference missing paths")

    # 4. Check tracked documents
    if check_documents:
        doc_report = []
        for doc_path in TRACKED_DOCUMENTS:
            full_path = REPO_ROOT / doc_path
            if full_path.exists():
                anchors = extract_markdown_anchors(full_path)
                doc_report.append({
                    'file': doc_path,
                    'exists': True,
                    'headings_count': len(anchors),
                    'headings': [a['anchor'] for a in anchors] if verbose else None
                })
            else:
                doc_report.append({
                    'file': doc_path,
                    'exists': False,
                    'headings_count': 0
                })
                issues.append(f"Tracked document missing: {doc_path}")

        report['details']['documents'] = {
            'tracked': len(TRACKED_DOCUMENTS),
            'found': len([d for d in doc_report if d['exists']]),
            'missing': len([d for d in doc_report if not d['exists']]),
            'items': doc_report
        }

    # Build summary
    report['drift_detected'] = len(issues) > 0
    report['summary'] = {
        'total_issues': len(issues),
        'issues': issues
    }

    return report


def generate_repair_plan(report: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Given a drift report, generate a repair plan.

    This is the foundation for autonomous self-healing.
    """
    plan = []

    if 'details' not in report:
        return plan

    # Plan for orphaned skills
    if 'skills' in report['details']:
        for skill in report['details']['skills'].get('orphaned_items', []):
            if isinstance(skill, dict):
                plan.append({
                    'type': 'DELETE_NODE',
                    'node_type': 'Skill',
                    'identifier': skill['name'],
                    'reason': f"Code file {skill.get('code_path')} no longer exists",
                    'cypher': f"MATCH (s:Skill {{name: '{skill['name']}'}}) DELETE s"
                })

        for skill in report['details']['skills'].get('undocumented_items', []):
            if isinstance(skill, dict):
                plan.append({
                    'type': 'CREATE_NODE',
                    'node_type': 'Skill',
                    'identifier': skill['name'],
                    'reason': f"File {skill.get('file')} exists but not in Brain",
                    'action': 'Register skill node in Brain with code_path'
                })

    # Plan for decisions without provenance
    if 'decisions' in report['details']:
        for decision in report['details']['decisions'].get('items_without_provenance', []):
            if isinstance(decision, str):
                text = decision[:50]
            elif isinstance(decision, dict) and decision.get('text'):
                text = decision.get('text', '')[:50]
            else:
                text = str(decision)[:50] if decision else 'Unknown'
            plan.append({
                'type': 'UPDATE_NODE',
                'node_type': 'Decision',
                'identifier': text,
                'reason': 'Decision lacks source provenance',
                'action': 'Add source_file and source_anchor properties'
            })

    return plan


def print_report(report: Dict[str, Any]):
    """Pretty print the drift report."""

    print("\n" + "=" * 70)
    print("WILLOW DRIFT DETECTION REPORT")
    print("=" * 70)
    print(f"Timestamp: {report['timestamp']}")
    print(f"Drift Detected: {'YES' if report['drift_detected'] else 'NO'}")
    print()

    if report['summary']['issues']:
        print("ISSUES FOUND:")
        print("-" * 40)
        for issue in report['summary']['issues']:
            print(f"  - {issue}")
        print()

    # Decisions
    if 'decisions' in report.get('details', {}):
        d = report['details']['decisions']
        print(f"DECISIONS: {d['total']} total, {d['without_provenance']} without provenance")

    # Skills
    if 'skills' in report.get('details', {}):
        s = report['details']['skills']
        print(f"SKILLS: {s['total_in_brain']} in Brain, {s['orphaned']} orphaned, {s['undocumented']} undocumented")

        if s['undocumented_items']:
            print("  Undocumented skills (in repo but not Brain):")
            for skill in s['undocumented_items'][:5]:
                name = skill if isinstance(skill, str) else skill.get('name')
                print(f"    - {name}")
            if len(s['undocumented_items']) > 5:
                print(f"    ... and {len(s['undocumented_items']) - 5} more")

    # Components
    if 'components' in report.get('details', {}):
        c = report['details']['components']
        print(f"COMPONENTS: {c['total']} total, {c['orphaned']} orphaned")

    # Documents
    if 'documents' in report.get('details', {}):
        docs = report['details']['documents']
        print(f"DOCUMENTS: {docs['tracked']} tracked, {docs['found']} found, {docs['missing']} missing")

    print()
    print("=" * 70)

    if report['drift_detected']:
        print("ACTION REQUIRED: Run generate_repair_plan() to get remediation steps")
    else:
        print("All systems nominal. Brain and Repo are in sync.")

    print("=" * 70 + "\n")


if __name__ == "__main__":
    print("Running Willow Drift Detection...")
    print("(This is Willow's first self-diagnostic capability!)")
    print()

    report = execute(verbose=True)
    print_report(report)

    if report['drift_detected']:
        print("\nGenerating repair plan...")
        plan = generate_repair_plan(report)
        print(f"Repair plan has {len(plan)} items:")
        for item in plan[:5]:
            print(f"  [{item['type']}] {item['node_type']}: {item['identifier'][:40]}...")
        if len(plan) > 5:
            print(f"  ... and {len(plan) - 5} more")
