import json
from pathlib import Path

POLICY_FILE = Path(__file__).parent / "policies.json"


def load_policies():
    if not POLICY_FILE.exists():
        raise FileNotFoundError(f"Policy file not found: {POLICY_FILE}")

    with open(POLICY_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def get_active_policy():
    data = load_policies()

    active_version = data["active_version"]
    policy = data["versions"].get(active_version)

    if not policy:
        raise ValueError(f"Active policy version '{active_version}' not found")

    return active_version, policy
