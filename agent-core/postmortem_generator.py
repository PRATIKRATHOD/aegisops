import json
import subprocess
from datetime import datetime
from path_config import INCIDENTS_PATH, POSTMORTEM_PATH
from audit_logger import write_audit

# ---------------- LOAD INCIDENT ----------------
def load_incidents():
    with open(INCIDENTS_PATH, "r") as f:
        return json.load(f)


# ---------------- LLM CALL ----------------
def call_llm(prompt: str):
    """Runs ollama mistral with a strict JSON-only instruction."""
    result = subprocess.run(
        ["ollama", "run", "mistral"],
        input=prompt.encode("utf-8"),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    raw_text = result.stdout.decode("utf-8", errors="ignore")

    return raw_text


# ---------------- JSON EXTRACTION ----------------
def extract_json(text: str):
    """Extracts the first valid JSON object from LLM output."""
    start = text.find("{")
    end = text.rfind("}")

    if start == -1 or end == -1:
        raise ValueError("No JSON object found")

    snippet = text[start:end + 1]

    # Try parsing
    try:
        return json.loads(snippet)
    except Exception:
        # Common fix: remove backslashes
        cleaned = snippet.replace("\\", "")
        return json.loads(cleaned)


# ---------------- MAIN ----------------
def main():
    incidents = load_incidents()

    if not incidents:
        print("❌ No incidents available.")
        return

    incident = incidents[-1]  # last incident

    prompt = f"""
You are a senior SRE generating a structured post-incident report.

Return ONLY valid JSON.
Do NOT add explanations or markdown.

INCIDENT DETAILS:
{json.dumps(incident, indent=2)}

OUTPUT JSON FORMAT:
{{
  "executive_summary": {{
      "incident_id": "",
      "summary": "",
      "impact": "",
      "duration": "",
      "root_cause": "",
      "initial_detection": "",
      "resolution_overview": ""
  }},
  "impact_analysis": {{
      "services_impacted": [],
      "customers_impacted": "",
      "timeline": []
  }},
  "root_cause_analysis": {{
      "primary_cause": "",
      "supporting_evidence": []
  }},
  "action_items": {{
      "what_went_well": [],
      "what_went_wrong": [],
      "preventive_actions": [],
      "long_term_recommendations": []
  }}
}}

Fill all sections based on the incident.
    """

    raw = call_llm(prompt)

    try:
        postmortem = extract_json(raw)
    except Exception:
        print("❌ Model did not return valid JSON.\n")
        print("RAW OUTPUT:\n", raw)

        # Fallback
        postmortem = {
            "executive_summary": {
                "incident_id": incident.get("incident_id"),
                "summary": "Postmortem unavailable — model returned invalid JSON.",
                "impact": incident.get("impact", "unknown"),
                "duration": "unknown",
                "root_cause": "unknown",
                "initial_detection": incident.get("opened_at"),
                "resolution_overview": "unknown"
            },
            "impact_analysis": {},
            "root_cause_analysis": {},
            "action_items": {}
        }

    # SAVE
    postmortem["generated_at"] = datetime.now().isoformat()

    with open(POSTMORTEM_PATH, "w") as f:
        json.dump(postmortem, f, indent=4)

    write_audit("POSTMORTEM_GENERATED", {
        "incident_id": incident.get("incident_id"),
        "status": "SUCCESS"
    })

    print("✅ Postmortem Generated Successfully")


if __name__ == "__main__":
    main()
