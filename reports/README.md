# Reports Directory

This directory contains generated evaluation reports.

## Report Format

Reports are stored as JSON files with the following structure:
- `report_id`: Unique identifier for the report
- `timestamp`: ISO 8601 timestamp
- `query`: The original query
- `prompt_version`: Version of the prompt used
- `decision`: Governance decision (approved/rejected)
- `risk_score`: Overall risk score (0.0-1.0)
- `evaluations`: Detailed evaluation results from all evaluators

