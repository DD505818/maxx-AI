"""Application settings using Pydantic BaseSettings."""

from pydantic import AnyUrl, Field
from typing import cast
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Load environment variables with defaults."""

    model_config = SettingsConfigDict(extra="ignore")

    orch_url: AnyUrl = Field(
        cast(AnyUrl, "http://localhost:8080"), alias="ORCH_URL"
    )
    max_drawdown_pct: float = Field(default=0.05, alias="MAX_DRAWDOWN_PCT")


settings = Settings()  # type: ignore[call-arg]
