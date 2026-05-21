'''Main entry point for the Banking_sim FastAPI application.

Provides CORS support and includes routers for clients, accounts, and transactions.
''' 

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
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


@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <!doctype html>
    <html lang="fr">
      <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>Banking Simulation API</title>
        <style>
          body {
            margin: 0;
            font-family: Arial, sans-serif;
            background: #f4f6f8;
            color: #1f2937;
          }
          main {
            max-width: 760px;
            margin: 48px auto;
            padding: 0 24px;
          }
          h1 {
            margin-bottom: 8px;
            font-size: 32px;
          }
          p {
            color: #4b5563;
            line-height: 1.5;
          }
          .links {
            display: grid;
            gap: 12px;
            margin-top: 28px;
          }
          a {
            display: block;
            padding: 16px;
            border: 1px solid #d1d5db;
            border-radius: 8px;
            background: white;
            color: #111827;
            text-decoration: none;
            font-weight: 600;
          }
          a:hover {
            border-color: #2563eb;
            color: #2563eb;
          }
          span {
            display: block;
            margin-top: 4px;
            color: #6b7280;
            font-size: 14px;
            font-weight: 400;
          }
        </style>
      </head>
      <body>
        <main>
          <h1>Banking Simulation API</h1>
          <p>Menu rapide pour acceder aux routes principales de l'API.</p>

          <div class="links">
            <a href="/docs">Swagger UI<span>Tester l'API depuis le navigateur</span></a>
            <a href="/clients/">Clients<span>Afficher la liste des clients</span></a>
            <a href="/accounts/">Comptes<span>Afficher les comptes et les soldes</span></a>
            <a href="/transactions/">Transactions<span>Afficher l'historique des virements</span></a>
            <a href="/openapi.json">OpenAPI JSON<span>Schema technique de l'API</span></a>
          </div>
        </main>
      </body>
    </html>
    """
