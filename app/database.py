'''Database configuration for Banking_sim.

Uses SQLite by default, but can be overridden via the DATABASE_URL environment variable.
''' 

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Get DB URL from env or default to local SQLite file
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./data/bank.db")

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
