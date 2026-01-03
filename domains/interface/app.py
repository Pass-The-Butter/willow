import os
import psycopg2
from flask import Flask, render_template, jsonify
from dotenv import load_dotenv
import requests
import sys
import platform

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Configuration
DB_HOST = os.getenv("PG_HOST", "bunny")
DB_PORT = os.getenv("PG_PORT", "5432")
DB_NAME = os.getenv("PG_DB", "population")
DB_USER = os.getenv("PG_USER", "willow")
DB_PASS = os.getenv("PG_PASS", "willowdev123")

def get_db_connection():
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )
    return conn

# --- Resource Tracking (Global) ---
RESOURCES = [
    {"name": "Python", "version": platform.python_version(), "type": "Language"},
    {"name": "Flask", "version": "3.0.0", "type": "Framework"},
    {"name": "Neo4j Driver", "version": "5.14.0", "type": "Database Driver"},
    {"name": "Psycopg2", "version": "2.9.9", "type": "Database Driver"},
    {"name": "Requests", "version": requests.__version__, "type": "HTTP Library"},
    {"name": "Tailscale", "version": "Detected", "type": "Infrastructure"},
    {"name": "Docker", "version": "Detected", "type": "Infrastructure"},
]

# --- Status Checks ---
def check_n8n_status():
    """Checks if N8N is reachable (assuming localhost tunnel or tailscale)."""
    try:
        # Pinging the local tunnel port or the bunny IP if known
        # In production this might be 'http://bunny:5678/healthz'
        # For this dashboard running ON the same network:
        response = requests.get("http://bunny:5678/healthz", timeout=1)
        return "ONLINE" if response.status_code == 200 else "ERROR"
    except:
        return "OFFLINE"

def check_telegram_status():
    """Checks if Telegram Bot is responsive via API."""
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        return "MISSING_TOKEN"
    try:
        url = f"https://api.telegram.org/bot{token}/getMe"
        response = requests.get(url, timeout=1)
        return "ONLINE" if response.status_code == 200 else "API_ERROR"
    except:
        return "UNREACHABLE"

