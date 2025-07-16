"""Agent state representation."""

from dataclasses import dataclass


@dataclass
class AgentState:
    name: str
    state: str
    timestamp: float
    reason: str | None = None
