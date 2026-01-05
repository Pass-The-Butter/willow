
import os
import requests
from dotenv import load_dotenv

load_dotenv()

def execute(message: str, token: str = None, chat_id: str = None) -> bool:
    """
    Sends a message to the N8N Telegram Grapevine (or any Telegram chat).
    
    Args:
        message (str): The message to send.
        token (str, optional): Telegram Bot Token. Defaults to TELEGRAM_BOT_TOKEN env var.
        chat_id (str, optional): Telegram Chat ID. Defaults to TELEGRAM_CHAT_ID env var.
    
    Returns:
        bool: True if successful, False otherwise.
    """
    token = token or os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = chat_id or os.getenv("TELEGRAM_CHAT_ID")
    
    if not token or not chat_id:
        print("⚠️ Telegram token or chat_id missing. Skipping notification.")
        return False

    try:
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        payload = {"chat_id": chat_id, "text": message, "parse_mode": "Markdown"}
        response = requests.post(url, json=payload, timeout=5)
        response.raise_for_status()
        print("📨 Telegram notification sent.")
        return True
    except Exception as e:
        print(f"⚠️ Failed to send Telegram: {e}")
        return False

if __name__ == "__main__":
    # Test execution
    execute("Hello from the Change Manager's telegraph skill! 🍇")
