from app.database import SessionLocal
from app import models
import random

def seed_data():
    db = SessionLocal()

    # CLEAN
    db.query(models.Transaction).delete()
    db.query(models.Account).delete()
    db.query(models.Client).delete()
    db.commit()

    # CLIENTS
    clients = [
        models.Client(name="Alice Martin", country="FR", risk_score=0),
        models.Client(name="Martina Germain", country="FR", risk_score=0),
        models.Client(name="Bob Smith", country="UK", risk_score=0),
        models.Client(name="JR Smith", country="UK", risk_score=0),
        models.Client(name="Charlie Dupont", country="FR", risk_score=0),
        models.Client(name="Antoine Dupont", country="FR", risk_score=0),
        models.Client(name="Charles Leclerc", country="FR", risk_score=0),
        models.Client(name="LeBron James", country="US", risk_score=0),
        models.Client(name="Victor Dubuisson", country="FR", risk_score=0),
        models.Client(name="Rory McIlroy", country="UK", risk_score=0),
    ]

    db.add_all(clients)
    db.commit()

    accounts = []

    for c in clients:
        balance_val = random.randint(1000, 100000)
        account = models.Account(
            client_id=c.id,
            balance=balance_val
        )
        accounts.append(account)

    db.add_all(accounts)
    db.commit()

    db.close()


if __name__ == "__main__":
    seed_data()
    print("Database seeded successfully 🚀")