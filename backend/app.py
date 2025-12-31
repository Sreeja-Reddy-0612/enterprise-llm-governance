from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from engine.governance_engine import GovernanceEngine

engine = GovernanceEngine()
app = FastAPI(title="Enterprise LLM Governance API")

# ---------- CORS ----------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------- Request & Response Models ----------
class EvaluateRequest(BaseModel):
    prompt_version: str
    question: str

class EvaluateResponse(BaseModel):
    risk_level: str
    approved: bool
    reasons: List[str]

# ---------- API Endpoint ----------
@app.post("/evaluate", response_model=EvaluateResponse)
def evaluate_prompt(data: EvaluateRequest):
    print("➡️ Received request")
    risk, approved, reasons = engine.run(data.question.lower())
    print("✅ Engine completed")
    return {
        "risk_level": risk,
        "approved": approved,
        "reasons": reasons
    }
