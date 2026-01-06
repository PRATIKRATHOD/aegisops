import json
from datetime import datetime
import os

# ---------------- PATHS ----------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(BASE_DIR, "..", "logs", "sample_app.log")
INCIDENT_FILE = os.path.join(BASE_DIR, "..", "incidents", "incidents.json")

# ---------------- HELPERS ----------------
def load_incidents():
    try:
        with open(INCIDENT_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_incidents(incidents):
    with open(INCIDENT_FILE, "w") as f:
        json.dump(incidents, f, indent=4)

def generate_incident_number(incidents):
    return "INC" + str(1000000 + len(incidents) + 1)

# ---------------- DETECTION ----------------
def detect_incident(log_lines):
    for line in log_lines:
        if "OutOfMemoryError" in line:
            return {
                "short_description": "Application crashed due to OutOfMemoryError",
                "description": "OutOfMemoryError detected in application logs",
                "category": "software",
                "subcategory": "application",
                "impact": "2",
                "urgency": "1",
                "priority": "2",
                "assignment_group": "Application Support",
                "comments": "Incident automatically created from log monitoring",
                "work_notes": line.strip(),
                "source": "LOG",
                "correlation_id": "LOG-OOM-001"
            }
    return None

# ---------------- CORRELATION ----------------
def find_open_incident(incidents, correlation_id):
    for inc in incidents:
        if (
            inc.get("correlation_id") == correlation_id
            and inc.get("status") in ["OPEN", "IN_PROGRESS"]
        ):
            return inc
    return None

# ---------------- MAIN ----------------
def main():
    if not os.path.exists(LOG_FILE):
        print("Log file not found")
        return

    with open(LOG_FILE, "r") as log:
        lines = log.readlines()

    detected = detect_incident(lines)

    if not detected:
        print("No incident detected")
        return

    incidents = load_incidents()

    existing = find_open_incident(incidents, detected["correlation_id"])

    if existing:
        # Correlate to existing incident
        existing["work_notes"] += (
            "\nRepeated occurrence detected at "
            + datetime.now().isoformat()
        )
        existing["sys_updated_on"] = datetime.now().isoformat()

        print("🔗 Correlated with existing incident:", existing["incident_id"])

    else:
        # Create NEW incident
        inc_number = generate_incident_number(incidents)

        new_incident = {
            "incident_id": inc_number,
            "number": inc_number,
            "status": "OPEN",
            "incident_state": "New",
            "opened_at": datetime.now().isoformat(),
            "opened_by": "aegisops-agent",
            **detected
        }

        incidents.append(new_incident)
        print("🆕 New incident created:", inc_number)

    save_incidents(incidents)

if __name__ == "__main__":
    main()
