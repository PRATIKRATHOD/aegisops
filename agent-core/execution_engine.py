import json
from datetime import datetime
from audit_logger import write_audit


INCIDENT_FILE = "../incidents/incidents.json"


# ----------------- LOAD & SAVE -----------------
def load_incidents():
    with open(INCIDENT_FILE, "r") as f:
        return json.load(f)


def save_incidents(incidents):
    with open(INCIDENT_FILE, "w") as f:
        json.dump(incidents, f, indent=4)


# ----------------- EXECUTION INTENT -----------------
def generate_execution_preview(incident):
    plan = incident.get("action_plan", {})
    steps = plan.get("steps", [])
    risk = plan.get("risk_level", "LOW")
    approval = plan.get("requires_approval", True)

    if not steps:
        return None

    preview_steps = []
    for step in steps:
        preview_steps.append({
            "step": step,
            "status": "PENDING",
            "notes": "This is a simulation. No actual execution performed."
        })

    return {
        "generated_at": datetime.now().isoformat(),
        "risk_level": risk,
        "requires_approval": approval,
        "execution_mode": "SIMULATION_ONLY",
        "steps": preview_steps
    }


# ---------------------- MAIN ----------------------
def main():
    incidents = load_incidents()
    incident = incidents[-1]

    preview = generate_execution_preview(incident)
    if preview:
        write_audit("EXECUTION_PREVIEW_CREATED", preview)
        incident["execution_preview"] = preview
        incidents[-1] = incident
        save_incidents(incidents)
        print("✅ Execution preview generated (simulation only)")
    else:
        print("⚠️ No action plan found — skipping execution simulation")


if __name__ == "__main__":
    main()