"""
Custom exception classes for the application.
Provides specific exception types for different error scenarios.
"""


class DocumentExtractorException(Exception):
    """Base exception for Document Extractor application."""

    pass


class OCRException(DocumentExtractorException):
    """Raised when OCR processing fails."""

    pass


class DocumentClassificationException(DocumentExtractorException):
    """Raised when document type classification fails."""

    pass


class LLMExtractionException(DocumentExtractorException):
    """Raised when LLM-based extraction fails."""

    pass


class ValidationException(DocumentExtractorException):
    """Raised when validation of extracted data fails."""

    pass


class StorageException(DocumentExtractorException):
    """Raised when database storage operations fail."""

    pass


class FileUploadException(DocumentExtractorException):
    """Raised when file upload processing fails."""

    pass


class ConfigurationException(DocumentExtractorException):
    """Raised when configuration is invalid or missing."""

    pass


class RepositoryException(DocumentExtractorException):
    """Raised when repository operations fail."""

    pass
