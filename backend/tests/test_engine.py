import asyncio

from backend.services.trading_engine import TradingEngine
from backend.services.market_data import TickSubscriber, Tick
from backend.services.risk_manager import RiskSentinel


class DummySub(TickSubscriber):
    def __init__(self) -> None:
        super().__init__(["BTCUSD"], delay=0.0)

    async def stream(self):
        for _ in range(3):
            yield Tick(symbol="BTCUSD", price=100.0)


def test_engine_run() -> None:
    engine = TradingEngine(
        tick_sub=DummySub(),
        risk=RiskSentinel(start_balance=100),
    )
    asyncio.run(engine.run(3))
    assert isinstance(engine.risk.balance, float)
