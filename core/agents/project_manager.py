#!/usr/bin/env python3
"""
Willow Project Manager Agent
Autonomous agent that reads organogram, delegates tasks, and monitors progress
"""

import os
import sys
from neo4j import GraphDatabase
import certifi

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

os.environ['SSL_CERT_FILE'] = certifi.where()


class ProjectManagerAgent:
    """
    PM Agent that operates at sprint level
    - Reads organogram for current tasks
    - Identifies blockers
    - Delegates to Feature Agents
    - Reports to Captain
    """
    
    def __init__(self):
        # Load credentials
        self.load_env()
        
        self.driver = GraphDatabase.driver(
            os.getenv('NEO4J_URI'),
            auth=(os.getenv('NEO4J_USER'), os.getenv('NEO4J_PASSWORD'))
        )
        
    def load_env(self):
        """Load environment variables from .env file"""
        env_path = os.path.join(os.path.dirname(__file__), '../../.env')
        with open(env_path) as f:
            for line in f:
                if '=' in line and not line.startswith('#'):
                    key, val = line.strip().split('=', 1)
                    os.environ[key] = val
    
    def bootstrap(self):
        """Bootstrap PM Agent - Load sprint context and sync boards"""
        print("=" * 80)
        print("📋 PROJECT MANAGER AGENT - BOOTSTRAPPING")
        print("=" * 80)
        
        # 1. Sync Boards
        self.sync_boards()
        
        print("\nConnecting to Brain (AuraDB)...")
        with self.driver.session() as session:
            # Test connection
            result = session.run("RETURN 'Connected!' as msg")
            print(f"✅ {result.single()['msg']}")
            
            # Load sprint tasks
            print("\n📊 LOADING SPRINT CONTEXT...")
            self.show_sprint_status(session)
            
            # Check messages
            print("\n📧 CHECKING MESSAGES...")
            self.check_messages(session)
            
            # Check RFCs
            print("\n📝 CHECKING RFCs...")
            self.check_rfcs(session)
            
            # Make recommendations
            print("\n💡 RECOMMENDATIONS:")
            self.make_recommendations(session)

    def sync_boards(self):
        """Synchronize task.md, AuraDB, and Linear"""
        print("\n🔄 SYNCHRONIZING KANBAN BOARDS...")
        
        repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
        task_md = os.path.join(repo_root, 'task.md')
        
        # 1. Sync task.md to AuraDB
        print("  -> Syncing local task.md to AuraDB Brain...")
        from core.skills import sync_brain_tasks
        try:
            tasks = sync_brain_tasks.parse_markdown_tasks(task_md)
            sync_brain_tasks.sync_to_brain(tasks)
            print("  ✅ Brain sync complete.")
        except Exception as e:
            print(f"  ❌ Brain sync failed: {e}")
            
        # 2. Sync task.md to Linear
        print("  -> Syncing local task.md to Linear...")
        from core.skills import sync_linear
        try:
            sync_linear.main()
            print("  ✅ Linear sync complete.")
        except Exception as e:
            print(f"  ❌ Linear sync failed: {e}")

        # 3. Generate Sidebar Report
        print("  -> Generating Sidebar Kanban report...")
        from core.skills import post_kanban_to_sidebar
        try:
            post_kanban_to_sidebar.generate_kanban_report()
            print("  ✅ Sidebar report complete.")
        except Exception as e:
            print(f"  ❌ Sidebar report failed: {e}")

    def show_sprint_status(self, session):
        """Show current sprint task status"""
        result = session.run("""
            MATCH (d:Domain)-[:HAS_COMPONENT]->(c:Component)-[:HAS_TASK]->(t:Task)
            RETURN d.name as domain,
                   count(t) as total_tasks,
                   sum(CASE WHEN t.status = 'Complete' THEN 1 ELSE 0 END) as completed,
                   sum(CASE WHEN t.status = 'In Progress' THEN 1 ELSE 0 END) as in_progress,
                   sum(CASE WHEN t.status = 'Not Started' THEN 1 ELSE 0 END) as not_started
            ORDER BY d.name
        """)
        
        print("\nDOMAIN STATUS:")
        for record in result:
            pct = int((record['completed'] / record['total_tasks']) * 100) if record['total_tasks'] > 0 else 0
            status = "🟢" if pct == 100 else "🟡" if pct > 0 else "⚪"
            print(f"  {status} {record['domain']}: {pct}% ({record['completed']}/{record['total_tasks']} complete)")
            if record['in_progress'] > 0:
                print(f"      🟡 {record['in_progress']} in progress")
            if record['not_started'] > 0:
                print(f"      ⚪ {record['not_started']} not started")
    
    def check_messages(self, session):
        """Check for unread messages"""
        result = session.run("""
            MATCH (m:Message {status: "Unread"})
            RETURN m.from as from,
                   m.to as to,
                   m.subject as subject,
                   m.priority as priority
            ORDER BY m.timestamp DESC
            LIMIT 5
        """)
        
        messages = list(result)
        if messages:
            print(f"\n  Found {len(messages)} unread message(s):")
            for msg in messages:
                priority_icon = "🔴" if msg['priority'] == 'High' else "🟡"
                print(f"  {priority_icon} {msg['from']} → {msg['to']}: {msg['subject']}")
        else:
            print("  ✅ No unread messages")
    
    def check_rfcs(self, session):
        """Check for open RFCs requiring decision"""
        result = session.run("""
            MATCH (rfc:RFC {status: "Open"})
            RETURN rfc.id as id,
                   rfc.title as title,
                   rfc.priority as priority
            ORDER BY rfc.priority DESC
        """)
        
        rfcs = list(result)
        if rfcs:
            print(f"\n  Found {len(rfcs)} open RFC(s):")
            for rfc in rfcs:
                print(f"  📋 {rfc['id']}: {rfc['title']} [{rfc['priority']}]")
        else:
            print("  ✅ No open RFCs")
    
    def make_recommendations(self, session):
        """Analyze and make task recommendations"""
        # Find tasks ready to start (no blockers)
        result = session.run("""
            MATCH (t:Task {status: 'Not Started'})
            OPTIONAL MATCH (t)-[:DEPENDS_ON]->(dep:Task)
            WHERE dep.status <> 'Complete'
            WITH t, collect(dep.name) as blockers
            WHERE size(blockers) = 0
            RETURN t.name as task
            LIMIT 3
        """)
        
        ready_tasks = list(result)
        if ready_tasks:
            print("\n  Tasks ready to start (no blockers):")
            for task in ready_tasks:
                print(f"    ✅ {task['task']}")
        else:
            print("\n  ⚠️  All available tasks have blockers or are in progress")
    
    def delegate_task(self, task_path: str):
        """
        Delegate a task to a Feature Agent
        
        Args:
            task_path: Task path like "Interface → Web App → Landing Page"
        """
        print(f"\n📤 DELEGATING TASK: {task_path}")
        
        # In a real implementation, this would:
        # 1. Spawn a new agent process/thread
        # 2. Pass scoped context from get_task_context()
        # 3. Monitor progress
        # 4. Report back when complete
        
        print(f"  ℹ️  To delegate manually:")
        print(f"     1. Open new Copilot chat")
        print(f"     2. Say: 'Bootstrap as Feature Agent for {task_path}'")
        print(f"     3. Agent will load scoped context and execute task")
        
    def close(self):
        """Close database connection"""
        self.driver.close()


def main():
    """Main entry point"""
    agent = ProjectManagerAgent()
    
    try:
        agent.bootstrap()
        
        print("\n" + "=" * 80)
        print("✅ PM AGENT READY")
        print("=" * 80)
        
        # Interactive mode (optional)
        if len(sys.argv) > 1 and sys.argv[1] == '--interactive':
            print("\nInteractive mode. Type 'help' for commands.")
            while True:
                cmd = input("\nPM> ").strip()
                if cmd == 'quit':
                    break
                elif cmd == 'status':
                    with agent.driver.session() as session:
                        agent.show_sprint_status(session)
                elif cmd == 'messages':
                    with agent.driver.session() as session:
                        agent.check_messages(session)
                elif cmd == 'help':
                    print("Commands: status, messages, delegate, quit")
                else:
                    print("Unknown command. Type 'help' for options.")
        
    finally:
        agent.close()


if __name__ == "__main__":
    main()
