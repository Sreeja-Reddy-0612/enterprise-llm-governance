from pydantic import BaseModel
from typing import List , Dict
from datetime import datetime
import uuid

class AuditReason(BaseModel):
    evaluator: str
    category: str
    severity: str
    message: str

class AuditRecord(BaseModel):
    timestamp: str
    question: str
    recommended_version: str
    policy_version: str
    comparisons: Dict