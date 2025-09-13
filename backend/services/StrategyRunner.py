import asyncio
from typing import List, Dict, Any, Callable


class BaseStrategy:

    name: str = "BaseStrategy"

    async def execute(self, market_data: Dict[str, Any]):

        raise NotImplementedError("Estratégia precisa implementar execute()")


class StrategyRunner:
    def __init__(self):
        self.strategies: List[BaseStrategy] = []
        self.running = False

    def add_strategy(self, strategy: BaseStrategy):
        self.strategies.append(strategy)

    def clear_strategies(self):
        self.strategies.clear()

    async def run(self, market_data_provider: Callable[[], Dict[str, Any]]):
        self.running = True
        while self.running:
            market_data = market_data_provider()

            for strategy in self.strategies:
                await strategy.execute(market_data)

            await asyncio.sleep(2)  # evita sobrecarga

    def stop(self):
        self.running = False
