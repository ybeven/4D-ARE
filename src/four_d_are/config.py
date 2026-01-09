"""
4D-ARE Configuration via Environment Variables

Uses pydantic-settings for validation and .env file support.
"""

from pathlib import Path
from typing import Literal

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # API Configuration
    openai_api_key: SecretStr = Field(
        ...,  # Required
        description="OpenAI API key (or compatible provider)",
    )
    openai_base_url: str = Field(
        default="https://api.openai.com/v1",
        description="API base URL for OpenAI-compatible providers",
    )

    # Model Selection
    model_agent: str = Field(
        default="gpt-4o",
        description="Model for agent execution",
    )

    # MCP Server Configuration
    mcp_server_type: Literal["demo", "mysql", "postgres", "excel"] = Field(
        default="demo",
        description="Type of MCP server to use for data access",
    )

    # MySQL Configuration
    mysql_host: str = Field(default="localhost")
    mysql_port: int = Field(default=3306)
    mysql_user: str = Field(default="root")
    mysql_password: SecretStr = Field(default=SecretStr(""))
    mysql_database: str = Field(default="analytics")

    # PostgreSQL Configuration
    postgres_host: str = Field(default="localhost")
    postgres_port: int = Field(default=5432)
    postgres_user: str = Field(default="postgres")
    postgres_password: SecretStr = Field(default=SecretStr(""))
    postgres_database: str = Field(default="analytics")

    # Excel Configuration
    excel_file_path: Path = Field(default=Path("./data/metrics.xlsx"))

    # Output Configuration
    output_dir: Path = Field(default=Path("./output"))

    @property
    def scenarios_path(self) -> Path:
        return self.output_dir / "scenarios.json"

    @property
    def results_path(self) -> Path:
        return self.output_dir / "results.csv"

    @property
    def detailed_results_path(self) -> Path:
        return self.output_dir / "detailed_results.json"


# Singleton pattern for settings
_settings: Settings | None = None


def get_settings() -> Settings:
    """Factory function to create or return cached settings instance."""
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings


def reset_settings() -> None:
    """Reset cached settings (useful for testing)."""
    global _settings
    _settings = None
