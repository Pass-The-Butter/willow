"""
Willow Skill: Query My Tasks
Claude queries its own roadmap from the graph
"""

from typing import Optional, List
from neo4j import GraphDatabase
import os
import certifi

NEO4J_URI = os.getenv("NEO4J_URI", "neo4j+s://e59298d2.databases.neo4j.io")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "c2U7h1mwvmYn2k2cr_Fp9EaUrZaLZdEQ3_Cawt6zvyU")

def execute(
    status: Optional[str] = None,
    priority: Optional[str] = None,
    sprint: Optional[str] = None,
    assigned_to: str = "claude",
    show_blocked: bool = False
) -> dict:
    """
    Query tasks from the roadmap

    Args:
        status: Filter by status (todo, in_progress, done, blocked, frozen)
        priority: Filter by priority (critical, high, medium, low)
        sprint: Filter by sprint name
        assigned_to: Who the task is assigned to (default: "claude")
        show_blocked: Include tasks that are blocked by other tasks

    Returns:
        dict with tasks and metadata
    """

    os.environ['SSL_CERT_FILE'] = certifi.where()
    os.environ['REQUESTS_CA_BUNDLE'] = certifi.where()

    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

    # Build query dynamically
    where_clauses = [f"t.assigned_to = '{assigned_to}'"]

    if status:
        where_clauses.append(f"t.status = '{status}'")
    if priority:
        where_clauses.append(f"t.priority = '{priority}'")

    where_clause = " AND ".join(where_clauses)

    query = f"""
    MATCH (t:Task)
    WHERE {where_clause}

    // Get sprint info if exists
    OPTIONAL MATCH (s:Sprint)-[:CONTAINS_TASK]->(t)

    // Get blocking tasks
    OPTIONAL MATCH (t)-[:BLOCKED_BY]->(blocker:Task)

    // Get related decisions
    OPTIONAL MATCH (t)-[:IMPLEMENTS_DECISION]->(d:Decision)

    // Get related skills
    OPTIONAL MATCH (t)-[:TESTS_SKILL|REQUIRES_SKILL]->(skill:Skill)

    WITH t, s,
         collect(DISTINCT blocker.id) as blocked_by,
         collect(DISTINCT d.text) as decisions,
         collect(DISTINCT skill.name) as skills

    {"WHERE size(blocked_by) = 0" if not show_blocked else ""}

    RETURN t.id as id,
           t.title as title,
           t.description as description,
           t.status as status,
           t.priority as priority,
           s.name as sprint,
           blocked_by,
           decisions,
           skills
    ORDER BY
        CASE t.priority
            WHEN 'critical' THEN 1
            WHEN 'high' THEN 2
            WHEN 'medium' THEN 3
            WHEN 'low' THEN 4
            ELSE 5
        END,
        t.id
    """

    try:
        with driver.session() as session:
            result = session.run(query)

            tasks = []
            for record in result:
                task = {
                    "id": record["id"],
                    "title": record["title"],
                    "description": record["description"],
                    "status": record["status"],
                    "priority": record["priority"],
                    "sprint": record["sprint"],
                    "blocked_by": record["blocked_by"] if record["blocked_by"] else [],
                    "implements_decisions": record["decisions"] if record["decisions"] else [],
                    "related_skills": record["skills"] if record["skills"] else []
                }
                tasks.append(task)

            driver.close()

            # Build summary
            summary = f"Found {len(tasks)} tasks"
            if status:
                summary += f" with status '{status}'"
            if priority:
                summary += f" and priority '{priority}'"

            return {
                "success": True,
                "summary": summary,
                "count": len(tasks),
                "tasks": tasks,
                "skill": "query_my_tasks"
            }

    except Exception as e:
        driver.close()
        return {
            "success": False,
            "error": str(e),
            "skill": "query_my_tasks"
        }

def get_next_task(assigned_to: str = "claude") -> dict:
    """
    Convenience function: What should I work on next?
    Returns highest priority task that is not blocked
    """
    result = execute(
        status="todo",
        assigned_to=assigned_to,
        show_blocked=False
    )

    if result["success"] and result["count"] > 0:
        next_task = result["tasks"][0]
        return {
            "success": True,
            "message": f"Next task: {next_task['id']} - {next_task['title']}",
            "task": next_task,
            "skill": "query_my_tasks"
        }
    else:
        return {
            "success": True,
            "message": "No unblocked tasks available!",
            "task": None,
            "skill": "query_my_tasks"
        }

if __name__ == "__main__":
    # Test: What am I working on?
    print("=== Current Tasks ===")
    result = execute(status="in_progress")
    print(f"{result['summary']}")
    for task in result['tasks']:
        print(f"  [{task['status']}] {task['id']}: {task['title']}")

    print("\n=== Next Task ===")
    result = get_next_task()
    print(result['message'])
    if result['task']:
        print(f"  Priority: {result['task']['priority']}")
        print(f"  Description: {result['task']['description']}")
