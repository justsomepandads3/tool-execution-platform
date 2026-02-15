"""
Application configuration using Pydantic BaseSettings.

This module defines all configuration options used across the application.
Configuration is loaded from environment variables with sensible defaults.
"""

from pathlib import Path
from typing import Optional

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.

    Attributes:
        APP_NAME: Name of the application
        DEBUG: Debug mode toggle
        MAX_FILE_SIZE: Maximum file upload size in bytes (10MB default)
        TEMP_DIR: Directory for temporary files
        ALLOWED_IMAGE_FORMATS: Tuple of allowed image formats
    """

    APP_NAME: str = "Tool Execution Platform"
    DEBUG: bool = True
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    TEMP_DIR: str = "/tmp/tool-execution"
    ALLOWED_IMAGE_FORMATS: tuple = ("png", "jpg", "jpeg", "webp", "gif", "bmp")

    class Config:
        env_file = ".env"
        case_sensitive = True


# Create a global settings instance
settings = Settings()
