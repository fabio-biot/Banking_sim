from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas

router = APIRouter(prefix="/clients", tags=["Clients"])

@router.post("/", response_model=schemas.ClientOut)
def create_client(client: schemas.ClientCreate, db: Session = Depends(get_db)):
    """Create a new client and store it in the database."""
    db_client = models.Client(name=client.name, country=client.country, risk_score=0)
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client

@router.get("/", response_model=List[schemas.ClientOut])
def get_clients(db: Session = Depends(get_db)):
    """Retrieve all clients from the database."""
    return db.query(models.Client).all()
