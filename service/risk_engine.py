def check_transaction_risk(amount: float, client_history_count: int):
    risk = 0

    if amount > 10000:
        risk += 50

    if client_history_count < 5:
        risk += 20

    if amount > 50000:
        risk += 100

    return risk