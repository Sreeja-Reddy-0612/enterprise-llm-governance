from typing import Dict, List


def build_explanation(
    prompt_version: str,
    risk: str,
    approved: bool,
    reasons: List[Dict],
    policy_version: str
) -> Dict:
    """
    Generates a human-readable explanation for a governance decision
    """

    explanation_lines = []

    explanation_lines.append(
        f"Prompt version '{prompt_version}' was evaluated using policy '{policy_version}'."
    )

    explanation_lines.append(
        f"Overall risk was classified as '{risk}'."
    )

    if approved:
        explanation_lines.append("The prompt was approved because no high-risk issues were detected.")
    else:
        explanation_lines.append("The prompt was not approved due to the following findings:")

        for r in reasons:
            explanation_lines.append(
                f"- [{r['severity']}] {r['category']}: {r['message']} (via {r['evaluator']})"
            )

    return {
        "summary": " ".join(explanation_lines),
        "details": explanation_lines
    }
