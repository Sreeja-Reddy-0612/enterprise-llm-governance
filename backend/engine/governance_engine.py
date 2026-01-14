from engine.decision_id import generate_decision_id
from engine.explainability import build_explanation
from policies.policy_loader import get_active_policy
from evaluators.hallucination import HallucinationEvaluator
from evaluators.policy import PolicyEvaluator
from evaluators.determinism import DeterminismEvaluator


class GovernanceEngine:
    def __init__(self):
        self.hallucination = HallucinationEvaluator()
        self.policy = PolicyEvaluator()
        self.determinism = DeterminismEvaluator()

    def run(self, text: str, prompt_version: str):
        decision_id = generate_decision_id()
        policy_version, policy = get_active_policy()

        reasons = []

        if "likely" in text:
            reasons.append({
                "evaluator": "HallucinationEvaluator",
                "category": "Hallucination Risk",
                "severity": policy["hallucination_threshold"],
                "message": "Speculative language detected ('likely')",
                "policy_path": f"versions.{policy_version}.hallucination_threshold",
                "evidence": "contains speculative term: 'likely'",
                "rule_id": "HALLUCINATION_001"
            })

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

        return {
            "decision_id": decision_id,
            "risk": risk,
            "approved": approved,
            "reasons": reasons,
            "policy_version": policy_version,
            "explanation": explanation
        }
