"""Select tradable stock symbols."""
from __future__ import annotations

from typing import List


class StockSelectionService:
    """Return a static list of symbols."""

    def select_stocks(self) -> List[str]:
        return ["AAPL", "MSFT", "GOOG"]
