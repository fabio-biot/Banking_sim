from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.database import Base
import datetime


class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    country = Column(String)
    risk_score = Column(Float, default=0)

    accounts = relationship("Account", back_populates="client")


class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)
    balance = Column(Float, default=0)
    client_id = Column(Integer, ForeignKey("clients.id"))
    client = relationship("Client", back_populates="accounts")
    transactions_from = relationship("Transaction",
                                     foreign_keys='Transaction.from_account')
    transactions_to = relationship("Transaction",
                                   foreign_keys='Transaction.to_account')


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    from_account = Column(Integer, ForeignKey("accounts.id"))
    to_account = Column(Integer, ForeignKey("accounts.id"))
    amount = Column(Float)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    status = Column(String, default="OK")
