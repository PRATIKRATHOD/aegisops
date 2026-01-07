import json
from datetime import datetime

INCIDENT_FILE = "../incidents/incidents.json"


# ---------- LOAD / SAVE ----------
def load_incidents():
    with open(INCIDENT_FILE, "r") as f:
        return json.load(f)


def save_incidents(incidents):
    with open(INCIDENT_FILE, "w") as f:
        json.dump(incidents, f, indent=4)


# ---------- ACTION CATALOG ----------
SAFE_ACTION_CATALOG = {
    "OutOfMemoryError": [
        {
            "action_id": "CHECK_HEAP_USAGE",
            "description": "Analyze JVM heap usage",
            "command": "jmap -heap <pid>",
            "risk": "LOW",
            "auto_executable": False
        },
        {
            "action_id": "INCREASE_HEAP",
            "description": "Increase JVM heap size",
            "command": "-Xmx increase",
            "risk": "MEDIUM",
            "auto_executable": False
        },
        {
            "action_id": "RESTART_SERVICE",
            "description": "Restart application service",
            "command": "systemctl restart app",
            "risk": "HIGH",
            "auto_executable": False
        }
    ]
}


# ---------- ACTION RECOMMENDATION ----------
def recommend_actions(incident):
    rca = incident.get("rca", {})
    decision = incident.get("agent_decision", {})

    if decision.get("decision") == "OBSERVE":
        return []

    probable_cause = rca.get("probable_cause", "")

    if "Heap" in probable_cause or "Memory" in probable_cause:
        return SAFE_ACTION_CATALOG.get("OutOfMemoryError", [])

    return []


# ---------- MAIN ----------
def main():
    incidents = load_incidents()
    incident = incidents[-1]

    recommendations = recommend_actions(incident)

    incident["action_recommendations"] = {
        "generated_at": datetime.now().isoformat(),
        "actions": recommendations
    }

    incidents[-1] = incident
    save_incidents(incidents)

    print("✅ Action recommendations generated (no execution performed)")


if __name__ == "__main__":
    main()
