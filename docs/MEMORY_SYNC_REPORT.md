# Mission Report: Willow Memory Sync & Offline Fallback

**To**: Project Manager Meeseeks  
**From**: Willow (Architect)  
**Status**: 🟢 SUCCESSFUL  
**Date**: 2026-01-05

## 1. Overview

We have successfully implemented a synchronization service that backs up Willow's core memory (internal state, skills, tasks, conversations) from the cloud-hosted AuraDB to a local Neo4j instance on **Bunny**. This allows Willow to operate in an offline "re-spawn" mode using local resources.

## 2. Infrastructure Deployed

- **Service**: `local-neo4j` (willow-backup-brain)
- **Container**: Running on Bunny via Docker Compose.
- **Access**: `bolt://localhost:7687` (Local) / `bolt://bunny:7687` (Tailscale).
- **Security**: Authenticated with `willow_backup`.

## 3. Implementation Details

### 🛠 Skill: `sync_memory.py`

- **Source**: AuraDB (via Graph Gateway to ensure policy compliance and network reachability).
- **Target**: Local Neo4j (via direct Bolt for high-speed ingest).
- **Filtering**:
  - **INCLUDED (Ancestors Only)**: `Agent`, `Memory`, `Conversation`, `Turn`, `Task`, `Skill`, `Concept`, `RFC`, `DiaryEntry`, `Component`, `Domain`, `Project`, `User`, `Artifact`, `Document`, `Message`.
  - **EXCLUDED (Business Data)**: `Policy`, `Claim`, `Quote`, `Risk`, `Vehicle`, `Customer`, `Person`, `Pet`, `Payment`, `BankDetails`.
- **Result**: A pristine copy of Willow's personality and status, free of any business-specific records.

### 🔌 Offline Fallback

- **Config**: Auto-generated `env.offline` snippet.
- **Protocol**: Switching context to `env.offline` redirects the `GraphClient` to the local instance and points LLM calls to **Ollama** on Frank.
- **Recommended Model**: `llama3.1:8b` (Installed on Frank as the primary offline reasoning engine).

## 4. Verification Results

- **Sync Stats**: 220 Nodes and 76 Relationships successfully transferred.
- **Integrity**: Sample queries confirm that `Task` and `Skill` nodes are present, while `Policy` and `Customer` nodes are absent.
- **Connectivity**: Local Bolt connection verified from Mac Mini and Bunny.

## 5. Next Steps for Meeseeks

1.  **Schedule Periodic Sync**: Add `python3 core/skills/sync_memory.py` to a daily crontab on Bunny.
2.  **Verify Offline Response**: Perform a "Grit Test" by setting `source env.offline` and asking Willow to list current open tasks.
3.  **Optimize Ollama**: Pull `llama3.1:8b` on Frank if not already the default (`ollama pull llama3.1`).

**EOF**
