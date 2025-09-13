from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from backend import models
from backend.database import Base, engine, get_db
from backend.routers import accounts, users, orders, trades
from backend.routers import portfolios, portfolio_orders
from backend.routers import strategies, strategy_rules
from backend.services.executor import execute_strategies
from backend.routers import analytics, auth, market_data, risk

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Automated Trading System")

# Routers
app.include_router(orders.router)
app.include_router(trades.router)
app.include_router(accounts.router)
app.include_router(users.router)
app.include_router(portfolios.router)
app.include_router(portfolio_orders.router)
app.include_router(strategies.router)
app.include_router(strategy_rules.router)
app.include_router(analytics.router)
app.include_router(auth.router)
app.include_router(market_data.router)
app.include_router(risk.router)

# Middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/ping")
def ping():
    return {"message": "pong"}

@app.post("/strategies/execute")
def run_strategies(db: Session = Depends(get_db)):
    execute_strategies(db)
    return {"status": "executed"}

@app.post("/accounts/bootstrap")
def bootstrap_account(name: str = "default", cash: float = 100000.0, db: Session = Depends(get_db)):
    from backend import crud
    acc = crud.get_or_create_account(db, name=name, initial_cash=cash)
    db.refresh(acc)
    return {"id": acc.id, "name": acc.name, "cash": acc.cash}

@app.get("/accounts/{account_id}")
def get_account(account_id: int, db: Session = Depends(get_db)):
    from backend import models
    acc = db.get(models.Account, account_id)
    if not acc:
        return {"detail": "Account not found"}
    positions = [
        {"symbol": p.symbol, "quantity": p.quantity, "avg_price": p.avg_price}
        for p in acc.positions
    ]
    return {"id": acc.id, "name": acc.name, "cash": acc.cash, "positions": positions}
