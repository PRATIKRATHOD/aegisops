import json
import requests
import os
from datetime import datetime

from path_config import INCIDENTS_PATH, HISTORICAL_RCA_PATH
from audit_logger import write_audit
from knowledge_base.incident_memory import find_similar_incident
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://host.docker.internal:11434")

# ---------------- REQUIRED FIELDS ----------------
REQUIRED_FIELDS = [
    "root_cause_type",
    "affected_component",
    "probable_cause",
    "evidence",
    "impact",
    "recommended_next_steps"
]


# ---------------- LOAD / SAVE ----------------
def load_incidents():
    with open(INCIDENTS_PATH, "r") as f:
        return json.load(f)


def save_incidents(incidents):
    with open(INCIDENTS_PATH, "w") as f:
        json.dump(incidents, f, indent=4)


# ---------------- LLM CALL (HTTP API) ----------------
def call_llm(prompt):
    payload = {
        "model": "mistral",
        "prompt": prompt,
        "stream": False
    }
    r = requests.post(f"{OLLAMA_URL}/api/generate", json=payload)
    return r.json().get("response", "")


def build_prompt(incident):
    return f"""
You are a senior SRE.

Generate a ROOT CAUSE ANALYSIS for this incident.
Return ONLY valid JSON. No extra text.

Incident Details:
Short: {incident['short_description']}
Category: {incident['category']}
Subcategory: {incident['subcategory']}
Priority: {incident['priority']}
Work Notes: {incident['work_notes']}

JSON Fields:
- root_cause_type
- affected_component
- probable_cause
- evidence (array)
- impact
- recommended_next_steps (array)
"""


# ---------------- PARSING ----------------
def extract_json(text):
    start = text.find("{")
    end = text.rfind("}")

    if start == -1 or end == -1:
        raise ValueError("No JSON found")

    return json.loads(text[start:end + 1])


def validate_rca(rca_obj):
    missing = [f for f in REQUIRED_FIELDS if f not in rca_obj]
    if missing:
        raise ValueError("Missing RCA fields: " + ", ".join(missing))


# ---------------- CONFIDENCE ENGINE ----------------
def calculate_confidence(rca, incident):
    score = 0.50
    reasons = []

    if "OutOfMemoryError" in incident.get("work_notes", ""):
        score += 0.20
        reasons.append("OOM signature detected")

    if "timeout" in incident.get("description", ""):
        score += 0.15
        reasons.append("Timeout keyword")

    if rca.get("affected_component"):
        score += 0.10
        reasons.append("Component identified")

    score = min(score, 0.95)

    risk_level = "LOW" if score >= 0.75 else "MEDIUM"

    return {
        "confidence_score": round(score, 2),
        "confidence_reason": ", ".join(reasons),
        "risk_level": risk_level,
        "requires_human_approval": score < 0.75
    }


# ---------------- AGENT DECISION ----------------
def make_agent_decision(conf):
    score = conf["confidence_score"]
    risk = conf["risk_level"]

    if score < 0.60:
        return {"decision": "OBSERVE", "action_allowed": False, "reason": "Low confidence"}

    if score < 0.80:
        return {"decision": "RECOMMEND", "action_allowed": False, "reason": "Medium confidence"}

    if score >= 0.80 and risk == "LOW":
        return {"decision": "ACT", "action_allowed": True, "reason": "High confidence / low risk"}

    return {"decision": "OBSERVE", "action_allowed": False, "reason": "Fallback safety"}


# ---------------- MAIN ----------------
def main():
    incidents = load_incidents()
    incident = incidents[-1]

    print(f"🧠 RCA Agent analyzing incident: {incident['incident_id']}")

    match = find_similar_incident(incident)
    if match:
        incident["memory_reference"] = {
            "matched_incident": match["incident_id"],
            "used_for_context": True
        }
        write_audit("RCA_MEMORY_MATCH", {"matched": match["incident_id"]})

    prompt = build_prompt(incident)

    raw_response = call_llm(prompt)

    try:
        rca = extract_json(raw_response)
        validate_rca(rca)
    except Exception as e:
        print("❌ RCA failed:", str(e))
        incident["rca"] = {"error": str(e), "raw_output": raw_response}
        save_incidents(incidents)
        return

    conf = calculate_confidence(rca, incident)
    rca["confidence"] = conf

    decision = make_agent_decision(conf)
    incident["agent_decision"] = decision

    incident["rca"] = {
        **rca,
        "generated_at": datetime.now().isoformat()
    }

    incidents[-1] = incident
    save_incidents(incidents)

    try:
        with open(HISTORICAL_RCA_PATH, "r") as f:
            hist = json.load(f)
    except:
        hist = []

    hist.append(incident["rca"])
    with open(HISTORICAL_RCA_PATH, "w") as f:
        json.dump(hist, f, indent=4)

    write_audit("RCA_GENERATED", {"incident": incident["incident_id"]})
    print("✅ RCA Completed Successfully")


if __name__ == "__main__":
    main()
