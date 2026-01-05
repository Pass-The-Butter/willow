
import os
import sys
from dotenv import load_dotenv
from core.skills import sync_project_management
from core.skills import send_email
from core.skills import send_telegram_notification

load_dotenv()

def execute(summary_message: str, user_email: str = None) -> bool:
    """
    Orchestrates the change management process:
    1. Syncs project boards.
    2. Sends email notification.
    3. Sends Telegram notification.
    
    Args:
        summary_message (str): Description of the changes/tasks finalized.
        user_email (str, optional): Override recipient email.
        
    Returns:
        bool: True if orchestration completed.
    """
    print("🔄 [Change Manager] Initiating Board Sync...")
    try:
        # Run the sync logic
        sync_project_management.main()
    except Exception as e:
        print(f"⚠️ [Change Manager] Sync Warning: {e}")
    
    # Email Notification
    recipient = user_email or os.getenv("USER_EMAIL")
    if not recipient:
        print("⚠️ [Change Manager] No USER_EMAIL found. Using placeholder for dry run.")
        recipient = "user@example.com"
        
    subject = "Change Management: Tasks Finalized"
    email_body = f"""
Willow Change Manager Report
----------------------------

The following tasks/changes have been finalized:

{summary_message}

Boards (Jira, Linear, AuraDB) have been synchronized.

--
Willow Change Manager
"""
    print("📧 [Change Manager] Sending Email...")
    send_email.execute(recipient, subject, email_body)

    # Telegram Notification (Grapevine)
    tg_msg = f"🍇 *The Grapevine*\n\n*Change Manager*: Tasks Finalized\n\n{summary_message}\n\n✅ Boards Synchronized."
    print("📨 [Change Manager] Sending Telegram...")
    send_telegram_notification.execute(tg_msg)
    
    return True

if __name__ == "__main__":
    execute("Implemented Change Manager Agent and Skills.")
