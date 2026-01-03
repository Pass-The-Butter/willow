#!/usr/bin/env python3
"""
Query Flight History

Retrieves the last N flight reports from MongoDB Mission Control.
Mission: GOPHER-rtb1tkjq - Part of the Mongo Mission Log integration.
"""
import os
import json
import certifi
from datetime import datetime
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

# Set SSL certificate for MongoDB connection
os.environ['SSL_CERT_FILE'] = certifi.where()

def query_flight_history(limit=10):
    """
    Retrieves the last N flight reports from MongoDB Atlas.

    Args:
        limit (int): Number of reports to retrieve (default: 10)

    Returns:
        list: List of flight reports, sorted by timestamp descending
    """
    uri = os.getenv("MONGO_URI")
    if not uri:
        print("⚠️ MONGO_URI not found in environment.")
        return []

    try:
        client = MongoClient(uri)
        db = client.get_database("willow-mission-control")
        collection = db.get_collection("flight_logs")

        # Query the last N reports, sorted by timestamp descending
        cursor = collection.find().sort("timestamp", -1).limit(limit)
        reports = list(cursor)

        print(f"📊 Retrieved {len(reports)} flight reports from Mission Control\n")

        for i, report in enumerate(reports, 1):
            timestamp = report.get("timestamp", "Unknown")
            if isinstance(timestamp, datetime):
                timestamp = timestamp.strftime("%Y-%m-%d %H:%M:%S")

            print(f"Report #{i} - {timestamp}")
            print(f"  Network: {report.get('network', {})}")
            print(f"  Neo4j: {report.get('data', {}).get('neo4j', {}).get('status', 'Unknown')}")
            print(f"  Graphiti: {report.get('memory', {}).get('graphiti', 'Unknown')}")

            # Check service health
            services = report.get('services', {})
            running_services = sum(1 for v in services.values() if v == "Running")
            total_services = len([k for k in services.keys() if k != "bunny_docker_up" and k != "error"])
            print(f"  Services: {running_services}/{total_services} running")
            print()

        return reports

    except Exception as e:
        print(f"❌ Failed to query MongoDB: {e}")
        return []

def export_history_json(limit=10, output_path="flight_history.json"):
    """
    Exports flight history to a JSON file.

    Args:
        limit (int): Number of reports to retrieve
        output_path (str): Path to save the JSON file
    """
    reports = query_flight_history(limit)

    if not reports:
        print("No reports to export.")
        return

    # Convert MongoDB ObjectId and datetime to strings for JSON
    export_data = []
    for report in reports:
        clean_report = {}
        for key, value in report.items():
            if key == "_id":
                clean_report[key] = str(value)
            elif isinstance(value, datetime):
                clean_report[key] = value.isoformat()
            else:
                clean_report[key] = value
        export_data.append(clean_report)

    with open(output_path, 'w') as f:
        json.dump(export_data, f, indent=2)

    print(f"💾 Flight history exported to {output_path}")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Query flight history from MongoDB Mission Control")
    parser.add_argument("--limit", type=int, default=10, help="Number of reports to retrieve (default: 10)")
    parser.add_argument("--export", type=str, help="Export to JSON file")

    args = parser.parse_args()

    if args.export:
        export_history_json(limit=args.limit, output_path=args.export)
    else:
        query_flight_history(limit=args.limit)
