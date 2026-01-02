"""
Willow Skill: Manage Episodic Memory (Neo4j Native)
Replaces Zep. Stores Session -> Turn -> Turn chains in the Graph.
"""

from neo4j import GraphDatabase
import os
import certifi
import uuid
import datetime
from neo4j import GraphDatabase
import os
import certifi
import uuid
import datetime
from core.utils.credentials import get_neo4j_auth

# Load credentials securely
NEO4J_URI, NEO4J_AUTH = get_neo4j_auth()
NEO4J_USER = NEO4J_AUTH[0]
NEO4J_PASSWORD = NEO4J_AUTH[1]

os.environ['SSL_CERT_FILE'] = certifi.where()

def add_turn(session_id: str, role: str, content: str, relevant_tasks: list = None) -> dict:
    """
    Log a conversational turn.
    Args:
        session_id: Unique ID for the conversation
        role: 'user' or 'assistant' or 'system'
        content: The text content
        relevant_tasks: Optional list of Task IDs this turn relates to
    """
    driver = GraphDatabase.driver(NEO4J_URI, auth=NEO4J_AUTH)
    
    turn_id = str(uuid.uuid4())
    timestamp = datetime.datetime.utcnow().isoformat()
    
    query = """
    MERGE (s:Session {id: $session_id})
    ON CREATE SET s.started_at = $timestamp, s.status = 'active'
    
    CREATE (t:Turn {
        id: $turn_id,
        role: $role,
        content: $content,
        timestamp: $timestamp
    })
    
    // Link Session to Turn (if first turn) or Append to Chain
    WITH s, t
    OPTIONAL MATCH (s)-[:HAS_TURN]->(last_turn:Turn)
    WHERE NOT (last_turn)-[:NEXT]->(:Turn)
    
    FOREACH (_ IN CASE WHEN last_turn IS NULL THEN [1] ELSE [] END |
        MERGE (s)-[:HAS_TURN]->(t)
    )
    
    FOREACH (_ IN CASE WHEN last_turn IS NOT NULL THEN [1] ELSE [] END |
        MERGE (last_turn)-[:NEXT]->(t)
    )
    
    RETURN t.id as id
    """
    
    # Task Linking logic
    task_link_query = """
    MATCH (t:Turn {id: $turn_id})
    MATCH (task:Task) WHERE task.id IN $task_ids
    MERGE (t)-[:RELATES_TO]->(task)
    """

    try:
        with driver.session() as session:
            session.run(query, session_id=session_id, turn_id=turn_id, role=role, content=content, timestamp=timestamp)
            
            if relevant_tasks:
                session.run(task_link_query, turn_id=turn_id, task_ids=relevant_tasks)
                
            return {"success": True, "turn_id": turn_id}
            
    except Exception as e:
        return {"success": False, "error": str(e)}
    finally:
        driver.close()

def get_recent_context(session_id: str, limit: int = 10) -> list:
    """
    Retrieve the last N turns for a session.
    """
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
    
    query = """
    MATCH (s:Session {id: $session_id})-[:HAS_TURN]->(first:Turn)
    MATCH path = (first)-[:NEXT*0..]->(t:Turn)
    RETURN t.role as role, t.content as content, t.timestamp as timestamp
    ORDER BY t.timestamp DESC
    LIMIT $limit
    """
    
    try:
        with driver.session() as session:
            result = session.run(query, session_id=session_id, limit=limit)
            history = [{"role": r["role"], "content": r["content"]} for r in result]
            # Reverse to get chronological order (since we sorted DESC for limit)
            return history[::-1]
    except Exception as e:
        return []
    finally:
        driver.close()

if __name__ == "__main__":
    # verification
    sid = "test-session-1"
    print(add_turn(sid, "user", "Hello Willow!"))
    print(add_turn(sid, "assistant", "Hello! I am ready."))
    print(get_recent_context(sid))
