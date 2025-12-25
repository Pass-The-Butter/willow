# Willow Infrastructure Inventory

## Network
- **Type**: Tailscale Mesh
- **Connectivity**: All devices mutually accessible via SSH/TCP.
- **Agent Access**: Allowed via SSH to any node.

## LocalCompute Resources

### 1. Dev Machine (Current Context)
- **Name**: `Mac Mini M4`
- **OS**: macOS
- **Specs**: 16GB RAM
- **Role**: 
    - Development Controller
    - Agent Host (Antigravity/Claude)
    - Codebase Source of Truth

### 2. Population Server
- **Name**: `Xeon Server` (Hostname: `bunny`)
- **OS**: Ubuntu Linux
- **Specs**: 128GB RAM
- **Access**: User `bunny` (Password provided)
- **Role**: 
    - **Population Database Host**: High-memory Postgres instance with `pgvector`.
    - **Scale**: Target 100 million "NPC" entities.
    - **Simulation**: "Infinite Library" / Sims-style evolution.

### 3. Compute Node
- **Name**: `Frank` (Hostname: `frank`)
- **OS**: Windows 11
- **Specs**: 64GB RAM, NVIDIA RTX 3090ti
- **Role**: 
    - **AI Inference**: Local LLM hosting (Ollama/VLLM).
    - **Rendering**: 3D/Unreal Engine processing for Interface domain.

## Deployment Strategy
- **Population Database**: To be deployed on `Xeon Server` (Postgres + pgvector).
- **Core Graph**: AuraDB (Cloud) - *Remains central coordinator*.
