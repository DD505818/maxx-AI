"""Ichimoku cloud strategy."""
from __future__ import annotations

import pandas as pd
import pandas_ta as ta
from typing import Tuple


class IchimokuCloud:
    """Generate signals using Ichimoku cloud components."""

    def generate_signal(self, data: pd.DataFrame) -> Tuple[str | None, float]:
        if len(data) < 60:
            return None, 0.0
        ichi = ta.ichimoku(data.high, data.low, data.close)
        conv = ichi[0]
        base = ichi[1]
        if conv.iloc[-1] > base.iloc[-1] and data.close.iloc[-1] > ichi[2].iloc[-1]:
            return "buy", 0.7
        if conv.iloc[-1] < base.iloc[-1] and data.close.iloc[-1] < ichi[3].iloc[-1]:
            return "sell", 0.7
        return None, 0.0
