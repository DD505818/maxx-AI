"""Simple triple moving average crossover strategy."""
from __future__ import annotations

import pandas as pd
from typing import Tuple


class TripleMACrossover:
    """Generate buy or sell signals based on three moving averages."""

    def generate_signal(self, data: pd.DataFrame) -> Tuple[str | None, float]:
        short_ma = data.close.rolling(window=5).mean()
        mid_ma = data.close.rolling(window=20).mean()
        long_ma = data.close.rolling(window=50).mean()
        if len(data) < 50:
            return None, 0.0
        if short_ma.iloc[-1] > mid_ma.iloc[-1] > long_ma.iloc[-1]:
            return "buy", 1.0
        if short_ma.iloc[-1] < mid_ma.iloc[-1] < long_ma.iloc[-1]:
            return "sell", 1.0
        return None, 0.0
