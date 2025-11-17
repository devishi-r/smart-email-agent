import google.generativeai as genai
import json
from .utils.prompt import GEMINI_EXTRACTION_PROMPT
from .config import Settings

settings = Settings()
genai.configure(api_key=settings.GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")

def extract_task_from_email(email_body: str):
    prompt = GEMINI_EXTRACTION_PROMPT.format(email_body=email_body)

    response = model.generate_content(prompt)
    raw = response.text

    # Ensure valid JSON
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return {"is_actionable": False}

    return data
