"""Bridge to query RisingWave sentiment data."""

from __future__ import annotations

import logging

import risingwave_connector as rw

logger = logging.getLogger(__name__)


async def sentiment_factor() -> float:
    """Fetch and clamp sentiment score between -1 and 1."""
    rwql = "SELECT avg_score FROM sentiment_30m LIMIT 1;"
    try:
        val = await rw.fetch_float(rwql)
    except Exception as exc:  # noqa: BLE001
        logger.error("sentiment fetch failed: %s", exc)
        return 0.0
    return max(-1.0, min(1.0, val or 0.0))
