import json
import subprocess
from datetime import datetime
from knowledge_base.incident_memory import find_similar_incident
from audit_logger import write_audit


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

def make_agent_decision(rca_block):
    confidence = rca_block["confidence"]["confidence_score"]
    risk = rca_block["confidence"]["risk_level"]

    # 1. Low confidence → observe only
    if confidence < 0.60:
        return {
            "decision": "OBSERVE",
            "reason": "Low confidence RCA",
            "action_allowed": False
        }

    # 2. Medium confidence → recommend
    if 0.60 <= confidence < 0.80:
        return {
            "decision": "RECOMMEND",
            "reason": "Moderate confidence RCA",
            "action_allowed": False
        }

    # 3. High confidence & low risk → act
    if confidence >= 0.80 and risk == "LOW":
        return {
            "decision": "ACT",
            "reason": "High confidence and low risk",
            "action_allowed": True
        }

    # Safety fallback
    return {
        "decision": "OBSERVE",
        "reason": "Safety fallback",
        "action_allowed": False
    }


# ---------- MAIN FLOW ----------
def main():
    incidents = load_incidents()
    incident = incidents[-1]
    memory_match = find_similar_incident(incident)

    if memory_match:
        incident["memory_reference"] = {
            "matched_incident": memory_match["incident_id"],
            "used_for_context": True
        }

    prompt = build_rca_prompt(incident)
    raw_rca = generate_raw_rca(prompt)

    try:
        parsed_rca = extract_json_from_text(raw_rca)
        validate_rca(parsed_rca)
        write_audit("RCA_GENERATED", parsed_rca)

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
    confidence = calculate_confidence(parsed_rca, incident)
    write_audit("CONFIDENCE_SCORED", confidence)

    
    if incident.get("memory_reference", {}).get("used_for_context"):
        confidence["confidence_score"] = round(
            min(confidence["confidence_score"] + 0.10, 0.95), 2
        )
        confidence["confidence_reason"] += ", boosted by historical match"

    incident["rca"] = {
        "generated_at": datetime.now().isoformat(),
        **parsed_rca,
        "confidence": confidence
    }
    decision = make_agent_decision(incident["rca"])
    write_audit("AGENT_DECISION", decision)

    incident["agent_decision"] = {
        **decision,
        "decided_at": datetime.now().isoformat()
    }


    incidents[-1] = incident
    save_incidents(incidents)

    print("✅ Structured RCA generated and stored successfully")

    # Save RCA to knowledge base
    try:
        with open("knowledge_base/historical_rca.json", "r") as f:
            history = json.load(f)
    except:
        history = []

    history.append(incident["rca"])

    with open("knowledge_base/historical_rca.json", "w") as f:
        json.dump(history, f, indent=4)

    write_audit("RCA_STORED_IN_KB", {"count": len(history)})


def calculate_confidence(rca, incident):
    score = 0.5
    reasons = []

    if "OutOfMemoryError" in incident.get("work_notes", ""):
        score += 0.2
        reasons.append("Clear OutOfMemoryError signature")

    if "Repeated occurrence" in incident.get("work_notes", ""):
        score += 0.1
        reasons.append("Issue observed multiple times")

    if rca.get("affected_component"):
        score += 0.1
        reasons.append("Specific component identified")

    score = min(score, 0.95)

    risk_level = "LOW" if score >= 0.75 else "MEDIUM"
    requires_approval = score < 0.75

    return {
        "confidence_score": round(score, 2),
        "confidence_reason": ", ".join(reasons),
        "risk_level": risk_level,
        "requires_human_approval": requires_approval
    }


if __name__ == "__main__":
    main()
