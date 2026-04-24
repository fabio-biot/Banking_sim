from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas import TransactionCreate, TransactionOut
from service.risk_engine import compute_risk

from app.database import get_db
from app import models, schemas

router = APIRouter(prefix="/transactions", tags=["Transactions"])


@router.post("/")
def create_transaction(tx: schemas.TransactionCreate, db: Session = Depends(get_db)):

    from_acc = db.query(models.Account).filter(
        models.Account.id == tx.from_account).first()
    to_acc = db.query(models.Account).filter(
        models.Account.id == tx.to_account).first()

    if not from_acc or not to_acc:
        raise HTTPException(status_code=404, detail="Account not found")

    if from_acc.balance < tx.amount:
        raise HTTPException(status_code=400, detail="Insufficient funds")

    from_acc.balance -= tx.amount
    to_acc.balance += tx.amount

    status = "OK"
    if tx.amount > 10000:
        status = "FLAGGED"

    db_tx = models.Transaction(
        from_account=tx.from_account,
        to_account=tx.to_account,
        amount=tx.amount,
        status=status
    )

    db.add(db_tx)
    db.commit()
    db.refresh(db_tx)

    return db_tx


@router.get("/")
def get_transactions(db: Session = Depends(get_db)):
    return db.query(models.Transaction).all()


@router.get("/transactions/{customer_id}/risk")
def get_risk(customer_id: int, db: Session = Depends(get_db)):
    transactions = db.query(Transaction).filter(
        Transaction.CustomerID == customer_id
    ).all()

    score = compute_risk(transactions)

    return {
        "customer_id": customer_id,
        "risk_score": score
    }
