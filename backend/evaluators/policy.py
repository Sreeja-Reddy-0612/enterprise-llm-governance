class PolicyEvaluator:
    def evaluate(self, text: str):
        reasons = []
        if "advice" in text:
            reasons.append("Policy violation: advice detected")
        return reasons
