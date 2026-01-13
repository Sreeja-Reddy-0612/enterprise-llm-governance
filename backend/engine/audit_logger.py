import json
from engine.audit_models import AuditRecord

AUDIT_FILE = "audit_logs.jsonl"

def log_audit(record: AuditRecord):
    with open(AUDIT_FILE, "a") as f:
        f.write(record.json() + "\n")
