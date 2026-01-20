"""Configuration management for Bronze AI Employee"""

from pathlib import Path
from typing import Optional

from pydantic_settings import BaseSettings # type: ignore


class Settings(BaseSettings):
    """Application configuration from .env"""

    # Gemini API
    gemini_api_key: str = "AIzaSyCHMs7jCo2ESkSuqO6Cp_Q25gjoDJrYcMM"

    # Gmail Configuration
    gmail_credentials_json: str = "./credentials.json"
    gmail_token_json: str = "./token.json"
    gmail_check_interval: int = 300  # seconds

    # WhatsApp Configuration
    whatsapp_api_key: str = ""
    whatsapp_webhook_url: str = "http://localhost:8000/whatsapp"

    # Filesystem Watcher
    watch_directories: str = "./inbox,./tasks"
    file_monitor_interval: int = 60  # seconds

    # MCP Server
    mcp_port: int = 8001
    mcp_host: str = "127.0.0.1"

    # Obsidian Vault
    vault_path: str = "./AI_Employee_Vault"

    # Agent Configuration
    agent_name: str = "BronzeAI"
    agent_role: str = "Personal AI Employee"
    ralph_wiggum_retries: int = 10
    ralph_wiggum_timeout: int = 300  # seconds

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


def get_settings() -> Settings:
    """Get application settings"""
    return Settings()


def get_vault_path() -> Path:
    """Get the Obsidian vault path"""
    settings = get_settings()
    return Path(settings.vault_path).resolve()
