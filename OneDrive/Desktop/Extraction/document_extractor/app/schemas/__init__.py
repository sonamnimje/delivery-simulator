"""
Pydantic schemas for request/response validation.
Defines data validation and serialization for API endpoints.
"""

from datetime import datetime
from typing import Any, Dict, Optional

from pydantic import BaseModel, Field


# Document Type Enums
class DocumentTypeEnum:
    """Supported document types."""

    AADHAAR = "aadhaar"
    DRIVING_LICENSE = "driving_license"
    PASSPORT = "passport"
    INVOICE = "invoice"

    @classmethod
    def get_all(cls):
        """Get all document types."""
        return [cls.AADHAAR, cls.DRIVING_LICENSE, cls.PASSPORT, cls.INVOICE]


# ===================== Extraction Field Schemas =====================


class AadhaarExtracted(BaseModel):
    """Extracted fields from Aadhaar card."""

    full_name: Optional[str] = None
    date_of_birth: Optional[str] = None
    aadhaar_number: Optional[str] = None
    address: Optional[str] = None

    class Config:
        from_attributes = True


class DrivingLicenseExtracted(BaseModel):
    """Extracted fields from Driving License."""

    full_name: Optional[str] = None
    license_number: Optional[str] = None
    date_of_birth: Optional[str] = None
    expiry_date: Optional[str] = None

    class Config:
        from_attributes = True


class PassportExtracted(BaseModel):
    """Extracted fields from Passport."""

    full_name: Optional[str] = None
    passport_number: Optional[str] = None
    nationality: Optional[str] = None
    expiry_date: Optional[str] = None

    class Config:
        from_attributes = True


class InvoiceExtracted(BaseModel):
    """Extracted fields from Invoice."""

    invoice_number: Optional[str] = None
    vendor_name: Optional[str] = None
    invoice_date: Optional[str] = None
    total_amount: Optional[str] = None

    class Config:
        from_attributes = True


# ===================== Document Upload Schemas =====================


class DocumentUploadResponse(BaseModel):
    """Response for document upload."""

    id: int
    original_filename: str
    document_type: str
    extracted_data: Dict[str, Any]
    confidence_score: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


# ===================== Document List Schemas =====================


class DocumentListItem(BaseModel):
    """Document item in list response."""

    id: int
    original_filename: str
    document_type: str
    confidence_score: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class DocumentListResponse(BaseModel):
    """Response for document list endpoint."""

    total: int
    documents: list[DocumentListItem]


# ===================== Document Detail Schemas =====================


class DocumentDetailResponse(BaseModel):
    """Response for document detail endpoint."""

    id: int
    original_filename: str
    document_type: str
    raw_text: str
    extracted_data: Dict[str, Any]
    confidence_score: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ===================== OCR Response Schemas =====================


class OCRResponse(BaseModel):
    """Response from OCR service."""

    raw_text: str
    language: Optional[str] = None
    processing_time_ms: float


# ===================== Classification Response Schemas =====================


class ClassificationResponse(BaseModel):
    """Response from document classification service."""

    document_type: str
    confidence: float
    reasons: list[str] = []


# ===================== Extraction Response Schemas =====================


class ExtractionResponse(BaseModel):
    """Response from LLM extraction service."""

    extracted_data: Dict[str, Any]
    confidence_score: float
    extraction_notes: Optional[str] = None


# ===================== Error Response Schemas =====================


class ErrorDetail(BaseModel):
    """Error detail response."""

    detail: str
    error_code: Optional[str] = None
