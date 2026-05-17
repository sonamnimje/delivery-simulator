"""
Configuration management using Pydantic Settings.
Loads configuration from environment variables.
"""

from functools import lru_cache
from typing import Optional

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Application
    app_name: str = "Document Extractor Platform"
    app_version: str = "1.0.0"
    debug: bool = False

    # Database
    database_url: str = "postgresql://user:password@localhost/document_extractor"
    database_pool_size: int = 20
    database_max_overflow: int = 40

    # OpenAI
    openai_api_key: str
    openai_model: str = "gpt-4-turbo"

    # File Upload
    upload_dir: str = "./uploads"
    max_file_size_mb: int = 10
    allowed_extensions: list = ["pdf", "jpg", "jpeg", "png"]

    # OCR
    ocr_engine: str = "paddleocr"  # paddleocr or tesseract
    ocr_timeout: int = 60

    # Logging
    log_level: str = "INFO"
    log_format: str = (
        "<level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
        "<level>{message}</level>"
    )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """
    Get application settings (cached).

    Returns:
        Settings: Application configuration
    """
    return Settings()
