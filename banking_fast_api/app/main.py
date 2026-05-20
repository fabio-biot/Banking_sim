from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from app.database import Base, engine, SessionLocal
from app.routes import clients, accounts, transactions, risk
from risk.features import build_features
from app.train_model.train_model import train_model
from app import models
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="🏦 Advanced Banking & Fraud Detection API",
    description="High-performance backend API with real-time transaction risk scoring and Machine Learning anomaly detection.",
    version="1.0.0"
)

Base.metadata.create_all(bind=engine)

app.include_router(transactions.router)
app.include_router(clients.router)
app.include_router(accounts.router)
app.include_router(risk.router)


@app.on_event("startup")
def startup_event():
    db = SessionLocal()
    try:
        logger.info("Initializing and training Isolation Forest model on historical transactions...")
        txs = db.query(models.Transaction).all()
        if not txs:
            logger.warning("No transactions found in database. ML model fallback activated.")
            app.state.model = None
            return

        # Group by customer
        by_customer = {}
        for tx in txs:
            by_customer.setdefault(tx.CustomerID, []).append(tx)

        # Build features
        feature_list = []
        for cust_id, cust_txs in by_customer.items():
            feats = build_features(cust_txs)
            feature_list.append([
                feats["velocity"],
                feats["avg_amount"],
                feats["max_amount"],
                feats["small_tx"],
                feats["nb_tx"]
            ])

        if len(feature_list) < 5:
            logger.warning("Too few customers to train Isolation Forest. ML model fallback activated.")
            app.state.model = None
            return

        model = train_model(feature_list)
        app.state.model = model
        logger.info(f"Isolation Forest model trained successfully on {len(feature_list)} customer profiles! 🚀")
    except Exception as e:
        logger.error(f"Error training ML model during startup: {e}")
        app.state.model = None
    finally:
        db.close()


@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Banking & Fraud Detection Platform</title>
        <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&family=JetBrains+Mono:wght@400;700&display=swap" rel="stylesheet">
        <style>
            :root {
                --bg-gradient: linear-gradient(135deg, #0f172a 0%, #020617 100%);
                --primary: #6366f1;
                --primary-glow: rgba(99, 102, 241, 0.15);
                --text-main: #f8fafc;
                --text-muted: #94a3b8;
                --glass-bg: rgba(30, 41, 59, 0.4);
                --glass-border: rgba(255, 255, 255, 0.08);
            }
            
            body {
                font-family: 'Outfit', sans-serif;
                background: var(--bg-gradient);
                color: var(--text-main);
                min-height: 100vh;
                margin: 0;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                overflow-x: hidden;
            }

            .container {
                max-width: 650px;
                padding: 48px;
                background: var(--glass-bg);
                backdrop-filter: blur(20px);
                -webkit-backdrop-filter: blur(20px);
                border: 1px solid var(--glass-border);
                border-radius: 24px;
                box-shadow: 0 20px 40px rgba(0, 0, 0, 0.5), 0 0 100px var(--primary-glow);
                text-align: center;
                transition: transform 0.3s ease, border-color 0.3s ease;
            }

            .container:hover {
                transform: translateY(-4px);
                border-color: rgba(99, 102, 241, 0.3);
            }

            .badge {
                display: inline-block;
                padding: 6px 16px;
                background: rgba(99, 102, 241, 0.2);
                border: 1px solid rgba(99, 102, 241, 0.4);
                border-radius: 9999px;
                color: #818cf8;
                font-weight: 600;
                font-size: 0.85rem;
                margin-bottom: 24px;
                text-transform: uppercase;
                letter-spacing: 0.05em;
            }

            h1 {
                font-size: 2.8rem;
                font-weight: 800;
                margin: 0 0 16px 0;
                background: linear-gradient(135deg, #fff 0%, #cbd5e1 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                letter-spacing: -0.02em;
            }

            p {
                color: var(--text-muted);
                font-size: 1.15rem;
                line-height: 1.6;
                margin: 0 0 40px 0;
            }

            .features {
                display: flex;
                justify-content: space-around;
                gap: 16px;
                margin-bottom: 44px;
            }

            .feature-card {
                flex: 1;
                background: rgba(15, 23, 42, 0.6);
                border: 1px solid var(--glass-border);
                padding: 16px;
                border-radius: 14px;
            }

            .feature-card h3 {
                margin: 0 0 6px 0;
                font-size: 1rem;
                color: #818cf8;
            }

            .feature-card p {
                margin: 0;
                font-size: 0.85rem;
                color: var(--text-muted);
            }

            a.btn-docs {
                display: inline-block;
                padding: 14px 32px;
                background: var(--primary);
                color: #fff;
                text-decoration: none;
                font-weight: 600;
                font-size: 1.05rem;
                border-radius: 12px;
                box-shadow: 0 4px 14px rgba(99, 102, 241, 0.4);
                transition: transform 0.2s ease, box-shadow 0.2s ease, background 0.2s ease;
            }

            a.btn-docs:hover {
                transform: translateY(-2px);
                box-shadow: 0 6px 20px rgba(99, 102, 241, 0.6), 0 0 30px rgba(99, 102, 241, 0.3);
                background: #4f46e5;
            }

            footer {
                margin-top: 36px;
                font-family: 'JetBrains Mono', monospace;
                font-size: 0.8rem;
                color: #475569;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <span class="badge">Production-Ready API</span>
            <h1>Banking & Fraud Engine</h1>
            <p>A high-performance banking transaction core backed by FastAPI, SQLAlchemy, and an online Isolation Forest Machine Learning model for instant anomaly scoring.</p>
            
            <div class="features">
                <div class="feature-card">
                    <h3>⚡ FastAPI Core</h3>
                    <p>Sub-millisecond endpoints for Clients, Accounts, & Transactions.</p>
                </div>
                <div class="feature-card">
                    <h3>🧠 Real-time ML</h3>
                    <p>Isolation Forest anomaly scoring trained dynamically at startup.</p>
                </div>
                <div class="feature-card">
                    <h3>🛡️ Dual Engine</h3>
                    <p>Combined heuristic rules + ML probability risk scoring.</p>
                </div>
            </div>

            <a href="/docs" class="btn-docs">Open Interactive API Documentation 🚀</a>
        </div>
        <footer>
            Built with FastAPI, Scikit-Learn & SQLite
        </footer>
    </body>
    </html>
    """
