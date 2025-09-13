from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from backend.database import get_db
from backend.models import Account
from .. import schemas

router = APIRouter(prefix = "/accounts", tags = ["accounts"])

@router.post("/", response_model = schemas.AccountOut)
def create_account(payload: schemas.AccountCreate, db: Session = Depends(get_db)):
    account = Account(name = payload.name, cash = payload.cash)
    db.add(account)
    db.commit()
    db.refresh(account)
    return account

@router.get("/", response_model = List[schemas.AccountOut])
def list_accounts(db: Session = Depends(get_db)):
    return db.query(Account).all()

@router.put("/{account_id}", response_model = schemas.AccountOut)
def update_account(account_id: int, payload: schemas.AccountOut, db: Session = Depends(get_db)):
    account = db.get(Account, account_id)
    if not account:
        raise HTTPException(status_code = 404, detail = "Account not found")
    account.name = payload.name
    account.cash = payload.cash
    db.commit()
    db.refresh(account)
    return account

@router.delete("/{account_id}")
def delete_account(account_id: int, db: Session = Depends(get_db)):
    account = db.get(Account, account_id)
    if not account:
        raise HTTPException(status_code = 404, detail = "Account not found")
    db.delete(account)
    db.commit()
    return {"ok": True}
