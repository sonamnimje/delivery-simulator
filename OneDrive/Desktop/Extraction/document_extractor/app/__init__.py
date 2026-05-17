"""Document Extractor Application Module."""

from app.core import get_settings, setup_logger
from app.main import app

setup_logger()

__all__ = ["app", "get_settings"]
