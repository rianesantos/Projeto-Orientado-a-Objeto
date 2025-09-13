from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from backend.database import get_db
# CORRIGIDO: Importar models diretamente
from backend.models import Order, Account, Position, Trade, Side
from .. import schemas, crud

router = APIRouter(prefix="/trades", tags=["trades"])

@router.post("/", response_model=schemas.TradeOut)
def execute_trade(payload: schemas.TradeCreate, db: Session = Depends(get_db)):
    order = db.get(Order, payload.order_id)  # Usar Order diretamente
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    if order.canceled:
        raise HTTPException(status_code=400, detail="Order is canceled")
    
    remaining = order.quantity - sum(t.quantity for t in order.trades)
    if payload.quantity > remaining:
        raise HTTPException(status_code=400, detail="Trade quantity exceeds remaining order size")
    
    account = db.get(Account, order.account_id)  # Usar Account diretamente
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    
    if order.side == Side.buy and account.cash < payload.quantity * payload.price:  # Usar Side diretamente
        raise HTTPException(status_code=400, detail="Insufficient cash")
    
    if order.side == Side.sell:  # Usar Side diretamente
        pos = db.query(Position).filter_by(  # Usar Position diretamente
            account_id=account.id, 
            symbol=order.symbol
        ).first()
        if not pos or pos.quantity < payload.quantity:
            raise HTTPException(status_code=400, detail="Insufficient position")
    
    trade = Trade(  # Usar Trade diretamente
        account_id=order.account_id,
        order_id=order.id,
        symbol=order.symbol,
        side=order.side,
        quantity=payload.quantity,
        price=payload.price
    )
    
    db.add(trade)
    db.flush()
    
    crud.upsert_position_on_trade(db, account, trade)
    crud.update_order_status_from_trades(db, order)
    
    db.commit()
    db.refresh(trade)
    return trade

@router.get("/", response_model=List[schemas.TradeOut])  # CORRIGIDO: espaço
def list_trades(db: Session = Depends(get_db)):
    return db.query(Trade).order_by(Trade.executed_at.desc()).all()