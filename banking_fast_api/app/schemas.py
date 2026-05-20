from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from typing import Optional


class ClientCreate(BaseModel):
    name: str
    country: str
    age: Optional[int] = 30


class ClientOut(BaseModel):
    id: int
    name: str
    country: str
    risk_score: float
    age: Optional[int]

    class Config:
        from_attributes = True


class AccountCreate(BaseModel):
    client_id: int
    balance: float = 0


class TransactionCreate(BaseModel):
    from_account: int
    to_account: int
    amount: float


class TransactionOut(BaseModel):
    TransactionID: str
    CustomerID_to_account: int
    CustomerID: int
    CustomerDOB: Optional[datetime]
    CustLocation: str
    CustAccountBalance: float
    TransactionDate: Optional[datetime]
    TransactionTime: int
    TransactionAmount_INR: float

    class Config:
        from_attributes = True
