def rule_high_amount(features: dict) -> int:
    if features["max_amount"] > 10000:
        return 30
    return 0


def rule_many_transactions(features: dict) -> int:
    if features["count"] > 20:
        return 20
    return 0


def rule_small_tx_pattern(features: dict) -> int:
    if features["small_tx_ratio"] > 0.8:
        return 25
    return 0


def rule_amount_anomaly(features: dict) -> int:
    if features["std_amount"] > features["mean_amount"]:
        return 25
    return 0


def rule_high_velocity(features: dict) -> int:
    if features.get("min_time_diff") and features["min_time_diff"] < 60:
        return 30
    return 0


def rule_based_score(features: dict) -> int:
    score = 0
    if features["velocity"] < 30:
        score += 40
    if features["max_amount"] > 10000:
        score += 20
    if features["small_tx"] > 5:
        score += 20
    if features["nb_tx"] > 20:
        score += 10
    return min(score, 100)