@app.route('/api/send_message', methods=['POST'])
def send_message():
    """Sends a message to the Grapevine (N8N)."""
    data = request.json
    message = data.get('message')
    
    if not message:
        return jsonify({"status": "error", "message": "No message provided"}), 400

    # Forward to N8N Grapevine Webhook
    n8n_webhook = "https://bunny.clouded-newton.ts.net/webhook/grapevine"
    payload = {
        "message": message,
        "source": "dashboard",
        "type": "TASK",
        "session_id": "dashboard-user"
    }

    try:
        # Fire and forget (or wait for ack)
        requests.post(n8n_webhook, json=payload, timeout=5)
        return jsonify({"status": "success", "message": "Sent to Grapevine"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/')
def landing():
    return render_template('landing.html')

@app.route('/demo')
def demo():
    return render_template('index.html')

@app.route('/quote')
def quote_form():
    return render_template('quote_form.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/board')
@app.route('/board')
def board():
    """Single Pane of Glass - Board Member View"""
    return render_template('board.html', resources=RESOURCES)

@app.route('/doc/password-sop')
def password_sop():
    """Render the Password Rotation SOP as simple HTML"""
    # Simple markdown render for the SOP
    try:
        with open('../../docs/procedures/HOW_TO_ROTATE_NEO4J_PASSWORD.md', 'r') as f:
            content = f.read()
        # Basic markdown to HTML conversion (very simple for now)
        html = f"""
        <html>
        <body style="font-family: sans-serif; max-width: 800px; margin: 2rem auto; line-height: 1.6;">
            <a href="/board">← Back to Board</a>
            <pre style="white-space: pre-wrap; background: #f4f4f4; padding: 20px; border-radius: 8px;">{content}</pre>
        </body>
        </html>
        """
        return html
    except Exception as e:
        return f"Error loading SOP: {e}"

@app.route('/docs/bios')
def docs_bios():
    """Render the BIOS as simple HTML"""
    try:
        with open('BIOS.md', 'r') as f:
            content = f.read()
        html = f"""
        <html>
        <head><title>Willow BIOS</title></head>
        <body style="font-family: monospace; max-width: 800px; margin: 2rem auto; line-height: 1.6; background: #1e1e1e; color: #d4d4d4; padding: 20px;">
            <a href="/board" style="color: #667eea; text-decoration: none;">← Back to Board</a>
            <pre style="white-space: pre-wrap;">{content}</pre>
        </body>
        </html>
        """
        return html
    except Exception as e:
        return f"Error loading BIOS: {e}"

@app.route('/report/memory')
def report_memory():
    """Render the Dynamic Memory Architecture Report"""
    return render_template('memory_report.html')

@app.route('/api/pulse')
def pulse():
    """Returns system status for the live dashboard."""
    from datetime import datetime
    return jsonify({
        "timestamp": datetime.now().isoformat(),
        "n8n": check_n8n_status(),
        "telegram": check_telegram_status(),
        "auradb": "ONLINE", 
        "bunny": "ONLINE",
        "vector_indexes": 4, 
        "tasks_pending": 12 
    })

@app.route('/api/metrics')
def get_metrics():
    """Returns dynamic counts from the population database."""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute("SELECT COUNT(*) FROM people;")
        people_count = cur.fetchone()[0]
        
        cur.execute("SELECT COUNT(*) FROM quotes WHERE status = 'ISSUED';")
        active_policies = cur.fetchone()[0]
        
        cur.execute("SELECT COUNT(*) FROM claims;")
        claims_count = cur.fetchone()[0]
        
        cur.close()
        conn.close()
        
        return jsonify({
            "people": people_count,
            "policies": active_policies,
            "claims": claims_count
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/organogram')
def get_organogram_data():
    """Fetches the project structure for the visual organogram."""
    from neo4j import GraphDatabase
    import certifi
    
    uri = os.getenv("NEO4J_URI")
    user = os.getenv("NEO4J_USER")
    password = os.getenv("NEO4J_PASSWORD")
    
    # Configure SSL
    os.environ['SSL_CERT_FILE'] = certifi.where()
    
    driver = GraphDatabase.driver(uri, auth=(user, password))
    
    try:
        with driver.session() as session:
            # Query for domains, components, and tasks
            result = session.run("""
                MATCH (p:Project)-[:HAS_DOMAIN]->(d:Domain)
                OPTIONAL MATCH (d)-[:HAS_COMPONENT]->(c:Component)
                OPTIONAL MATCH (c)-[:HAS_TASK]->(t:Task)
                RETURN p.name as project,
                       d.name as domain,
                       collect(DISTINCT c.name) as components,
                       collect(DISTINCT {name: t.name, status: t.status}) as tasks
            """)
            
            nodes = []
            links = []
            
            # Root node
            nodes.append({"id": "Willow", "label": "Willow", "type": "Project"})
            
            for record in result:
                domain = record["domain"]
                nodes.append({"id": domain, "label": domain, "type": "Domain"})
                links.append({"source": "Willow", "target": domain})
                
                for comp in record["components"]:
                    if comp:
                        comp_id = f"{domain}_{comp}"
                        nodes.append({"id": comp_id, "label": comp, "type": "Component"})
                        links.append({"source": domain, "target": comp_id})
                        
                        # Add tasks for this component
                        for task in record["tasks"]:
                            # Note: This simple query might need more precision to link task to component
                            # but for now we'll just link all tasks in record to the first component
                            # or just show tasks under components.
                            if task and task['name']:
                                task_id = f"task_{task['name']}"
                                nodes.append({"id": task_id, "label": task['name'], "type": "Task", "status": task['status']})
                                links.append({"source": comp_id, "target": task_id})
            
            return jsonify({"nodes": nodes, "links": links})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        driver.close()

@app.route('/organogram')
def organogram():
    """Render the Visual Organogram page"""
    return render_template('organogram.html')

@app.route('/kanban')
def kanban():
    """Render the Visual Kanban Board page"""
    return render_template('kanban.html')

@app.route('/api/kanban')
def get_kanban_data():
    """Fetches tasks for the Kanban board from AuraDB."""
    from neo4j import GraphDatabase
    import certifi
    
    uri = os.getenv("NEO4J_URI")
    user = os.getenv("NEO4J_USER")
    password = os.getenv("NEO4J_PASSWORD")
    
    os.environ['SSL_CERT_FILE'] = certifi.where()
    
    driver = GraphDatabase.driver(uri, auth=(user, password))
    
    try:
        with driver.session() as session:
            result = session.run("""
                MATCH (t:Task)
                RETURN t.id as id, 
                       t.title as title, 
                       t.description as description, 
                       t.status as status, 
                       t.priority as priority, 
                       t.assigned_to as assigned_to,
                       t.created_at as created_at
                ORDER BY t.priority DESC
            """)
            
            tasks = []
            for record in result:
                tasks.append({
                    "id": record["id"],
                    "title": record["title"],
                    "description": record["description"],
                    "status": record["status"].lower().replace(' ', '_'), # Normalize status
                    "priority": record["priority"],
                    "assignee": record["assigned_to"],
                    "date": record["created_at"].strftime('%d %b') if record["created_at"] else "N/A"
                })
            
            return jsonify({"tasks": tasks})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        driver.close()

@app.route('/people')
def people_viewer():
    """Simple People Viewer: Just peek at the crowd."""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Simple fetch of 50 people
        # In a real app we'd paginate, but this is a "peek"
        query = """
            SELECT id, first_name, last_name, age, risk_score, policy_start_date, active 
            FROM people 
            LIMIT 100;
        """
        cur.execute(query)
        rows = cur.fetchall()
        
        people = []
        for row in rows:
            people.append({
                "id": row[0],
                "first_name": row[1],
                "last_name": row[2],
                "age": row[3],
                "risk_score": row[4],
                "policy_start_date": row[5],
                "active": row[6]
            })
            
        cur.close()
        conn.close()
        
        return render_template('people.html', people=people, count=len(people))

    except Exception as e:
        return f"Error loading people: {str(e)}"

@app.route('/api/random-customer')
def random_customer():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Fetch a random person with a quote
        # Using TABLESAMPLE for speed if possible, but ORDER BY RANDOM() is safer for small datasets
        # Note: Schema does not have city yet, so we return a placeholder
        query = """
            SELECT p.id, p.first_name, p.last_name, q.text 
            FROM people p 
            JOIN quotes q ON p.id = q.person_id 
            ORDER BY RANDOM() 
            LIMIT 1;
        """
        cur.execute(query)
        row = cur.fetchone()
        
        cur.close()
        conn.close()
        
        if row:
            return jsonify({
                "id": row[0],
                "name": f"{row[1]} {row[2]}",
                "location": "United Kingdom", # Placeholder until schema update
                "quote": row[3],
                "status": "Active"
            })
        else:
            return jsonify({"error": "No data found. Is Frank running?"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Run on 0.0.0.0 to be accessible via Tailscale if running on Bunny/Mac
    # Port 5000 is often taken by macOS Control Center (AirPlay), so we use 5001
    app.run(host='0.0.0.0', port=5001, debug=True)
