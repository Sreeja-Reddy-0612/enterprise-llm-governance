import json
from pathlib import Path

POLICY_FILE = Path("policies/policies.json")


def load_policies():
    if not POLICY_FILE.exists():
        raise FileNotFoundError("policies.json not found")
    with open(POLICY_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_policies(data: dict):
    with open(POLICY_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def get_active_policy():
    data = load_policies()
    active_version = data["active_version"]
    policy = data["versions"][active_version]
    return active_version, policy
