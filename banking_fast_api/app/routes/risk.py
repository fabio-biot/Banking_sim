from fastapi import Depends, APIRouter, Request, HTTPException
from sqlalchemy.orm import Session
from app import models
from app.database import get_db
from risk.engine import compute_global_risk

router = APIRouter(prefix="/risk", tags=["Risk"])


@router.get("/{customer_id}")
def get_risk(customer_id: int, request: Request, db: Session = Depends(get_db)):
    # Check if client exists
    client = db.query(models.Client).filter(models.Client.id == customer_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    # Get accounts of this client
    accounts = db.query(models.Account).filter(models.Account.client_id == customer_id).all()
    account_ids = [acc.id for acc in accounts]

    # Get transactions where this client is either the sender or receiver
    transactions = db.query(models.Transaction).filter(
        models.Transaction.CustomerID.in_(account_ids) | 
        models.Transaction.CustomerID_to_account.in_(account_ids)
    ).all()

    # Get trained model from app state
    model = getattr(request.app.state, "model", None)

    # Compute risk score
    result = compute_global_risk(transactions, model=model)

    return {
        "client_name": client.name,
        "client_country": client.country,
        "risk_analysis": result
    }
