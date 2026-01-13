from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List
from engine.governance_engine import GovernanceEngine
from engine.audit_models import AuditRecord
from engine.audit_logger import log_audit

app = FastAPI(title="Enterprise LLM Governance API")
engine = GovernanceEngine()

# ---------- CORS ----------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------- Request Models ----------
class CompareRequest(BaseModel):
    prompt_version: str
    question: str

# ---------- Response Models ----------
class Finding(BaseModel):
    category: str
    severity: str
    message: str

class VersionResult(BaseModel):
    risk: str
    approved: bool
    reasons: List[Finding]

class CompareResponse(BaseModel):
    comparisons: Dict[str, VersionResult]
    recommended_version: str

class EvaluateRequest(BaseModel):
    prompt_version: str
    question: str


# ---------- API Endpoint ----------
@app.post("/compare")
def compare_prompt_versions(data: EvaluateRequest):
    versions = ["v1", "v2", "v3"]
    comparisons = {}

    for v in versions:
        risk, approved, reasons = engine.run(data.question.lower(), v)

        record = AuditRecord(
            evaluation_id=AuditRecord.create_id(),
            prompt_version=v,
            question=data.question,
            risk_level=risk,
            approved=approved,
            reasons=reasons,
            timestamp=AuditRecord.now()
        )

        log_audit(record)

        comparisons[v] = {
            "risk": risk,
            "approved": approved,
            "reasons": reasons
        }

    recommended = min(
        comparisons.keys(),
        key=lambda v: ["LOW", "MEDIUM", "HIGH"].index(comparisons[v]["risk"])
    )

    return {
        "comparisons": comparisons,
        "recommended_version": recommended
    }