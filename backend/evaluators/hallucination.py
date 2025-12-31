class HallucinationEvaluator:
    def evaluate(self, text: str):
        keywords = ["maybe", "likely", "probably", "might"]

        if any(word in text for word in keywords):
            return ["Speculative language detected"]

        return []
