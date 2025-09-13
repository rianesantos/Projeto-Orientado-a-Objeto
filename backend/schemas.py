from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
from datetime import datetime
from backend.models import Side, OrderStatus

class PositionOut(BaseModel):
    symbol: str
    quantity: float
    avg_price: float
    
    class Config:
        from_attributes = True

class AccountCreate(BaseModel):
    username: str
    cash: float = 100000.0
    
class AccountOut(BaseModel):
    id: int
    username: str
    cash: float
    positions: List[PositionOut] = []
    
    class Config:
        from_attributes = True
        
class OrderCreate(BaseModel):
    account_id: int 
    symbol: str
    side: Side
    quantity: float = Field(gt=0)
    
class OrderOut(BaseModel): 
    id: int
    account_id: int
    symbol: str
    side: Side
    quantity: float
    status: OrderStatus
    canceled: bool
    created_at: datetime
    
    class Config:
        from_attributes = True
        
class TradeCreate(BaseModel):
    order_id: int
    symbol: str  # ADICIONADO
    side: Side  # ADICIONADO
    quantity: float = Field(gt=0)
    price: float = Field(gt=0)

class TradeOut(BaseModel):
    id: int
    order_id: int
    account_id: int 
    symbol: str
    side: Side
    quantity: float
    price: float 
    executed_at: datetime
    
    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    username: str
    email: str
    
    class Config:
        from_attributes = True

class PortfolioCreate(BaseModel):
    user_id: int
    asset: str

class PortfolioOut(BaseModel):
    id: int
    user_id: int
    asset: str
    quantity: float
    avg_price: float
    
    class Config:
        from_attributes = True

class PortfolioOrderCreate(BaseModel):
    portfolio_id: int
    asset: str
    quantity: float = Field(gt=0)
    price: float = Field(gt=0)
    type: Side

class PortfolioOrderOut(BaseModel):
    id: int
    portfolio_id: int
    asset: str
    quantity: float
    price: float
    type: Side
    timestamp: datetime
    
    class Config:
        from_attributes = True
        
class StrategyCreate(BaseModel):
    username: str
    description: str

class StrategyOut(BaseModel):
    id: int
    username: str
    description: str

    class Config:
        from_attributes = True
        
class StrategyRuleCreate(BaseModel):
    strategy_id: int
    asset: str
    condition: str
    target_price: float
    action: Side
    quantity: float

class StrategyRuleOut(BaseModel):
    id: int
    strategy_id: int
    asset: str
    condition: str
    target_price: float
    action: Side
    quantity: float

    class Config:
        from_attributes = True
        
class ExecutionLogOut(BaseModel):
    id: int
    strategy_id: int
    rule_id: int
    asset: str
    price: float
    quantity: float
    action: Side
    timestamp: datetime

    class Config:
        from_attributes = True
        
class NotificationOut(BaseModel):
    id: int
    user_id: int
    message: str
    timestamp: datetime

    class Config:
        from_attributes = True