# ✉️ Handoff Instructions for Frank

**To**: The Agent running on Frank (Windows 11)
**From**: Arch-Willow (Mac Mini)
**Date**: 2025-12-22
**Subject**: Population Generation & Autonomy

---

## 🎯 Your Mission
You are the **Muscle**. Your primary directive is to generate a synthetic population of 100,000,000 entities. You have the compute power (Windows/GPU) and the local tools (Python/Ollama).

## 📋 Immediate Tasks

### 1. Run the Generator
The script `domains/population/remote_generator.py` is your primary tool.
*   **Target**: `bunny` (Postgres on Xeon).
*   **Locale**: `en_GB` (UK).
*   **Action**: Execute the script and keep it running. Monitor for errors.

### 2. Autonomy
*   **Do not wait for commands.** If the script stops, restart it.
*   **Monitor Resources**: Ensure you don't melt the CPU.
*   **Report Status**: We (the Mac) will check the Postgres database count to verify your progress.

## 🔮 Future Tasks (The "Leaves")
Once the population base is established, we will move to:
1.  **Quote Generation**: Using Ollama to generate unique quotes for selected individuals.
2.  **Web Interface**: We will build a frontend to showcase these people (likely hosted on Bunny).

## 🛠 Technical Notes
*   **Repo Path**: `C:\Users\peter\dev\willow`
*   **Python Env**: `.venv`
*   **Update**: Run `git pull` frequently to get the latest schemas.

---
*Good luck, Frank. We are counting on you.*
