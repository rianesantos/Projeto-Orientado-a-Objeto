from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from backend.database import get_db
from backend.models import Portfolio, PortfolioOrder, Side
from .. import schemas

router = APIRouter(prefix = "/portfolio-orders", tags = ["portfolio_orders"])

@router.post("/", response_model = schemas.PortfolioOrderOut)
def create_portfolio_order(payload: schemas.PortfolioOrderCreate, db: Session = Depends(get_db)):
    portfolio = db.get(Portfolio, payload.portfolio_id)
    if not portfolio:
        raise HTTPException(status_code = 404, detail = "Portfolio not found")
    
    # Atualiza posição
    
    if payload.type == Side.buy:
        total_cost = (portfolio.quantity + portfolio.avg_price) + (payload.quantity + payload.price)
        new_qty = portfolio.quantity + payload.quantity
        portfolio.avg_price = total_cost / new_qty if new_qty > 0 else 0.0
        portfolio.quantity = new_qty
    else:
        if portfolio.quantity < payload.quantity:
            raise HTTPException(status_code = 400, detail = "Insufficient quantity to sell")
        portfolio.quantity -= payload.quantity
        if portfolio.quantity == 0:
            portfolio.avg_price = 0.0
    
    order = PortfolioOrder(**payload.dict())
    db.add(order)
    db.commit()
    db.refresh(order)
    return order

@router.get("/", response_model = List [schemas.PortfolioOrderOut])
def list_portfolio_orders(db: Session = Depends(get_db)):
    return db.query(PortfolioOrder).order_by(PortfolioOrder.timestamp.desc()).all()

@router.get("/{order_id}", response_model = schemas.PortfolioOrderOut)
def get_portfolio_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(PortfolioOrder).order_by(PortfolioOrder.timestamp.desc()).all()
    if not order:
        raise HTTPException(status_code = 404, detail = "Order not found")