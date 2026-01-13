from datetime import datetime
from audit.audit_store import save_audit


def log_audit_event(question, comparisons, recommended_version):
    record = {
        "timestamp": datetime.utcnow().isoformat(),
        "question": question,
        "recommended_version": recommended_version,
        "comparisons": comparisons,
    }

    save_audit(record)
