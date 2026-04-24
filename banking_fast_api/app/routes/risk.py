from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from app.schemas import Transaction
from app.database import get_db
from risk.engine import compute_global_risk

router = APIRouter(prefix="/risk", tags=["Risk"])


@router.get("/risk/{customer_id}")
def get_risk(customer_id: int, db: Session = Depends(get_db)):

    transactions = db.query(Transaction)\
        .filter(Transaction.CustomerID == customer_id)\
        .all()

    result = compute_global_risk(transactions)

    return result
