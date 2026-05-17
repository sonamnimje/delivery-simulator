"""
Mock Document Field Extraction Service.
Temporarily bypasses OpenAI API calls for local testing/demo.
"""

from loguru import logger

from app.core.config import get_settings
from app.core.exceptions import LLMExtractionException
from app.schemas import (
    DocumentTypeEnum,
    ExtractionResponse,
)


class LLMExtractionService:
    """
    Extracts structured fields from documents.
    Currently using mock extraction instead of OpenAI.
    """

    def __init__(self):
        self.settings = get_settings()
        logger.info(
            "Mock LLM Extraction Service initialized (OpenAI bypassed)"
        )

    def extract_fields(
        self,
        raw_text: str,
        document_type: str
    ) -> ExtractionResponse:
        """
        Return mock structured data based on document type.

        Args:
            raw_text: OCR extracted text
            document_type: Classified document type

        Returns:
            ExtractionResponse
        """

        logger.info(
            f"Starting mock extraction for {document_type}"
        )

        try:
            extracted_data = self._generate_mock_data(
                raw_text,
                document_type
            )

            confidence = self._calculate_confidence(
                extracted_data
            )

            logger.info(
                f"Mock extraction completed successfully for {document_type}"
            )

            return ExtractionResponse(
                extracted_data=extracted_data,
                confidence_score=confidence,
                extraction_notes="Mock extraction used (OpenAI disabled for local testing)"
            )

        except Exception as e:
            logger.error(
                f"Mock extraction failed: {str(e)}"
            )
            raise LLMExtractionException(
                f"Field extraction failed: {str(e)}"
            )

    def _generate_mock_data(
        self,
        raw_text: str,
        document_type: str
    ) -> dict:
        """
        Generate dummy extracted fields based on document type.
        """

        if document_type == DocumentTypeEnum.AADHAAR:
            return {
                "full_name": "Demo User",
                "date_of_birth": "2002-05-10",
                "aadhaar_number": "1234 5678 9012",
                "address": "Jabalpur, Madhya Pradesh",
                "raw_text_preview": raw_text[:300]
            }

        elif document_type == DocumentTypeEnum.DRIVING_LICENSE:
            return {
                "full_name": "Demo User",
                "license_number": "MP20DL1234567",
                "date_of_birth": "2002-05-10",
                "expiry_date": "2032-05-10",
                "raw_text_preview": raw_text[:300]
            }

        elif document_type == DocumentTypeEnum.PASSPORT:
            return {
                "full_name": "Demo User",
                "passport_number": "P1234567",
                "nationality": "Indian",
                "expiry_date": "2035-01-01",
                "raw_text_preview": raw_text[:300]
            }

        elif document_type == DocumentTypeEnum.INVOICE:
            return {
                "invoice_number": "INV-2026-001",
                "vendor_name": "ABC Pvt Ltd",
                "invoice_date": "2026-05-08",
                "total_amount": "₹5,000",
                "raw_text_preview": raw_text[:300]
            }

        else:
            return {
                "document_type": document_type,
                "raw_text_preview": raw_text[:300],
                "message": "Unknown document type"
            }

    def _calculate_confidence(
        self,
        extracted_data: dict
    ) -> float:
        """
        Mock confidence calculation.
        """

        filled_fields = len(
            [
                value for value in extracted_data.values()
                if value is not None
            ]
        )

        total_fields = len(extracted_data)

        if total_fields == 0:
            return 0.0

        confidence = filled_fields / total_fields
        return min(confidence, 1.0)