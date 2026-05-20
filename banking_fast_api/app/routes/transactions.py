from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas import TransactionCreate, TransactionOut
from service.risk_engine import compute_risk

from app.database import get_db
from app import models, schemas

router = APIRouter(prefix="/transactions", tags=["Transactions"])


@router.post("/", response_model=TransactionOut)
def create_transaction(tx: schemas.TransactionCreate, db: Session = Depends(get_db)):
    import uuid
    import datetime

    from_acc = db.query(models.Account).filter(
        models.Account.id == tx.from_account).first()
    to_acc = db.query(models.Account).filter(
        models.Account.id == tx.to_account).first()

    if not from_acc or not to_acc:
        raise HTTPException(status_code=404, detail="Account not found")

    if from_acc.balance < tx.amount:
        raise HTTPException(status_code=400, detail="Insufficient funds")

    # 💸 UPDATE BALANCES
    from_acc.balance -= tx.amount
    to_acc.balance += tx.amount

    now = datetime.datetime.utcnow()

    db_tx = models.Transaction(
        TransactionID=str(uuid.uuid4()),
        CustomerID=tx.from_account,
        CustomerID_to_account=tx.to_account,
        CustomerDOB=None,
        CustLocation="API Transfer",
        CustAccountBalance=from_acc.balance,
        TransactionDate=now,
        TransactionTime=int(now.strftime("%H%M%S")),
        TransactionAmount_INR=tx.amount
    )

    db.add(db_tx)
    db.commit()
    db.refresh(db_tx)

    return db_tx


@router.get("/")
def get_transactions(db: Session = Depends(get_db)):
    return db.query(models.Transaction).all()


@router.get("/{customer_id}/risk")
def get_risk(customer_id: int, db: Session = Depends(get_db)):
    transactions = db.query(models.Transaction).filter(
        models.Transaction.CustomerID == customer_id
    ).all()

    score = compute_risk(transactions)

    return {
        "customer_id": customer_id,
        "risk_score": score
    }
