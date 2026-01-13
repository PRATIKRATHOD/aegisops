import json
import random
import time
from datetime import datetime

from path_config import INCIDENTS_PATH
from audit_logger import write_audit


# ------------- LOAD / SAVE -------------
def load_incidents():
    with open(INCIDENTS_PATH, "r") as f:
        return json.load(f)


def save_incidents(incidents):
    with open(INCIDENTS_PATH, "w") as f:
        json.dump(incidents, f, indent=4)


# ------------- EXECUTE SINGLE STEP (SIMULATED) -------------
def execute_step_simulation(step):
    """
    Simulates execution of an action.
    Random 10% failure rate for realism.
    """

    start = time.time()
    time.sleep(0.3)  # Simulated execution delay

    failed = random.random() < 0.10  # 10% chance of failure

    return {
        "step": step["step"],
        "command": step["command"],
        "risk": step["risk"],
        "status": "FAILED" if failed else "SUCCESS",
        "execution_time_ms": int((time.time() - start) * 1000),
        "output": (
            "Simulated failure due to environment issue"
            if failed
            else "Executed successfully in safe simulation mode"
        )
    }


# ------------- DETERMINE OVERALL RESULT -------------
def determine_overall_result(executed_steps):
    success = all(s["status"] == "SUCCESS" for s in executed_steps)

    if success:
        return "RESOLVED"
    elif any(s["status"] == "SUCCESS" for s in executed_steps):
        return "PARTIALLY_RESOLVED"
    else:
        return "FAILED"


# ------------- MAIN LOGIC -------------
def main():
    incidents = load_incidents()
    incident = incidents[-1]

    preview = incident.get("execution_preview", {})
    steps = preview.get("steps", [])

    if not steps:
        print("❌ No execution preview found. Run Agent-4 first.")
        return

    print(f"🤖 Agent-5 Starting Self-Healing for {incident['incident_id']}...")

    executed_steps = []

    for step in steps:
        result = execute_step_simulation(step)
        executed_steps.append(result)
        print(f"   → {result['step']} : {result['status']}")

    overall = determine_overall_result(executed_steps)

    healing_result = {
        "executed_at": datetime.now().isoformat(),
        "final_status": overall,
        "steps": executed_steps
    }

    # Attach to incident
    incident["self_healing_result"] = healing_result
    incidents[-1] = incident
    save_incidents(incidents)

    # Audit Log
    write_audit("SELF_HEALING_COMPLETED", {
        "incident": incident["incident_id"],
        "final_status": overall
    })

    print(f"✅ Agent-5 Finished — Final State: {overall}")


if __name__ == "__main__":
    main()
