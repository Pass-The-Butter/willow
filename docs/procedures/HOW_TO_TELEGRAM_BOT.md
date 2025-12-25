# 🤖 How to Connect Willow to Telegram

> "Communication is priority #1."

This guide will help you create a **Telegram Bot** (your interface to Willow) and connect it to **The Grapevine** (N8N).

## Phase 1: The BotFather (5 Minutes)

1.  Open Telegram app (Desktop or Mobile).
2.  Search for **@BotFather** (Verified account).
3.  Send the message: `/newbot`
4.  **Name your bot**: e.g., `Willow AI`
5.  **Choose a username**: Must end in `bot`, e.g., `Willow_AgileMesh_Bot`.
6.  **Copy the API Token**: It looks like `123456789:ABCdefGHIjklMNOpq...`.

## Phase 2: Add Keys to Willow (2 Minutes)

1.  Open your local `.env` file in VS Code.
2.  Paste the token:
    ```bash
    TELEGRAM_BOT_TOKEN=123456789:ABCdefGHIjklMNOpq...
    ```
3.  (Optional but recommended) send a message to `@userinfobot` to get your numeric `Chat ID` and add it to `TELEGRAM_CHAT_ID` in `.env`.

## Phase 3: Wire the Grapevine (N8N)

1.  Open your **[N8N Dashboard](http://lisa:5678)**.
    - **User**: `willow`
    - **Pass**: `willowdev123`
2.  **Add Credentials**:
    - Go to **Credentials** -> **Add Credential** -> Search "Telegram".
    - Paste your **API Token**.
    - Name it: `Telegram account`.
    - Save.
3.  **Import Workflows**:
    - Click **Workflows** -> **Import from File**.
    - Select `bootstrap/grapevine_core_workflow.json` (The Brain).
    - Select `bootstrap/telegram_listener_workflow.json` (The Ear).
4.  **Activate**:
    - Toggle "Active" switch to **ON** for both workflows.

## Phase 4: Test Contact

1.  Open your new bot in Telegram.
2.  Send: _"Willow, are you online?"_
3.  **Expected Result**:
    - Willow replies: "🍇 heard you."
    - The message is logged in AuraDB (The Diary).

---

> **Note**: This setup ensures you can talk to Willow from anywhere in the world, securely, via the Grapevine.
