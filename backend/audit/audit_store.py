from pathlib import Path
import json

BASE_DIR = Path(__file__).resolve().parent.parent
AUDIT_LOG_PATH = BASE_DIR / "audit_logs.json"


def _ensure_file():
    if not AUDIT_LOG_PATH.exists():
        AUDIT_LOG_PATH.write_text("[]", encoding="utf-8")


def read_all_audits():
    _ensure_file()
    with open(AUDIT_LOG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def save_audit(record: dict):
    audits = read_all_audits()
    audits.append(record)

    with open(AUDIT_LOG_PATH, "w", encoding="utf-8") as f:
        json.dump(audits, f, indent=2)


def get_audits(limit: int = 20):
    audits = read_all_audits()
    return audits[-limit:][::-1]


def get_audit_by_index(index: int):
    audits = read_all_audits()
    if index < 0 or index >= len(audits):
        return None
    return audits[index]
