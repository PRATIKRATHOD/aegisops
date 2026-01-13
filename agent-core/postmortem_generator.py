import json
import requests
import os
from datetime import datetime
from path_config import INCIDENTS_PATH, POSTMORTEM_PATH
from audit_logger import write_audit
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://host.docker.internal:11434")

# ---------------- LOAD INCIDENT ----------------
def load_incidents():
    with open(INCIDENTS_PATH, "r") as f:
        return json.load(f)


# ---------------- LLM CALL (HTTP) ----------------
def call_llm(prompt):
    payload = {
        "model": "mistral",
        "prompt": prompt,
        "stream": False
    }
    r = requests.post(f"{OLLAMA_URL}/api/generate", json=payload)
    return r.json().get("response", "")


# ---------------- JSON EXTRACTION ----------------
def extract_json(text: str):
    start = text.find("{")
    end = text.rfind("}")

    if start == -1 or end == -1:
        raise ValueError("No JSON object found")

    snippet = text[start:end + 1]

    try:
        return json.loads(snippet)
    except Exception:
        cleaned = snippet.replace("\\", "")
        return json.loads(cleaned)


# ---------------- MAIN ----------------
def main():
    incidents = load_incidents()

    if not incidents:
        print("❌ No incidents available.")
        return

    incident = incidents[-1]

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
    """

    raw = call_llm(prompt)

    try:
        postmortem = extract_json(raw)
    except Exception:
        postmortem = {
            "executive_summary": {
                "incident_id": incident.get("incident_id"),
                "summary": "Postmortem unavailable — invalid JSON.",
                "impact": incident.get("impact", "unknown"),
                "duration": "unknown",
                "root_cause": "unknown",
                "initial_detection": incident.get("opened_at"),
                "resolution_overview": "unknown"
            }
        }

    postmortem["generated_at"] = datetime.now().isoformat()

    # Attach inside incident object
    incident["postmortem"] = postmortem
    incident["postmortem_available"] = True
    incident["postmortem_generated_at"] = postmortem["generated_at"]

    with open(INCIDENTS_PATH, "w") as f:
        json.dump(incidents, f, indent=4)

    write_audit("POSTMORTEM_GENERATED", {
        "incident_id": incident.get("incident_id"),
        "status": "SUCCESS"
    })

    print("✅ Postmortem Generated Successfully")


if __name__ == "__main__":
    main()
