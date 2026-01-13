from policies.policy_loader import load_policies, save_policies
from datetime import datetime


def submit_policy(version: str):
    """
    Move a policy into UNDER_REVIEW state
    """
    data = load_policies()

    if version not in data["versions"]:
        raise ValueError("Policy version not found")

    data["versions"][version]["status"] = "UNDER_REVIEW"
    data["versions"][version]["submitted_at"] = datetime.utcnow().isoformat()

    save_policies(data)


def approve_policy(version: str, approved_by: str = "system"):
    """
    Approve a policy that is under review
    """
    data = load_policies()

    if version not in data["versions"]:
        raise ValueError("Policy version not found")

    policy = data["versions"][version]

    if policy.get("status") != "UNDER_REVIEW":
        raise ValueError("Policy is not under review")

    policy["status"] = "APPROVED"
    policy["approved_by"] = approved_by
    policy["approved_at"] = datetime.utcnow().isoformat()

    save_policies(data)


def activate_policy(version: str):
    """
    Activate an approved policy
    Automatically rolls back the currently active policy
    """
    data = load_policies()

    if version not in data["versions"]:
        raise ValueError("Policy version not found")

    policy = data["versions"][version]

    if policy.get("status") != "APPROVED":
        raise ValueError("Only APPROVED policies can be activated")

    current_active = data["active_version"]

    # Roll back current policy
    data["versions"][current_active]["status"] = "ROLLED_BACK"

    # Activate new policy
    policy["status"] = "ACTIVE"
    policy["activated_at"] = datetime.utcnow().isoformat()
    data["active_version"] = version

    save_policies(data)


def rollback_policy(previous_version: str):
    """
    Roll back to a previous policy version
    """
    data = load_policies()

    if previous_version not in data["versions"]:
        raise ValueError("Policy version not found")

    current_active = data["active_version"]

    # Mark current active as rolled back
    data["versions"][current_active]["status"] = "ROLLED_BACK"

    # Restore previous policy
    data["versions"][previous_version]["status"] = "ACTIVE"
    data["versions"][previous_version]["activated_at"] = datetime.utcnow().isoformat()
    data["active_version"] = previous_version

    save_policies(data)
