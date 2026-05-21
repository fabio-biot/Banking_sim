from pydantic import BaseModel, Field


class ClientCreate(BaseModel):
    name: str
    country: str


class ClientOut(BaseModel):
    id: int
    name: str
    country: str
    risk_score: float

    class Config:
        from_attributes = True


class AccountCreate(BaseModel):
    client_id: int
    balance: float = Field(default=0, ge=0)


class AccountOut(BaseModel):
    id: int
    client_id: int
    balance: float

    class Config:
        from_attributes = True


class TransactionCreate(BaseModel):
    from_account: int
    to_account: int
    amount: float = Field(gt=0)


class TransactionOut(BaseModel):
    id: int
    from_account: int
    to_account: int
    amount: float
    status: str

    class Config:
        from_attributes = True
