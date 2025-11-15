import base64
import email
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

def get_gmail_service():
    flow = InstalledAppFlow.from_client_secrets_file(
        "app/credentials.json", SCOPES
    )
    creds = flow.run_local_server(port=0)
    service = build("gmail", "v1", credentials=creds)
    return service

def fetch_unread_emails():
    service = get_gmail_service()

    results = service.users().messages().list(
        userId="me", labelIds=["UNREAD"], maxResults=10
    ).execute()

    messages = results.get("messages", [])
    emails = []

    for msg in messages:
        msg_obj = service.users().messages().get(
            userId="me", id=msg["id"], format="full"
        ).execute()

        payload = msg_obj["payload"]
        headers = payload["headers"]

        # Extract subject and sender
        subject = next((h["value"] for h in headers if h["name"] == "Subject"), "")
        sender = next((h["value"] for h in headers if h["name"] == "From"), "")

        # Extract body
        body = ""
        if "parts" in payload:
            for part in payload["parts"]:
                if part["mimeType"] == "text/plain":
                    body = base64.urlsafe_b64decode(
                        part["body"]["data"]
                    ).decode("utf-8")
        else:
            body = base64.urlsafe_b64decode(
                payload["body"]["data"]
            ).decode("utf-8")

        emails.append({
            "id": msg["id"],
            "sender": sender,
            "subject": subject,
            "body": body
        })

    return emails
