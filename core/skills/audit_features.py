#!/usr/bin/env python3
"""
Feature Audit Skill - Query Neo4j Brain for all features, tasks, RFCs, decisions, and insights.

This skill connects to the Neo4j AuraDB instance (The Brain) and extracts comprehensive
information about all features, tasks, RFCs, decisions, insights, and diary entries.
"""

import os
import json
import certifi
from neo4j import GraphDatabase
from datetime import datetime


class FeatureAuditor:
    """Audits all features and ideas from Neo4j Brain."""

    def __init__(self):
        """Initialize Neo4j connection."""
        self.uri = os.getenv("NEO4J_URI", "neo4j+s://e59298d2.databases.neo4j.io")
        self.user = os.getenv("NEO4J_USER", "neo4j")
        self.password = os.getenv("NEO4J_PASSWORD")

        # Note: neo4j+s:// URI scheme already implies encryption
        # Don't use 'encrypted' or 'trust' parameters with neo4j+s://
        self.driver = GraphDatabase.driver(
            self.uri,
            auth=(self.user, self.password)
        )

    def close(self):
        """Close Neo4j connection."""
        if self.driver:
            self.driver.close()

    def query_tasks(self):
        """Query all Task nodes with relationships."""
        query = """
        MATCH (t:Task)
        OPTIONAL MATCH (t)-[r]-(related)
        RETURN t,
               collect(DISTINCT {
                   type: labels(related)[0],
                   name: related.name,
                   relationship: type(r)
               }) as relationships
        """
        with self.driver.session() as session:
            results = session.run(query)
            tasks = []
            for record in results:
                task = dict(record["t"])
                task["relationships"] = record["relationships"]
                tasks.append(task)
            return tasks

    def query_rfcs(self):
        """Query all RFC nodes with relationships."""
        query = """
        MATCH (r:RFC)
        OPTIONAL MATCH (r)-[rel]-(related)
        RETURN r,
               collect(DISTINCT {
                   type: labels(related)[0],
                   name: related.name,
                   relationship: type(rel)
               }) as relationships
        """
        with self.driver.session() as session:
            results = session.run(query)
            rfcs = []
            for record in results:
                rfc = dict(record["r"])
                rfc["relationships"] = record["relationships"]
                rfcs.append(rfc)
            return rfcs

    def query_decisions(self):
        """Query all Decision nodes with relationships."""
        query = """
        MATCH (d:Decision)
        OPTIONAL MATCH (d)-[rel]-(related)
        RETURN d,
               collect(DISTINCT {
                   type: labels(related)[0],
                   name: related.name,
                   relationship: type(rel)
               }) as relationships
        """
        with self.driver.session() as session:
            results = session.run(query)
            decisions = []
            for record in results:
                decision = dict(record["d"])
                decision["relationships"] = record["relationships"]
                decisions.append(decision)
            return decisions

    def query_insights(self):
        """Query all Insight nodes with relationships."""
        query = """
        MATCH (i:Insight)
        OPTIONAL MATCH (i)-[rel]-(related)
        RETURN i,
               collect(DISTINCT {
                   type: labels(related)[0],
                   name: related.name,
                   relationship: type(rel)
               }) as relationships
        """
        with self.driver.session() as session:
            results = session.run(query)
            insights = []
            for record in results:
                insight = dict(record["i"])
                insight["relationships"] = record["relationships"]
                insights.append(insight)
            return insights

    def query_diary_entries(self, limit=100):
        """Query recent diary entries to understand work history."""
        query = """
        MATCH (d:DiaryEntry)
        RETURN d
        ORDER BY d.date DESC, d.timestamp DESC
        LIMIT $limit
        """
        with self.driver.session() as session:
            results = session.run(query, limit=limit)
            entries = []
            for record in results:
                entries.append(dict(record["d"]))
            return entries

    def query_all_labels(self):
        """Get all node labels in the database."""
        query = """
        CALL db.labels() YIELD label
        RETURN label
        ORDER BY label
        """
        with self.driver.session() as session:
            results = session.run(query)
            return [record["label"] for record in results]

    def query_nodes_by_label(self, label, limit=50):
        """Query nodes by label."""
        query = f"""
        MATCH (n:{label})
        OPTIONAL MATCH (n)-[r]-(related)
        RETURN n,
               collect(DISTINCT {{
                   type: labels(related)[0],
                   name: related.name,
                   relationship: type(r)
               }}) as relationships
        LIMIT $limit
        """
        with self.driver.session() as session:
            results = session.run(query, limit=limit)
            nodes = []
            for record in results:
                node = dict(record["n"])
                node["_label"] = label
                node["relationships"] = record["relationships"]
                nodes.append(node)
            return nodes

    def audit_all(self):
        """Perform comprehensive audit of all Brain content."""
        print("🧠 Connecting to Neo4j Brain...")

        audit_data = {
            "timestamp": datetime.now().isoformat(),
            "tasks": [],
            "rfcs": [],
            "decisions": [],
            "insights": [],
            "diary_entries": [],
            "other_nodes": {},
            "labels": []
        }

        try:
            # Get all labels first
            print("📋 Discovering node types...")
            audit_data["labels"] = self.query_all_labels()
            print(f"   Found {len(audit_data['labels'])} node types: {', '.join(audit_data['labels'])}")

            # Query standard node types
            print("\n📝 Querying Tasks...")
            audit_data["tasks"] = self.query_tasks()
            print(f"   Found {len(audit_data['tasks'])} tasks")

            print("📄 Querying RFCs...")
            audit_data["rfcs"] = self.query_rfcs()
            print(f"   Found {len(audit_data['rfcs'])} RFCs")

            print("⚖️  Querying Decisions...")
            audit_data["decisions"] = self.query_decisions()
            print(f"   Found {len(audit_data['decisions'])} decisions")

            print("💡 Querying Insights...")
            audit_data["insights"] = self.query_insights()
            print(f"   Found {len(audit_data['insights'])} insights")

            print("📖 Querying Diary Entries...")
            audit_data["diary_entries"] = self.query_diary_entries(limit=100)
            print(f"   Found {len(audit_data['diary_entries'])} diary entries")

            # Query other node types
            standard_labels = {"Task", "RFC", "Decision", "Insight", "DiaryEntry"}
            other_labels = [l for l in audit_data["labels"] if l not in standard_labels]

            if other_labels:
                print(f"\n🔍 Querying other node types: {', '.join(other_labels)}")
                for label in other_labels:
                    try:
                        nodes = self.query_nodes_by_label(label)
                        audit_data["other_nodes"][label] = nodes
                        print(f"   {label}: {len(nodes)} nodes")
                    except Exception as e:
                        print(f"   ⚠️  Error querying {label}: {e}")

            print("\n✅ Brain audit complete!")
            return audit_data

        except Exception as e:
            print(f"❌ Error during audit: {e}")
            raise
        finally:
            self.close()


def main():
    """Main execution function."""
    auditor = FeatureAuditor()

    try:
        audit_data = auditor.audit_all()

        # Save to JSON file
        output_file = "/Volumes/Delila/dev/Willow/neo4j_audit_output.json"
        with open(output_file, "w") as f:
            json.dump(audit_data, indent=2, fp=f, default=str)

        print(f"\n💾 Results saved to: {output_file}")

        # Print summary statistics
        print("\n" + "="*60)
        print("AUDIT SUMMARY")
        print("="*60)
        print(f"Tasks:         {len(audit_data['tasks'])}")
        print(f"RFCs:          {len(audit_data['rfcs'])}")
        print(f"Decisions:     {len(audit_data['decisions'])}")
        print(f"Insights:      {len(audit_data['insights'])}")
        print(f"Diary Entries: {len(audit_data['diary_entries'])}")

        if audit_data["other_nodes"]:
            print("\nOther Node Types:")
            for label, nodes in audit_data["other_nodes"].items():
                print(f"  {label}: {len(nodes)}")

        print("="*60)

        return audit_data

    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
        return None


if __name__ == "__main__":
    main()
