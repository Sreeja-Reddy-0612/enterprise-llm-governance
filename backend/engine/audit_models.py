from pydantic import BaseModel
from typing import List
from datetime import datetime
import uuid

class AuditReason(BaseModel):
    evaluator: str
    category: str
    severity: str
    message: str

class AuditRecord(BaseModel):
    evaluation_id: str
    prompt_version: str
    question: str
    risk_level: str
    approved: bool
    reasons: List[AuditReason]
    timestamp: str

    @staticmethod
    def create_id():
        return str(uuid.uuid4())

    @staticmethod
    def now():
        return datetime.utcnow().isoformat()
