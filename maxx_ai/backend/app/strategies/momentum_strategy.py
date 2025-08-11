"""Momentum strategy."""
from __future__ import annotations

import pandas as pd
from typing import Tuple


class MomentumStrategy:
    """Buy when price momentum is positive."""

    def generate_signal(self, data: pd.DataFrame) -> Tuple[str | None, float]:
        if len(data) < 20:
            return None, 0.0
        momentum = data.close.pct_change(5).iloc[-1]
        if momentum > 0.02:
            return "buy", momentum
        if momentum < -0.02:
            return "sell", -momentum
        return None, 0.0
