from datetime import datetime
import numpy as np
import pandas as pd


def compute_features(transactions: pd.DataFrame) -> dict:
    amounts = np.array([t.TransactionAmount_INR for t in transactions])
    # times = np.array([t.TransactionTime for t in transactions])
    # if I add a time notion in the future developpement

    return {
        "count": len(transactions),
        "mean_amount": np.mean(amounts) if len(amounts) else 0,
        "std_amount": np.std(amounts) if len(amounts) else 0,
        "max_amount": np.max(amounts) if len(amounts) else 0,
        "small_tx_ratio": np.sum(amounts < 100) / len(amounts) if len(amounts) else 0,
    }


def build_features(transactions: pd.DataFrame) -> dict:
    datetimes = []

    for t in transactions:
        if t.TransactionDate and t.TransactionTime:
            time_str = str(t.TransactionTime).zfill(6)
            dt = datetime.combine(
                t.TransactionDate.date(),
                datetime.strptime(time_str, "%H%M%S").time()
            )
            datetimes.append(dt)
    datetimes.sort()
    diffs = [
        (t2 - t1).total_seconds()
        for t1, t2 in zip(datetimes, datetimes[1:])
    ]
    velocity = min(diffs) if diffs else 999999
    amounts = [t.TransactionAmount_INR for t in transactions if t.TransactionAmount_INR]
    avg_amount = np.mean(amounts) if amounts else 0
    max_amount = np.max(amounts) if amounts else 0
    small_tx = len([a for a in amounts if a < 100])

    return {
        "velocity": velocity,
        "avg_amount": avg_amount,
        "max_amount": max_amount,
        "small_tx": small_tx,
        "nb_tx": len(transactions)
    }
