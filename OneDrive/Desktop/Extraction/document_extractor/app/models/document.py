"""
SQLAlchemy database models for document extraction.
Defines the schema for storing documents and extracted data.
"""

from datetime import datetime
from typing import Optional

from sqlalchemy import JSON, Column, DateTime, Integer, String, Text

from app.core.database import Base


class DocumentModel(Base):
    """
    Model for storing uploaded documents and their extraction results.

    Attributes:
        id: Primary key
        original_filename: Original name of uploaded file
        document_type: Type of document (aadhaar, driving_license, passport, invoice)
        raw_text: Raw OCR extracted text
        extracted_data: Extracted structured data as JSON
        confidence_score: Confidence score of extraction (0-1)
        file_path: Path to stored file
        created_at: Timestamp of document creation
        updated_at: Timestamp of last update
    """

    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    original_filename = Column(String(255), nullable=False)
    document_type = Column(String(50), nullable=False, index=True)
    raw_text = Column(Text, nullable=False)
    extracted_data = Column(JSON, nullable=True)
    confidence_score = Column(String(10), nullable=True)  # Stored as string for precision
    file_path = Column(String(500), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    class Config:
        """SQLAlchemy configuration."""

        from_attributes = True
