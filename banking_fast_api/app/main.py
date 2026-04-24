from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from app.database import Base, engine
from app.routes import clients
from app.routes import transactions
from app.routes import clients, accounts


app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(transactions.router)
app.include_router(clients.router)
app.include_router(accounts.router)


@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <h1>Banking API</h1>
    <ul>
        <li><a href="/docs">Go to App !</a></li>
    </ul>
    """
