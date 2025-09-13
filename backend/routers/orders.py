from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
# CORRIGIDO: Importar models diretamente
from backend.models import Account, Position, Order, OrderStatus, Side
from .. import schemas

router = APIRouter(prefix="/orders", tags=["orders"])

@router.post("/", response_model=schemas.OrderOut)
def create_order(payload: schemas.OrderCreate, db: Session = Depends(get_db)):
    account = db.get(Account, payload.account_id)  # Usar Account diretamente
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    
    if payload.side == Side.sell:  # Usar Side diretamente
        pos = db.query(Position).filter_by(  # Usar Position diretamente
            account_id=payload.account_id, 
            symbol=payload.symbol
        ).first()
        if not pos or pos.quantity < payload.quantity:
            raise HTTPException(status_code=400, detail="Insufficient position to sell")
    
    order = Order(  # Usar Order diretamente
        account_id=payload.account_id,
        symbol=payload.symbol,
        side=payload.side,
        quantity=payload.quantity,
        status=OrderStatus.open  # Usar OrderStatus diretamente
    )
    
    db.add(order)
    db.commit()
    db.refresh(order)
    return order

@router.get("/", response_model=List[schemas.OrderOut])
def list_orders(db: Session = Depends(get_db)):
    return db.query(Order).order_by(Order.created_at.desc()).all()

@router.get("/{order_id}", response_model=schemas.OrderOut)
def get_order(order_id: int, db: Session = Depends(get_db)):
    order = db.get(Order, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@router.post("/{order_id}/cancel", response_model=schemas.OrderOut)  # CORRIGIDO: OrderOut
def cancel_order(order_id: int, db: Session = Depends(get_db)):
    order = db.get(Order, order_id)
    if not order: 
        raise HTTPException(status_code=404, detail="Order not found")
    
    # CORRIGIDO: Indentação e lógica
    if order.status in [OrderStatus.filled, OrderStatus.canceled]:
        raise HTTPException(status_code=400, detail="Order cannot be canceled")
    
    order.canceled = True
    order.status = OrderStatus.canceled
    db.commit()
    db.refresh(order)
    return order