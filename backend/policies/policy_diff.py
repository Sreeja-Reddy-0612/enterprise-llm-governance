def diff_policy_results(old_result, new_result):
    """
    Compare governance outcomes between two policy versions
    """

    diff = {
        "risk_changed": old_result["risk"] != new_result["risk"],
        "approved_changed": old_result["approved"] != new_result["approved"],
        "old_risk": old_result["risk"],
        "new_risk": new_result["risk"],
        "old_approved": old_result["approved"],
        "new_approved": new_result["approved"],
        "new_violations": [],
        "resolved_violations": [],
    }

    old_msgs = {r["message"] for r in old_result["reasons"]}
    new_msgs = {r["message"] for r in new_result["reasons"]}

    diff["new_violations"] = list(new_msgs - old_msgs)
    diff["resolved_violations"] = list(old_msgs - new_msgs)

    return diff
