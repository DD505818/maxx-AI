"""Market data subscription utilities."""

import asyncio
from dataclasses import dataclass
from random import random
from typing import AsyncGenerator, List


@dataclass
class Tick:
    """A market tick."""
    symbol: str
    price: float
    volume: float


class TickSubscriber:
    """Async generator of market ticks."""

    def __init__(self, symbols: List[str]):
        self.symbols = symbols

    async def stream(self) -> AsyncGenerator[Tick, None]:
        while True:
            await asyncio.sleep(1)
            for sym in self.symbols:
                yield Tick(symbol=sym, price=100 * (1 + random()), volume=1.0)
