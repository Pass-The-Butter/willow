#!/usr/bin/env python3
"""
Willow Feature Agent
Generic agent that can execute any task in the organogram with scoped context
"""

import os
import sys
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from core.skills import get_task_context
from core.clients.graph_client import GraphClient


class FeatureAgent:
    """
    Feature Agent that operates at task level
    - Loads scoped context for specific task
    - Executes task with minimal context
    - Logs work to diary
    - Reports completion to PM
    """
    
    def __init__(self, task_path: str):
        """
        Initialize Feature Agent for specific task
        
        Args:
            task_path: Task path like "Interface → Web App → Landing Page"
        """
        self.task_path = task_path
        self.load_env()
        
        self.task_path = task_path
        self.load_env()
        
        self.client = GraphClient(agent_id="feature-agent")
        
        self.context = None
        
    def load_env(self):
        """Load environment variables from .env file"""
        env_path = os.path.join(os.path.dirname(__file__), '../../.env')
        with open(env_path) as f:
            for line in f:
                if '=' in line and not line.startswith('#'):
                    key, val = line.strip().split('=', 1)
                    os.environ[key] = val
    
    def bootstrap(self):
        """Bootstrap Feature Agent - Load scoped context for task"""
        print("=" * 80)
        print(f"🔧 FEATURE AGENT - BOOTSTRAPPING")
        print("=" * 80)
        print(f"\nTask: {self.task_path}")
        
        # Load scoped context
        print("\n📚 Loading scoped context...")
        self.context = get_task_context.execute(self.task_path)
        
        if 'error' in self.context:
            print(f"❌ Error: {self.context['error']}")
            return False
        
        # Display context summary
        task = self.context['task']
        print(f"\n✅ Context loaded:")
        print(f"   Task: {task['title']}")
        print(f"   Status: {task['status']}")
        print(f"   Description: {task['description']}")
        
        if self.context['specification']:
            spec = self.context['specification']
            print(f"\n📋 Specification:")
            for key, val in spec.items():
                if key != 'reference':
                    print(f"   - {key}: {val}")
        
        if self.context['acceptance_criteria']:
            print(f"\n✅ Acceptance Criteria:")
            for key, val in self.context['acceptance_criteria'].items():
                print(f"   - {key}: {val}")
        
        if self.context['dependencies']:
            print(f"\n⚠️  Dependencies: {len(self.context['dependencies'])} task(s)")
            for dep in self.context['dependencies']:
                print(f"   - {dep['name']}: {dep.get('status', 'Unknown')}")
        
        # Check recent work
        if self.context['diary_entries']:
            print(f"\n📖 Recent diary entries: {len(self.context['diary_entries'])}")
            latest = self.context['diary_entries'][0]
            print(f"   Last: {latest['agent']} - {latest['notes'][:60]}...")
        
        # Check messages
        if self.context['messages']:
            print(f"\n📧 Unread messages: {len(self.context['messages'])}")
            for msg in self.context['messages']:
                print(f"   From {msg['from']}: {msg['subject']}")
        
        return True
    
    def execute(self):
        """
        Execute the task
        
        This is where the actual work happens. In a real implementation,
        this would call specialized handlers based on task type.
        """
        print("\n" + "=" * 80)
        print("⚙️  EXECUTING TASK")
        print("=" * 80)
        
        task_name = self.context['task']['title']
        component = self.context['component']['name']
        
        # Route to appropriate handler
        if component == "Web App":
            return self.execute_web_task()
        elif component == "Generator":
            return self.execute_generator_task()
        else:
            print(f"ℹ️  No specialized handler for {component} tasks")
            print("   Manual implementation required")
            return False
    
    def execute_web_task(self):
        """Execute web app tasks (Landing Page, Quote Form, etc)"""
        task_name = self.context['task']['title']
        
        print(f"\n🌐 Web Task: {task_name}")
        print("\nℹ️  Implementation options:")
        print("   1. Use Copilot Edits: Add domains/interface/ to working set")
        print("   2. Manual edit: Create templates/[task].html")
        print("   3. Delegate to human developer")
        
        print("\n📁 Relevant files:")
        print(f"   - {self.context['component']['location']}")
        print("   - domains/interface/templates/")
        
        if self.context['specification']:
            print("\n📋 Requirements from spec:")
            spec = self.context['specification']
            if 'framework' in spec:
                print(f"   Framework: {spec['framework']}")
            if 'reference' in spec:
                print(f"   Reference: {spec['reference']}")
        
        return False  # Requires manual implementation
    
    def execute_generator_task(self):
        """Execute generator tasks (Faker Integration, Ollama, etc)"""
        task_name = self.context['task']['title']
        
        print(f"\n🔧 Generator Task: {task_name}")
        print(f"\nℹ️  Relevant location: {self.context['component']['location']}")
        
        return False  # Requires manual implementation
    
    def log_work(self, notes: str, status: str = "In Progress"):
        """Log work to diary"""
        self.client.run("""
            MATCH (t:Task {title: $task_name})
            CREATE (t)-[:HAS_DIARY_ENTRY]->(d:DiaryEntry {
                agent: "Feature Agent",
                timestamp: datetime(),
                status: $status,
                notes: $notes
            })
        """, {"task_name": self.context['task']['title'], "status": status, "notes": notes})
        
        print(f"📝 Logged to diary: {notes[:60]}...")
    
    def mark_complete(self):
        """Mark task as complete in organogram"""
        self.client.run("""
            MATCH (t:Task {title: $task_name})
            SET t.status = 'Complete',
                t.completed_at = datetime()
        """, {"task_name": self.context['task']['title']})
        
        print(f"✅ Task marked complete: {self.context['task']['title']}")
    
    def close(self):
        """Close database connection"""
        self.client.close()


def main():
    """Main entry point"""
    if len(sys.argv) < 2:
        print("Usage: feature_agent.py '<task_path>'")
        print("Example: feature_agent.py 'Interface → Web App → Landing Page'")
        sys.exit(1)
    
    task_path = sys.argv[1]
    
    agent = FeatureAgent(task_path)
    
    try:
        # Bootstrap
        if not agent.bootstrap():
            sys.exit(1)
        
        print("\n" + "=" * 80)
        print("✅ FEATURE AGENT READY")
        print("=" * 80)
        print("\nAgent has loaded scoped context for this task.")
        print("Ready to execute or provide guidance for manual implementation.")
        
        # Optionally execute
        if len(sys.argv) > 2 and sys.argv[2] == '--execute':
            agent.execute()
        
    finally:
        agent.close()


if __name__ == "__main__":
    main()
