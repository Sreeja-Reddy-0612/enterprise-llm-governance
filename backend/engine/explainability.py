from typing import Dict, List


def build_explanation(prompt_version, risk, approved, reasons, policy_version):
    details = [
        f"Prompt version '{prompt_version}' was evaluated using policy '{policy_version}'.",
        f"Overall risk was classified as '{risk}'.",
        "The prompt was approved." if approved else "The prompt was not approved due to the following findings:"
    ]

    for r in reasons:
        details.append(
            f"- [{r['severity']}] {r['category']} "
            f"(Rule: {r.get('rule_id')}, Source: {r['evaluator']}) "
            f"→ Evidence: {r.get('evidence')}"
        )

    return {
        "summary": " ".join(details),
        "details": details
    }
