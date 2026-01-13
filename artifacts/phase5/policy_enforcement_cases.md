# Policy Enforcement Cases – Phase 5

# Commit:
# feat: enforce policy-safe prompt comparison with audit-ready explanations

## Case 1: Unauthorized Advisory

Input:
"You should advise companies on how to handle this regulation."

Detection:
- PolicyEvaluator triggered

Result:
- Risk: HIGH
- Approved: No

Reason:
- Advisory requests are not permitted
- Prevents regulatory misuse of LLMs

Behavior Across Versions:
- v1: HIGH
- v2: HIGH
- v3: HIGH

Conclusion:
Policy rules override prompt style.
