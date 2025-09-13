import yfinance as yf

def simulate_strategy(asset: str, condition: str, target_price: float, action: str, quantity: float):
    ticker = yf.Ticker(asset)
    data = ticker.history(period="30d")
    results = []

    for date, row in data.iterrows():
        price = row["Close"]
        if (
            (condition == "<" and price < target_price) or
            (condition == ">" and price > target_price) or
            (condition == "<=" and price <= target_price) or
            (condition == ">=" and price >= target_price)
        ):
            results.append({
                "date": date.strftime("%Y-%m-%d"),
                "price": round(price, 2),
                "action": action,
                "quantity": quantity
            })

    return results
