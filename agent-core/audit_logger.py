import json
from datetime import datetime
import os

AUDIT_FILE = "../incidents/audit_log.json"


# ------------- ENSURE AUDIT LOG EXISTS -------------
def _ensure_file():
    if not os.path.exists(AUDIT_FILE):
        with open(AUDIT_FILE, "w") as f:
            json.dump([], f, indent=4)


# ------------- WRITE AUDIT ENTRY -------------
def write_audit(event_type, details):
    _ensure_file()

    audit_entry = {
        "timestamp": datetime.now().isoformat(),
        "event_type": event_type,
        "details": details
    }

    with open(AUDIT_FILE, "r") as f:
        logs = json.load(f)

    logs.append(audit_entry)

    with open(AUDIT_FILE, "w") as f:
        json.dump(logs, f, indent=4)

    print(f"📝 Audit logged: {event_type}")
