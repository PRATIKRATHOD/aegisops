import json
from datetime import datetime

from path_config import INCIDENTS_PATH
from audit_logger import write_audit


# ---------------- LOAD / SAVE ----------------
def load_incidents():
    with open(INCIDENTS_PATH, "r") as f:
        return json.load(f)


# ---------------- NOTIFICATION SIMULATIONS ----------------
def send_slack_message(incident_id, message):
    print(f"\n💬 [SLACK] #{incident_id}: {message}")
    write_audit("SLACK_NOTIFICATION", {"incident": incident_id})


def send_email(incident_id, subject, body):
    print(f"\n📧 [EMAIL] #{incident_id}: {subject}\n{body}")
    write_audit("EMAIL_NOTIFICATION", {"incident": incident_id})


def log_console_alert(incident_id, message):
    print(f"\n⚠️ [ALERT] Incident {incident_id}: {message}")
    write_audit("CONSOLE_ALERT", {"incident": incident_id})


# ---------------- DECISION LOGIC ----------------
def process_decision(incident):
    decision = incident.get("agent_decision", {})
    incident_id = incident.get("incident_id")

    if not decision:
        print("❌ No agent decision found")
        return

    state = decision.get("decision")

    # ---- HIGH CONFIDENCE → ACT ----
    if state == "ACT":
        msg = "High confidence: Automated fix READY for execution."
        send_slack_message(incident_id, msg)
        send_email(
            incident_id,
            "AUTO-EXECUTION APPROVED",
            f"Incident {incident_id} is safe for automated remediation."
        )
        log_console_alert(incident_id, "Auto-execution green status.")

    # ---- MEDIUM CONFIDENCE → RECOMMEND ----
    elif state == "RECOMMEND":
        msg = "Medium confidence: Human approval required."
        send_slack_message(incident_id, msg)
        send_email(
            incident_id,
            "MANUAL REVIEW REQUIRED",
            f"Incident {incident_id}: Please approve recommended actions."
        )

    # ---- LOW CONFIDENCE → OBSERVE ----
    elif state == "OBSERVE":
        msg = "Low confidence: Monitoring continues."
        log_console_alert(incident_id, msg)

    else:
        print("Unknown decision:", state)

    write_audit("INCIDENT_NOTIFIED", {"incident": incident_id, "state": state})
 



# ---------------- MAIN ----------------
def main():
    incidents = load_incidents()
    incident = incidents[-1]

    print("\n🔔 Running Agent 7: Incident Notifier\n")

    process_decision(incident)
    incident["notification_state"] = incident.get("agent_decision", {}).get("decision")
    incident["notified_at"] = datetime.now().isoformat()

    with open(INCIDENTS_PATH, "w") as f:
        json.dump(incidents, f, indent=4)


    print("\n✅ Agent 7 completed successfully\n")


if __name__ == "__main__":
    main()
