import json
import subprocess
from datetime import datetime

INCIDENT_FILE = "../incidents/incidents.json"

REQUIRED_FIELDS = [
    "root_cause_type",
    "affected_component",
    "probable_cause",
    "evidence",
    "impact",
    "recommended_next_steps"
]


# ---------- LOAD / SAVE ----------
def load_incidents():
    with open(INCIDENT_FILE, "r") as f:
        return json.load(f)


def save_incidents(incidents):
    with open(INCIDENT_FILE, "w") as f:
        json.dump(incidents, f, indent=4)


# ---------- PROMPT ----------
def build_rca_prompt(incident):
    return f"""
You are a senior Site Reliability Engineer.

Analyze the following production incident and generate a ROOT CAUSE ANALYSIS.

Return ONLY valid JSON with these fields:
- root_cause_type
- affected_component
- probable_cause
- evidence (array)
- impact
- recommended_next_steps (array)

Incident Details:
Short Description: {incident["short_description"]}
Category: {incident["category"]}
Priority: {incident["priority"]}
Work Notes: {incident["work_notes"]}
"""


# ---------- LLM CALL ----------
def generate_raw_rca(prompt):
    result = subprocess.run(
        ["ollama", "run", "mistral"],
        input=prompt,
        capture_output=True,
        encoding="utf-8",
        errors="replace"
    )
    return result.stdout


# ---------- NORMALIZATION ----------
def extract_json_from_text(text):
    start = text.find("{")
    end = text.rfind("}")

    if start == -1 or end == -1:
        raise ValueError("No JSON found in AI output")

    json_text = text[start:end + 1]
    return json.loads(json_text)


def validate_rca(rca_obj):
    missing = [f for f in REQUIRED_FIELDS if f not in rca_obj]
    if missing:
        raise ValueError("Missing RCA fields: " + ", ".join(missing))


# ---------- MAIN FLOW ----------
def main():
    incidents = load_incidents()
    incident = incidents[-1]

    prompt = build_rca_prompt(incident)
    raw_rca = generate_raw_rca(prompt)

    try:
        parsed_rca = extract_json_from_text(raw_rca)
        validate_rca(parsed_rca)
    except Exception as e:
        print("❌ RCA generation failed:", str(e))
        incident["rca"] = {
            "generated_at": datetime.now().isoformat(),
            "error": "RCA generation failed",
            "raw_output": raw_rca
        }
        save_incidents(incidents)
        return

    # Attach normalized RCA
    incident["rca"] = {
        "generated_at": datetime.now().isoformat(),
        **parsed_rca
    }

    incidents[-1] = incident
    save_incidents(incidents)

    print("✅ Structured RCA generated and stored successfully")


if __name__ == "__main__":
    main()
