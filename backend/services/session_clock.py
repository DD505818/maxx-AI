"""Trading session schedule utilities."""

from datetime import datetime, timezone


def session_active() -> bool:
    """Return True if within London or New York trading hours."""
    now = datetime.now(timezone.utc)
    h = now.hour + now.minute / 60
    return (7 <= h < 16) or (12.5 <= h < 21)
