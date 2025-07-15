"""Signal generation via ensemble methods."""

from __future__ import annotations

from collections import deque
from typing import Iterable, List

import numpy as np


class AlphaEngine:
    """Blend momentum, mean reversion, and breakout signals."""

    def __init__(self, symbols: Iterable[str] | None = None):
        symbols = symbols or ["BTCUSD", "ETHUSD", "EURUSD"]
        self.prices = {sym: deque(maxlen=200) for sym in symbols}

    def update(self, symbol: str, price: float) -> None:
        self.prices[symbol].append(price)

    def score(self, symbol: str) -> float:
        p: List[float] = list(self.prices[symbol])
        if len(p) < 50:
            return 0.0
        mom = np.tanh(np.polyfit(range(len(p)), p, 1)[0] * 100)
        mean_rev = -np.tanh((p[-1] - np.mean(p[-20:])) / (np.std(p[-20:]) + 1e-9))
        high, low = max(p[-50:]), min(p[-50:])
        breakout = 1.0 if p[-1] >= high * 0.995 else -1.0 if p[-1] <= low * 1.005 else 0.0
        return 0.5 * mom + 0.3 * mean_rev + 0.2 * breakout

    def size(self, price: float, balance: float, alpha: float, vix: float = 18) -> float:
        btc_prices = list(self.prices["BTCUSD"])[-50:]
        if len(btc_prices) < 10:
            return 0.0
        kelly = max(0.01, min(0.5 / (1 + vix / 20), alpha / (np.std(btc_prices) ** 2)))
        risk_dollars = balance * 0.003
        qty = abs(kelly) * risk_dollars / price
        return round(qty, 6)
