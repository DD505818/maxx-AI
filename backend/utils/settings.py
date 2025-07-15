"""Application settings using Pydantic BaseSettings."""

from pydantic import AnyUrl, Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Load environment variables with defaults."""

    orch_url: AnyUrl = Field("http://localhost:8080", env="ORCH_URL")


settings = Settings()
