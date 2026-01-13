from engine.audit_models import AuditRecord, AuditReason
from engine.audit_logger import log_audit

from evaluators.hallucination import HallucinationEvaluator
from evaluators.policy import PolicyEvaluator
from evaluators.determinism import DeterminismEvaluator

class GovernanceEngine:
    def __init__(self):
        self.hallucination = HallucinationEvaluator()
        self.policy = PolicyEvaluator()
        self.determinism = DeterminismEvaluator()

    def run(self, text: str, version: str):
        reasons = []

        for r in self.hallucination.evaluate(text):
            reasons.append(
                AuditReason(
                    evaluator="HallucinationEvaluator",
                    category="Hallucination Risk",
                    severity=r.severity,
                    message=r.message
                )
            )

        for r in self.policy.evaluate(text):
            reasons.append(
                AuditReason(
                    evaluator="PolicyEvaluator",
                    category="Policy Violation",
                    severity=r.severity,
                    message=r.message
                )
            )

        for r in self.determinism.evaluate(text):
            reasons.append(
                AuditReason(
                    evaluator="DeterminismEvaluator",
                    category="Non-determinism",
                    severity=r.severity,
                    message=r.message
                )
            )

        if not reasons:
            risk = "LOW"
            approved = True
            reasons.append(
                AuditReason(
                    evaluator="System",
                    category="No Risk",
                    severity="LOW",
                    message="No governance issues detected"
                )
            )
        else:
            risk = "HIGH" if any(r.severity == "HIGH" for r in reasons) else "MEDIUM"
            approved = False

        return risk, approved, reasons
