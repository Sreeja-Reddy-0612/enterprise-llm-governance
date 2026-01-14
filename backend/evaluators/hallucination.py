from engine.evaluation_result import EvaluationResult

class HallucinationEvaluator:
    RULE_ID = "HALLUCINATION_001"
    POLICY_PATH = "versions.{version}.hallucination_threshold"

    def evaluate(self, text: str, policy: dict, policy_version: str):
        findings = []

        if "likely" in text:
            findings.append({
                "rule_id": self.RULE_ID,
                "evaluator": "HallucinationEvaluator",
                "category": "Hallucination Risk",
                "severity": policy["hallucination_threshold"],
                "message": "Speculative language detected ('likely')",
                "policy_path": self.POLICY_PATH.format(version=policy_version),
                "evidence": "contains speculative term: 'likely'"
            })

        return findings
