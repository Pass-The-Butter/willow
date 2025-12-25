# 🚀 BUNNY DEPLOYMENT TASK - Engineering Agent

**Assigned To**: Engineering Agent
**Priority**: HIGH (blocks everything else)
**Estimated Time**: 1-2 hours
**Cost**: $0 (uses existing infrastructure)
**Status**: Ready to execute

---

## 🎯 OBJECTIVE

Deploy full AgileMesh.net stack on Bunny server:
1. ✅ N8N community edition (workflow automation)
2. ✅ AgileMesh.net website (Peter's consulting business)
3. ✅ Willow dashboard (live demo at /willow)
4. ✅ Cloudflare Tunnel (public access to agilemesh.net)
5. ✅ Email server (optional: willow@agilemesh.net, peter@agilemesh.net)

---

## 🖥️ INFRASTRUCTURE DETAILS

**Server**: Bunny
- **SSH Access**: `ssh peter@bunny` (via Tailscale)
- **OS**: Ubuntu
- **RAM**: 128GB
- **Network**: Tailscale mesh (`bunny` on tailnet)
- **Existing Services**: PostgreSQL (population database)
- **Docker**: Installed (verify: `docker --version`)

**Public Access Strategy**:
- Cloudflare Tunnel (no open ports, secure, free)
- Domain: agilemesh.net (Peter already owns)
- URLs:
  - https://agilemesh.net → Website homepage
  - https://agilemesh.net/willow → Willow dashboard
  - https://n8n.agilemesh.net → N8N interface

---

## 📋 DEPLOYMENT STEPS

### **Step 1: Prepare Bunny** ⏱️ 10 minutes

```bash
# SSH to Bunny
ssh peter@bunny

# Create project directory
mkdir -p ~/agilemesh
cd ~/agilemesh

# Create subdirectories
mkdir -p {website,n8n,email,config}

# Install Cloudflare Tunnel (cloudflared)
wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb
sudo dpkg -i cloudflared-linux-amd64.deb
cloudflared version  # Verify installation
```

---

### **Step 2: Create Docker Compose Stack** ⏱️ 15 minutes

Create `~/agilemesh/docker-compose.yml`:

```yaml
version: '3.8'

services:
  # N8N Workflow Automation
  n8n:
    image: n8nio/n8n:latest
    container_name: agilemesh-n8n
    restart: unless-stopped
    ports:
      - "5678:5678"
    environment:
      - N8N_BASIC_AUTH_ACTIVE=true
      - N8N_BASIC_AUTH_USER=willow
      - N8N_BASIC_AUTH_PASSWORD=${N8N_PASSWORD}
      - N8N_HOST=n8n.agilemesh.net
      - N8N_PORT=5678
      - N8N_PROTOCOL=https
      - WEBHOOK_URL=https://n8n.agilemesh.net/
      - GENERIC_TIMEZONE=Europe/London
      - DB_TYPE=postgresdb
      - DB_POSTGRESDB_HOST=postgres
      - DB_POSTGRESDB_PORT=5432
      - DB_POSTGRESDB_DATABASE=n8n
      - DB_POSTGRESDB_USER=n8n
      - DB_POSTGRESDB_PASSWORD=${POSTGRES_PASSWORD}
    volumes:
      - ./n8n/data:/home/node/.n8n
      - ./n8n/files:/files
    depends_on:
      - postgres
    networks:
      - agilemesh

  # PostgreSQL for N8N
  postgres:
    image: postgres:15-alpine
    container_name: agilemesh-postgres
    restart: unless-stopped
    environment:
      - POSTGRES_USER=n8n
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
      - POSTGRES_DB=n8n
    volumes:
      - ./postgres/data:/var/lib/postgresql/data
    networks:
      - agilemesh

  # AgileMesh.net Website + Willow Dashboard
  website:
    image: python:3.11-slim
    container_name: agilemesh-website
    restart: unless-stopped
    working_dir: /app
    ports:
      - "8000:8000"
    environment:
      - FLASK_APP=app.py
      - FLASK_ENV=production
      - NEO4J_URI=${NEO4J_URI}
      - NEO4J_USER=${NEO4J_USER}
      - NEO4J_PASSWORD=${NEO4J_PASSWORD}
      - PG_HOST=bunny
      - PG_PORT=5432
      - PG_DB=population
      - PG_USER=willow
      - PG_PASS=${PG_PASS}
    volumes:
      - ./website:/app
      - /Volumes/Delila/dev/Willow:/willow:ro
    command: >
      sh -c "pip install -q flask neo4j psycopg2-binary python-dotenv certifi &&
             python app.py"
    networks:
      - agilemesh

  # Cloudflare Tunnel
  cloudflared:
    image: cloudflare/cloudflared:latest
    container_name: agilemesh-tunnel
    restart: unless-stopped
    command: tunnel --no-autoupdate run
    environment:
      - TUNNEL_TOKEN=${CLOUDFLARE_TUNNEL_TOKEN}
    networks:
      - agilemesh

networks:
  agilemesh:
    driver: bridge
```

---

### **Step 3: Create Environment Variables** ⏱️ 5 minutes

Create `~/agilemesh/.env`:

```bash
# N8N
N8N_PASSWORD=GENERATE_STRONG_PASSWORD_HERE

# PostgreSQL
POSTGRES_PASSWORD=GENERATE_STRONG_PASSWORD_HERE

# AuraDB (from main Willow .env)
NEO4J_URI=neo4j+s://e59298d2.databases.neo4j.io
NEO4J_USER=neo4j
NEO4J_PASSWORD=COPY_FROM_WILLOW_ENV

# Bunny PostgreSQL (Population DB)
PG_PASS=willowdev123

# Cloudflare Tunnel (will be filled after Step 5)
CLOUDFLARE_TUNNEL_TOKEN=WILL_BE_GENERATED_IN_STEP_5
```

**Security Note**: Generate strong passwords, don't use defaults!

---

### **Step 4: Create Website Application** ⏱️ 20 minutes

Create `~/agilemesh/website/app.py`:

```python
from flask import Flask, render_template, jsonify
import os
import certifi
from neo4j import GraphDatabase
import psycopg2

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)

# Set SSL certificate
os.environ['SSL_CERT_FILE'] = certifi.where()

# Homepage
@app.route('/')
def home():
    return render_template('index.html')

# Willow Dashboard
@app.route('/willow')
def willow_dashboard():
    """Live Willow metrics dashboard"""

    # Query AuraDB for real-time stats
    driver = GraphDatabase.driver(
        os.getenv('NEO4J_URI'),
        auth=(os.getenv('NEO4J_USER'), os.getenv('NEO4J_PASSWORD'))
    )

    with driver.session() as session:
        # Get domain stats
        domains = session.run("""
            MATCH (d:Domain)-[:HAS_COMPONENT]->(c:Component)-[:HAS_TASK]->(t:Task)
            RETURN d.name as domain,
                   count(DISTINCT c) as components,
                   count(t) as total_tasks,
                   sum(CASE WHEN t.status = 'Complete' THEN 1 ELSE 0 END) as completed_tasks
            ORDER BY d.name
        """).data()

        # Get idea stats
        ideas = session.run("""
            MATCH (i:Idea)
            RETURN count(i) as total,
                   sum(CASE WHEN i.priority = 'Critical' THEN 1 ELSE 0 END) as critical,
                   sum(CASE WHEN i.priority = 'High' THEN 1 ELSE 0 END) as high,
                   sum(CASE WHEN i.priority = 'Medium' THEN 1 ELSE 0 END) as medium
        """).single()

    driver.close()

    # Get population database stats
    conn = psycopg2.connect(
        host=os.getenv('PG_HOST'),
        port=os.getenv('PG_PORT'),
        database=os.getenv('PG_DB'),
        user=os.getenv('PG_USER'),
        password=os.getenv('PG_PASS')
    )
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM customers")
    customer_count = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM pets")
    pet_count = cur.fetchone()[0]
    cur.close()
    conn.close()

    return render_template('willow.html',
                          domains=domains,
                          ideas=ideas,
                          customers=customer_count,
                          pets=pet_count)

# API endpoint for live metrics
@app.route('/api/metrics')
def metrics():
    # Same as above but return JSON
    pass

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
```

Create `~/agilemesh/website/templates/index.html`:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AgileMesh - Graph Databases Made Simple</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            line-height: 1.6;
            color: #333;
        }
        .container { max-width: 1200px; margin: 0 auto; padding: 0 20px; }

        /* Hero Section */
        .hero {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 100px 20px;
            text-align: center;
        }
        .hero h1 { font-size: 3em; margin-bottom: 20px; }
        .hero p { font-size: 1.5em; margin-bottom: 30px; opacity: 0.9; }
        .cta-button {
            display: inline-block;
            padding: 15px 40px;
            background: white;
            color: #667eea;
            text-decoration: none;
            border-radius: 5px;
            font-weight: bold;
            margin: 10px;
            transition: transform 0.2s;
        }
        .cta-button:hover { transform: translateY(-2px); }

        /* Services Section */
        .services {
            padding: 80px 20px;
            background: #f8f9fa;
        }
        .services h2 {
            text-align: center;
            font-size: 2.5em;
            margin-bottom: 50px;
        }
        .service-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 30px;
        }
        .service-card {
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .service-card h3 { color: #667eea; margin-bottom: 15px; }

        /* Showcase Section */
        .showcase {
            padding: 80px 20px;
            text-align: center;
        }
        .showcase h2 { font-size: 2.5em; margin-bottom: 30px; }
        .showcase-box {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 60px;
            border-radius: 15px;
            margin: 30px 0;
        }
        .showcase-box h3 { font-size: 2em; margin-bottom: 20px; }

        /* Contact Section */
        .contact {
            padding: 80px 20px;
            background: #f8f9fa;
            text-align: center;
        }
        .contact h2 { font-size: 2.5em; margin-bottom: 30px; }
        .contact-links a {
            display: inline-block;
            margin: 10px 20px;
            color: #667eea;
            text-decoration: none;
            font-size: 1.2em;
        }

        footer {
            background: #333;
            color: white;
            text-align: center;
            padding: 30px;
        }
    </style>
</head>
<body>
    <div class="hero">
        <div class="container">
            <h1>AgileMesh</h1>
            <p>Graph Databases Made Simple</p>
            <p style="font-size: 1.2em;">Helping companies adopt Neo4j & Tailscale<br>
            The easier alternative to Data Mesh complexity</p>
            <a href="mailto:peter@agilemesh.net" class="cta-button">Book Consultation</a>
            <a href="/willow" class="cta-button">View Live Demo</a>
        </div>
    </div>

    <div class="services">
        <div class="container">
            <h2>Services</h2>
            <div class="service-grid">
                <div class="service-card">
                    <h3>🔗 Tailscale Mesh Networking</h3>
                    <p>Secure, zero-config VPN for connecting your infrastructure. Simpler than traditional VPNs.</p>
                </div>
                <div class="service-card">
                    <h3>📊 Neo4j Graph Databases</h3>
                    <p>Implementation and consulting. Faster than SQL for relationship queries, easier than Data Mesh.</p>
                </div>
                <div class="service-card">
                    <h3>🤖 AI-Powered Automation</h3>
                    <p>Workflow automation using N8N + AI agents. Autonomous operations without manual overhead.</p>
                </div>
                <div class="service-card">
                    <h3>💡 Data Mesh Alternative</h3>
                    <p>Graph databases offer simpler architecture than Data Mesh with better performance for connected data.</p>
                </div>
            </div>
        </div>
    </div>

    <div class="showcase">
        <div class="container">
            <h2>Case Study: Willow AI</h2>
            <div class="showcase-box">
                <h3>Live Demonstration</h3>
                <p>Willow is an AI-native organization running entirely on graph databases and automated workflows.</p>
                <p style="margin: 20px 0;">
                    • Multi-agent coordination via Neo4j<br>
                    • Autonomous task delegation<br>
                    • Real-time metrics and monitoring<br>
                    • 500-1000% ROI demonstrated
                </p>
                <a href="/willow" class="cta-button">View Live Dashboard →</a>
            </div>
        </div>
    </div>

    <div class="contact">
        <div class="container">
            <h2>Get Started</h2>
            <p style="font-size: 1.2em; margin-bottom: 30px;">
                Ready to simplify your data architecture?
            </p>
            <div class="contact-links">
                <a href="mailto:peter@agilemesh.net">📧 peter@agilemesh.net</a>
                <a href="https://linkedin.com/in/YOUR_LINKEDIN" target="_blank">💼 LinkedIn</a>
                <a href="https://linkedin.com/company/willow-ai" target="_blank">🤖 Willow AI</a>
            </div>
        </div>
    </div>

    <footer>
        <div class="container">
            <p>&copy; 2025 AgileMesh. Graph Databases Made Simple.</p>
            <p style="margin-top: 10px; opacity: 0.7;">Built by Peter [LastName] | Powered by Neo4j & Willow AI</p>
        </div>
    </footer>
</body>
</html>
```

Create `~/agilemesh/website/templates/willow.html` (similar styling, shows live dashboard)

---

### **Step 5: Set Up Cloudflare Tunnel** ⏱️ 15 minutes

```bash
# Login to Cloudflare (opens browser)
cloudflared tunnel login

# Create tunnel
cloudflared tunnel create agilemesh

# This generates a credentials file and tunnel ID
# Copy the tunnel token from output

# Create tunnel config
cat > ~/.cloudflared/config.yml <<EOF
tunnel: agilemesh
credentials-file: /home/peter/.cloudflared/<TUNNEL_ID>.json

ingress:
  - hostname: agilemesh.net
    service: http://localhost:8000
  - hostname: www.agilemesh.net
    service: http://localhost:8000
  - hostname: n8n.agilemesh.net
    service: http://localhost:5678
  - service: http_status:404
EOF

# Add tunnel token to .env
echo "CLOUDFLARE_TUNNEL_TOKEN=<your_token_here>" >> ~/agilemesh/.env

# Route DNS (in Cloudflare dashboard):
# Go to Zero Trust → Networks → Tunnels → agilemesh → Public Hostnames
# Add:
#   - agilemesh.net → http://localhost:8000
#   - www.agilemesh.net → http://localhost:8000
#   - n8n.agilemesh.net → http://localhost:5678
```

---

### **Step 6: Deploy Everything** ⏱️ 5 minutes

```bash
cd ~/agilemesh

# Start the stack
docker compose up -d

# Check services
docker compose ps

# View logs
docker compose logs -f

# Test locally
curl http://localhost:8000
curl http://localhost:5678
```

---

### **Step 7: Verify Public Access** ⏱️ 5 minutes

```bash
# From your Mac (or any device):
curl https://agilemesh.net
# Should return HTML homepage

curl https://n8n.agilemesh.net
# Should return N8N login page
```

**Access**:
- https://agilemesh.net - Public website
- https://agilemesh.net/willow - Willow dashboard
- https://n8n.agilemesh.net - N8N (login: willow / password from .env)

---

## 📧 OPTIONAL: Email Server Setup

If Peter wants dedicated email (not just Cloudflare forwarding):

```yaml
# Add to docker-compose.yml:
  mailserver:
    image: mailserver/docker-mailserver:latest
    container_name: agilemesh-mail
    hostname: mail.agilemesh.net
    ports:
      - "25:25"
      - "587:587"
      - "993:993"
    volumes:
      - ./mail/data:/var/mail
      - ./mail/state:/var/mail-state
      - ./mail/config:/tmp/docker-mailserver
    environment:
      - ENABLE_SPAMASSASSIN=1
      - ENABLE_CLAMAV=1
      - ENABLE_FAIL2BAN=1
      - ONE_DIR=1
    networks:
      - agilemesh
```

Then create accounts:
```bash
docker exec -it agilemesh-mail setup email add willow@agilemesh.net PASSWORD
docker exec -it agilemesh-mail setup email add peter@agilemesh.net PASSWORD
```

---

## ✅ SUCCESS CRITERIA

**Deployment successful when**:
1. ✅ https://agilemesh.net loads (Peter's business site)
2. ✅ https://agilemesh.net/willow shows live Willow dashboard
3. ✅ https://n8n.agilemesh.net accessible (workflow automation)
4. ✅ All services running (`docker compose ps` shows 4 containers)
5. ✅ No errors in logs (`docker compose logs`)

---

## 🔐 SECURITY CHECKLIST

- [x] Strong passwords in .env (not defaults)
- [x] N8N basic auth enabled
- [x] Cloudflare Tunnel (no exposed ports)
- [x] SSL/TLS via Cloudflare (automatic)
- [x] .env file permissions (chmod 600)
- [x] Regular updates (docker compose pull)

---

## 📊 MONITORING

Add health checks to monitor services:

```bash
# Create cron job for health checks
crontab -e

# Add:
*/5 * * * * curl -f https://agilemesh.net/health || echo "Website down" | mail -s "AgileMesh Alert" peter@agilemesh.net
*/5 * * * * curl -f https://n8n.agilemesh.net || echo "N8N down" | mail -s "N8N Alert" peter@agilemesh.net
```

---

## 🆘 TROUBLESHOOTING

**Website not loading**:
```bash
docker compose logs website
# Check for Python errors

docker compose restart website
```

**N8N not accessible**:
```bash
docker compose logs n8n
# Check PostgreSQL connection

docker compose restart n8n
```

**Cloudflare Tunnel issues**:
```bash
docker compose logs cloudflared
# Check tunnel status

cloudflared tunnel info agilemesh
```

---

## 📝 HANDOFF TO PM AGENT

**When complete**:
1. Create Linear task: "Deployment complete - verify public access"
2. Assign to: Peter (for verification)
3. Log to AuraDB diary:
   - Deployment timestamp
   - All URLs (agilemesh.net, n8n.agilemesh.net)
   - Credentials stored where
   - Any issues encountered

**Next tasks after deployment**:
- Marketing Agent: Populate website content
- Engineering Agent: Build N8N workflows
- Peter: Create Willow LinkedIn account
- Peter: Update personal LinkedIn with AgileMesh

---

**Estimated Total Time**: 1-2 hours
**Cost**: $0/month
**Status**: Ready to execute

**Engineering Agent: You have permission to proceed. Execute this deployment.**
