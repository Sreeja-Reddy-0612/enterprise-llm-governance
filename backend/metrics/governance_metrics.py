from collections import Counter
from typing import Dict
from audit.audit_store import get_audits


def compute_governance_metrics(limit: int = 100) -> Dict:
    audits = get_audits(limit)

    if not audits:
        return {
            "total_evaluations": 0,
            "approval_rate": 0.0,
            "risk_distribution": {},
            "top_violated_rules": {}
        }

    total = len(audits)
    approved_count = 0
    risk_counter = Counter()
    rule_counter = Counter()

    for audit in audits:
        comparisons = audit.get("comparisons", {})
        recommended = audit.get("recommended_version")

        if recommended and recommended in comparisons:
            decision = comparisons[recommended]
            risk_counter[decision["risk"]] += 1

            if decision["approved"]:
                approved_count += 1

            for reason in decision.get("reasons", []):
                rule = reason.get("category", "UNKNOWN")
                rule_counter[rule] += 1

    return {
        "total_evaluations": total,
        "approval_rate": round((approved_count / total) * 100, 2),
        "risk_distribution": dict(risk_counter),
        "top_violated_rules": dict(rule_counter.most_common(5))
    }
