from fastapi import FastAPI
from .config import Settings
from .gmail_client import fetch_unread_emails

from .ai_service import extract_task_from_email
from .priority import apply_priority_rules
from .gmail_client import fetch_unread_emails

from datetime import datetime
import pytz

app = FastAPI()
settings = Settings()

@app.get("/")
def root():
    return {"status": "Smart Email Agent backend running!"}

@app.get("/test-gmail")
def test_gmail():
    try:
        emails = fetch_unread_emails()
        return {"count": len(emails), "emails": emails}
    except Exception as e:
        return {"error": str(e)}

@app.get("/process-email-test")
def process_test():
    emails = fetch_unread_emails()
    emails = emails[:1]
    results = []

    # india_timezone = pytz.timezone("Asia/Kolkata")
    # today_date = datetime.now(india_timezone).date()

    for mail in emails:
        ai_data = extract_task_from_email(mail["body"])
        ai_data = apply_priority_rules(ai_data, mail["sender"], mail["subject"])

        ai_data["raw_email_id"] = mail["id"]
        ai_data["raw_subject"] = mail["subject"]
        ai_data["raw_sender"] = mail["sender"]

        results.append(ai_data)

    return results
