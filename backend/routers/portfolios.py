from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from backend.database import get_db
from backend.models import Portfolio, User
from .. import schemas

router = APIRouter(prefix = "/portfolios", tags = ["portfolios"])

@router.post("/", response_model = schemas.PortfolioOut)
def create_portfolio(payload: schemas.PortfolioCreate, db: Session = Depends(get_db)):
    user = db.get(User, payload.user_id)
    if not user:
        raise HTTPException(status_code = 404, detail = "User not found")
    
    portfolio = Portfolio(
        user_id = payload.user_id,
        asset = payload.asset,
        quantity = 0, 
        avg_price = 0
    )
    db.add(portfolio)
    db.commit()
    db.refresh(portfolio)
    return portfolio

@router.get("/", response_model = List [schemas.PortfolioOut])
def list_portfolios(db: Session = Depends(get_db)):
    return db.query(Portfolio).all()

@router.get("/{portfolio_id}", response_model = schemas.PortfolioOut)
def get_portfolio(portfolio_id: int, db: Session = Depends(get_db)):
    portfolio = db.get(Portfolio, portfolio_id)
    if not portfolio:
        raise HTTPException(status_code = 404, detail = "Portfolio not found")
    return portfolio

@router.delete("/{portfolio_id}")
def delete_portfolio(portfolio_id: int, db: Session = Depends(get_db)):
    portfolio = db.get(Portfolio, portfolio_id)
    if not portfolio: 
        raise HTTPException(status_code = 404, detail = "Portfolio not found")
    db.delete(portfolio)
    db.commit()
    return {"ok": True}