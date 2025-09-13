from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from backend.database import get_db
from backend.models import Strategy
from .. import schemas

router = APIRouter(prefix = "/strategies", tags = ["strategies"])

@router.post("/", response_model = schemas.StrategyOut)
def create_strategy(payload: schemas.StrategyCreate, db: Session = Depends(get_db)):
    strategy = Strategy(name = payload.name, description = payload.description)
    db.add(strategy)
    db.commit()
    db.refresh(strategy)
    return strategy

@router.get("/", response_model = List[schemas.StrategyOut])
def list_strategies(db: Session = Depends(get_db)):
    return db.query(Strategy).all()

@router.get("/{strategy_id}", response_model = schemas.StrategyOut)
def get_strategy(strategy_id: int, db: Session = Depends(get_db)):
    strategy = db.get(Strategy, strategy_id)
    if not strategy:
        raise HTTPException(status_code = 404, detail = "Strategy not found")
    return strategy

@router.put("/{strategy_id}", response_model = schemas.StrategyOut)
def update_strategy(strategy_id: int, payload: schemas.StrategyCreate, db: Session = Depends(get_db)):

    strategy = db.get(Strategy, strategy_id)
    if not strategy:
        raise HTTPException(status_code = 404, detail = "Strategy not found")
    
    for field, value in payload.dict().items():
        setattr(strategy, field, value)
    
    db.add(strategy)
    db.commit()
    db.refresh(strategy)
    return strategy

@router.delete("/{strategy_id}")
def delete_strategy(strategy_id: int, db: Session = Depends(get_db)):
    strategy = db.get(Strategy, strategy_id)
    if not strategy:
        raise HTTPException(status_code = 404, detail = "Strategy not found")
    db.delete(strategy)
    db.commit()
    return {"ok": True}