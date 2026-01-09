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
def generate_execution_preview(action_plan):
    """Safe simulation (no real commands run)."""

    preview_steps = []

    for step in action_plan.get("steps", []):
        preview_steps.append({
            "step": step,
            "status": "PENDING",
            "notes": "Simulation only – no actual execution performed."
        })

    return preview_steps


# ---------------- MAIN EXECUTION LOGIC ----------------
def main():
    incidents = load_incidents()
    incident = incidents[-1]

    # Load decision and plan
    decision = incident.get("agent_decision", {})
    action_plan = incident.get("action_plan", None)

    if not action_plan:
        print("❌ No action_plan found. Run action_planner.py first.")
        return

    # Execution mode
    execution_mode = (
        "SIMULATION_ONLY"
        if not decision.get("action_allowed", False)
        else "SAFE_MODE"
    )

    preview_steps = generate_execution_preview(action_plan)

    execution_preview = {
        "generated_at": datetime.now().isoformat(),
        "risk_level": action_plan.get("risk_level", "UNKNOWN"),
        "requires_approval": action_plan.get("requires_approval", True),
        "execution_mode": execution_mode,
        "steps": preview_steps
    }

    # Save into incident
    incident["execution_preview"] = execution_preview
    incidents[-1] = incident
    save_incidents(incidents)

    # Audit log
    write_audit("EXECUTION_PREVIEW_CREATED", {
        "incident_id": incident.get("incident_id"),
        "steps": len(preview_steps),
        "mode": execution_mode
    })

    print("✅ Execution Preview Generated Successfully")


if __name__ == "__main__":
    main()
