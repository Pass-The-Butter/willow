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
def board():
    """Single Pane of Glass - Board Member View"""
    return render_template('board.html', resources=RESOURCES)

@app.route('/chat')
def chat():
    """Command Center - Interactive Willow Chat"""
    return render_template('chat.html')

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

@app.route('/api/organogram/business')
def get_business_organogram_data():
    """Fetches the Business Ontology entities for the visual organogram."""
    from neo4j import GraphDatabase
    import certifi
    
    uri = os.getenv("NEO4J_URI")
    user = os.getenv("NEO4J_USER")
    password = os.getenv("NEO4J_PASSWORD")
    
    os.environ['SSL_CERT_FILE'] = certifi.where()
    
    driver = GraphDatabase.driver(uri, auth=(user, password))
    
    try:
        with driver.session() as session:
            # Query for Business Entities and their Relationships
            result = session.run("""
                MATCH (n)
                WHERE n:Person OR n:Pet OR n:Policy OR n:Claim OR n:VetPractice OR n:Diagnosis OR n:Address OR n:Insurer
                OPTIONAL MATCH (n)-[r]->(m)
                WHERE m:Person OR m:Pet OR m:Policy OR m:Claim OR m:VetPractice OR m:Diagnosis OR m:Address OR m:Insurer
                RETURN n, r, m
            """)
            
            nodes = {}
            links = []
            
            # Helper to get label
            def get_label(node):
                if node.get('name'): return node.get('name')
                if node.get('reference_number'): return node.get('reference_number')
                if node.get('policy_number'): return node.get('policy_number')
                if node.get('description'): return node.get('description')[:20] + "..."
                if node.get('line1'): return node.get('line1')
                if node.get('code'): return node.get('code')
                return "Entity"

            def get_type(node):
                return list(node.labels)[0] if node.labels else "Unknown"

            for record in result:
                source_node = record['n']
                target_node = record['m']
                rel = record['r']
                
                # Add source node
                s_id = str(source_node.element_id)
                if s_id not in nodes:
                    nodes[s_id] = {
                        "id": s_id,
                        "label": get_label(source_node),
                        "type": get_type(source_node)
                    }
                
                if target_node and rel:
                    # Add target node
                    t_id = str(target_node.element_id)
                    if t_id not in nodes:
                        nodes[t_id] = {
                            "id": t_id,
                            "label": get_label(target_node),
                            "type": get_type(target_node)
                        }
                    
                    # Add link
                    links.append({
                        "source": s_id,
                        "target": t_id,
                        "type": type(rel).__name__
                    })
            
            return jsonify({"nodes": list(nodes.values()), "links": links})
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

@app.route('/factory')
def factory():
    """Render the GSAP Factory Floor Scrollytelling page"""
    return render_template('factory.html')

@app.route('/api/factory/story')
def get_factory_story():
    """Fetches a complete claim journey for the Factory visualization."""
    print("DEBUG: /api/factory/story requested...", flush=True)
    from core.clients.graph_client import GraphClient
    
    client = GraphClient(agent_id="WebInterface")
    
    try:
        # Query for a complete story suitable for the factory
        cypher = """
            MATCH (p:Person)-[:OWNS]->(pet:Pet)<-[:CONCERNS]-(c:Claim)-[:FILED_AGAINST]->(pol:Policy)
            OPTIONAL MATCH (pet)-[:VISITED]->(vet:VetPractice)-[:DIAGNOSED]->(d:Diagnosis)
            OPTIONAL MATCH (dec:Decision)-[:DECIDED_ON]->(c)
            RETURN properties(p) as person,
                   properties(pet) as pet,
                   properties(c) as claim,
                   properties(pol) as policy,
                   properties(vet) as vet,
                   properties(d) as diagnosis,
                   properties(dec) as decision
            ORDER BY elementId(c) DESC
            LIMIT 1
        """
        results = client.run(cypher)
        
        if not results:
            return jsonify({"status": "empty", "message": "No active claims found in the factory queue."})
        
        record = results[0]
        p = record['person']
        pet = record['pet']
        c = record['claim']
        pol = record['policy']
        vet = record['vet'] or {}
        d = record['diagnosis'] or {}
        dec = record['decision'] or {}
        
        story = {
            "person": {
                "name": p.get('name', 'Unknown'),
                "id": p.get('id', '')
            },
            "pet": {
                "name": pet.get('name', 'Unknown'),
                "species": pet.get('species', 'Animal')
            },
            "policy": {
                "insurer": "Purely Pets",
                "number": pol.get('id', 'N/A')
            },
            "event": {
                "vet_name": vet.get('name', 'Central Pet Hospital'),
                "diagnosis_code": d.get('code', 'DX-000'),
                "diagnosis_desc": d.get('description', 'Undiagnosed')
            },
            "claim": {
                "status": c.get('status', 'Pending'),
                "amount": f"£{c.get('amount', 0)}"
            },
            "decision": {
                "outcome": dec.get('decision', 'PENDING'),
                "reason": dec.get('reason', 'Under Review')
            }
        }
        
        return jsonify({"status": "success", "story": story})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/factory/graph')
