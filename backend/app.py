from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List
from datetime import datetime

from engine.governance_engine import GovernanceEngine
from audit.audit_logger import log_audit_event
from audit.audit_store import get_audits, get_audit_by_index

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

# ---------- Models ----------
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


class AuditRecord(BaseModel):
    timestamp: str
    question: str
    recommended_version: str
    comparisons: Dict


# ---------- APIs ----------
@app.post("/compare", response_model=CompareResponse)
def compare_prompt_versions(data: EvaluateRequest):
    versions = ["v1", "v2", "v3"]
    comparisons = {}

    for v in versions:
        risk, approved, reasons = engine.run(data.question.lower(), v)
        comparisons[v] = {
            "risk": risk,
            "approved": approved,
            "reasons": reasons,
        }

    recommended = min(
        comparisons.keys(),
        key=lambda v: ["LOW", "MEDIUM", "HIGH"].index(comparisons[v]["risk"]),
    )

    timestamp = datetime.utcnow().isoformat()

    log_audit_event(
        question=data.question,
        comparisons=comparisons,
        recommended_version=recommended,
    )

    return {
        "comparisons": comparisons,
        "recommended_version": recommended,
        "timestamp": timestamp,
    }


@app.get("/audit/logs", response_model=List[AuditRecord])
def fetch_audit_logs(limit: int = 20):
    return get_audits(limit)


@app.get("/audit/logs/{index}", response_model=AuditRecord)
def fetch_audit_detail(index: int):
    record = get_audit_by_index(index)
    if not record:
        raise HTTPException(status_code=404, detail="Audit record not found")
    return record
