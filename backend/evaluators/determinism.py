class DeterminismEvaluator:
    def evaluate(self, text: str):
        reasons = []
        if len(text.split()) > 100:
            reasons.append("Non-deterministic or overly verbose input")
        return reasons
