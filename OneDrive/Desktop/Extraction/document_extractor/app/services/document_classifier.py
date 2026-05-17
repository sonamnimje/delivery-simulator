"""
Document Classification Service.
Identifies document type from OCR extracted text.
"""

from loguru import logger

from app.core.exceptions import DocumentClassificationException
from app.schemas import ClassificationResponse, DocumentTypeEnum


class DocumentClassifier:
    """
    Classifies document type based on extracted text.
    Uses keyword matching and heuristics.
    """

    # Document type keywords for classification
    DOCUMENT_KEYWORDS = {
        DocumentTypeEnum.AADHAAR: [
            "aadhaar",
            "आधार",
            "uid",
            "date of birth",
            "address",
        ],
        DocumentTypeEnum.DRIVING_LICENSE: [
            "driving license",
            "license number",
            "dl number",
            "driving",
            "license",
            "expiry",
        ],
        DocumentTypeEnum.PASSPORT: [
            "passport",
            "passport number",
            "nationality",
            "valid until",
            "issued",
        ],
        DocumentTypeEnum.INVOICE: [
            "invoice",
            "invoice number",
            "total amount",
            "vendor",
            "seller",
            "amount due",
        ],
    }

    def classify(self, raw_text: str) -> ClassificationResponse:
        """
        Classify document type based on extracted text.

        Args:
            raw_text: Raw OCR extracted text

        Returns:
            ClassificationResponse: Document type and confidence score

        Raises:
            DocumentClassificationException: If classification fails
        """
        logger.info("Starting document classification")

        try:
            text_lower = raw_text.lower()
            scores = {}

            # Calculate confidence score for each document type
            for doc_type, keywords in self.DOCUMENT_KEYWORDS.items():
                matching_keywords = sum(
                    1 for keyword in keywords if keyword.lower() in text_lower
                )
                confidence = matching_keywords / len(keywords)
                scores[doc_type] = confidence

            # Get document type with highest confidence
            best_match = max(scores, key=scores.get)
            confidence_score = scores[best_match]

            # Check if confidence is above threshold
            if confidence_score < 0.3:
                logger.warning(
                    f"Low confidence classification: {best_match} ({confidence_score:.2f})"
                )

            logger.info(
                f"Document classified as {best_match} with confidence {confidence_score:.2f}"
            )

            return ClassificationResponse(
                document_type=best_match,
                confidence=confidence_score,
                reasons=self._get_classification_reasons(
                    best_match, text_lower
                ),
            )

        except Exception as e:
            logger.error(f"Document classification failed: {str(e)}")
            raise DocumentClassificationException(
                f"Failed to classify document: {str(e)}"
            )

    def _get_classification_reasons(
        self, doc_type: str, text_lower: str
    ) -> list[str]:
        """
        Get reasons for classification decision.

        Args:
            doc_type: Classified document type
            text_lower: Lowercased extracted text

        Returns:
            list[str]: List of reasons for classification
        """
        reasons = []
        keywords = self.DOCUMENT_KEYWORDS.get(doc_type, [])

        for keyword in keywords:
            if keyword.lower() in text_lower:
                reasons.append(f"Found keyword: '{keyword}'")

        return reasons[:3]  # Return top 3 reasons
