import json
from datetime import datetime
from path_config import AUDIT_LOG_PATH


def ensure_file_exists(path):
    try:
        with open(path, "r") as f:
            json.load(f)
    except:
        with open(path, "w") as f:
            json.dump([], f, indent=4)


def write_audit(event_type, details):
    ensure_file_exists(AUDIT_LOG_PATH)

    with open(AUDIT_LOG_PATH, "r") as f:
        logs = json.load(f)

    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "event_type": event_type,
        "details": details
    }

    logs.append(log_entry)

    with open(AUDIT_LOG_PATH, "w") as f:
        json.dump(logs, f, indent=4)

    print(f"📝 Audit logged: {event_type}")
