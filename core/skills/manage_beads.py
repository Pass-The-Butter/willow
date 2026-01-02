"""
Willow Skill: Manage Beads (Task Graph)
Implements 'Beads in the Graph'.
Nodes: Task (The Bead)
Relationships: BLOCKS, SUBTASK_OF
"""

from neo4j import GraphDatabase
import os
import certifi
import uuid
from neo4j import GraphDatabase
import os
import certifi
import uuid
from core.utils.credentials import get_neo4j_auth

# Load credentials securely
NEO4J_URI, NEO4J_AUTH = get_neo4j_auth()

os.environ['SSL_CERT_FILE'] = certifi.where()

def create_bead(title: str, description: str, bead_type: str = "Task", parent_id: str = None) -> dict:
    """
    Create a new Bead (Task or Epic).
    """
    driver = GraphDatabase.driver(NEO4J_URI, auth=NEO4J_AUTH)
    bead_id = str(uuid.uuid4())[:8] # Short ID like Beads
    
    query = """
    CREATE (t:Task {
        id: $bead_id,
        title: $title,
        description: $description,
        type: $bead_type,
        status: 'todo',
        created_at: datetime()
    })
    RETURN t
    """
    
    parent_link = """
    MATCH (child:Task {id: $bead_id}), (parent:Task {id: $parent_id})
    MERGE (child)-[:SUBTASK_OF]->(parent)
    """

    try:
        with driver.session() as session:
            session.run(query, bead_id=bead_id, title=title, description=description, bead_type=bead_type)
            
            if parent_id:
                session.run(parent_link, bead_id=bead_id, parent_id=parent_id)
                
            return {"success": True, "bead_id": bead_id}
    finally:
        driver.close()

def add_dependency(blocker_id: str, blocked_id: str) -> dict:
    """
    Link a blocker to a blocked task.
    (:Task {id: blocker_id})-[:BLOCKS]->(:Task {id: blocked_id})
    """
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
    query = """
    MATCH (blocker:Task {id: $blocker_id})
    MATCH (blocked:Task {id: $blocked_id})
    MERGE (blocker)-[:BLOCKS]->(blocked)
    """
    try:
        with driver.session() as session:
            session.run(query, blocker_id=blocker_id, blocked_id=blocked_id)
            return {"success": True, "message": f"{blocker_id} blocks {blocked_id}"}
    finally:
        driver.close()

def search_ready_beads(limit: int = 5) -> list:
    """
    Find tasks that are in 'todo' status and HAVE NO ACTIVE BLOCKERS.
    This is the core 'Agentic' logic.
    """
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
    query = """
    MATCH (t:Task)
    WHERE t.status = 'todo'
    AND NOT EXISTS {
        MATCH (blocker:Task)-[:BLOCKS]->(t)
        WHERE blocker.status IN ['todo', 'in_progress']
    }
    RETURN t.id as id, t.title as title, t.type as type
    LIMIT $limit
    """
    try:
        with driver.session() as session:
            result = session.run(query, limit=limit)
            return [{"id": r["id"], "title": r["title"], "type": r["type"]} for r in result]
    finally:
        driver.close()
        
def land_the_plane(bead_id: str, summary: str):
    """
    Consolidation Step: Mark done and add context summary.
    """
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
    query = """
    MATCH (t:Task {id: $bead_id})
    SET t.status = 'done',
        t.completed_at = datetime(),
        t.context_summary = $summary
    """
    try:
        with driver.session() as session:
            session.run(query, bead_id=bead_id, summary=summary)
            return {"success": True}
    finally:
        driver.close()
