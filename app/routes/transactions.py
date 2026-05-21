from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session

from app.crud import create_transaction as create_transaction_crud
from app.database import get_db
from app import models, schemas

router = APIRouter(prefix="/transactions", tags=["Transactions"])


@router.post("/", response_model=schemas.TransactionOut)
def create_transaction(tx: schemas.TransactionCreate, db: Session = Depends(get_db)):
    try:
        return create_transaction_crud(db, tx)
    except ValueError as exc:
        message = str(exc)
        status_code = 404 if message == "Account not found" else 400
        raise HTTPException(status_code=status_code, detail=message)


@router.get("/", response_model=List[schemas.TransactionOut])
def get_transactions(db: Session = Depends(get_db)):
    return db.query(models.Transaction).all()
