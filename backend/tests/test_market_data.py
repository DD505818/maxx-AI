import asyncio
from backend.services.market_data import TickSubscriber, Tick


def test_tick_stream() -> None:
    sub = TickSubscriber(["BTCUSD"])
    tick = asyncio.run(sub.stream().__anext__())
    assert isinstance(tick, Tick)
    assert tick.symbol == "BTCUSD"
