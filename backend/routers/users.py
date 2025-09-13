from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session 
from typing import List
from backend.database import get_db
from backend.models import User
from .. import schemas
from passlib.hash import bcrypt # type: ignore
from backend.auth.dependencies import get_current_user

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=schemas.UserOut)
def create_user(payload: schemas.UserCreate, db: Session = Depends(get_db)):
    # Verifica se usuário já existe
    existing_user = db.query(User).filter(User.username == payload.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")
 
    hashed_pw = bcrypt.hash(payload.password)
    user = User(username=payload.username, email=payload.email, hashed_password=hashed_pw)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.get("/me", response_model=schemas.UserOut)
def get_profile(current_user: User = Depends(get_current_user)):
    return current_user

@router.get("/", response_model=List[schemas.UserOut])  # Corrigido: removido {user_id}
def list_users(db: Session = Depends(get_db)):
    return db.query(User).all()

@router.get("/{user_id}", response_model=schemas.UserOut)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}