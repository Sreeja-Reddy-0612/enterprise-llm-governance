from engine.explainability import ExplainableReason
from engine.evaluation_result import EvaluationResult

def map_evaluation_result(result: EvaluationResult) -> ExplainableReason:
    if result.id.startswith("HALLUCINATION"):
        return ExplainableReason(
            category="Hallucination Risk",
            severity=result.severity,
            explanation=(
                "The input contains speculative language that implies uncertainty "
                "without citing authoritative sources or legal thresholds."
            ),
            recommendation=(
                "Rephrase the statement using factual language or provide verified references."
            )
        )

    if result.id.startswith("POLICY"):
        return ExplainableReason(
            category="Policy Violation",
            severity=result.severity,
            explanation=(
                "The request seeks guidance that may bypass or undermine regulatory obligations, "
                "which is not allowed under enterprise AI usage policies."
            ),
            recommendation=(
                "Reframe the question to focus on compliant processes or lawful alternatives."
            )
        )

    if result.id.startswith("DETERMINISM"):
        return ExplainableReason(
            category="Non-Deterministic Input",
            severity=result.severity,
            explanation=(
                "The input is overly verbose or ambiguous, making deterministic interpretation difficult."
            ),
            recommendation=(
                "Simplify and narrow the question to one clear, specific request."
            )
        )

    # Fallback (safe)
    return ExplainableReason(
        category="General Risk",
        severity="MEDIUM",
        explanation=result.message,
        recommendation="Review and clarify the request."
    )
