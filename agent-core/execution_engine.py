import json
from datetime import datetime
from path_config import INCIDENTS_PATH
from audit_logger import write_audit


# ---------------- LOAD / SAVE ----------------
def load_incidents():
    with open(INCIDENTS_PATH, "r") as f:
        return json.load(f)


def save_incidents(incidents):
    with open(INCIDENTS_PATH, "w") as f:
        json.dump(incidents, f, indent=4)


# ---------------- SIMULATION ENGINE ----------------
def generate_execution_preview(actions):
    """
    Creates a SAFE execution preview (simulation only).
    No commands are run.
    """

    preview_steps = []

    for action in actions:
        preview_steps.append({
            "step": action["description"],
            "command": action["command"],
            "risk": action["risk"],
            "status": "PENDING",
            "notes": "This is a simulation only. No real execution performed."
        })

    return preview_steps


# ---------------- MAIN EXECUTION LOGIC ----------------
def main():
    incidents = load_incidents()
    incident = incidents[-1]

    action_block = incident.get("action_recommendations", {})
    action_plan = action_block.get("actions", [])
    decision = incident.get("agent_decision", {})

    if not action_plan:
        print("❌ No action plan found. Run Agent-3 first.")
        return

    # Determine execution mode
    if decision.get("action_allowed", False):
        execution_mode = "SAFE_MODE"    # Acting but simulated
    else:
        execution_mode = "SIMULATION_ONLY"

    preview_steps = generate_execution_preview(action_plan)

    execution_preview = {
        "generated_at": datetime.now().isoformat(),
        "execution_mode": execution_mode,
        "risk_level": decision.get("reason", "UNKNOWN"),
        "requires_approval": not decision.get("action_allowed", False),
        "steps": preview_steps
    }

    # Attach execution preview
    incident["execution_preview"] = execution_preview
    incidents[-1] = incident
    save_incidents(incidents)

    # Audit logging
    write_audit("EXECUTION_PREVIEW_CREATED", {
        "incident": incident.get("incident_id"),
        "steps": len(preview_steps),
        "mode": execution_mode
    })

    print("✅ Execution preview generated successfully for", incident["incident_id"])


if __name__ == "__main__":
    main()
