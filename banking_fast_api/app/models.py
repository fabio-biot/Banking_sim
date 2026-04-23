from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.database import Base
import datetime


class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    age = Column(String)
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
                                     foreign_keys='Transaction.CustomerID')
    transactions_to = relationship("Transaction",
                                   foreign_keys='Transaction.CustomerID_to_account')


class Transaction(Base):
    __tablename__ = "transactions"

    TransactionID = Column(String, primary_key=True, index=True)
    CustomerID_to_account = Column(Integer, ForeignKey("accounts.id"))
    CustomerID = Column(Integer, ForeignKey("accounts.id"))
    CustomerDOB = Column(DateTime, nullable=True)
    CustLocation = Column(String)
    CustAccountBalance = Column(Float)
    TransactionDate = Column(DateTime, nullable=True)
    TransactionTime = Column(Integer)
    TransactionAmount_INR = Column(Float)
