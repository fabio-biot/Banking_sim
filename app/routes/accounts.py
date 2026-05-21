from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas

router = APIRouter(prefix="/accounts", tags=["Accounts"])


@router.post("/", response_model=schemas.AccountOut)
def create_account(account: schemas.AccountCreate, db: Session = Depends(get_db)):

    client = db.query(models.Client).filter(models.Client.id == account.client_id).first()

    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    db_account = models.Account(
        client_id=account.client_id,
        balance=account.balance
    )

    db.add(db_account)
    db.commit()
    db.refresh(db_account)

    return db_account


@router.get("/", response_model=List[schemas.AccountOut])
def get_accounts(db: Session = Depends(get_db)):
    return db.query(models.Account).all()
