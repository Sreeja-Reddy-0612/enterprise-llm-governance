from engine.evaluation_result import EvaluationResult

class DeterminismEvaluator:
    def evaluate(self, text: str):
        results = []

        if len(text.split()) > 100:
            results.append(
                EvaluationResult(
                    id="DETERMINISM_01",
                    severity="MEDIUM",
                    message="Input is overly verbose and non-deterministic"
                )
            )

        return results
