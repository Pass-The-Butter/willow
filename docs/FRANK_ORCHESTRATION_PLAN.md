# Frank Orchestration & Control Plan

This document outlines the strategy for controlling "Frank" (Windows 11 Node) from the rest of the Willow infrastructure. We utilize a **Hybrid Control Plane** approach, leveraging SSH for infrastructure tasks and N8N for AI agent orchestration.

## 1. The Architecture

*   **Controller (Mac)**: Development, Git Source of Truth, Manual Triggers.
*   **Database (Bunny/Xeon)**: Postgres (Population), Neo4j (Graph), **N8N (Orchestrator)**.
*   **Compute (Frank/Win11)**: Ollama (Inference), Python Scripts (Population Generation).

## 2. Control Methods

### A. Infrastructure Layer (SSH via Tailscale)
**Use Case:** System maintenance, running heavy one-off scripts (e.g., Population Generator), updates.
**Mechanism:**
1.  **Tailscale**: Provides a secure mesh network. Frank is accessible at `frank` (or its Tailscale IP).
2.  **OpenSSH Server**: Running on Frank.
3.  **PowerShell**: The shell environment on Frank.

**Action Plan:**
*   [x] Install Tailscale on Frank.
*   [ ] Enable OpenSSH Server on Frank (via `run_on_frank.ps1`).
*   [ ] Establish SSH Key Trust (Mac -> Frank).

### B. Orchestration Layer (N8N on Bunny)
**Use Case:** AI Agent workflows, recurring tasks, "Thinking" loops.
**Mechanism:**
1.  **N8N Container**: Runs on Bunny (Docker).
2.  **Ollama API**: Frank exposes Ollama on port `11434`.
3.  **Connectivity**: N8N connects to `http://frank:11434` via Tailscale or local LAN.

**Why N8N?**
*   Visual workflow builder.
*   Can run locally on the powerful Xeon server (Bunny).
*   Can trigger "Generation" tasks on Frank via HTTP (if we run a small listener) or simply use Frank as the *Intelligence Unit* (Ollama) while N8N handles the logic.

## 3. Immediate Task: Population Generation

For the immediate goal of generating 100M entities, **Method A (SSH)** is preferred because it is a long-running, resource-intensive process that doesn't require complex decision logic, just raw execution.

### Step-by-Step Execution Plan

#### Phase 1: Bootstrap Frank (One-Time)
1.  **Manual Access**: Log into Frank physically or via Remote Desktop.
2.  **Install Tailscale**: Join the mesh.
3.  **Run Bootstrap Script**:
    *   **Option A (Git)**: Clone repo and run `.\domains\population\run_on_frank.ps1`.
    *   **Option B (Direct Download)**: Run this one-liner to bypass Git issues:
        ```powershell
        Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://raw.githubusercontent.com/Pass-The-Butter/willow/master/domains/population/run_on_frank.ps1'))
        ```

#### Phase 2: Remote Execution (Routine)
From your Mac (Controller):
```bash
# SSH into Frank
ssh user@frank

# Navigate to repo
cd C:\Users\user\dev\willow

# Run Generator
python domains/population/remote_generator.py
```

#### Phase 3: Future N8N Integration
1.  Deploy N8N on Bunny (`docker-compose`).
2.  Create N8N Workflow:
    *   **Trigger**: Cron (Every night) or Webhook.
    *   **Action**: HTTP Request to Frank (Ollama) -> "Generate a backstory for Person X".
    *   **Action**: Write to Neo4j.

## 4. Summary of Responsibilities

| Node | Role | Software |
| :--- | :--- | :--- |
| **Frank** | The Muscle & Brain | Python (Generator), Ollama (LLM), OpenSSH |
| **Bunny** | The Vault & Conductor | Postgres, Neo4j, N8N |
| **Mac** | The Architect | VS Code, Git, SSH Client |
