"""Configuration management for Poke MCP Production."""
from typing import List
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Server Configuration
    server_name: str = Field(default="poke-mcp-production", alias="SERVER_NAME")
    server_version: str = Field(default="1.0.0", alias="SERVER_VERSION")
    host: str = Field(default="0.0.0.0", alias="HOST")
    port: int = Field(default=8000, alias="PORT")

    # Authentication
    api_key: str = Field(default="", alias="API_KEY")
    allowed_origins: str = Field(
        default="http://localhost:*,https://yourdomain.com",
        alias="ALLOWED_ORIGINS",
    )

    # Logging
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")
    log_format: str = Field(default="json", alias="LOG_FORMAT")
    log_file: str = Field(default="logs/server.log", alias="LOG_FILE")

    # Monitoring
    enable_metrics: bool = Field(default=True, alias="ENABLE_METRICS")
    metrics_port: int = Field(default=9090, alias="METRICS_PORT")

    # PokeAPI
    pokeapi_base_url: str = Field(
        default="https://pokeapi.co/api/v2",
        alias="POKEAPI_BASE_URL",
    )
    pokeapi_timeout: int = Field(default=30, alias="POKEAPI_TIMEOUT")

    # Rate Limiting
    rate_limit_enabled: bool = Field(default=True, alias="RATE_LIMIT_ENABLED")
    rate_limit_requests: int = Field(default=100, alias="RATE_LIMIT_REQUESTS")
    rate_limit_window: int = Field(default=60, alias="RATE_LIMIT_WINDOW")

    # Production Settings
    environment: str = Field(default="production", alias="ENVIRONMENT")
    debug: bool = Field(default=False, alias="DEBUG")

    @property
    def allowed_origins_list(self) -> List[str]:
        """Parse allowed origins into a list."""
        return [origin.strip() for origin in self.allowed_origins.split(",")]


# Global settings instance
settings = Settings()
