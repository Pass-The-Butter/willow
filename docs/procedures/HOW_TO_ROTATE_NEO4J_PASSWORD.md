# 🔐 SOP: How to Rotate Neo4j AuraDB Password

**To**: Peter (Board Member / Human Agent)
**From**: Project Management Office (PMO)
**Date**: 2025-12-25
**Ticket**: [PENDING-LINEAR-SETUP]

---

## 🚨 Context
Our public repository contains a hardcoded password for the Neo4j instance "The Brain". For security compliance, this must be rotated immediately.

## 🛠️ Instructions

### Step 1: Rotate in Neo4j (The Brain)
1. Log in to the **[Neo4j Aura Console](https://console.neo4j.io)**.
   - Use your credentials (email/password).
2. Locate the instance named **"Instance01"** (or similar, URI ends in `e59298d2`).
3. Click the instance name to open details (or look for the `...` menu).
4. Select **"Password"** or **"Reset Password"**.
5. Generate a **NEW, STRONG password**.
   - Copy this password immediately. You won't see it again.
6. Confirm the reset. (The database will restart, taking 1-2 minutes).

### Step 2: Update Local Environment
1. Open your local `.env` file in VS Code:
   ```bash
   code /Volumes/Delila/dev/Willow/.env
   ```
2. Locate the line starting with `NEO4J_PASSWORD=`.
3. Replace the old value with the **NEW** password you just generated.
4. Save the file.

### Step 3: Verify Connection
1. Wait for the AuraDB instance to show "Running" in the console.
2. Run the connection test script in your terminal:
   ```bash
   cd /Volumes/Delila/dev/Willow
   source .venv/bin/activate
   python test_connections.py
   ```
3. Ensure you see: `✅ Neo4j connected!`

### Step 4: Notify PMO
1. Reply to this thread (or notify via chat) that the plumbing job is complete.
2. Mark the task as **"Ready to Test"**.

---

**Troubleshooting**:
- If `test_connections.py` fails with `AuthError`, double-check the .env file and ensure you saved it.
- If AuraDB is "Updating", wait a few more minutes.

*End of Procedure*
