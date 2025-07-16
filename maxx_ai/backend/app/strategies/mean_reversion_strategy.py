"""Mean reversion strategy."""
from __future__ import annotations

import pandas as pd
from typing import Tuple


class MeanReversionStrategy:
    """Sell when price is far above moving average; buy when below."""

    def generate_signal(self, data: pd.DataFrame) -> Tuple[str | None, float]:
        if len(data) < 30:
            return None, 0.0
        ma = data.close.rolling(window=20).mean()
        diff = (data.close.iloc[-1] - ma.iloc[-1]) / ma.iloc[-1]
        if diff > 0.03:
            return "sell", diff
        if diff < -0.03:
            return "buy", -diff
        return None, 0.0
