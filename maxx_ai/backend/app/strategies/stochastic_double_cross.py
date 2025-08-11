"""Stochastic oscillator based strategy."""
from __future__ import annotations

import pandas as pd
from typing import Tuple


class StochasticDoubleCross:
    """Generate buy/sell using stochastic oscillator crosses."""

    def generate_signal(self, data: pd.DataFrame) -> Tuple[str | None, float]:
        if len(data) < 15:
            return None, 0.0
        import pandas_ta as ta
        stoch = ta.stoch(data.high, data.low, data.close)
        k = stoch["STOCHk_14_3_3"]
        d = stoch["STOCHd_14_3_3"]
        if k.iloc[-2] < d.iloc[-2] and k.iloc[-1] > d.iloc[-1] and k.iloc[-1] < 20:
            return "buy", 0.8
        if k.iloc[-2] > d.iloc[-2] and k.iloc[-1] < d.iloc[-1] and k.iloc[-1] > 80:
            return "sell", 0.8
        return None, 0.0
