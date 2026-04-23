from app.models import Account, Transaction
from service.risk_engine import check_transaction_risk


def create_transaction(db, data):

    from_acc = db.query(Account).filter(Account.id == data.from_account).first()
    to_acc = db.query(Account).filter(Account.id == data.to_account).first()

    if from_acc.balance < data.amount:
        raise Exception("Insufficient funds")

    from_acc.balance -= data.amount
    to_acc.balance += data.amount

    risk = check_transaction_risk(data.amount, 0)

    status = "FLAGGED" if risk > 50 else "OK"

    transaction = Transaction(
        from_account=data.from_account,
        to_account=data.to_account,
        amount=data.amount,
        status=status
    )

    db.add(transaction)
    db.commit()
    db.refresh(transaction)

    return transaction
