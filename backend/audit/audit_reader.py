import json
from pathlib import Path
from typing import Optional, Dict

AUDIT_LOG_FILE = Path("backend/audit_logs.jsonl")


def get_audit_by_timestamp(timestamp: str) -> Optional[Dict]:
    if not AUDIT_LOG_FILE.exists():
        return None

    with open(AUDIT_LOG_FILE, "r", encoding="utf-8") as f:
        for line in f:
            record = json.loads(line)
            if record.get("timestamp") == timestamp:
                return record

    return None
