from fastapi import FastAPI
from .config import Settings
from .gmail_client import fetch_unread_emails

from .ai_service import extract_task_from_email
from .priority import apply_priority_rules
from .gmail_client import fetch_unread_emails
from .task_repository import save_task
from .scheduler_jobs import process_new_emails_job

from datetime import datetime
import pytz

from apscheduler.schedulers.background import BackgroundScheduler

app = FastAPI()
settings = Settings()

scheduler = BackgroundScheduler()
scheduler.add_job(process_new_emails_job, "interval", minutes=5)
scheduler.start()

# testing routes:

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

def process_new_emails_job():
    print("Running scheduled email processing job...")

    emails = fetch_unread_emails()

    # Filter for today's emails
    india_tz = pytz.timezone("Asia/Kolkata")
    today = datetime.now(india_tz).date()

    for mail in emails:
        msg_ts = int(mail["timestamp"])
        email_dt = datetime.fromtimestamp(msg_ts / 1000, india_tz)

        if email_dt.date() != today:
            continue

        ai_data = extract_task_from_email(mail["body"])
        ai_data = apply_priority_rules(ai_data, mail["sender"], mail["subject"])

        ai_data["raw_email_id"] = mail["id"]
        ai_data["raw_subject"] = mail["subject"]
        ai_data["raw_sender"] = mail["sender"]
        ai_data["status"] = "PENDING"

        saved_task = save_task(ai_data)

        # If actionable → create calendar event
        if saved_task.get("is_actionable"):
            create_calendar_event(saved_task)

