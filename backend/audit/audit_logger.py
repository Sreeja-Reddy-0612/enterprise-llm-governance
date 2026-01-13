from datetime import datetime
from audit.audit_store import save_audit


def log_audit_event(question, comparisons, recommended_version):
    clean_comparisons = {}

    for version, data in comparisons.items():
        clean_comparisons[version] = {
            "risk": data["risk"],
            "approved": data["approved"],
            "reasons": [
                {
                    "category": r.category,
                    "severity": r.severity,
                    "message": r.message,
                    "evaluator": r.evaluator,
                }
                for r in data["reasons"]
            ],
        }

    record = {
        "timestamp": datetime.utcnow().isoformat(),
        "question": question,
        "recommended_version": recommended_version,
        "comparisons": clean_comparisons,
    }

    save_audit(record)
