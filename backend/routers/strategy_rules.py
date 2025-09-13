from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from backend.database import get_db
from backend.models import Strategy, StrategyRule
from .. import schemas

router = APIRouter(prefix = "/strategy-rules", tags = ["strategy_rules"])

@router.post("/", response_model = schemas.StrategyRuleOut)
def create_rule(payload: schemas.StrategyRuleCreate, db: Session = Depends(get_db)):
    strategy = db.get(Strategy, payload.strategy_id)
    if not strategy:
        raise HTTPException(status_code = 404, detail = "Stratety")
    
    rule = StrategyRule(**payload.dict())
    db.add(rule)
    db.commit()
    db.refresh()
    return rule

@router.get("/", response_model = List[schemas.StrategyRuleOut])
def list_rules(db: Session = Depends(get_db)):
    return db.query(StrategyRule).all()

@router.get("/{rule_id}, response_model = schemas.StrategyRuleOut")
def get_rule(rule_id: int, db: Session = Depends(get_db)):
    rule =  db.get(StrategyRule, rule_id)
    if not rule:
        raise HTTPException(status_code = 404, detail = "Rule not found")
    return rule

@router.delete("/{rule_id}")
def delete_rule(rule_id: int, db: Session = Depends(get_db)):
    rule = db.get(StrategyRule, rule_id)
    if not rule:
        raise HTTPException(status_code = 404, detail = "Rule not found")
    db.delete(rule)
    db.commit()
    return {"ok": True}