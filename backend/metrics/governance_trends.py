from collections import defaultdict
from datetime import datetime


def compute_governance_trends(audits):
    """
    Builds time-based governance trends from audit logs.
    """

    risk_trend = defaultdict(lambda: defaultdict(int))
    approval_trend = defaultdict(lambda: {"approved": 0, "total": 0})
    policy_drift = defaultdict(int)
    rule_instability = defaultdict(int)

    for audit in audits:
        date = audit["timestamp"].split("T")[0]
        policy_version = audit.get("policy_version", "unknown")

        policy_drift[policy_version] += 1

        for _, result in audit["comparisons"].items():
            risk = result["risk"]
            approved = result["approved"]

            # ---- Risk trend ----
            risk_trend[date][risk] += 1

            # ---- Approval trend ----
            approval_trend[date]["total"] += 1
            if approved:
                approval_trend[date]["approved"] += 1

            # ---- Rule instability ----
            for reason in result.get("reasons", []):
                rule_instability[reason["category"]] += 1

    # Convert approval counts to rate
    approval_rate_trend = {
        d: round(v["approved"] / v["total"], 2) if v["total"] else 0
        for d, v in approval_trend.items()
    }

    return {
        "risk_trend": dict(risk_trend),
        "approval_rate_trend": approval_rate_trend,
        "policy_drift": dict(policy_drift),
        "unstable_rules": dict(rule_instability),
    }
