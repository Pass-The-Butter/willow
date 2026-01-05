
import os
import smtplib
from email.message import EmailMessage
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

def execute(to_email: str, subject: str, body: str, smtp_config: Optional[dict] = None) -> bool:
    """
    Sends an email using SMTP credentials from environment or arguments.
    Gracefully falls back to a dry run if credentials are missing.

    Args:
        to_email (str): Recipient email address.
        subject (str): Email subject.
        body (str): Email body content.
        smtp_config (dict, optional): Dictionary containing SMTP config. 
                                      Keys: HOST, PORT, USER, PASS, FROM.
                                      Defaults to os.environ.

    Returns:
        bool: True if sent (or dry run successful), False on error.
    """
    # Load config from env if not provided
    config = smtp_config or os.environ
    
    host = config.get("SMTP_HOST")
    port = config.get("SMTP_PORT")
    user = config.get("SMTP_USER")
    password = config.get("SMTP_PASS")
    sender = config.get("SMTP_FROM") or user

    # Dry Run / Missing Config Check
    if not all([host, port, user, password]):
        print(f"⚠️  [DRY RUN] Email Config Missing. Would have sent email to: {to_email}")
        print(f"   Subject: {subject}")
        print(f"   Body Preview: {body[:50]}...")
        return True # Return True to indicate logic flow success even without actual send

    try:
        msg = EmailMessage()
        msg.set_content(body)
        msg['Subject'] = subject
        msg['From'] = sender
        msg['To'] = to_email

        # Convert port to int, default to 587
        port = int(port) if port else 587

        with smtplib.SMTP(host, port) as server:
            server.starttls()
            server.login(user, password)
            server.send_message(msg)
        
        print(f"📧 Email sent successfully to {to_email}")
        return True

    except Exception as e:
        print(f"❌ Failed to send email: {e}")
        return False

if __name__ == "__main__":
    # Test dry run
    execute("test@example.com", "Test Subject", "This is a test body.")
