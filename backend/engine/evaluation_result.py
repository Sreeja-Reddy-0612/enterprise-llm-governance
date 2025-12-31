from dataclasses import dataclass

@dataclass
class EvaluationResult:
    id: str
    severity: str   # LOW | MEDIUM | HIGH
    message: str
