from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List
from datetime import datetime
from engine.governance_engine import GovernanceEngine
from audit.audit_logger import log_audit_event

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
    evaluator: str

class VersionResult(BaseModel):
    risk: str
    approved: bool
    reasons: List[Finding]

class CompareResponse(BaseModel):
    comparisons: Dict[str, VersionResult]
    recommended_version: str
    timestamp: str

class EvaluateRequest(BaseModel):
    prompt_version: str
    question: str


# ---------- API Endpoint ----------
@app.post("/compare", response_model=CompareResponse)
def compare_prompt_versions(data: EvaluateRequest):
    versions = ["v1", "v2", "v3"]
    comparisons = {}

    for v in versions:
        risk, approved, reasons = engine.run(data.question.lower(), v)
        comparisons[v] = {
            "risk": risk,
            "approved": approved,
            "reasons": reasons
        }

    recommended = min(
        comparisons.keys(),
        key=lambda v: ["LOW", "MEDIUM", "HIGH"].index(comparisons[v]["risk"])
    )

    # Evaluate timestamp and audit log
    evaluated_at = datetime.utcnow().isoformat()

    # 🔐 AUDIT LOGGING (Phase 6 – Step 1)
    log_audit_event(
        question=data.question,
        comparisons=comparisons,
        recommended_version=recommended
    )

    return {
        "comparisons": comparisons,
        "recommended_version": recommended,
        "timestamp": evaluated_at,
    }
