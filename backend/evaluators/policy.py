from engine.evaluation_result import EvaluationResult

class PolicyEvaluator:
    def evaluate(self, text: str):
        results = []

        if "bypass" in text or "avoid regulation" in text or "how to evade" in text:
            results.append(
                EvaluationResult(
                    id="POLICY_01",
                    severity="HIGH",
                    message="Policy violation detected: request to bypass regulations"
                )
            )

        if "advise" in text:
            results.append(
                EvaluationResult(
                    id="POLICY_02",
                    severity="HIGH",
                    message="Unauthorized advisory request detected"
                )
            )

        return results
