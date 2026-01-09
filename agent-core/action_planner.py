import json
from datetime import datetime
from path_config import INCIDENTS_PATH, ACTIONS_HISTORY_PATH
from audit_logger import write_audit


# ------------------------
# Load incidents
# ------------------------
def load_incidents():
    with open(INCIDENTS_PATH, "r") as f:
        return json.load(f)


def save_incidents(incidents):
    with open(INCIDENTS_PATH, "w") as f:
        json.dump(incidents, f, indent=4)


# ------------------------
# Simple rule-based action planner
# ------------------------
def generate_action_plan(incident):
    steps = []

    # Example logic
    if "OutOfMemoryError" in incident.get("work_notes", ""):
        steps = [
            "Analyze JVM heap usage",
            "Increase JVM heap size",
            "Restart application service"
        ]
        risk = "HIGH"
    else:
        steps = ["Review incident details"]
        risk = "LOW"

    return {
        "generated_at": datetime.now().isoformat(),
        "steps": steps,
        "risk_level": risk,
        "requires_approval": (risk != "LOW")
    }


# ------------------------
# Save to action KB
# ------------------------
def save_actions_history(plan):
    try:
        with open(ACTIONS_HISTORY_PATH, "r") as f:
            history = json.load(f)
    except:
        history = []

    history.append(plan)

    with open(ACTIONS_HISTORY_PATH, "w") as f:
        json.dump(history, f, indent=4)

    write_audit("ACTION_PLAN_STORED_IN_KB", {"count": len(history)})


# ------------------------
# MAIN FLOW
# ------------------------
def main():
    incidents = load_incidents()
    incident = incidents[-1]  # latest

    # Generate plan
    plan = generate_action_plan(incident)

    # Attach to incident.json
    incident["action_plan"] = plan
    incidents[-1] = incident
    save_incidents(incidents)

    # Log audit
    write_audit("ACTION_PLAN_CREATED", plan)

    # Save to KB
    save_actions_history(plan)

    print("✅ Action plan generated and saved successfully")


if __name__ == "__main__":
    main()
