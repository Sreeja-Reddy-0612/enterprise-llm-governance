from typing import Dict, List
from datetime import datetime
from audit.audit_store import get_audits


DEFAULT_THRESHOLDS = {
    "min_approval_rate": 0.2,        # 20%
    "max_high_risk_ratio": 0.3,       # 30%
    "max_rule_violations": 10,        # per rule
    "max_policy_drift": 5
}


def generate_governance_alerts(
    limit: int = 100,
    thresholds: Dict = DEFAULT_THRESHOLDS
) -> List[Dict]:

    audits = get_audits(limit)
    alerts = []

    if not audits:
        return alerts

    total = len(audits)
    approved = 0
    high_risk = 0
    rule_counts = {}
    policy_versions = {}

    for record in audits:
        for version_data in record["comparisons"].values():
            if version_data["approved"]:
                approved += 1

            if version_data["risk"] == "HIGH":
                high_risk += 1

            for reason in version_data["reasons"]:
                rule = reason["category"]
                rule_counts[rule] = rule_counts.get(rule, 0) + 1

        pv = record.get("policy_version", "unknown")
        policy_versions[pv] = policy_versions.get(pv, 0) + 1

    approval_rate = approved / total
    high_risk_ratio = high_risk / total

    # ---- Approval rate alert ----
    if approval_rate < thresholds["min_approval_rate"]:
        alerts.append({
            "type": "LOW_APPROVAL_RATE",
            "severity": "HIGH",
            "message": f"Approval rate dropped to {approval_rate:.2f}",
            "value": approval_rate
        })

    # ---- High risk spike ----
    if high_risk_ratio > thresholds["max_high_risk_ratio"]:
        alerts.append({
            "type": "HIGH_RISK_SPIKE",
            "severity": "HIGH",
            "message": f"High risk ratio increased to {high_risk_ratio:.2f}",
            "value": high_risk_ratio
        })

    # ---- Unstable rules ----
    for rule, count in rule_counts.items():
        if count > thresholds["max_rule_violations"]:
            alerts.append({
                "type": "UNSTABLE_RULE",
                "severity": "MEDIUM",
                "message": f"Rule '{rule}' violated {count} times",
                "rule": rule,
                "count": count
            })

    # ---- Policy drift ----
    for pv, count in policy_versions.items():
        if count > thresholds["max_policy_drift"]:
            alerts.append({
                "type": "POLICY_DRIFT",
                "severity": "MEDIUM",
                "message": f"Policy '{pv}' used {count} times",
                "policy_version": pv,
                "count": count
            })

    return alerts
