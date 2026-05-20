# 🏦 Advanced Banking Core & ML-Powered Fraud Detection API

An institutional-grade banking API featuring robust accounts management, vectorized transaction pipelines, and a **real-time Hybrid Fraud Detection Engine** combining rule-based heuristics and **Isolation Forest Unsupervised Machine Learning** (Scikit-Learn).

This API is built for sub-millisecond route performance and trains its predictive models dynamically on startup using historical client profiles.

---

## 🚀 Key Features

* **⚡ FastAPI Core Engine:** Fully asynchronous, clean REST API implementing endpoints for Clients, Accounts, and Transactions.
* **🧠 Dynamic ML Anomaly Detection:** An online **Isolation Forest** model automatically trains at server startup on the active database to classify transaction behavior anomalies.
* **🛡️ Dual-Layer Risk Engine:** Calculates a hybrid risk score (0 to 100) combining:
  * *Heuristics:* Velocity anomalies, small transaction patterns, high amount spikes, and statistical standard deviation variance.
  * *Machine Learning:* Unsupervised multidimensional anomaly detection.
* **📊 Vectorized ETL Pipeline (`seed.py`):** Structured loading, formatting, and relational seeding of **100k+ real Kaggle bank transactions** joined against custom client profiles using Pandas and NumPy.
* **✨ Glassmorphic Interactive Gateway:** A gorgeous CSS glassmorphism home page serving as the entrance to the Swagger interactive documentation.

---

## 📐 Architecture & Modules

```
banking_fast_api/
│
├── app/
│   ├── routes/
│   │     ├── clients.py         # Client creation and listing (with Age & Country)
│   │     ├── accounts.py        # Account creations (with balance verification)
│   │     ├── transactions.py    # Transaction processing and inline validation
│   │     └── risk.py            # Unified ML & rule-based risk evaluation endpoint
│   │
│   ├── train_model/
│   │     └── train_model.py     # Isolation Forest Scikit-Learn training utility
│   │
│   ├── database.py              # SQLAlchemy connection & session manager
│   ├── models.py                # SQLite relational schemas (Clients, Accounts, Transactions)
│   ├── schemas.py               # Pydantic data validation and formatting schemas
│   ├── seed.py                  # Kaggle dataset cleaner and database seeder
│   └── main.py                  # API entry point & startup ML training lifecycles
│
├── risk/                        # Concurrency-aware Fraud Engine
│   ├── engine.py                # Global hybrid score computer
│   ├── features.py              # Transaction behavior feature extractor
│   └── rules.py                 # Pure rule-based fraud scoring heuristics
│
├── service/
│   └── risk_engine.py           # Legacy transactional rule services
│
├── data/
│   ├── Base Client.xlsx         # Seeding source for clients
│   ├── bank_transactions.csv    # Kaggle dataset (100k rows)
│   └── bank.db                  # Seeded SQLite Database
│
├── makefile                     # Quick automation shortcuts
├── requirements.txt             # Python dependencies
└── README.md                    # Project documentation
```

---

## 🧠 The Hybrid Fraud Detection Engine

The system uses a two-pronged strategy to protect accounts and flag suspicious activities:

### 1. Feature Engineering
When a risk score is requested for a customer, the `risk/features.py` module aggregates the customer's transactions to build the following profile:
* **Velocity:** The minimum time difference (in seconds) between sequential transactions.
* **Avg Amount:** Mean transaction amount.
* **Max Amount:** Highest amount spent.
* **Small Tx count:** Number of micro-transactions (< 100 INR/currency unit) which often precedes carding fraud.
* **Nb Tx:** Total volume of transactions.

### 2. Isolation Forest ML Model
At server startup, the API queries all transactions in the database, extracts these 5 behavioral features for every customer, and fits an **Isolation Forest** model (`contamination=0.05`). 
During API runtime, the trained model evaluates the client profile:
* **Normal Behavior:** Returns standard risk profiles.
* **Anomalous Profiles:** Automatically adds a **+50 risk penalty** to the customer profile.

### 3. Rule-Based Heuristics
A static layer computes risk based on deterministic banking rules:
* **Transaction Velocity:** If velocity < 30 seconds between transactions, adds a **+40 penalty**.
* **Micro-transaction patterns:** Frequent small transactions adds a **+20 penalty**.
* **High-value spikes:** Transactions > 10,000 add a **+20 penalty**.

The final score is a weighted average: `0.7 * Rules_Score + 0.3 * ML_Score`, returning a transparent risk breakdown.

---

## 🛠️ Installation & Execution

### 1. Clone & Set Up Environment
```bash
# Navigate to project
cd banking_fast_api

# Create a virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Seed the Database
Run the pipeline to format, clean, and load the 100k+ Kaggle transactions into the SQLite relational database:
```bash
PYTHONPATH=. python3 app/seed.py
```

### 3. Start the Server
Run the FastAPI application with Uvicorn:
```bash
PYTHONPATH=. python3 -m uvicorn app.main:app --reload --port 8000
```
On startup, you will see the logs showing the **successful training of the Isolation Forest model** on the seeded profiles.

---

## 🔗 Endpoints Preview

* **`GET /`** - Elegant landing page.
* **`GET /docs`** - Interactive OpenAPI Swagger UI.
* **`POST /clients/`** - Create new clients.
* **`POST /accounts/`** - Open accounts with custom opening balances.
* **`POST /transactions/`** - Process new transfers with account balances validation and auto-updates.
* **`GET /risk/{customer_id}`** - **The ML Gateway.** Evaluates and yields the transaction velocity, stats, rule scoring, and ML anomaly prediction in under **2 milliseconds**.

---

*This project highlights advanced Backend Software Engineering, real-time ML deployment patterns, and transactional safety best practices.*
