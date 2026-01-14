from evaluators.hallucination import HallucinationEvaluator
from evaluators.policy import PolicyEvaluator
from evaluators.determinism import DeterminismEvaluator
from policies.policy_loader import get_active_policy
from engine.explainability import build_explanation


class GovernanceEngine:
    def __init__(self):
        self.hallucination = HallucinationEvaluator()
        self.policy = PolicyEvaluator()
        self.determinism = DeterminismEvaluator()

    def run(self, text: str, prompt_version: str):
        policy_version, policy = get_active_policy()
        reasons = []

        # ---- Evaluators ----
        reasons.extend(
            self.hallucination.evaluate(text, policy, policy_version)
        )

        # ---- Risk Calculation ----
        risk = (
            "HIGH" if any(r["severity"] == "HIGH" for r in reasons)
            else "MEDIUM" if reasons
            else "LOW"
        )

        approved = risk == "LOW"

        explanation = build_explanation(
            prompt_version=prompt_version,
            risk=risk,
            approved=approved,
            reasons=reasons,
            policy_version=policy_version
        )

        return risk, approved, reasons, policy_version, explanation

    def run_with_policy(self, text: str, policy: dict):
        reasons = []

        if "likely" in text:
            reasons.append({
                "rule_id": "HALLUCINATION_001",
                "category": "Hallucination Risk",
                "severity": policy["hallucination_threshold"],
                "message": "Speculative language detected ('likely')",
                "evidence": "contains speculative term: 'likely'"
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
