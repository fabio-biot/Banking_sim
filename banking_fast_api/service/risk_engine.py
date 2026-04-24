import pandas as pd
import numpy as np


def check_transaction_risk(amount: float, client_history_count: int) -> int:
    risk = 0
    if amount > 10000:
        risk += 50
    if client_history_count < 5:
        risk += 20
    if amount > 50000:
        risk += 100
    return risk


def compute_risk(transactions: pd.DataFrame) -> int:
    score = 0
    amounts = np.array([t.TransactionAmount_INR for t in transactions])
    if len(amounts) == 0:
        return 0
    mean = np.mean(amounts)
    std = np.std(amounts)
    if any(amounts > mean + 3 * std):
        score += 40
    if len(transactions) > 15:
        score += 20
    small_tx = sum(a < 100 for a in amounts)
    if small_tx / len(transactions) > 0.8:
        score += 20
    """
    IF 80% or more of the transactions are less than 100,
    fraud probability increases
    """
    return score


def compute_velocity(transactions):
    times = sorted([t.TransactionTime for t in transactions])

    diffs = [t2 - t1 for t1, t2 in zip(times, times[1:])]

    return min(diffs) if diffs else None
