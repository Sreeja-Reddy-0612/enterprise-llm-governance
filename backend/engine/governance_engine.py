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
        # Load active policy
        policy_version, policy = get_active_policy()

        reasons = []

        # ---- Hallucination check (example rule) ----
        if "likely" in text:
            reasons.append({
                "evaluator": "HallucinationEvaluator",
                "category": "Hallucination Risk",
                "severity": policy["hallucination_threshold"],
                "message": "Speculative language detected ('likely')"
            })

        # ---- Risk calculation ----
        if any(r["severity"] == "HIGH" for r in reasons):
            risk = "HIGH"
        elif reasons:
            risk = "MEDIUM"
        else:
            risk = "LOW"

        approved = risk == "LOW"

        # ---- Explainability ----
        explanation = build_explanation(
            prompt_version=prompt_version,
            risk=risk,
            approved=approved,
            reasons=reasons,
            policy_version=policy_version
        )

        return risk, approved, reasons, policy_version, explanation

    def run_with_policy(self, text: str, policy: dict):
        """
        Used for policy impact analysis (Phase 6 – Step 4.2)
        """
        reasons = []

        if "likely" in text:
            reasons.append({
                "evaluator": "HallucinationEvaluator",
                "category": "Hallucination Risk",
                "severity": policy["hallucination_threshold"],
                "message": "Speculative language detected ('likely')"
            })

        if any(r["severity"] == "HIGH" for r in reasons):
            risk = "HIGH"
        elif reasons:
            risk = "MEDIUM"
        else:
            risk = "LOW"

        approved = risk == "LOW"

        return {
            "risk": risk,
            "approved": approved,
            "reasons": reasons
        }
