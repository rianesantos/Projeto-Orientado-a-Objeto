import yfinance as yf
from sqlalchemy.orm import Session
from backend.models import StrategyRule, PortfolioOrder, Portfolio, Side, ExecutionLog, Notification


def get_market_price(asset: str) -> float:
    ticker = yf.Ticker(asset)
    data = ticker.history(period = "1d")
    if data.empty:
        return None
    return data["Close"].iloc[-1]

def execute_strategies(db: Session):
    rules = db.query(StrategyRule).all()
    
    for rule in rules:
        price = get_market_price(rule.asset)
        if price is None:
            continue 
        
        condition_met = False 
        if rule.condition == "<" and price < rule.target_price:
            condition_met = True
        elif rule.condition == ">" and price > rule.target_price:
            condition_met = True
        elif rule.condition == "<=" and price <= rule.target_price:
            condition_met = True
        elif rule.condition == ">=" and price >= rule.target_price:
            condition_met = True
            
        if condition_met:
            portfolio = db.query(Portfolio).filter_by(user_id = rule.strategy.id).first()
            if not portfolio:
                continue
            
            order = PortfolioOrder(
                portfolio_id = portfolio.id,
                asset = rule.asset,
                quantity = rule.quantity,
                price = price,
                type = rule.action
            )
            
            #Atualiza posição
            if rule.action == Side.buy:
                total_cost = (portfolio.quantity * portfolio.avg_price) + (rule.quantity * price)
                new_qty = portfolio.quantity + rule.quantity
                portfolio.avg_price = total_cost / new_qty if new_qty > 0 else 0.0
                portfolio.quantity = new_qty
            else:
                if portfolio.quantity < rule.quantity:
                    continue
                portfolio.quantity -= rule.quantity
                if portfolio.quantity == 0:
                    portfolio.avg_price = 0.0
            
            db.add(order)
            db.commit()
            log = ExecutionLog(
                strategy_id = rule.strategy_id,
                rule_id = rule.id,
                asset = rule.asset,
                price = price,
                quantity = rule.quantity,
                action = rule.action
                )
            db.add(log)
            db.commit()
            db.refresh(order)
            
            notif = Notification(
                user_id = portfolio.user_id,
                message = f"Your order to {rule.action.value} {rule.quantity} shares of {rule.asset} has been executed at a price of R${price:.2f}"
                )
            db.add(notif)
            db.commit()
            
            