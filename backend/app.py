from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List, Optional
from datetime import datetime

from engine.governance_engine import GovernanceEngine
from audit.audit_logger import log_audit_event
from audit.audit_store import get_audits, get_audit_by_index
from policies.policy_loader import load_policies
from policies.policy_diff import diff_policy_results

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
    evaluator: str
    category: str
    severity: str
    message: str
    policy_path: Optional[str] = None
    evidence: Optional[str] = None


class VersionResult(BaseModel):
    decision_id: str
    risk: str
    approved: bool
    reasons: List[Finding]
    explanation: Dict


class CompareResponse(BaseModel):
    comparisons: Dict[str, VersionResult]
    recommended_version: str
    policy_version: str
    timestamp: str


class EvaluateRequest(BaseModel):
    prompt_version: str
    question: str


class AuditRecord(BaseModel):
    timestamp: str
    question: str
    recommended_version: str
    comparisons: Dict
    policy_version: Optional[str] = "unknown"


class PolicyImpactRequest(BaseModel):
    question: str
    old_policy_version: str
    new_policy_version: str

@app.post("/compare", response_model=CompareResponse)
def compare_prompt_versions(data: EvaluateRequest):
    versions = ["v1", "v2", "v3"]
    comparisons = {}

    policy_version = "unknown"

    for v in versions:
        result = engine.run(data.question.lower(), v)

        policy_version = result["policy_version"]

        comparisons[v] = VersionResult(
            decision_id=result["decision_id"],
            risk=result["risk"],
            approved=result["approved"],
            reasons=[Finding(**r) for r in result["reasons"]],
            explanation=result["explanation"]
        )

    recommended = min(
        comparisons.keys(),
        key=lambda v: ["LOW", "MEDIUM", "HIGH"].index(comparisons[v].risk)
    )

    timestamp = datetime.utcnow().isoformat()

    log_audit_event(
        question=data.question,
        comparisons={
            k: {
                "decision_id": v.decision_id,
                "risk": v.risk,
                "approved": v.approved,
                "reasons": [r.model_dump() for r in v.reasons]
            }
            for k, v in comparisons.items()
        },
        recommended_version=recommended,
        policy_version=policy_version
    )

    return CompareResponse(
        comparisons=comparisons,
        recommended_version=recommended,
        policy_version=policy_version,
        timestamp=timestamp
    )

# ---------- APIs ----------

@app.post("/policy/impact")
def policy_impact_analysis(data: PolicyImpactRequest):
    policies_data = load_policies()
    versions = policies_data["versions"]

    if data.old_policy_version not in versions:
        raise HTTPException(status_code=404, detail="Old policy version not found")

    if data.new_policy_version not in versions:
        raise HTTPException(status_code=404, detail="New policy version not found")

    old_policy = versions[data.old_policy_version]
    new_policy = versions[data.new_policy_version]

    old_result = engine.run_with_policy(data.question.lower(), old_policy)
    new_result = engine.run_with_policy(data.question.lower(), new_policy)

    impact = diff_policy_results(old_result, new_result)

    return {
        "old_policy_version": data.old_policy_version,
        "new_policy_version": data.new_policy_version,
        "impact": impact
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
