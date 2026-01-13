# Evaluator Contract – Phase 2

# Commit:
# implement enterprise LLM governance engine with modular evaluators

## Evaluator Interface

Each evaluator must:
- Accept input text
- Return zero or more EvaluationResult objects

## EvaluationResult Fields
- id: Unique rule identifier
- severity: LOW | MEDIUM | HIGH
- message: Human-readable explanation
- source: Evaluator name

## Example

EvaluationResult(
  id="HALLUCINATION_01",
  severity="MEDIUM",
  message="Speculative language detected ('likely')",
  source="HallucinationEvaluator"
)
