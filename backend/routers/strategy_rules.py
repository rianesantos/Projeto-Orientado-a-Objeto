from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from backend.database import get_db
from backend.models import Strategy, StrategyRule, User
from .. import schemas
from backend.auth.dependencies import get_current_user

router = APIRouter(prefix="/strategy-rules", tags=["strategy_rules"])

@router.post("/", response_model=schemas.StrategyRuleOut)
def create_rule(
    payload: schemas.StrategyRuleCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    strategy = db.get(Strategy, payload.strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    
    if strategy.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    rule = StrategyRule(**payload.dict())
    db.add(rule)
    db.commit()
    db.refresh(rule)
    return rule

@router.get("/", response_model=List[schemas.StrategyRuleOut])
def list_rules(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    user_strategies = db.query(Strategy).filter(Strategy.user_id == current_user.id).all()
    strategy_ids = [s.id for s in user_strategies]
    return db.query(StrategyRule).filter(StrategyRule.strategy_id.in_(strategy_ids)).all()

@router.get("/{rule_id}", response_model=schemas.StrategyRuleOut)  
def get_rule(
    rule_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    rule = db.get(StrategyRule, rule_id)
    if not rule:
        raise HTTPException(status_code=404, detail="Rule not found")
    
    strategy = db.get(Strategy, rule.strategy_id)
    if not strategy or strategy.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    return rule

@router.delete("/{rule_id}")
def delete_rule(
    rule_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    rule = db.get(StrategyRule, rule_id)
    if not rule:
        raise HTTPException(status_code=404, detail="Rule not found")

    strategy = db.get(Strategy, rule.strategy_id)
    if not strategy or strategy.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    db.delete(rule)
    db.commit()
    return {"ok": True}
