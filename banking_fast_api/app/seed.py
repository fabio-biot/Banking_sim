from app.database import SessionLocal
from app import models
import random
import pandas as pd
import numpy as np

data_kaggle = pd.read_csv("data/bank_transactions.csv")
data_client = pd.read_excel("data/Base Client.xlsx")


def seed_data_tosql(data_kaggle: pd.DataFrame, data_client: pd.DataFrame) -> None:
    db = SessionLocal()
    try:
        db.query(models.Transaction).delete()
        db.query(models.Account).delete()
        db.query(models.Client).delete()
        db.commit()

        clients = []
        for _, row in data_client.iterrows():
            client = models.Client(
                name=row["name"],
                country=row["country"],
                age=int(row["age"]),
                risk_score=0,
            )
            clients.append(client)

        db.add_all(clients)
        db.commit()

        for client in clients:
            db.refresh(client)

        accounts = []
        for client in clients:
            account = models.Account(
                client_id=client.id,
                balance=float(random.randint(1000, 100000)),
            )
            accounts.append(account)

        db.add_all(accounts)
        db.commit()

        for account in accounts:
            db.refresh(account)

        account_id_map = {
            index: account.id for index, account in enumerate(accounts, start=1)
        }

        transactions = []
        for _, row in data_kaggle.iterrows():
            customer_account_id = account_id_map.get(int(row["CustomerID"]))
            target_account_id = account_id_map.get(int(row["CustomerID_to_account"]))

            if customer_account_id is None or target_account_id is None:
                continue

            transaction = models.Transaction(
                TransactionID=str(row["TransactionID"]),
                CustomerID_to_account=target_account_id,
                CustomerID=customer_account_id,
                CustomerDOB=row["CustomerDOB"].to_pydatetime(),
                CustLocation=str(row["CustLocation"]),
                CustAccountBalance=float(row["CustAccountBalance"]),
                TransactionDate=row["TransactionDate"].to_pydatetime(),
                TransactionTime=int(row["TransactionTime"]),
                TransactionAmount_INR=float(row["TransactionAmount (INR)"]),
            )
            transactions.append(transaction)

        db.add_all(transactions)
        db.commit()
    finally:
        db.close()


def formating_kaggle_dataset(data_kaggle: pd.DataFrame, nb_customers: int) -> pd.DataFrame:
    """
    Here I convert the CUSTOMER_ID column of the kaggle dataset'
    in id from 1 to the number of fake customers
    I generated to grant model relationships
    """
    data_kaggle["CustomerID"] = np.random.randint(1, nb_customers + 1, size=len(data_kaggle))

    data_kaggle["CustomerID_to_account"] = np.random.randint(1, nb_customers + 1, size=len(data_kaggle))
    mask = data_kaggle["CustomerID_to_account"] == data_kaggle["CustomerID"]
    data_kaggle.loc[mask, "CustomerID_to_account"] = (
        data_kaggle.loc[mask, "CustomerID_to_account"] % nb_customers
    ) + 1
    data_kaggle = data_kaggle.copy()

    data_kaggle["TransactionDate"] = pd.to_datetime(
        data_kaggle["TransactionDate"],
        format="%d/%m/%y",
        errors="coerce",
        dayfirst=True
    )

    data_kaggle["CustomerDOB"] = pd.to_datetime(
        data_kaggle["CustomerDOB"],
        format="%d/%m/%y",
        errors="coerce",
        dayfirst=True
    )
    data_kaggle = data_kaggle[
        data_kaggle["TransactionDate"].notna() &
        data_kaggle["CustomerDOB"].notna() &
        data_kaggle["TransactionTime"].notna()
    ].copy()
    data_kaggle["TransactionTime"] = data_kaggle["TransactionTime"].astype(int)
    data_kaggle["CustAccountBalance"] = data_kaggle["CustAccountBalance"].fillna(0.0)
    return data_kaggle


if __name__ == "__main__":
    data_kaggle = formating_kaggle_dataset(data_kaggle, len(data_client))
    seed_data_tosql(data_kaggle, data_client)
    print("Database seeded successfully 🚀")
