#!/bin/bash
# Deploy Services on Bunny (Xeon Server)

echo "🐰 Bunny Deployment Sequence Initiated..."

# 1. Setup Python Environment for Dashboard
echo "Setting up Python Venv..."
if [ ! -d ".venv" ]; then
    python3 -m venv .venv
fi
source .venv/bin/activate

echo "Installing Dashboard dependencies..."
pip install -r requirements.txt

# 2. Start Dashboard (Background)
# Check if already running
if pgrep -f "domains/interface/app.py" > /dev/null; then
    echo "Dashboard already running. Restarting..."
    pkill -f "domains/interface/app.py"
    nohup python domains/interface/app.py > dashboard.log 2>&1 &
else
    echo "Starting Dashboard..."
    nohup python domains/interface/app.py > dashboard.log 2>&1 &
fi

# 3. Configure Tailscale Serve
# Note: Requires user to be Operator or Root. Assuming user 'bunny' has permissions.
echo "Configuring Tailscale Funnel..."

# We use 'tailscale serve' to proxy localhost ports to the Tailnet URL
# Root / -> Dashboard (5001)
tailscale serve --bg --set-path / http://127.0.0.1:5001

# /n8n -> N8N (5678)
tailscale serve --bg --set-path /n8n http://127.0.0.1:5678

# /api -> Willow API (8000)
tailscale serve --bg --set-path /api http://127.0.0.1:8000

# /graphiti -> Graphiti Memory (8002)
tailscale serve --bg --set-path /graphiti http://127.0.0.1:8002

echo "✅ Deployment Configuration Complete."
echo "Status:"
tailscale serve status
