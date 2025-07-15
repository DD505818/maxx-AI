"""Intraday and per-trade risk controls."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Fill:
    order_id: str
    symbol: str
    side: str
    qty: float
    price: float


class RiskSentinel:
    """Simple risk management with drawdown halt."""

    def __init__(self) -> None:
        self.balance = 100_000.0
        self.day_start = self.balance
        self.halt = False
        self.fills: list[Fill] = []

    def update(self, fill: Fill | None) -> None:
        if not fill:
            return
        self.fills.append(fill)
        delta = fill.qty * (fill.price if fill.side == "SELL" else -fill.price)
        self.balance += delta
        if self.intraday_dd() >= 0.05:
            self.halt = True

    def unrealized_pnl(self) -> float:
        return sum(f.qty * f.price for f in self.fills)

    def intraday_dd(self) -> float:
        return max(0.0, 1 - self.balance / self.day_start)
