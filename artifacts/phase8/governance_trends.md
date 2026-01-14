🧾 Artifact 8.2 — Governance Trends (Time-Series Analysis)
Files involved
backend/metrics/governance_trends.py
backend/app.py
audit/audit_store.py

API
GET /metrics/governance/trends

Example Output
{
  "risk_trend": {
    "2026-01-14": { "MEDIUM": 18 },
    "2026-01-13": { "MEDIUM": 12 }
  },
  "approval_rate_trend": {
    "2026-01-14": 0,
    "2026-01-13": 0
  },
  "policy_drift": {
    "v1": 10
  },
  "unstable_rules": {
    "Hallucination Risk": 30
  }
}

What this proves

Risk behavior over time

Approval rate trends

Policy usage drift

Rule instability detection

Enterprise value

Detects slow compliance decay before it becomes an incident.