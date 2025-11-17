GEMINI_EXTRACTION_PROMPT = """
You are an AI assistant that analyzes emails and extracts actionable tasks.

Given the email below, return a JSON response with the following fields:

- is_actionable: true or false
- type: "TASK" or "MEETING"
- task_title: brief summary of the task
- deadline: ISO datetime if mentioned, else null
- priority: "HIGH" or "NORMAL"

Rules:
- HIGH priority if email has urgent language (urgent, ASAP, final reminder) or deadline < 24 hours.
- HIGH priority if sender appears important (professor, manager).
- If no action needed, set is_actionable=false and leave other fields null.

Return ONLY JSON. No explanations.

Email content:
---
{email_body}
---
"""
