from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas

router = APIRouter(prefix="/clients", tags=["Clients"])

@router.post("/", response_model=schemas.ClientOut)
def create_client(client: schemas.ClientCreate, db: Session = Depends(get_db)):

    db_client = models.Client(
        name=client.name,
        country=client.country,
        age=client.age,
        risk_score=0
    )

    db.add(db_client)
    db.commit()
    db.refresh(db_client)

    return db_client


@router.get("/")
def get_clients(db: Session = Depends(get_db)):
    return db.query(models.Client).all()

