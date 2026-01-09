import json
from datetime import datetime

from path_config import INCIDENTS_PATH, ACTIONS_HISTORY_PATH
from audit_logger import write_audit


OOM_ACTIONS = [
    {
        "action_id": "CHECK_HEAP",
        "description": "Analyze JVM heap usage",
        "command": "jmap -heap <pid>",
        "risk": "LOW",
        "auto_executable": False
    },
    {
        "action_id": "INCREASE_HEAP",
        "description": "Increase JVM heap space",
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


def load_incidents():
    with open(INCIDENTS_PATH, "r") as f:
        return json.load(f)


def save_incidents(incidents):
    with open(INCIDENTS_PATH, "w") as f:
        json.dump(incidents, f, indent=4)


def store_actions_in_history(actions):
    try:
        with open(ACTIONS_HISTORY_PATH, "r") as f:
            hist = json.load(f)
    except:
        hist = []

    hist.append({
        "generated_at": datetime.now().isoformat(),
        "actions": actions
    })

    with open(ACTIONS_HISTORY_PATH, "w") as f:
        json.dump(hist, f, indent=4)

    write_audit("ACTIONS_STORED_IN_KB", {"count": len(hist)})


def main():
    incidents = load_incidents()
    incident = incidents[-1]

    probable = incident.get("rca", {}).get("probable_cause", "")

    actions = []

    if "memory" in probable.lower() or "heap" in probable.lower() or "outofmemory" in probable.lower():
        actions = OOM_ACTIONS

    incident["action_recommendations"] = {
        "generated_at": datetime.now().isoformat(),
        "actions": actions
    }

    save_incidents(incidents)

    write_audit("ACTION_RECOMMENDATIONS_GENERATED", {
        "incident_id": incident.get("incident_id"),
        "actions_count": len(actions)
    })

    store_actions_in_history(actions)

    print("✅ Action Recommendations Generated")


if __name__ == "__main__":
    main()
