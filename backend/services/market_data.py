"""Asynchronous market data feed simulator."""

from __future__ import annotations

import asyncio
import random
from dataclasses import dataclass
from typing import Iterable, AsyncGenerator


@dataclass
class Tick:
    """Market tick data."""

    symbol: str
    price: float


class TickSubscriber:
    """Simulates subscription to a live market data feed."""

    def __init__(self, symbols: Iterable[str]):
        self.symbols = list(symbols)

    async def stream(self) -> AsyncGenerator[Tick, None]:
        """Yield ticks indefinitely."""
        prices = {s: random.uniform(100, 50000) for s in self.symbols}
        while True:
            await asyncio.sleep(0.5)
            sym = random.choice(self.symbols)
            delta = random.uniform(-0.5, 0.5)
            prices[sym] = max(1.0, prices[sym] * (1 + delta / 100))
            yield Tick(symbol=sym, price=prices[sym])
