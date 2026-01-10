import json
import subprocess
from datetime import datetime

from path_config import INCIDENTS_PATH, ACTIONS_HISTORY_PATH
from audit_logger import write_audit


# ---------------- LOAD/SAVE ----------------
def load_incidents():
    with open(INCIDENTS_PATH, "r") as f:
        return json.load(f)


def save_incidents(incidents):
    with open(INCIDENTS_PATH, "w") as f:
        json.dump(incidents, f, indent=4)


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


# ---------------- PROMPT ----------------
def build_action_prompt(incident):
    rca = incident.get("rca", {})

    return f"""
Return ONLY a JSON array. No explanation.

Based on this RCA, generate a list of recommended remediation actions:

RCA:
Root Cause: {rca.get("root_cause_type")}
Affected Component: {rca.get("affected_component")}
Probable Cause: {rca.get("probable_cause")}
Impact: {rca.get("impact")}

JSON FORMAT (strict):
[
  {{
    "description": "",
    "command": "",
    "risk": "LOW|MEDIUM|HIGH"
  }}
]
"""


# ---------------- LLM CALL ----------------
def generate_actions(prompt):
    result = subprocess.run(
        ["ollama", "run", "mistral"],
        input=prompt,
        capture_output=True,
        encoding="utf-8",
        errors="replace"
    )
    return result.stdout


# ---------------- FIXED JSON PARSER ----------------
def extract_json(text):
    # Clean junk characters
    cleaned = (
        text.replace("\\", "")
            .replace("`", "")
            .replace("json", "")
            .replace("\n", " ")
            .strip()
    )

    # Fix common AI mistakes
    cleaned = cleaned.replace("}, {", "}, {")
    cleaned = cleaned.replace("], {", "], {")

    # Fix trailing commas
    cleaned = cleaned.replace(", ]", "]")
    cleaned = cleaned.replace(",]", "]")

    start = cleaned.find("[")
    end = cleaned.rfind("]")

    if start == -1 or end == -1:
        raise ValueError("No JSON array found in LLM output")

    json_block = cleaned[start:end+1]

    # DEBUG
    print("\nRAW CLEANED BLOCK:\n", json_block, "\n")

    try:
        return json.loads(json_block)
    except Exception:
        raise


# ---------------- MAIN ----------------
def main():
    incidents = load_incidents()
    incident = incidents[-1]

    if "rca" not in incident:
        print("❌ No RCA found. Run Agent 2 first.")
        return

    prompt = build_action_prompt(incident)
    raw = generate_actions(prompt)

    try:
        actions = extract_json(raw)
    except Exception as e:
        print("❌ Failed to parse actions:", e)
        print(raw)
        return

    action_block = {
        "generated_at": datetime.now().isoformat(),
        "actions": actions
    }

    incident["action_recommendations"] = action_block
    incidents[-1] = incident
    save_incidents(incidents)

    save_actions_history(action_block)

    write_audit("ACTION_PLAN_GENERATED", {
        "incident": incident["incident_id"],
        "actions": len(actions)
    })

    print("✅ Action plan generated successfully for", incident["incident_id"])


if __name__ == "__main__":
    main()
