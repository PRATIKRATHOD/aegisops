import json
from datetime import datetime
import os
import random

# ---------------- PATHS ----------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INCIDENT_FILE = os.path.join(
    BASE_DIR, "..", "backend", "src", "main", "resources", "data", "incidents.json"
)

# ---------------- INCIDENT SIGNATURES ----------------
INCIDENT_TEMPLATES = [
    {
        "match": "OutOfMemoryError",
        "short": "Application crashed due to OutOfMemoryError",
        "desc": "OutOfMemoryError detected in application logs",
        "category": "software",
        "subcategory": "application",
        "priority": "2",
        "correlation": "LOG-OOM-001",
    },
    {
        "match": "DB timeout",
        "short": "Database connection timeout",
        "desc": "Application unable to connect to DB",
        "category": "database",
        "subcategory": "connectivity",
        "priority": "1",
        "correlation": "LOG-DB-001",
    },
    {
        "match": "High CPU",
        "short": "High CPU usage detected",
        "desc": "CPU usage above threshold",
        "category": "infrastructure",
        "subcategory": "cpu",
        "priority": "2",
        "correlation": "LOG-CPU-001",
    },
    {
        "match": "API latency",
        "short": "API latency spike detected",
        "desc": "High latency observed in API",
        "category": "performance",
        "subcategory": "latency",
        "priority": "3",
        "correlation": "LOG-API-001",
    },
]

# ---------------- HELPERS ----------------
def load_incidents():
    try:
        with open(INCIDENT_FILE, "r") as f:
            return json.load(f)
    except:
        return []


def save_incidents(incidents):
    with open(INCIDENT_FILE, "w") as f:
        json.dump(incidents, f, indent=4)


def generate_incident_number(incidents):
    return "INC" + str(1000000 + len(incidents) + 1)


# ---------------- DETECTION ----------------
def detect_incident(line):
    for tpl in INCIDENT_TEMPLATES:
        if tpl["match"] in line:
            return tpl, line
    return None, None


# ---------------- CORRELATION ----------------
def find_existing_incident(incidents, correlation_id):
    for inc in incidents:
        if inc.get("correlation_id") == correlation_id and inc.get("status") == "OPEN":
            return inc
    return None


# ---------------- MAIN AGENT ----------------
def main():
    # ---- Simulate ONE event per run ----
    log_events = [
        "OutOfMemoryError: Java heap space",
        "High CPU detected on server",
        "API latency above threshold",
        "DB timeout after 30 seconds"
    ]

    log = random.choice(log_events)
    print(f"🔍 Processing log event: {log}")

    template, matched_line = detect_incident(log)
    if not template:
        print("No incident detected")
        return

    incidents = load_incidents()
    correlation_id = template["correlation"]

    existing = find_existing_incident(incidents, correlation_id)

    # ---------------- UPDATE EXISTING INCIDENT ----------------
    if existing:
        existing["work_notes"] += f"\nRepeated event at {datetime.now().isoformat()}"

        existing["timeline"].append({
            "event": "CORRELATED_EVENT",
            "timestamp": datetime.now().isoformat(),
            "details": matched_line,
        })

        print(f"🔗 Updated existing incident: {existing['incident_id']}")

    # ---------------- CREATE NEW INCIDENT ----------------
    else:
        new_id = generate_incident_number(incidents)

        new_incident = {
            "incident_id": new_id,
            "number": new_id,
            "status": "OPEN",
            "incident_state": "New",
            "opened_at": datetime.now().isoformat(),
            "opened_by": "aegisops-agent",

            "short_description": template["short"],
            "description": template["desc"],
            "category": template["category"],
            "subcategory": template["subcategory"],
            "impact": "2",
            "urgency": "2",
            "priority": template["priority"],
            "assignment_group": "Application Support",
            "comments": "Auto-generated incident",
            "work_notes": matched_line,
            "source": "LOG",
            "correlation_id": correlation_id,

            "timeline": [
                {
                    "event": "INCIDENT_CREATED",
                    "timestamp": datetime.now().isoformat(),
                    "details": matched_line,
                }
            ]
        }

        incidents.append(new_incident)
        print(f"🆕 New incident created: {new_id}")

    save_incidents(incidents)
    print("✅ Agent 1 Completed Successfully")


if __name__ == "__main__":
    main()
