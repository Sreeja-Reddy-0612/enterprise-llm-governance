# Risk Scoring Logic – Phase 3

# Commit:
# feat: stabilize governance API with semantic and rule-based evaluators

## Risk Levels

LOW
- No evaluator flags
- Approved = true

MEDIUM
- At least one MEDIUM severity issue
- Approved = false

HIGH
- Any HIGH severity issue
- Approved = false

## Aggregation Rules
- HIGH overrides MEDIUM and LOW
- MEDIUM overrides LOW
- Reasons are accumulated for auditability

## Outcome
- Deterministic, explainable decisions
- Consistent behavior across inputs
