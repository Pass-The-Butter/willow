"""
Willow Skill: Get Task Context from Organogram
Retrieve scoped context for a specific task based on its position in the project tree
"""

from neo4j import GraphDatabase
import os
import certifi
from typing import Optional

NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USER = os.getenv("NEO4J_USER")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")


def execute(task_path: str) -> dict:
    """
    Get context for a task by its organogram path
    
    Args:
        task_path: Path in format "Domain → Component → Task"
                  e.g., "Population → Generator → Faker Integration"
    
    Returns:
        dict with:
        - task: Task details
        - parent_component: Component info
        - parent_domain: Domain info
        - specifications: Required specs
        - acceptance_criteria: Test criteria
        - dependencies: Other tasks this depends on
        - diary_entries: Recent work logs
        - messages: Unread messages for this task
        - rfcs: Related RFCs
    """
    os.environ['SSL_CERT_FILE'] = certifi.where()
    os.environ['REQUESTS_CA_BUNDLE'] = certifi.where()
    
    # Parse task path
    parts = [p.strip() for p in task_path.split("→")]
    if len(parts) != 3:
        return {"error": f"Invalid task path. Expected 'Domain → Component → Task', got: {task_path}"}
    
    domain_name, component_name, task_name = parts
    
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
    
    try:
        with driver.session() as session:
            result = session.run("""
                // Find the task
                MATCH (domain:Domain {name: $domain_name})
                      -[:HAS_COMPONENT]->(component:Component {name: $component_name})
                      -[:HAS_TASK]->(task:Task {name: $task_name})
                
                // Get specifications
                OPTIONAL MATCH (task)-[:REQUIRES]->(spec:Specification)
                
                // Get acceptance criteria
                OPTIONAL MATCH (task)-[:MUST_SATISFY]->(criteria:TestCriteria)
                
                // Get dependencies
                OPTIONAL MATCH (task)-[:DEPENDS_ON]->(dep:Task)
                
                // Get recent diary entries (last 7 days)
                OPTIONAL MATCH (task)-[:HAS_DIARY_ENTRY]->(diary:DiaryEntry)
                WHERE diary.timestamp > datetime() - duration('P7D')
                
                // Get unread messages
                OPTIONAL MATCH (task)<-[:TARGETS]-(msg:Message {status: "Unread"})
                
                // Get related RFCs
                OPTIONAL MATCH (component)-[:HAS_RFC]->(rfc:RFC)
                WHERE rfc.status = "Open"
                
                RETURN 
                  domain,
                  component,
                  task,
                  spec,
                  criteria,
                  collect(DISTINCT dep) as dependencies,
                  collect(DISTINCT diary) as diary_entries,
                  collect(DISTINCT msg) as messages,
                  collect(DISTINCT rfc) as rfcs
            """, domain_name=domain_name, component_name=component_name, task_name=task_name)
            
            record = result.single()
            
            if not record:
                return {"error": f"Task not found: {task_path}"}
            
            # Build context dictionary
            context = {
                "task_path": task_path,
                "domain": dict(record["domain"]) if record["domain"] else None,
                "component": dict(record["component"]) if record["component"] else None,
                "task": dict(record["task"]) if record["task"] else None,
                "specification": dict(record["spec"]) if record["spec"] else None,
                "acceptance_criteria": dict(record["criteria"]) if record["criteria"] else None,
                "dependencies": [dict(d) for d in record["dependencies"] if d],
                "diary_entries": [dict(e) for e in record["diary_entries"] if e],
                "messages": [dict(m) for m in record["messages"] if m],
                "rfcs": [dict(r) for r in record["rfcs"] if r]
            }
            
            # Summary
            context["summary"] = {
                "task_name": context["task"]["name"],
                "status": context["task"]["status"],
                "has_dependencies": len(context["dependencies"]) > 0,
                "blocked_by": [d["name"] for d in context["dependencies"] if d.get("status") != "Complete"],
                "recent_activity": len(context["diary_entries"]),
                "unread_messages": len(context["messages"]),
                "open_rfcs": len(context["rfcs"])
            }
            
            return context
            
    finally:
        driver.close()


if __name__ == "__main__":
    # Example usage
    import json
    
    # Test with Faker Integration task
    context = execute("Population → Generator → Faker Integration")
    
    print("=" * 80)
    print("TASK CONTEXT")
    print("=" * 80)
    print(json.dumps(context, indent=2, default=str))
