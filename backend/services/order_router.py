"""Order routing and execution."""

import asyncio
from dataclasses import dataclass
from typing import Optional


@dataclass
class Fill:
    """Execution fill data."""
    symbol: str
    side: str
    qty: float
    price: float
    venue: str


class Router:
    """Simulated order router with simple best-venue logic."""

    def __init__(self) -> None:
        self.venues = ["exchangeA", "exchangeB"]

    def best_venue(self, symbol: str) -> str:
        return self.venues[0]

    async def execute(self, leg) -> Optional[Fill]:
        await asyncio.sleep(0.1)
        return Fill(symbol=leg.symbol, side=leg.side, qty=leg.qty, price=leg.price, venue=self.best_venue(leg.symbol))