def get_factory_graph():
    """Fetches the ego-graph for the latest factory claim for D3 visualization."""
    from core.clients.graph_client import GraphClient
    client = GraphClient(agent_id="WebInterface")
    
    try:
        # Serializable Node query
        cypher_nodes = """
            MATCH (p:Person)-[:OWNS]->(pet:Pet)<-[:CONCERNS]-(c:Claim)-[:FILED_AGAINST]->(pol:Policy)
            WITH p, pet, c, pol ORDER BY elementId(c) DESC LIMIT 1
            MATCH (n) WHERE n IN [p, pet, c, pol]
            OPTIONAL MATCH (pet)-[:VISITED]->(vet:VetPractice)
            OPTIONAL MATCH (vet)-[:DIAGNOSED]->(diag:Diagnosis)
            OPTIONAL MATCH (dec:Decision)-[:DECIDED_ON]->(c)
            
            WITH collect(p)+collect(pet)+collect(c)+collect(pol)+collect(vet)+collect(diag)+collect(dec) as all_nodes
            UNWIND all_nodes as n
            WITH DISTINCT n WHERE n IS NOT NULL
            RETURN elementId(n) as id, labels(n) as labels, properties(n) as props
        """
        nodes_res = client.run(cypher_nodes)
        
        # Link query
        cypher_links = """
            MATCH (p:Person)-[:OWNS]->(pet:Pet)<-[:CONCERNS]-(c:Claim)-[:FILED_AGAINST]->(pol:Policy)
            WITH p, pet, c, pol ORDER BY elementId(c) DESC LIMIT 1
            WITH [p, pet, c, pol] as core_nodes
            MATCH (n)-[r]->(m) 
            WHERE n IN core_nodes OR m IN core_nodes
            RETURN elementId(n) as source, elementId(m) as target, type(r) as type
        """
        links_res = client.run(cypher_links)
        
        return jsonify({
            "nodes": [{"id": n['id'], "label": n['props'].get('name') or n['props'].get('id') or n['labels'][0], "type": n['labels'][0], "properties": n['props']} for n in nodes_res],
            "links": links_res
        })
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/kanban')
def get_kanban_data():
    """Fetches tasks for the Kanban board from AuraDB."""
    from core.clients.graph_client import GraphClient
    client = GraphClient(agent_id="WebInterface")
    
    try:
        results = client.run("""
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
        for r in results:
            tasks.append({
                "id": r["id"],
                "title": r["title"],
                "description": r["description"],
                "status": r["status"].lower().replace(' ', '_') if r["status"] else "to_do",
                "priority": r["priority"],
                "assignee": r["assigned_to"],
                "date": r["created_at"]
            })
        
        return jsonify({"tasks": tasks})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/people')
def people_viewer():
    """Simple People Viewer: Just peek at the crowd."""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # New Schema: customers table
        query = """
            SELECT id, full_name, email, city, postcode, date_of_birth, is_active 
            FROM customers 
            LIMIT 100;
        """
        cur.execute(query)
        rows = cur.fetchall()
        
        people = []
        for row in rows:
            # Calculate age from DOB
            from datetime import date
            dob = row[5]
            today = date.today()
            age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
            
            people.append({
                "id": row[0],
                "full_name": row[1],
                "email": row[2],
                "city": row[3],
                "postcode": row[4],
                "age": age,
                "active": row[6]
            })
            
        cur.close()
        conn.close()
        
        return render_template('people.html', people=people, count=len(people))

    except Exception as e:
        return f"Error loading people: {str(e)}"

# --- Operations (Robin's) Endpoints ---

@app.route('/api/ops/stock')
def get_ops_stock():
    """Returns the 'Stock' level: Outstanding claims requiring assessment."""
    from core.clients.graph_client import GraphClient
    from datetime import datetime
    
    client = GraphClient(agent_id="WebInterface")
    
    try:
        # Stock is claims in 'Pending' or 'Under Review' status
        results = client.run("""
            MATCH (c:Claim)
            WHERE c.status IN ['Pending', 'Under Review']
            RETURN count(c) as stock_count
        """)
        stock = results[0]['stock_count'] if results else 0
        
        return jsonify({
            "status": "success",
            "stock": stock,
            "label": "Outstanding Claims (Stock)",
            "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/ops/performance')
def get_ops_performance():
    """Returns Claims per FTE per Hour for the previous week (Mock data for MVP)."""
    fte_data = [
        {"name": "Anne Farraday", "assessed": [3, 4, 2, 5, 4, 3, 4, 2], "hours": ["09:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00"]},
        {"name": "Brian Miller", "assessed": [2, 3, 3, 2, 3, 4, 3, 3], "hours": ["09:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00"]},
        {"name": "Chloe Smith", "assessed": [4, 5, 4, 1, 5, 6, 4, 5], "hours": ["09:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00"]},
        {"name": "David Jones", "assessed": [1, 2, 3, 3, 2, 2, 3, 2], "hours": ["09:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00"]}
    ]
    
    return jsonify({
        "status": "success",
        "data": fte_data,
        "period": "Last Week (Mon-Fri Average)",
        "metric": "Claims Assessed per Hour"
    })

# --- Assessor (Enrichment) Endpoints ---

@app.route('/api/submit-quote', methods=['POST'])
def submit_quote():
    """Handles manual quote submission and injects into AuraDB."""
    from core.clients.graph_client import GraphClient
    data = request.form
    
    client = GraphClient(agent_id="WebInterface")
    
    # Create Customer, Pet, and Quote in AuraDB
    cypher = """
        MERGE (p:Person {email: $email})
        SET p.name = $full_name,
            p.phone = $phone,
            p.address = $address,
            p.city = $city,
            p.postcode = $postcode,
            p.dob = $dob
            
        MERGE (pet:Pet {name: $pet_name, owner_email: $email})
        SET pet.species = $species,
            pet.breed = $breed,
            pet.gender = $gender,
            pet.microchipped = $microchipped
            
        MERGE (p)-[:OWNS]->(pet)
        
        CREATE (q:Quote {
            id: 'QT-' + randomUUID(),
            cover_type: $cover_type,
            excess: $excess,
            limit: $limit,
            timestamp: datetime()
        })
        CREATE (q)-[:FOR_PET]->(pet)
        CREATE (p)-[:REQUESTED]->(q)
        RETURN q.id as quote_id
    """
    
    try:
        params = {
            "full_name": data.get('full_name'),
            "email": data.get('email'),
            "phone": data.get('phone_mobile'),
            "address": data.get('address_line_1'),
            "city": data.get('city'),
            "postcode": data.get('postcode'),
            "dob": data.get('date_of_birth'),
            "pet_name": data.get('pet_name'),
            "species": data.get('species'),
            "breed": data.get('breed'),
            "gender": data.get('gender'),
            "microchipped": data.get('microchipped') == 'true',
            "cover_type": data.get('cover_type'),
            "excess": data.get('excess_amount'),
            "limit": data.get('vet_fee_limit')
        }
        
        results = client.run(cypher, params)
        quote_id = results[0]['quote_id'] if results else "UNKNOWN"
        
        return render_template('quote_success.html', quote_id=quote_id)
        
    except Exception as e:
        return f"Error submitting quote to Brain: {str(e)}", 500

@app.route('/api/quote/bridge-from-npc/<int:customer_id>', methods=['POST'])
def bridge_npc_to_aura(customer_id):
    """Bridges an NPC from Postgres to AuraDB as a Quote."""
    from core.clients.graph_client import GraphClient
    
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # 1. Fetch NPC Details
        cur.execute("SELECT full_name, email, phone_mobile, address_line_1, city, postcode, date_of_birth FROM customers WHERE id = %s", (customer_id,))
        c_row = cur.fetchone()
        if not c_row:
            return jsonify({"error": "Customer not found"}), 404
            
        # 2. Fetch Pet Details
        cur.execute("SELECT pet_name, species, breed, date_of_birth, gender, microchipped FROM pets WHERE customer_id = %s LIMIT 1", (customer_id,))
        p_row = cur.fetchone()
        
        # 3. Fetch a Quote Detail (or generate one)
        cur.execute("SELECT cover_type, excess_amount, vet_fee_limit, monthly_premium FROM quotes WHERE customer_id = %s LIMIT 1", (customer_id,))
        q_row = cur.fetchone()
        
        cur.close()
        conn.close()
        
        # 4. Ingest into AuraDB
        client = GraphClient(agent_id="PopulationBridge")
        
        cypher = """
            MERGE (p:Person {email: $email})
            SET p.name = $full_name,
                p.phone = $phone,
                p.city = $city,
                p.postcode = $postcode
                
            MERGE (pet:Pet {name: $pet_name, owner_email: $email})
            SET pet.species = $species,
                pet.breed = $breed,
                pet.gender = $gender
                
            MERGE (p)-[:OWNS]->(pet)
            
            CREATE (q:Quote {
                id: 'QT-BR-' + randomUUID(),
                cover_type: $cover_type,
                monthly_premium: $premium,
                source: 'PopulationBridge',
                timestamp: datetime()
            })
            CREATE (q)-[:FOR_PET]->(pet)
            CREATE (p)-[:REQUESTED]->(q)
            RETURN q.id as quote_id
        """
        
        params = {
            "full_name": c_row[0],
            "email": c_row[1],
            "phone": c_row[2],
            "city": c_row[4],
            "postcode": c_row[5],
            "pet_name": p_row[0] if p_row else "Unknown",
            "species": p_row[1] if p_row else "Dog",
            "breed": p_row[2] if p_row else "Mixed",
            "gender": p_row[4] if p_row else "Unknown",
            "cover_type": q_row[0] if q_row else "Lifetime",
            "premium": float(q_row[3]) if q_row else 25.0
        }
        
        results = client.run(cypher, params)
        return jsonify({"status": "success", "quote_id": results[0]['quote_id'] if results else "N/A"})
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/assessor/summary/<claim_ref>')
def get_assessor_summary(claim_ref):
    """Fetches the enriched summary for a specific claim."""
    from core.skills.assess_claim_context import ClaimAssessorEnrichment
    enricher = ClaimAssessorEnrichment()
    summary = enricher.get_claim_summary(claim_ref)
    return jsonify(summary)

@app.route('/api/assessor/assess_note', methods=['POST'])
def assess_claim_note():
    """Assesses the relevance of a raw note to a claim (Apollo-1 logic)."""
    from core.skills.assess_claim_context import ClaimAssessorEnrichment
    data = request.json
    claim_ref = data.get('claim_ref')
    note = data.get('note')
    
    if not claim_ref or not note:
        return jsonify({"error": "Missing claim_ref or note"}), 400
        
    enricher = ClaimAssessorEnrichment()
    assessment = enricher.assess_unstructured_relevance(claim_ref, note)
    return jsonify(assessment)

@app.route('/api/assessor/adjust', methods=['POST'])
def record_adjustment():
    """Logs a human-in-the-loop adjustment for Apollo-1 heuristic betterment."""
    from core.skills.assess_claim_context import ClaimAssessorEnrichment
    data = request.json
    claim_ref = data.get('claim_ref')
    step = data.get('step', 'General')
    adjustment = data.get('adjustment')
    
    if not claim_ref or not adjustment:
        return jsonify({"error": "Missing claim_ref or adjustment"}), 400
        
    enricher = ClaimAssessorEnrichment()
    enricher.log_assessor_adjustment(claim_ref, step, adjustment)
    return jsonify({"status": "success", "message": "Adjustment logged to Brain"})

if __name__ == '__main__':
    # Run on 0.0.0.0 to be accessible via Tailscale if running on Bunny/Mac
    # Port 5000 is often taken by macOS Control Center (AirPlay), so we use 5001
    app.run(host='0.0.0.0', port=5001, debug=True)
