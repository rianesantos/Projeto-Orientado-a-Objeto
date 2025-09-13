from sqlalchemy.orm import Session
from sqlalchemy import select
from passlib.context import CryptContext
from backend.models import Account, Position, Order, Trade, OrderStatus, Side, User
from backend.schemas import UserCreate

# Create the password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, user: UserCreate):
    hashed_password = pwd_context.hash(user.password)
    db_user = User(
        email=user.email, 
        hashed_password=hashed_password, 
        username=user.username 
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_or_create_account(db: Session, name: str, initial_cash: float = 100000.0):
    stmt = select(Account).where(Account.name == name)
    account = db.scalar(stmt)
    if account:
        return account
    account = Account(name=name, cash=initial_cash)
    db.add(account)
    db.commit()
    db.refresh(account)
    return account

def get_position(db: Session, account_id: int, symbol: str):
    stmt = select(Position).where(
        Position.account_id == account_id,
        Position.symbol == symbol
    )
    return db.scalar(stmt)

def upsert_position_on_trade(db: Session, account: Account, trade: Trade):
    pos = get_position(db, account.id, trade.symbol)
    
    if not pos:
        pos = Position(
            account_id=account.id, 
            symbol=trade.symbol, 
            quantity=0.0, 
            avg_price=0.0
        )
        db.add(pos)
        db.flush()
    
    if trade.side == Side.buy:
        # BUY: increase position, update average price
        new_qty = pos.quantity + trade.quantity
        total_cost = (pos.quantity * pos.avg_price) + (trade.quantity * trade.price)
        pos.avg_price = total_cost / new_qty if new_qty > 0 else 0.0
        pos.quantity = new_qty
        account.cash -= trade.quantity * trade.price
    else:
        # SELL: reduce position, maintain average price
        if pos.quantity < trade.quantity:
            raise ValueError("Insufficient position to sell")
        
        pos.quantity -= trade.quantity
        account.cash += trade.quantity * trade.price
        
        if pos.quantity == 0:
            pos.avg_price = 0.0

    db.flush()
    return pos

def update_order_status_from_trades(db: Session, order: Order):
    filled_qty = sum(t.quantity for t in order.trades)
    
    if order.canceled:
        order.status = OrderStatus.canceled
    elif filled_qty == 0:
        order.status = OrderStatus.open
    elif filled_qty < order.quantity:
        order.status = OrderStatus.partially_filled
    else:
        order.status = OrderStatus.filled
    
    db.flush()