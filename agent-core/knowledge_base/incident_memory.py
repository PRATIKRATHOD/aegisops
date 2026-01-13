import json

INCIDENT_FILE = "../../incidents/incidents.json"


def load_incident_history():
    try:
        with open(INCIDENT_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return []


def find_similar_incident(current_incident):
    history = load_incident_history()
    current_error = current_incident.get("work_notes", "")

    for incident in history[:-1]:
        past_error = incident.get("work_notes", "")

        if current_error and current_error in past_error:
            return {
                "incident_id": incident.get("incident_id"),
                "rca": incident.get("rca"),
                "actions": incident.get("action_recommendations", {})
            }

    return None
