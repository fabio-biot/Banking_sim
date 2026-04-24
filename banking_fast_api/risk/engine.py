
from sklearn.ensemble import IsolationForest
from .features import compute_features, build_features
from .rules import rule_amount_anomaly, rule_small_tx_pattern, rule_high_amount, rule_many_transactions, rule_based_score
import pandas as pd
import numpy as np


def compute_risk(transactions: pd.DataFrame) -> int:
    features = compute_features(transactions)

    score = 0

    rules = [
        rule_high_amount,
        rule_many_transactions,
        rule_small_tx_pattern,
        rule_amount_anomaly
    ]

    for rule in rules:
        score += rule(features)

    return min(score, 100), features


def ml_score(features, model=None):
    X = np.array([[
        features["velocity"],
        features["avg_amount"],
        features["max_amount"],
        features["small_tx"],
        features["nb_tx"]
    ]])

    if model is None:
        return 0  # fallback

    pred = model.predict(X)  # -1 anomalie, 1 normal

    return 50 if pred[0] == -1 else 0


def compute_global_risk(transactions, model=None):
    features = build_features(transactions)

    rule_score = rule_based_score(features)
    ml_part = ml_score(features, model)

    final_score = 0.7 * rule_score + 0.3 * ml_part

    return {
        "score": int(final_score),
        "details": {
            "rules": rule_score,
            "ml": ml_part,
            "features": features
        }
    }
