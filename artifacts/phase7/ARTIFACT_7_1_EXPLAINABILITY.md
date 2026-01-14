## Artifact 7.1 — Explainability Layer

### Files Involved
- engine/explainability.py
- engine/governance_engine.py
- app.py

### What Was Implemented
Each prompt evaluation now produces a structured explanation that includes:
- Natural language summary
- Step-by-step reasoning
- Approval / rejection justification
- Policy version used

### Sample Output
```json
"explanation": {
  "summary": "Prompt version 'v1' was evaluated using policy 'v1'. Overall risk was classified as 'MEDIUM'.",
  "details": [
    "Prompt version 'v1' was evaluated using policy 'v1'.",
    "Overall risk was classified as 'MEDIUM'.",
    "The prompt was not approved due to the following findings:",
    "- [MEDIUM] Hallucination Risk: Speculative language detected ('likely')"
  ]
}
