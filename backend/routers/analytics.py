from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from backend.database import get_db
from backend.models import Strategy, StrategyRule, PortfolioOrder, User, Portfolio, ExecutionLog, Side, Notification, AuditLog
from typing import List
import yfinance as yf
from .. import schemas
from backend.services.backtest import simulate_strategy
from backend.auth.dependencies import get_current_user  # Adicionado import

router = APIRouter(prefix="/analytics", tags=["analytics"])

# NOVO ENDPOINT - user-summary sem user_id (pega do usuário logado)
@router.get("/user-summary")
def user_summary(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    portfolios = db.query(Portfolio).filter_by(user_id=current_user.id).all()
    portfolio_ids = [p.id for p in portfolios]
    
    orders = db.query(PortfolioOrder).filter(PortfolioOrder.portfolio_id.in_(portfolio_ids)).all()
    total_volume = sum(o.quantity * o.price for o in orders) if orders else 0
    assets = {}
    for o in orders:
        assets[o.asset] = assets.get(o.asset, 0) + o.quantity
    
    most_traded = max(assets, key=assets.get) if assets else None
    
    strategies = db.query(Strategy).filter(Strategy.name.ilike(f"%{current_user.username}%")).all()
    
    return {
        "user_id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
        "portfolios": len(portfolios),
        "orders_executed": len(orders),
        "total_volume": round(total_volume, 2),
        "most_traded_asset": most_traded,
        "strategies_linked": [s.name for s in strategies]
    }

@router.get("/strategy-performance")
def strategy_performance(db: Session = Depends(get_db)):
    strategies = db.query(Strategy).all()
    result = []
    
    for strategy in strategies:
        rules = strategy.rules
        total_orders = 0
        total_volume = 0.0
        assets = {}
        
        for rule in rules:
            orders = db.query(PortfolioOrder).filter_by(asset=rule.asset).all()
            total_orders += len(orders)
            for order in orders:
                total_volume += order.quantity * order.price
                assets[order.asset] = assets.get(order.asset, 0) + 1
        
        most_trade = max(assets, key=assets.get) if assets else None
        
        result.append({
            "strategy_id": strategy.id,
            "strategy_name": strategy.name,
            "executions": total_orders,
            "total_volume": round(total_volume, 2),
            "most_traded_asset": most_trade
        })
    
    return result

@router.get("/user-summary/{user_id}")
def user_summary_by_id(user_id: int, db: Session = Depends(get_db)):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    portfolios = db.query(Portfolio).filter_by(user_id=user_id).all()
    portfolio_ids = [p.id for p in portfolios]
    
    orders = db.query(PortfolioOrder).filter(PortfolioOrder.portfolio_id.in_(portfolio_ids)).all()
    total_volume = sum(o.quantity * o.price for o in orders) if orders else 0
    assets = {}
    for o in orders:
        assets[o.asset] = assets.get(o.asset, 0) + o.quantity
    
    most_traded = max(assets, key=assets.get) if assets else None
    
    strategies = db.query(Strategy).filter(Strategy.name.ilike(f"%{user.username}%")).all()
    
    return {
        "user_id": user.id,
        "username": user.username,
        "email": user.email,
        "portfolios": len(portfolios),
        "orders_executed": len(orders),
        "total_volume": round(total_volume, 2),
        "most_traded_asset": most_traded,
        "strategies_linked": [s.name for s in strategies]
    }

@router.get("/execution-logs", response_model=List[schemas.ExecutionLogOut])
def get_execution_logs(db: Session = Depends(get_db)):
    logs = db.query(ExecutionLog).order_by(ExecutionLog.timestamp.desc()).all()
    return logs

@router.get("/notifications/{user_id}", response_model=List[schemas.NotificationOut])
def get_notifications(user_id: int, db: Session = Depends(get_db)):
    return db.query(Notification).filter_by(user_id=user_id).order_by(Notification.timestamp.desc()).all()

@router.get("/user-pnl/{user_id}")
def user_pnl(user_id: int, db: Session = Depends(get_db)):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    portfolios = db.query(Portfolio).filter_by(user_id=user_id).all()
    result = []

    for p in portfolios:
        try:
            ticker = yf.Ticker(p.asset)
            data = ticker.history(period="1d")
            if data.empty:
                continue
            current_price = data["Close"].iloc[-1]
            pnl = (current_price - p.avg_price) * p.quantity

            result.append({
                "asset": p.asset,
                "quantity": p.quantity,
                "avg_price": round(p.avg_price, 2),
                "current_price": round(current_price, 2),
                "estimated_pnl": round(pnl, 2)
            })
        except:
            continue

    return {
        "user_id": user.id,
        "username": user.username,
        "portfolio_pnl": result
    }
    
@router.get("/strategy-ranking")
def strategy_ranking(db: Session = Depends(get_db)):
    strategies = db.query(Strategy).all()
    result = []
    
    for strategy in strategies:
        pnl_total = 0.0
        rules = strategy.rules
        for rule in rules:
            orders = db.query(PortfolioOrder).filter_by(asset=rule.asset).all()
            if not orders:
                continue
            try:
                ticker = yf.Ticker(rule.asset)  # Corrigido: rule.asset em vez de rules.asset
                data = ticker.history(period="1d")
                if data.empty:
                    continue
                current_price = data["Close"].iloc[-1]
                for order in orders:
                    if order.type == Side.buy:
                        pnl = (current_price - order.price) * order.quantity
                    else:
                        pnl = (order.price - current_price) * order.quantity
                    pnl_total += pnl
            except:
                continue
                    
        result.append({
            "strategy_id": strategy.id,
            "strategy_name": strategy.name,
            "estimated_pnl": round(pnl_total, 2)
        })
        
    result.sort(key=lambda x: x["estimated_pnl"], reverse=True)
    return result

@router.get("/risk/{user_id}")
def user_risk(user_id: int, db: Session = Depends(get_db)):
    portfolios = db.query(Portfolio).filter_by(user_id=user_id).all()
    total_value = 0.0
    asset_values = {}
    
    for p in portfolios:
        try:
            ticker = yf.Ticker(p.asset)
            data = ticker.history(period="1d")
            if data.empty:
                continue
            current_price = data["Close"].iloc[-1]
            value = current_price * p.quantity
            total_value += value
            asset_values[p.asset] = value
        except:
            continue
        
    exposure = {
        asset: round((value / total_value) * 100, 2)
        for asset, value in asset_values.items()  # Corrigido: items() em vez de itms()
    } if total_value > 0 else {}
    
    return {
        "user_id": user_id,
        "total_portfolio_value": round(total_value, 2),
        "asset_exposure_percent": exposure
    }

@router.get("/backtest")
def backtest(asset: str, condition: str, target_price: float, action: str, quantity: float):
    return simulate_strategy(asset, condition, target_price, action, quantity)

@router.get("/audit/{user_id}")
def get_audit_logs(user_id: int, db: Session = Depends(get_db)):
    return db.query(AuditLog).filter_by(user_id=user_id).order_by(AuditLog.timestamp.desc()).all()