import json
from datetime import datetime
from audit_logger import write_audit


INCIDENT_FILE = "../incidents/incidents.json"


# ------------- LOAD / SAVE HELPERS -------------
def load_incidents():
    with open(INCIDENT_FILE, "r") as f:
        return json.load(f)


def save_incidents(incidents):
    with open(INCIDENT_FILE, "w") as f:
        json.dump(incidents, f, indent=4)


# ------------- STEP GENERATION LOGIC -------------
def generate_plan_steps(recommendations):
    steps = []
    for action in recommendations:
        steps.append(action.get("description"))
    return steps


# ------------- RISK EVALUATION -------------
def evaluate_plan_risk(recommendations):
    risks = [a.get("risk", "LOW") for a in recommendations]

    if "HIGH" in risks:
        return "HIGH"
    if "MEDIUM" in risks:
        return "MEDIUM"
    return "LOW"


# ------------- APPROVAL LOGIC -------------
def approval_required(risk_level):
    return risk_level in ["HIGH", "MEDIUM"]


# ------------- MAIN PLAN BUILDER -------------
def build_action_plan(incident):
    recommendations = incident.get("action_recommendations", {}).get("actions", [])
    if not recommendations:
        return None

    steps = generate_plan_steps(recommendations)
    risk_level = evaluate_plan_risk(recommendations)
    approval = approval_required(risk_level)

    return {
        "generated_at": datetime.now().isoformat(),
        "steps": steps,
        "risk_level": risk_level,
        "requires_approval": approval
    }


# ------------- MAIN RUNNER -------------
def main():
    incidents = load_incidents()
    incident = incidents[-1]

    plan = build_action_plan(incident)
    if plan:
        write_audit("ACTION_PLAN_CREATED", plan)
        incident["action_plan"] = plan
           # ---------------------- ADD THIS BLOCK HERE ----------------------
        try:
            with open("knowledge_base/actions_history.json", "r") as f:
                actions_hist = json.load(f)
        except:
            actions_hist = []

        actions_hist.append(plan)

        with open("knowledge_base/actions_history.json", "w") as f:
            json.dump(actions_hist, f, indent=4)

        write_audit("ACTION_PLAN_STORED_IN_KB", {"count": len(actions_hist)})
        incidents[-1] = incident
        save_incidents(incidents)
        print("✅ Action plan generated successfully")
    else:
        print("⚠️ No recommendations available — plan skipped")


if __name__ == "__main__":
    main()
