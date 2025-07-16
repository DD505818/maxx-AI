"""Sentiment bridge to RisingWave."""

from typing import Optional
import risingwave_connector as rw


async def sentiment_factor() -> float:
    """Fetch sentiment factor between -1 and 1."""
    rwql = "SELECT avg_score FROM sentiment_30m LIMIT 1;"
    val: Optional[float] = await rw.fetch_float(rwql)
    if val is None:
        return 0.0
    return max(-1.0, min(1.0, val))
