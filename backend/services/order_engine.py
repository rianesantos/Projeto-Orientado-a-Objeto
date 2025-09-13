import asyncio
from typing import List, Dict, Any
from services.market_service import fetch_latest_quote
from datetime import datetime

# In-memory stores (substituir por DB real)
order_rules: List[Dict[str, Any]] = []
executed_orders: List[Dict[str, Any]] = []
portfolios: Dict[str, List[Dict[str, Any]]] = {}  # user_id -> list of positions

async def order_engine_loop(poll_interval: float = 3.0):
    while True:
        await asyncio.sleep(poll_interval)
        await check_and_execute_rules()

async def check_and_execute_rules():
    for rule in list(order_rules):  # copy
        try:
            symbol = rule["symbol"]
            q = fetch_latest_quote(symbol)
            if not q:
                continue
            price = q["price"]
            condition = rule["condition"]  # e.g., {"type":"price_above", "value": 10.5}
            should_fire = False
            if condition["type"] == "price_above" and price > condition["value"]:
                should_fire = True
            if condition["type"] == "price_below" and price < condition["value"]:
                should_fire = True

            if should_fire:
                # Simulate execution
                execution = {
                    "timestamp": datetime.utcnow().isoformat(),
                    "symbol": symbol,
                    "price": price,
                    "quantity": rule["quantity"],
                    "side": rule["side"],
                    "rule_id": rule["id"]
                }
                executed_orders.append(execution)
                # update portfolio simple logic
                user = rule.get("user", "default")
                pos = portfolios.setdefault(user, [])
                pos.append({
                    "symbol": symbol,
                    "quantity": rule["quantity"],
                    "avg_price": price
                })
                # if rule is one-time, remove it; else you could keep for repeated triggers
                if rule.get("one_time", True):
                    order_rules.remove(rule)
        except Exception:
            continue

# helpers to manage rules
def add_rule(rule: Dict[str, Any]):
    order_rules.append(rule)

def list_rules():
    return order_rules

def list_executions():
    return executed_orders

def get_portfolio(user: str = "default"):
    return portfolios.get(user, [])