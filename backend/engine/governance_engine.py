from evaluators.hallucination import HallucinationEvaluator
from evaluators.determinism import DeterminismEvaluator
from evaluators.policy import PolicyEvaluator

class GovernanceEngine:
    def __init__(self):
        self.evaluators = [
            HallucinationEvaluator(),
            DeterminismEvaluator(),
            PolicyEvaluator()
        ]

    def run(self, text: str):
        all_results = []

        for evaluator in self.evaluators:
            try:
                results = evaluator.evaluate(text)
                all_results.extend(results)
            except Exception:
                all_results.append({
                    "id": "SYSTEM_FAIL",
                    "severity": "HIGH",
                    "message": "Evaluator failed safely"
                })

        if not all_results:
            return "LOW", True, ["No governance issues detected"]

        severity_levels = [r.severity for r in all_results]

        if "HIGH" in severity_levels:
            risk = "HIGH"
        elif "MEDIUM" in severity_levels:
            risk = "MEDIUM"
        else:
            risk = "LOW"

        approved = risk == "LOW"

        reasons = [r.message for r in all_results]

        return risk, approved, reasons
