from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from .config import Settings

settings = Settings()

SCOPES = ["https://www.googleapis.com/auth/calendar"]

def get_calendar_service():
    flow = InstalledAppFlow.from_client_secrets_file(
        "app/credentials.json", SCOPES
    )
    creds = flow.run_local_server(port=0)
    service = build("calendar", "v3", credentials=creds)
    return service


def create_calendar_event(task):
    service = get_calendar_service()
    
    event = {
        "summary": f"{'[HIGH PRIORITY] ' if task['priority'] == 'HIGH' else ''}{task['task_title']}",
        "description": f"Extracted from email:\n{task['raw_subject']} \n\nSender: {task['raw_sender']}",
        "start": {"dateTime": task["deadline"],
                "timeZone" : "Asia/Kolkata" },
        "end": {"dateTime": task["deadline"],
                "timeZone": "Asia/Kolkata"},  # same end time; you can set +30 mins
    }

    # HIGH priority = Red color
    if task["priority"] == "HIGH":
        event["colorId"] = "11"

    created_event = service.events().insert(
        calendarId=settings.CALENDAR_ID,
        body=event
    ).execute()

    return created_event
