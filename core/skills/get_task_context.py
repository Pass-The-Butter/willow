"""
Willow Skill: Get Task Context from Organogram
Retrieve scoped context for a specific task based on its position in the project tree
"""

from core.clients.graph_client import GraphClient
import os
from typing import Optional


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
    # 1. Initialize Client
    client = GraphClient(agent_id="skill-get-context")
    
    try:
        # Parse task path
        parts = [p.strip() for p in task_path.split("→")]
        if len(parts) != 3:
            return {"error": f"Invalid task path. Expected 'Domain → Component → Task', got: {task_path}"}
        
        domain_name, component_name, task_name = parts

        results = client.run("""
            MATCH (domain:Domain {name: $domain_name})
                  -[:HAS_COMPONENT]->(component:Component {name: $component_name})
                  -[:HAS_TASK]->(task:Task {title: $task_name})
            
            OPTIONAL MATCH (task)-[:REQUIRES]->(spec:Specification)
            OPTIONAL MATCH (task)-[:MUST_SATISFY]->(criteria:TestCriteria)
            OPTIONAL MATCH (task)-[:DEPENDS_ON]->(dep:Task)
            
            OPTIONAL MATCH (task)-[:HAS_DIARY_ENTRY]->(diary:DiaryEntry)
            WHERE diary.timestamp > datetime() - duration('P7D')
            
            OPTIONAL MATCH (task)<-[:TARGETS]-(msg:Message {status: "Unread"})
            
            OPTIONAL MATCH (component)-[:HAS_RFC]->(rfc:RFC)
            WHERE rfc.status = "Open"
            
            RETURN 
              domain {.*},
              component {.*},
              task {.*},
              spec {.*},
              criteria {.*},
              collect(DISTINCT dep {.*}) as dependencies,
              collect(DISTINCT diary {.*}) as diary_entries,
              collect(DISTINCT msg {.*}) as messages,
              collect(DISTINCT rfc {.*}) as rfcs
        """, {"domain_name": domain_name, "component_name": component_name, "task_name": task_name})
        
        if not results:
             return {"error": f"Task not found: {task_path}"}
             
        record = results[0]

        # Build context dictionary
        context = {
            "task_path": task_path,
            "domain": record.get("domain"),
            "component": record.get("component"),
            "task": record.get("task"),
            "specification": record.get("spec"),
            "acceptance_criteria": record.get("criteria"),
            "dependencies": record.get("dependencies", []),
            "diary_entries": record.get("diary_entries", []),
            "messages": record.get("messages", []),
            "rfcs": record.get("rfcs", [])
        }
        
        # Summary
        context["summary"] = {
            "task_name": context["task"].get("name") if context["task"] else "Unknown",
            "status": context["task"].get("status") if context["task"] else "Unknown",
            "has_dependencies": len(context.get("dependencies", [])) > 0,
            "blocked_by": [d.get("name") for d in context.get("dependencies", []) if d.get("status") != "Complete"],
            "recent_activity": len(context.get("diary_entries", [])),
            "unread_messages": len(context.get("messages", [])),
            "open_rfcs": len(context.get("rfcs", []))
        }
        
        return context
            
    finally:
        client.close()


if __name__ == "__main__":
    # Example usage
    import json
    
    # Test with Faker Integration task
    context = execute("Population → Generator → Faker Integration")
    
    print("=" * 80)
    print("TASK CONTEXT")
    print("=" * 80)
    print(json.dumps(context, indent=2, default=str))
