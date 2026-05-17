"""
Document processing API routes.
"""

from typing import Any, Dict, List

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from loguru import logger
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.exceptions import DocumentExtractorException
from app.repositories import DocumentRepository
from app.schemas import (
    DocumentDetailResponse,
    DocumentListResponse,
    DocumentTypeEnum,
    DocumentUploadResponse,
    ErrorDetail,
)
from app.services import (
    DocumentClassifier,
    LLMExtractionService,
    OCRService,
    StorageService,
    ValidationService,
)

router = APIRouter(prefix="/api/v1", tags=["documents"])

# Service instances (lazy initialized)
_ocr_service = None
classifier = DocumentClassifier()
llm_service = LLMExtractionService()
storage_service = StorageService()

def get_ocr_service():
    global _ocr_service
    if _ocr_service is None:
        try:
            _ocr_service = OCRService()
        except Exception as e:
            logger.warning(f"OCR service failed to initialize: {e}. Using mock extraction.")
            _ocr_service = None
    return _ocr_service


@router.post(
    "/upload-document",
    response_model=DocumentUploadResponse,
    responses={400: {"model": ErrorDetail}},
)
async def upload_document(
    file: UploadFile = File(...), db: Session = Depends(get_db)
) -> DocumentUploadResponse:
    """
    Upload and process a document.

    Process flow:
    1. Validate and save file
    2. Extract text via OCR
    3. Classify document type
    4. Extract structured fields using LLM
    5. Validate extracted data
    6. Store in database
    7. Return extracted data

    Args:
        file: Document file (PDF/JPG/PNG)
        db: Database session

    Returns:
        DocumentUploadResponse: Processed document with extracted fields

    Raises:
        HTTPException: If processing fails
    """
    try:
        logger.info(f"Document upload started: {file.filename}")

        # 1. Read and validate file
        file_content = await file.read()
        if not file_content:
            raise HTTPException(status_code=400, detail="Empty file")

        # 2. Save file
        file_path = storage_service.save_uploaded_file(
            file_content, file.filename
        )
        logger.info(f"File saved: {file_path}")

        # 3. Handle PDF conversion if needed
        if file.filename.lower().endswith(".pdf"):
            image_paths = storage_service.convert_pdf_to_images(
                file_path
            )
            if not image_paths:
                raise HTTPException(
                    status_code=400, detail="PDF conversion failed"
                )
            ocr_image_path = image_paths[0]
        else:
            ocr_image_path = file_path

        # 4. Extract text via OCR
        ocr_service = get_ocr_service()
        if ocr_service:
            ocr_response = ocr_service.extract_text(ocr_image_path)
        else:
            # Fallback: use mock OCR
            from app.schemas import OCRResponse
            ocr_response = OCRResponse(
                raw_text="Mock OCR: Document text extraction unavailable",
                confidence=0.0,
                processing_time=0.0
            )
        logger.info(
            f"OCR completed: {len(ocr_response.raw_text)} characters"
        )

        # 5. Classify document type
        classification = classifier.classify(ocr_response.raw_text)
        logger.info(
            f"Document classified as: {classification.document_type}"
        )

        # 6. Extract structured fields
        extraction = llm_service.extract_fields(
            ocr_response.raw_text, classification.document_type
        )
        logger.info(
            f"Fields extracted with confidence: {extraction.confidence_score:.2f}"
        )

        # 7. Validate extracted data
        validated_data = ValidationService.validate_extracted_data(
            extraction.extracted_data, classification.document_type
        )
        logger.info("Data validation successful")

        # 8. Store in database
        repository = DocumentRepository(db)
        document = repository.create(
            original_filename=file.filename,
            document_type=classification.document_type,
            raw_text=ocr_response.raw_text,
            extracted_data=validated_data,
            confidence_score=f"{extraction.confidence_score:.2f}",
            file_path=file_path,
        )

        logger.info(f"Document processed successfully: ID {document.id}")

        return DocumentUploadResponse(
            id=document.id,
            original_filename=document.original_filename,
            document_type=document.document_type,
            extracted_data=document.extracted_data,
            confidence_score=document.confidence_score,
            created_at=document.created_at,
        )

    except DocumentExtractorException as e:
        logger.error(f"Document processing error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error during document upload: {str(e)}")
        raise HTTPException(
            status_code=500, detail="Internal server error"
        )


@router.get(
    "/documents",
    response_model=DocumentListResponse,
    responses={500: {"model": ErrorDetail}},
)
def get_documents(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
) -> DocumentListResponse:
    """
    Get all processed documents with pagination.

    Args:
        skip: Number of records to skip (default: 0)
        limit: Maximum records to return (default: 100)
        db: Database session

    Returns:
        DocumentListResponse: List of documents and total count

    Raises:
        HTTPException: If retrieval fails
    """
    try:
        logger.info(f"Fetching documents - skip: {skip}, limit: {limit}")

        repository = DocumentRepository(db)
        documents, total = repository.get_all(skip, limit)

        return DocumentListResponse(
            total=total,
            documents=[
                {
                    "id": doc.id,
                    "original_filename": doc.original_filename,
                    "document_type": doc.document_type,
                    "confidence_score": doc.confidence_score,
                    "created_at": doc.created_at,
                }
                for doc in documents
            ],
        )

    except Exception as e:
        logger.error(f"Error fetching documents: {str(e)}")
        raise HTTPException(
            status_code=500, detail="Failed to fetch documents"
        )


@router.get(
    "/documents/{document_id}",
    response_model=DocumentDetailResponse,
    responses={404: {"model": ErrorDetail}, 500: {"model": ErrorDetail}},
)
def get_document(
    document_id: int, db: Session = Depends(get_db)
) -> DocumentDetailResponse:
    """
    Get specific document with full details.

    Args:
        document_id: ID of document
        db: Database session

    Returns:
        DocumentDetailResponse: Full document details

    Raises:
        HTTPException: If document not found or retrieval fails
    """
    try:
        logger.info(f"Fetching document: {document_id}")

        repository = DocumentRepository(db)
        document = repository.get_by_id(document_id)

        if not document:
            logger.warning(f"Document not found: {document_id}")
            raise HTTPException(status_code=404, detail="Document not found")

        return DocumentDetailResponse(
            id=document.id,
            original_filename=document.original_filename,
            document_type=document.document_type,
            raw_text=document.raw_text,
            extracted_data=document.extracted_data,
            confidence_score=document.confidence_score,
            created_at=document.created_at,
            updated_at=document.updated_at,
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching document: {str(e)}")
        raise HTTPException(
            status_code=500, detail="Failed to fetch document"
        )


@router.get("/health", tags=["health"])
def health_check() -> Dict[str, str]:
    """
    Health check endpoint.

    Returns:
        dict: Health status
    """
    return {"status": "healthy"}
