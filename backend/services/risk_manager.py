"""Intraday and per-trade risk controls."""

from __future__ import annotations

from dataclasses import dataclass

from backend.utils.settings import settings

@dataclass
class Fill:
    order_id: str
    symbol: str
    side: str
    qty: float
    price: float


class RiskSentinel:
    """Simple risk management with configurable drawdown halt."""

    def __init__(self, max_dd: float | None = None, start_balance: float = 100_000.0) -> None:
        """Create a risk sentinel.

        Parameters
        ----------
        max_dd:
            Maximum intraday drawdown allowed before halting trading.
        start_balance:
            Starting account equity for the session.
        """

        self.max_dd = max_dd if max_dd is not None else settings.max_drawdown_pct
        self.max_dd = max(0.0, min(1.0, self.max_dd))
        self.balance = float(start_balance)
        self.day_start = self.balance
        self.halt = False
        self.fills: list[Fill] = []

    def update(self, fill: Fill | None) -> None:
        if not fill:
            return
        self.fills.append(fill)
        delta = fill.qty * (fill.price if fill.side == "SELL" else -fill.price)
        self.balance += delta
        if self.intraday_dd() >= self.max_dd:
            self.halt = True

    def unrealized_pnl(self) -> float:
        return sum(f.qty * f.price for f in self.fills)

    def intraday_dd(self) -> float:
        return max(0.0, 1 - self.balance / self.day_start)
