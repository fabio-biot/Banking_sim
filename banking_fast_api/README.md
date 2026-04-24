fchaput

This project aims to be a banking simulation, working with python, SQL and Strealit/PowerBI as viz tool
It also uses a virtual environement and a requirements.txt file, as well as FastAPI to work with the built-in models.

External Dataset:

https://www.kaggle.com/datasets/shivamb/bank-customer-segmentation
A Personnal Name generator made in Excel.

Architechture:

banking_sim/
│
├── app/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── crud.py
│   ├── services/
│   │     └── risk.py
│   └── routes/
│         ├── clients.py
│         ├── accounts.py
│         └── transactions.py
│
├── data/
│   └── bank.db
│
├── dashboard/
│   └── streamlit_app.py
│
├── requirements.txt
└── README.md
└── Makefile


On va aller se chercher le dataset Kaggle et tej le Gender, mais le rajouter au client et rajouter une 
colonne id client au dataset Kaggle pour se faire des stats dessus

Moteur ML 

1. Feature engineering   → transformer les transactions
2. Rules engine          → règles métier (rapide, explicable)
3. ML model              → détection anomalies
4. Score final           → combinaison