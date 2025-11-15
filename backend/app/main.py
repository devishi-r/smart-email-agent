from fastapi import FastAPI
from .config import Settings
from .gmail_client import fetch_unread_emails   # ✅ add this

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
