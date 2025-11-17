def apply_priority_rules(data, sender, subject):
    if not data.get("is_actionable"):
        return data

    # rule 1: urgent keywords
    urgent_keywords = ["urgent", "asap", "immediately", "final reminder", "attention"]
    if any(word in subject.lower() for word in urgent_keywords):
        data["priority"] = "HIGH"

    # rule 2: important senders list
    important_senders = ["prof", "manager", "hr", "admin"]
    if any(key in sender.lower() for key in important_senders):
        data["priority"] = "HIGH"

    return data
