from evaluators.hallucination import HallucinationEvaluator
from evaluators.policy import PolicyEvaluator
from evaluators.determinism import DeterminismEvaluator
from policies.policy_loader import get_active_policy


class GovernanceEngine:
    def __init__(self):
        self.hallucination = HallucinationEvaluator()
        self.policy = PolicyEvaluator()
        self.determinism = DeterminismEvaluator()

    def run(self, text: str, prompt_version: str):
        policy_version, policy = get_active_policy()
        reasons = []

        if "likely" in text:
            reasons.append({
                "evaluator": "HallucinationEvaluator",
                "category": "Hallucination Risk",
                "severity": policy["hallucination_threshold"],
                "message": "Speculative language detected ('likely')"
            })

        risk = (
            "HIGH" if any(r["severity"] == "HIGH" for r in reasons)
            else "MEDIUM" if reasons
            else "LOW"
        )

        approved = risk == "LOW"

        return risk, approved, reasons, policy_version

    def run_with_policy(self, text: str, policy: dict):
        reasons = []

        if "likely" in text:
            reasons.append({
                "evaluator": "HallucinationEvaluator",
                "category": "Hallucination Risk",
                "severity": policy["hallucination_threshold"],
                "message": "Speculative language detected ('likely')"
            })

        risk = (
            "HIGH" if any(r["severity"] == "HIGH" for r in reasons)
            else "MEDIUM" if reasons
            else "LOW"
        )

        approved = risk == "LOW"

        return {
            "risk": risk,
            "approved": approved,
            "reasons": reasons
        }
