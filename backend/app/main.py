from fastapi import FastAPI
from .config import Settings
from .gmail_client import fetch_unread_emails

from .ai_service import extract_task_from_email
from .priority import apply_priority_rules
from .gmail_client import fetch_unread_emails
from .task_repository import save_task

from datetime import datetime
import pytz

app = FastAPI()
settings = Settings()

from .calendar_client import create_calendar_event

@app.get("/test-calendar")  
def test_calendar():
    sample_task = {
        "task_title": "Test Auto Event",
        "deadline": "2025-02-04T18:00:00",
        "priority": "HIGH",
        "raw_subject": "Testing Event",
        "raw_sender": "system@test"
    }
    
    return create_calendar_event(sample_task)


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
    # emails = emails[:1]
    results = []

    india_timezone = pytz.timezone("Asia/Kolkata")
    today_date = datetime.now(india_timezone).date()

    todays_emails = []
    for mail in emails:
        gmail_timestamp = int(mail["timestamp"])  # Gmail gives epoch ms
        email_dt = datetime.fromtimestamp(gmail_timestamp / 1000, india_timezone)

        if email_dt.date() == today_date:
            todays_emails.append(mail)

    todays_emails = todays_emails[:5]

    for mail in todays_emails:
        ai_data = extract_task_from_email(mail["body"])
        ai_data = apply_priority_rules(ai_data, mail["sender"], mail["subject"])

        ai_data["raw_email_id"] = mail["id"]
        ai_data["raw_subject"] = mail["subject"]
        ai_data["raw_sender"] = mail["sender"]

        saved = save_task(ai_data)
        results.append(saved)

    return results
