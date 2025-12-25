# 🔒 Tailscale SSL & Overlay Mesh Strategy ("Pass-The-Butter")

> "It's an Overlay mesh VPN especially for this type of thing."

## The Goal

Move away from temporary, fragile HTTP tunnels (`n8n start --tunnel`) and `localhost` port forwarding.
Adopts **Tailscale Funnel** to expose services securely via the overlay mesh, certified by Let's Encrypt automatically handling SSL.

## The Architecture: "The Overlay"

Instead of opening Firewall ports (Dangerous) or using random Tunnels (Fragile):

1.  **Bunny** joins the Tailnet (User: `Pass-The-Butter`).
2.  **MagicDNS** assigns `bunny.tailnet-name.ts.net`.
3.  **Tailscale Serve/Funnel** maps internal ports (5678) to the public internet OR just the mesh.

## Implementation Steps (The Plumber's Protocol)

### 1. Install Tailscale on Bunny

```bash
curl -fsSL https://tailscale.com/install.sh | sh
sudo tailscale up
# Authenticate with "Pass-The-Butter" credentials
```

### 2. Enable HTTPS (SSL)

Tailscale handles certs for us.

```bash
sudo tailscale cert bunny.tailnet-name.ts.net
```

### 3. Expose N8N (The "Funnel")

We want N8N to be reachable by Telegram (Public Internet) securely.

```bash
# Allow public traffic to hit port 443 (SSL) and route to local 5678
sudo tailscale funnel --bg --https=443 localhost:5678
```

### 4. Update N8N Configuration

We verify the funnel URL (e.g., `https://bunny.camel-crocodile.ts.net`) and update `.env`:

```bash
N8N_WEBHOOK_URL=https://bunny.camel-crocodile.ts.net/
```

Then we restart N8N **without** `--tunnel`.

## Benefits

- **Security**: Minimal attack surface. Traffic enters via WireGuard node.
- **Persistence**: URL stays the same across restarts.
- **Identity**: We use "Pass-The-Butter" ACLs to control who manages the node.
