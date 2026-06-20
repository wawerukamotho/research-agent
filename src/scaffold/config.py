from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    # API Keys
    openai_api_key: Optional[str] = None
    anthropic_api_key: Optional[str] = None
    openrouter_api_key: Optional[str] = None
    google_api_key: Optional[str] = None
    serper_api_key: Optional[str] = None
    tavily_api_key: Optional[str] = None
    github_token: Optional[str] = None
    news_api_key: Optional[str] = None

    # Database & Cache
    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/research"
    redis_url: str = "redis://localhost:6379/0"

    # Application
    app_name: str = "Deep Research Agent"
    environment: str = "development"
    debug: bool = True
    port: int = 8000
    host: str = "0.0.0.0"

    # LLM Configuration
    default_llm_model: str = "openrouter/free"
    fallback_llm_model: str = "openrouter/free"
    openrouter_api_key: Optional[str] = None

    # Observability
    otel_exporter_otlp_endpoint: str = "http://jaeger:4317"
    prometheus_port: int = 9091


settings = Settings()
