import os
import json
import subprocess
import requests
from datetime import datetime
from dotenv import load_dotenv
from neo4j import GraphDatabase
import certifi
from pymongo import MongoClient

load_dotenv()

def ping_host(host):
    """Checks if a host is reachable."""
    try:
        # Ping count 1, timeout 2 seconds
        # Adjust command for OS (Mac/Linux support)
        cmd = ["ping", "-c", "1", "-W", "2000", host] if os.uname().sysname == 'Darwin' else ["ping", "-c", "1", "-W", "2", host]
        subprocess.check_call(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except subprocess.CalledProcessError:
        return False

def check_docker_remote(host):
    """Checks Docker services on a remote host via SSH."""
    try:
        # Assumes SSH access is configured via .ssh/config or keys loaded
        cmd = ["ssh", host, "docker", "ps", "--format", "{{.Names}}"]
        output = subprocess.check_output(cmd, stderr=subprocess.DEVNULL).decode('utf-8').strip()
        services = output.split('\n') if output else []
        return services
    except subprocess.CalledProcessError:
        return None

def check_neo4j():
    """Checks Neo4j connectivity and node count."""
    uri = os.getenv("NEO4J_URI")
    user = os.getenv("NEO4J_USER")
    password = os.getenv("NEO4J_PASSWORD")
    os.environ['SSL_CERT_FILE'] = certifi.where()
    
    try:
        driver = GraphDatabase.driver(uri, auth=(user, password))
        with driver.session() as session:
            count = session.run("MATCH (n) RETURN count(n) as c").single()['c']
        driver.close()
        return {"status": "ONLINE", "node_count": count}
    except Exception as e:
        return {"status": "OFFLINE", "error": str(e)}

def check_graphiti():
    """Checks Graphiti memory service."""
    try:
        resp = requests.get("http://bunny:8002/", timeout=5)
        if resp.status_code == 200:
             return "ONLINE"
        else:
             return f"ERROR_{resp.status_code}"
    except Exception as e:
        return f"OFFLINE ({str(e)})"

def save_to_mongodb(report):
    """Saves the report to MongoDB Atlas Mission Control (flight_logs collection)."""
    uri = os.getenv("MONGO_URI")
    if not uri:
        print("⚠️ MONGO_URI missing. Skipping MongoDB backup.")
        return None

    try:
        client = MongoClient(uri)
        db = client.get_database("willow-mission-control")
        collection = db.get_collection("flight_logs")
        report["timestamp"] = datetime.now()
        result = collection.insert_one(report)
        print(f"💾 Flight log stored in MongoDB Mission Control (ID: {result.inserted_id})")
        return report
    except Exception as e:
        print(f"⚠️ Failed to backup to MongoDB: {e}")
        return None

def save_to_starlight(report):
    """Saves the report as a Markdown file in the Starlight landings directory."""
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"landing_{timestamp}.md"
    filepath = os.path.join(os.getcwd(), "domains/sidebar/src/content/docs/landings", filename)

    # Ensure directory exists
    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    content = f"""---
title: "Landing Report: {timestamp}"
description: "Automated system verification report."
---

# ✈️ Landing the Plane Report

**Timestamp**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## 🌐 Network Status

"""
    for host, status in report["network"].items():
        icon = "🟢" if status == "Alive" else "🔴"
        content += f"- **{host}**: {icon} {status}\n"

    content += "\n## 🐳 Services (Bunny)\n\n"
    if "error" in report["services"]:
        content += f"❌ Error: {report['services']['error']}\n"
    else:
        for svc, state in report["services"].items():
            if svc != "bunny_docker_up":
                icon = "🟢" if state == "Running" else "🔴"
                content += f"- {icon} {svc}\n"

    content += f"\n## 🧠 Data (Neo4j)\n\n"
    content += f"- **Status**: {report['data']['neo4j']['status']}\n"
    content += f"- **Node Count**: {report['data']['neo4j'].get('node_count', 'N/A')}\n"

    content += f"\n## 💾 Memory (Graphiti)\n\n"
    content += f"- **Status**: {report['memory']['graphiti']}\n"

    try:
        with open(filepath, "w") as f:
            f.write(content)
        print(f"📄 Report written to Starlight: {filename}")
    except Exception as e:
        print(f"⚠️ Failed to write Starlight report: {e}")

def land_the_plane():
    """
    Executes a system-wide "Beads" check.
    """
    report = {
        "network": {},
        "services": {},
        "data": {},
        "memory": {}
    }

    print("✈️  Landing the Plane: Initiating System Check...")

    # 1. Network Connectivity
    hosts = ["bunny", "frank"]
    for h in hosts:
        status = ping_host(h)
        report["network"][h] = "Alive" if status else "Dead"
        print(f"Network [{h}]: {report['network'][h]}")

    # 2. Remote Services (Bunny)
    if report["network"]["bunny"] == "Alive":
        containers = check_docker_remote("bunny")
        expected = ["willow-dashboard", "willow-n8n", "willow-graphiti", "willow-neo4j-mcp", "willow-population-db", "willow-proxy", "willow-sidebar"]
        report["services"]["bunny_docker_up"] = True if containers is not None else False
        
        if containers:
            for ex in expected:
                report["services"][ex] = "Running" if any(ex in c for c in containers) else "MISSING"
                print(f"Service [{ex}]: {report['services'][ex]}")
        else:
             report["services"]["error"] = "Could not list containers"

    # 3. Data Consistency (Neo4j)
    neo_status = check_neo4j()
    report["data"]["neo4j"] = neo_status
    print(f"Data [Neo4j]: {neo_status['status']} (Nodes: {neo_status.get('node_count', 'N/A')})")

    # 4. Memory (Graphiti)
    graphiti_status = check_graphiti()
    report["memory"]["graphiti"] = graphiti_status
    print(f"Memory [Graphiti]: {graphiti_status}")

    # 5. Backup & Report
    mongo_report = save_to_mongodb(report)
    save_to_starlight(report)
    send_telegram_report(report)

    # Save evidence for mission rtb1tkjq
    if mongo_report:
        evidence_dir = os.path.join(os.getcwd(), "artifacts/evidence")
        os.makedirs(evidence_dir, exist_ok=True)
        evidence_path = os.path.join(evidence_dir, "mongo_push_rtb1tkjq.json")
        with open(evidence_path, "w") as f:
            # Convert datetime and other non-serializable types to strings
            evidence_data = {}
            for key, value in mongo_report.items():
                if key == "_id":
                    evidence_data[key] = str(value)
                elif isinstance(value, datetime):
                    evidence_data[key] = value.isoformat()
                else:
                    evidence_data[key] = value
            json.dump(evidence_data, f, indent=2)
        print(f"📋 Evidence saved: {evidence_path}")

    return report

def send_telegram_report(report):
    """Sends the landing report to Telegram."""
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    
    if not token or not chat_id:
        print("⚠️ Telegram token or chat_id missing. Skipping notification.")
        return

    # Construct message
    status_emoji = "✅" if report["services"].get("bunny_docker_up") else "❌"
    msg = f"{status_emoji} *Flight Controller Report*\n\n"
    
    msg += "*Network:*\n"
    for host, status in report["network"].items():
        msg += f"- {host}: {status}\n"
    
    msg += "\n*Services (Bunny):*\n"
    if "error" in report["services"]:
         msg += f"❌ Error: {report['services']['error']}\n"
    else:
        for svc, state in report["services"].items():
            if svc != "bunny_docker_up":
                icon = "🟢" if state == "Running" else "🔴"
                msg += f"{icon} {svc}\n"
    
    msg += f"\n*Data Check:* {report['data']['neo4j']['status']}\n"
    msg += f"*Memory Check:* {report['memory']['graphiti']}\n"

    try:
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        payload = {"chat_id": chat_id, "text": msg, "parse_mode": "Markdown"}
        requests.post(url, json=payload, timeout=5)
        print("📨 Telegram notification sent.")
    except Exception as e:
        print(f"⚠️ Failed to send Telegram: {e}")

if __name__ == "__main__":
    land_the_plane()
