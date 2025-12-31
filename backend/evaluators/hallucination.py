from engine.evaluation_result import EvaluationResult

class HallucinationEvaluator:
    SPECULATIVE_WORDS = ["likely", "probably", "may", "might", "could"]

    def evaluate(self, text: str):
        results = []

        for word in self.SPECULATIVE_WORDS:
            if word in text:
                results.append(
                    EvaluationResult(
                        id="HALLUCINATION_01",
                        severity="MEDIUM",
                        message=f"Speculative language detected ('{word}')"
                    )
                )
                break

        return results
