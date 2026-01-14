import uuid
from datetime import datetime

def generate_decision_id():
    return f"DEC-{datetime.utcnow().strftime('%Y%m%d')}-{uuid.uuid4().hex[:8]}"
