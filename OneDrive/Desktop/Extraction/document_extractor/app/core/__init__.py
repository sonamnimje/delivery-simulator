"""Core module - Configuration, logging, and exceptions."""

from .config import Settings, get_settings
from .exceptions import (
    ConfigurationException,
    DocumentClassificationException,
    DocumentExtractorException,
    FileUploadException,
    LLMExtractionException,
    OCRException,
    RepositoryException,
    StorageException,
    ValidationException,
)
from .logger import setup_logger

__all__ = [
    "Settings",
    "get_settings",
    "setup_logger",
    "DocumentExtractorException",
    "OCRException",
    "DocumentClassificationException",
    "LLMExtractionException",
    "ValidationException",
    "StorageException",
    "FileUploadException",
    "ConfigurationException",
    "RepositoryException",
]
