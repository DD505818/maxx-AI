"""Application settings using Pydantic BaseSettings."""

from pydantic import AnyUrl, Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Load environment variables with defaults."""

    orch_url: AnyUrl = Field("http://localhost:8080", env="ORCH_URL")
    max_drawdown_pct: float = Field(0.05, env="MAX_DRAWDOWN_PCT")


settings = Settings()
