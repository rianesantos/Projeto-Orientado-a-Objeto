from sqlalchemy import Column, Integer, String, Float, Enum, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from enum import Enum as PyEnum
from backend.database import Base

class Side(str, PyEnum):
    buy = "buy"
    sell = "sell"

class OrderStatus(str, PyEnum):
    open = "open"
    partially_filled = "partially_filled"
    filled = "filled"
    canceled = "canceled"

class Account(Base):
    __tablename__ = "accounts"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    cash = Column(Float, default=100000.0)
    
    positions = relationship("Position", back_populates="account", cascade="all, delete-orphan")
    orders = relationship("Order", back_populates="account", cascade="all, delete-orphan")
    trades = relationship("Trade", back_populates="account", cascade="all, delete-orphan")

class Position(Base):
    __tablename__ = "positions"
    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer, ForeignKey("accounts.id"), index=True)
    symbol = Column(String, index=True)
    quantity = Column(Float, default=0.0)
    avg_price = Column(Float, default=0.0)
    
    account = relationship("Account", back_populates="positions")

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer, ForeignKey("accounts.id"), index=True)
    symbol = Column(String, index=True)
    side = Column(Enum(Side), index=True)
    quantity = Column(Float)
    status = Column(Enum(OrderStatus), default=OrderStatus.open, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    canceled = Column(Boolean, default=False)
    
    account = relationship("Account", back_populates="orders")
    trades = relationship("Trade", back_populates="order", cascade="all, delete-orphan")

class Trade(Base):
    __tablename__ = "trades"
    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer, ForeignKey("accounts.id"), index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), index=True)
    symbol = Column(String, index=True)
    side = Column(Enum(Side), index=True)
    quantity = Column(Float)
    price = Column(Float)
    executed_at = Column(DateTime, default=datetime.utcnow)
    
    account = relationship("Account", back_populates="trades")
    order = relationship("Order", back_populates="trades")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    portfolios = relationship("Portfolio", back_populates="user")

class Portfolio(Base):
    __tablename__ = "portfolios"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    asset = Column(String, index=True)
    quantity = Column(Float, default=0)
    avg_price = Column(Float, default=0)

    user = relationship("User", back_populates="portfolios")  # ✅ Corrigido de "owner" para "user"
    orders = relationship("PortfolioOrder", back_populates="portfolio", cascade="all, delete-orphan")


class PortfolioOrder(Base):
    __tablename__ = "portfolio_orders"
    id = Column(Integer, primary_key=True, index=True)
    portfolio_id = Column(Integer, ForeignKey("portfolios.id"))
    asset = Column(String, index=True)
    quantity = Column(Float)
    price = Column(Float)
    type = Column(Enum(Side))  # Corrigido para Enum
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    portfolio = relationship("Portfolio", back_populates="orders")  # Corrigido para match

class Strategy(Base):
    __tablename__ = "strategies"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    description = Column(String)
    rules = relationship("StrategyRule", back_populates="strategy", cascade="all, delete-orphan")
    
class StrategyRule(Base):
    __tablename__ = "strategy_rules"
    id = Column(Integer, primary_key=True, index=True)
    strategy_id = Column(Integer, ForeignKey("strategies.id"))
    asset = Column(String, index=True)
    condition = Column(String)  # Ex: "<", ">", "<=", ">="
    target_price = Column(Float)
    action = Column(Enum(Side))  # buy ou sell
    quantity = Column(Float)
    
    strategy = relationship("Strategy", back_populates="rules")
    
class ExecutionLog(Base):
    __tablename__ = "execution_logs"
    id = Column(Integer, primary_key=True, index=True)
    strategy_id = Column(Integer, ForeignKey("strategies.id"))
    rule_id = Column(Integer, ForeignKey("strategy_rules.id"))
    asset = Column(String)
    price = Column(Float)
    quantity = Column(Float)
    action = Column(Enum(Side))
    timestamp = Column(DateTime, default=datetime.utcnow)

    strategy = relationship("Strategy")
    rule = relationship("StrategyRule")
    
class Notification(Base):
    __tablename__ = "notifications"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    message = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)

    user = relationship("User")

class AuditLog(Base):
    __tablename__ = "audit_logs"
    id = Column(Integer, primary_key = True, index = True)
    user_id = Column(Integer, ForeignKey("users.id"))
    action = Column(String)
    timestamp = Column(DateTime, default = datetime.utcnow)

    user = relationship("User")
