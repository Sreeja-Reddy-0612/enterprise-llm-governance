from evaluators.hallucination import HallucinationEvaluator
from evaluators.determinism import DeterminismEvaluator
from evaluators.policy import PolicyEvaluator
from engine.evaluation_result import EvaluationResult

class GovernanceEngine:
    def __init__(self):
        self.hallucination = HallucinationEvaluator()
        self.determinism = DeterminismEvaluator()
        self.policy = PolicyEvaluator()

    def run(self, text: str):
        reasons: list[str] = []

        # --- Hallucination ---
        for r in self.hallucination.evaluate(text):
            reasons.append(r.message)

        # --- Determinism ---
        for r in self.determinism.evaluate(text):
            reasons.append(r.message)

        # --- Policy ---
        for r in self.policy.evaluate(text):
            reasons.append(r.message)

        # --- Risk decision ---
        if not reasons:
            return "LOW", True, ["No governance issues detected"]
        elif len(reasons) == 1:
            return "MEDIUM", False, reasons
        else:
            return "HIGH", False, reasons
