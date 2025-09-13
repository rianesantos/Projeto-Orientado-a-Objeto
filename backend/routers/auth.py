from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models import User
from backend.schemas import UserCreate
from backend.crud import create_user, get_user_by_email
from backend.auth.jwt import create_access_token
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username).first()
    
    if not user or not pwd_context.verify(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token = create_access_token(data={"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}

@router.post("/register")
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    user = get_user_by_email(db, email=user_data.email)
    if user:
        raise HTTPException(status_code=400, detail="Email already registered.")

    db_user = create_user(db=db, user=user_data)
    
    return {"message": "User registered successfully!", "user_id": db_user.id}