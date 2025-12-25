# Tailscale Integration for Distributed AI System

## 1. Tailscale Overview

Tailscale creates a secure, peer-to-peer mesh network (tailnet) that connects your devices regardless of their physical location or network environment. For a distributed AI system, this provides a secure backbone for communication between agents, databases, and compute nodes.

### Key Features

*   **Mesh Network**: Devices connect directly to each other (NAT traversal) rather than tunneling through a central gateway. This reduces latency and improves throughput, which is critical for AI data flows.
*   **Access Control Lists (ACLs)**: Fine-grained control over which devices and users can communicate. Policies are defined in a `huJSON` format and are deny-by-default.
    *   *Relevance*: Isolate sensitive components (e.g., "Frank" the Windows workstation) from public-facing parts of the system.
*   **Tailscale SSH**: Allows SSH access to devices using Tailscale identity for authentication instead of managing SSH key pairs.
    *   *Relevance*: Secure, keyless access to remote nodes for maintenance and deployment. Supports "Check Mode" to require re-authentication for sensitive sessions.
*   **Tailscale Serve**: Expose local services (like a development server or internal API) to other devices within the tailnet.
    *   *Relevance*: Share internal AI agent APIs or dashboards securely within the private network.
*   **Tailscale Funnel**: Expose a local service to the public internet via a secure tunnel and a public URL (e.g., `https://node.tailnet.ts.net`).
    *   *Relevance*: Temporarily expose a webhook endpoint or a demo interface to the outside world without configuring firewalls.

## 2. Tailscale API

The Tailscale API allows for programmatic management of the tailnet, enabling automation of infrastructure tasks.

*   **Authentication**: Uses Access Tokens (API Keys) generated from the Admin Console or OAuth clients for scoped access.
*   **Capabilities**:
    *   **Device Management**: List devices, delete devices, update device attributes (e.g., tags).
    *   **ACL Management**: Retrieve and update the tailnet policy file (ACLs) programmatically. This enables "Infrastructure as Code" for network security.
    *   **Key Management**: Generate auth keys for registering new devices (e.g., ephemeral keys for containers).
    *   **DNS**: Manage MagicDNS settings and nameservers.

## 3. Tailscale MCP (Model Context Protocol)

There is currently no official "Tailscale MCP" server available. However, one can be built to allow AI agents to manage the network infrastructure.

### Building a Tailscale MCP Server

An MCP server can be developed (e.g., in Python using the `mcp` library) to wrap the Tailscale API.

**Proposed Tools:**

1.  `list_devices()`: Returns a list of devices in the tailnet with their status, IP addresses, and tags.
2.  `get_acl_policy()`: Retrieves the current ACL JSON policy.
3.  `update_acl_policy(new_policy_json)`: Updates the ACL policy (carefully, with validation).
4.  `generate_auth_key(tags, ephemeral=True)`: Creates a new auth key for onboarding a new node (e.g., a new Docker container).
5.  `get_device_details(device_id)`: detailed info for a specific node.

**Implementation Strategy:**
*   Use the `tailscale` Python SDK or direct HTTP requests to `https://api.tailscale.com/api/v2/`.
*   Secure the API Key via environment variables.
*   Implement strict validation for `update_acl_policy` to prevent locking out the agent.

## 4. Windows SSH Setup (for "Frank")

To enable "Frank" (Windows 11) as a remote node accessible via SSH:

### Step 1: Install OpenSSH Server
Open PowerShell as Administrator and run:
```powershell
# Check if installed
Get-WindowsCapability -Online | Where-Object Name -like 'OpenSSH.Server*'

# Install if not present
Add-WindowsCapability -Online -Name OpenSSH.Server~~~~0.0.1.0
```

### Step 2: Start and Configure Service
```powershell
# Start the sshd service
Start-Service sshd

# Set to start automatically on boot
Set-Service -Name sshd -StartupType 'Automatic'
```

### Step 3: Verify Firewall
Ensure the firewall allows inbound SSH traffic (usually configured automatically during installation):
```powershell
if (!(Get-NetFirewallRule -Name "OpenSSH-Server-In-TCP" -ErrorAction SilentlyContinue)) {
    New-NetFirewallRule -Name 'OpenSSH-Server-In-TCP' -DisplayName 'OpenSSH Server (sshd)' -Enabled True -Direction Inbound -Protocol TCP -Action Allow -LocalPort 22
}
```

### Step 4: Tailscale SSH (Optional but Recommended)
If Tailscale is installed on Frank, you can enable Tailscale SSH to bypass standard SSH key management:
```powershell
tailscale set --ssh
```
*Note: This requires ACLs to allow SSH access from your source device.*

## 5. Connecting Arch-Willow (Mac) to Frank (Windows)

To enable the AI agent (Arch-Willow) to control Frank remotely, we establish an SSH trust.

### The "Plumbing" (SSH Key Setup)

1.  **Get Arch-Willow's Public Key**:
    ```bash
    cat ~/.ssh/id_ed25519.pub
    # Output: ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIAbGLxzNfR58nZM38+LVhcgz/qlPPcHPxcfAO+86F2eT peter@Lisa.local
    ```

2.  **Authorize on Frank**:
    Run this PowerShell block on Frank (as Administrator) to allow Arch-Willow in:
    ```powershell
    $Key = "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIAbGLxzNfR58nZM38+LVhcgz/qlPPcHPxcfAO+86F2eT peter@Lisa.local"
    
    # Create .ssh directory if missing
    $sshPath = "$env:ProgramData\ssh"
    if (!(Test-Path $sshPath)) { New-Item -Path $sshPath -ItemType Directory }
    
    # Add key to administrators_authorized_keys
    Add-Content -Path "$sshPath\administrators_authorized_keys" -Value $Key
    
    # Set permissions (Critical for Windows SSH)
    $acl = Get-Acl "$sshPath\administrators_authorized_keys"
    $ar = New-Object System.Security.AccessControl.FileSystemAccessRule("NT AUTHORITY\SYSTEM", "FullControl", "Allow")
    $acl.SetAccessRule($ar)
    $ar = New-Object System.Security.AccessControl.FileSystemAccessRule("BUILTIN\Administrators", "FullControl", "Allow")
    $acl.SetAccessRule($ar)
    Set-Acl "$sshPath\administrators_authorized_keys" $acl
    ```

3.  **Verify Connection**:
    From Arch-Willow:
    ```bash
    ssh peter@frank
    ```
