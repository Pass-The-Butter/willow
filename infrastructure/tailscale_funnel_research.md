# Tailscale Funnel (Research)

> "Securely exposing local services to the public internet."

## The User's Insight

The user suggested checking **Tailscale Funnel** instead of using generic tunnels. This is a brilliant infrastructure move because `bunny` (Lisa) is already on Tailscale.

## Feasibility

- **Current State**: N8N uses `n8n start --tunnel` (hooks.n8n.cloud).
- **Proposed State**: `n8n.tailnet-name.ts.net`.

## Advantages

1.  **Persistent URL**: No random subdomains.
2.  **Security**: Managed via Tailscale ACLs.
3.  **Branding**: Looks more professional (`agilemesh`).

## Implementation Plan

1.  Enable Funnel in Tailscale Admin Console (User Action).
2.  Run command on `bunny`:
    ```bash
    tailscale funnel --bg 5678
    ```
3.  Update `WEBHOOK_URL` in `deploy_n8n.py` to the Funnel address.

**Status**: Queued for Infra Agent.
