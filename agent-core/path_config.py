import os

# When running in Docker, we will mount backend/data → /data

if os.path.exists("/data"):
    BASE_PATH = "/data"
else:
    BASE_PATH = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "..",
            "backend",
            "src",
            "main",
            "resources",
            "data"
        )
    )

INCIDENTS_PATH = os.path.join(BASE_PATH, "incidents.json")
AUDIT_LOG_PATH = os.path.join(BASE_PATH, "audit_log.json")
HISTORICAL_RCA_PATH = os.path.join(BASE_PATH, "historical_rca.json")
ACTIONS_HISTORY_PATH = os.path.join(BASE_PATH, "actions_history.json")
POSTMORTEM_PATH = os.path.join(BASE_PATH, "postmortem.json")
