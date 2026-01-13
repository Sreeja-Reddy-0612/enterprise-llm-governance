import json
from datetime import datetime
from pathlib import Path

AUDIT_LOG_PATH = Path("audit_logs.json")


def log_audit_event(
    question: str,
    comparisons: dict,
    recommended_version: str
):
    """
    Persist an audit record for governance decisions.
    """

    audit_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "question": question,
        "results": {
            version: {
                "risk": data["risk"],
                "approved": data["approved"]
            }
            for version, data in comparisons.items()
        },
        "recommended_version": recommended_version
    }

    # Load existing logs
    if AUDIT_LOG_PATH.exists():
        with open(AUDIT_LOG_PATH, "r", encoding="utf-8") as f:
            logs = json.load(f)
    else:
        logs = []

    logs.append(audit_entry)

    # Save back
    with open(AUDIT_LOG_PATH, "w", encoding="utf-8") as f:
        json.dump(logs, f, indent=2)
