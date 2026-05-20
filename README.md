fchaput

This project aims to be a banking simulation, working with python, SQL and Strealit/PowerBI as viz tool
It also uses a virtual environement and a requirements.txt file, as well as FastAPI to work with the built-in models.

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
