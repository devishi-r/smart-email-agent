# ensures no duplicates
# data persists for front end to render
# record each email

from .db import tasks_collection
from datetime import datetime

def save_task(task_data):
    task_data["created_at"] = datetime.utcnow()
    
    # Store only if task for this email wasn't already saved
    existing = tasks_collection.find_one({
        "raw_email_id": task_data["raw_email_id"]
    })
    
    if existing:
        return existing  # avoid duplicates
    
    tasks_collection.insert_one(task_data)
    return task_data


def get_pending_tasks():
    return list(tasks_collection.find({"status": "PENDING"}))
