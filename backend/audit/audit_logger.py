from datetime import datetime
from audit.audit_store import save_audit


def log_audit_event(question, comparisons, recommended_version, policy_version):
    record = {
        "timestamp": datetime.utcnow().isoformat(),
        "policy_version": policy_version,
        "question": question,
        "recommended_version": recommended_version,
        "comparisons": comparisons
    }

    save_audit(record)
