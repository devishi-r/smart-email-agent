# app/scheduler_jobs.py

from datetime import datetime
import pytz
from .gmail_client import fetch_unread_emails
from .ai_service import extract_task_from_email
from .priority import apply_priority_rules
from .task_repository import save_task
from .calendar_client import create_calendar_event

def process_new_emails_job():
    print("Running scheduler job...")

    emails = fetch_unread_emails()
    india_tz = pytz.timezone("Asia/Kolkata")
    today = datetime.now(india_tz).date()

    for mail in emails:
        ts = int(mail["timestamp"])
        email_dt = datetime.fromtimestamp(ts/1000, india_tz)

        if email_dt.date() != today:
            continue

        task = extract_task_from_email(mail["body"])
        task = apply_priority_rules(task, mail["sender"], mail["subject"])

        task["raw_email_id"] = mail["id"]
        task["raw_subject"] = mail["subject"]
        task["raw_sender"] = mail["sender"]
        task["status"] = "PENDING"

        saved = save_task(task)

        if saved.get("is_actionable"):
            create_calendar_event(saved)
