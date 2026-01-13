# audit/audit_store.py
from typing import List, Dict

# In-memory store (Phase 6 – Step 2)
AUDIT_LOGS: List[Dict] = []

def save_audit(record: Dict):
    AUDIT_LOGS.append(record)

def get_audits(limit: int = 50):
    return AUDIT_LOGS[-limit:]
