# Prompt Versioning Strategy – Phase 4

# Commit:
# feat: add prompt version comparison and recommendation logic

## Prompt Versions

v1 – Creative
- More flexible language
- Higher chance of speculative phrasing

v2 – Conservative
- Neutral tone
- Reduced risk of advisory language

v3 – Strict
- Highly constrained
- Designed for regulated outputs

## Evaluation Strategy
- Same question evaluated against all versions
- Governance logic remains constant
- Outputs compared side-by-side

## Recommendation Logic
- Select version with lowest risk
- Tie-breaker favors earlier versions (v1 > v2 > v3)

## Outcome
- Prompt-level governance capability
