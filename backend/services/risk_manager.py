"""Risk management utilities."""

from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Fill:
    symbol: str
    side: str
    qty: float
    price: float


class RiskSentinel:
    """Tracks balance and drawdown, halts on risk limit breach."""

    def __init__(self) -> None:
        self.balance: float = 100_000.0
        self.day_start: float = self.balance
        self.halt: bool = False
        self.fills: List[Fill] = []

    def update(self, fill: Optional[Fill]) -> None:
        if not fill:
            return
        self.fills.append(fill)
        impact = fill.qty * (fill.price if fill.side == "SELL" else -fill.price)
        self.balance += impact
        if self.intraday_dd() >= 0.05:
            self.halt = True

    def unrealized_pnl(self) -> float:
        return sum(f.qty * f.price for f in self.fills)

    def intraday_dd(self) -> float:
        return max(0.0, 1 - self.balance / self.day_start)
