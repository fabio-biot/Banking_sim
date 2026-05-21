'''Main entry point for the Banking_sim FastAPI application.

Provides CORS support and includes routers for clients, accounts, and transactions.
''' 

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine
from app.routes import clients, accounts, transactions

app = FastAPI(title="Banking Simulation API", version="1.0.0")

# Allow all origins for simplicity; adjust in production.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create database tables
Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(clients.router)
app.include_router(accounts.router)
app.include_router(transactions.router)
