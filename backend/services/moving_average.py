from backend.services.StrategyRunner import BaseStrategy

class MovingAverageStrategy(BaseStrategy):
    name = "MovingAverage"

    def __init__(self, short: int = 20, long: int = 50):
        self.short = short
        self.long = long

    async def execute(self, market_data):
        prices = market_data.get("prices", [])
        if len(prices) < self.long:
            return

        short_avg = sum(prices[-self.short:]) / self.short
        long_avg = sum(prices[-self.long:]) / self.long

        if short_avg > long_avg:
            print("📈 Sinal de COMPRA")
        elif short_avg < long_avg:
            print("📉 Sinal de VENDA")