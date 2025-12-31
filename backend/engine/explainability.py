from pydantic import BaseModel

class ExplainableReason(BaseModel):
    category: str          # hallucination / policy / determinism
    severity: str          # LOW / MEDIUM / HIGH
    explanation: str       # human-readable reason
    recommendation: str   # what user should do
