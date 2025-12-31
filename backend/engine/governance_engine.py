from evaluators import (
    HallucinationEvaluator,
    ToneEvaluator,
    DeterminismEvaluator,
    RefusalEvaluator,
    PolicyEvaluator,
)

class GovernanceEngine:
    def __init__(self):
        # Initialize all evaluators once
        self.evaluators = [
            HallucinationEvaluator(),
            ToneEvaluator(),
            DeterminismEvaluator(),
            RefusalEvaluator(),
            PolicyEvaluator(),
        ]

    def run(self, text: str):
        reasons = []

        # Run each evaluator safely (NO blocking possible)
        for evaluator in self.evaluators:
            try:
                findings = evaluator.evaluate(text)

                # Ensure evaluator always returns a list
                if findings:
                    reasons.extend(findings)

            except Exception as e:
                # Defensive guard — evaluator failure should NOT break system
                reasons.append(
                    f"{evaluator.__class__.__name__} failed safely"
                )

        # ---------- Risk decision logic (TOTAL & GUARANTEED) ----------
        if not reasons:
            return "LOW", True, ["No governance issues detected"]

        if len(reasons) == 1:
            return "MEDIUM", False, reasons

        return "HIGH", False, reasons
