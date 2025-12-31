from semantic.semantic_guard import SemanticGuard
from evaluators.hallucination import HallucinationEvaluator
from evaluators.determinism import DeterminismEvaluator
from evaluators.policy import PolicyEvaluator
from engine.explanation_mapper import map_evaluation_result

class GovernanceEngine:
    def __init__(self):
        self.semantic_guard = SemanticGuard()
        self.hallucination = HallucinationEvaluator()
        self.determinism = DeterminismEvaluator()
        self.policy = PolicyEvaluator()

    def run(self, text: str):
        explainable_reasons = []

        # 🔹 Semantic intent checks
        if self.semantic_guard.check_speculation(text):
            explainable_reasons.append({
                "category": "Semantic Hallucination Risk",
                "severity": "MEDIUM",
                "explanation": (
                    "The intent suggests uncertainty or probabilistic claims "
                    "without firm grounding."
                ),
                "recommendation": (
                    "Clarify assumptions or cite authoritative sources."
                )
            })

        if self.semantic_guard.check_policy_violation(text):
            explainable_reasons.append({
                "category": "Semantic Policy Risk",
                "severity": "HIGH",
                "explanation": (
                    "The intent indicates a request to bypass or avoid regulatory controls."
                ),
                "recommendation": (
                    "Modify the request to align with lawful and compliant practices."
                )
            })

        # 🔹 Rule-based evaluators
        for evaluator in [self.hallucination, self.determinism, self.policy]:
            results = evaluator.evaluate(text)
            for r in results:
                explainable_reasons.append(map_evaluation_result(r).dict())

        # 🔹 Risk aggregation
        if not explainable_reasons:
            return "LOW", True, [{
                "category": "No Risk",
                "severity": "LOW",
                "explanation": "No governance issues detected.",
                "recommendation": "None required."
            }]

        high_risk = any(r["severity"] == "HIGH" for r in explainable_reasons)
        risk_level = "HIGH" if high_risk else "MEDIUM"

        return risk_level, False, explainable_reasons
