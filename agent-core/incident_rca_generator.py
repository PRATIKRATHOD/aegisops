import json
import subprocess
from datetime import datetime

from path_config import INCIDENTS_PATH, HISTORICAL_RCA_PATH
from knowledge_base.incident_memory import find_similar_incident
from audit_logger import write_audit

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


# ---------------- STRONG JSON PROMPT ----------------
def build_rca_prompt(incident):
    return f"""
You are a senior Site Reliability Engineer.

STRICT INSTRUCTION:
Return ONLY a VALID JSON object. 
The response MUST start with '{{' and end with '}}'.
NEVER include explanation, never include markdown.

JSON fields required:
- root_cause_type
- affected_component
- probable_cause
- evidence (array)
- impact
- recommended_next_steps (array)

Example Format:
{{
  "root_cause_type": "...",
  "affected_component": "...",
  "probable_cause": "...",
  "evidence": ["..."],
  "impact": "...",
  "recommended_next_steps": ["...", "..."]
}}

Now generate RCA for this incident:

Short Description: {incident["short_description"]}
Category: {incident.get("category", "unknown")}
Priority: {incident.get("priority", "unknown")}
Work Notes: {incident.get("work_notes", "")}
"""


# ---------------- LLM CALL ----------------
def generate_raw_rca(prompt):
    result = subprocess.run(
        ["ollama", "run", "mistral"],
        input=prompt,
        capture_output=True,
        encoding="utf-8"
    )
    return result.stdout


# ---------------- JSON EXTRACTION ----------------
def extract_json_from_text(text):
    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end == -1:
        raise ValueError("No JSON found")
    return json.loads(text[start:end + 1])


# ---------------- VALIDATION ----------------
def validate_rca(rca):
    missing = [f for f in REQUIRED_FIELDS if f not in rca]
    if missing:
        raise ValueError("Missing fields: " + ", ".join(missing))


# ---------------- CONFIDENCE MODEL ----------------
def calculate_confidence(rca, incident):
    score = 0.5
    reasons = []

    if "OutOfMemoryError" in incident.get("work_notes", ""):
        score += 0.2
        reasons.append("OOM pattern detected")

    if rca.get("affected_component"):
        score += 0.1
        reasons.append("Component identified")

    score = min(score, 0.95)

    return {
        "confidence_score": round(score, 2),
        "confidence_reason": ", ".join(reasons),
        "risk_level": "LOW" if score >= 0.75 else "MEDIUM",
        "requires_human_approval": score < 0.75
    }


# ---------------- DECISION ENGINE ----------------
def make_agent_decision(rca_block):
    conf = rca_block["confidence"]["confidence_score"]
    risk = rca_block["confidence"]["risk_level"]

    if conf < 0.60:
        return {"decision": "OBSERVE", "reason": "Low confidence", "action_allowed": False}

    if conf < 0.80:
        return {"decision": "RECOMMEND", "reason": "Medium confidence", "action_allowed": False}

    if conf >= 0.80 and risk == "LOW":
        return {"decision": "ACT", "reason": "High confidence", "action_allowed": True}

    return {"decision": "OBSERVE", "reason": "Fallback safety", "action_allowed": False}


# ---------------- MAIN FLOW ----------------
def main():

    incidents = load_incidents()
    incident = incidents[-1]

    # MEMORY MATCH
    match = find_similar_incident(incident)
    if match:
        incident["memory_reference"] = {
            "matched_incident": match.get("incident_id", "unknown"),
            "used_for_context": True
        }

    # PROMPT + LLM
    prompt = build_rca_prompt(incident)
    raw = generate_raw_rca(prompt)

    # PARSING
    try:
        rca = extract_json_from_text(raw)
        validate_rca(rca)
        write_audit("RCA_GENERATED", rca)
    except Exception as e:
        incident["rca"] = {"error": str(e), "raw_output": raw}
        save_incidents(incidents)
        return

    # CONFIDENCE
    conf = calculate_confidence(rca, incident)
    rca["confidence"] = conf
    write_audit("CONFIDENCE_SCORED", conf)

    incident["rca"] = {**rca, "generated_at": datetime.now().isoformat()}

    # DECISION
    decision = make_agent_decision(incident["rca"])
    incident["agent_decision"] = decision
    write_audit("AGENT_DECISION", decision)

    # SAVE BACK
    incidents[-1] = incident
    save_incidents(incidents)

    # SAVE TO KB
    try:
        with open(HISTORICAL_RCA_PATH, "r") as f:
            hist = json.load(f)
    except:
        hist = []

    hist.append(incident["rca"])
    with open(HISTORICAL_RCA_PATH, "w") as f:
        json.dump(hist, f, indent=4)

    write_audit("RCA_STORED_IN_KB", {"count": len(hist)})

    print("✅ RCA Generated Successfully")


if __name__ == "__main__":
    main()
