"""
Repository Pattern implementation for database access.
"""

from typing import Any, Dict, List, Optional

from loguru import logger
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.exceptions import RepositoryException
from app.models import DocumentModel


class DocumentRepository:
    """
    Repository for document database operations.
    Implements the repository pattern for clean data access.
    """

    def __init__(self, db: Session):
        """
        Initialize repository with database session.

        Args:
            db: SQLAlchemy database session
        """
        self.db = db

    def create(
        self,
        original_filename: str,
        document_type: str,
        raw_text: str,
        extracted_data: Dict[str, Any],
        confidence_score: Optional[str] = None,
        file_path: Optional[str] = None,
    ) -> DocumentModel:
        """
        Create new document record in database.

        Args:
            original_filename: Original filename
            document_type: Type of document
            raw_text: Raw OCR extracted text
            extracted_data: Extracted structured data
            confidence_score: Confidence score of extraction
            file_path: Path to stored file

        Returns:
            DocumentModel: Created document instance

        Raises:
            RepositoryException: If creation fails
        """
        try:
            logger.debug(
                f"Creating document record: {original_filename}"
            )

            document = DocumentModel(
                original_filename=original_filename,
                document_type=document_type,
                raw_text=raw_text,
                extracted_data=extracted_data,
                confidence_score=confidence_score,
                file_path=file_path,
            )

            self.db.add(document)
            self.db.commit()
            self.db.refresh(document)

            logger.info(f"Document created with ID: {document.id}")
            return document

        except Exception as e:
            self.db.rollback()
            logger.error(f"Failed to create document: {str(e)}")
            raise RepositoryException(
                f"Failed to create document record: {str(e)}"
            )

    def get_by_id(self, document_id: int) -> Optional[DocumentModel]:
        """
        Retrieve document by ID.

        Args:
            document_id: Document ID

        Returns:
            DocumentModel: Document instance or None if not found

        Raises:
            RepositoryException: If retrieval fails
        """
        try:
            logger.debug(f"Retrieving document with ID: {document_id}")

            stmt = select(DocumentModel).where(
                DocumentModel.id == document_id
            )
            document = self.db.execute(stmt).scalar_one_or_none()

            if document:
                logger.debug(f"Document found: {document_id}")
            else:
                logger.debug(f"Document not found: {document_id}")

            return document

        except Exception as e:
            logger.error(f"Failed to retrieve document: {str(e)}")
            raise RepositoryException(
                f"Failed to retrieve document: {str(e)}"
            )

    def get_all(
        self, skip: int = 0, limit: int = 100
    ) -> tuple[List[DocumentModel], int]:
        """
        Retrieve all documents with pagination.

        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            tuple: (List of documents, total count)

        Raises:
            RepositoryException: If retrieval fails
        """
        try:
            logger.debug(
                f"Retrieving documents - skip: {skip}, limit: {limit}"
            )

            # Get total count
            count_stmt = select(DocumentModel)
            total = len(self.db.execute(count_stmt).scalars().all())

            # Get paginated results
            stmt = select(DocumentModel).offset(skip).limit(limit)
            documents = self.db.execute(stmt).scalars().all()

            logger.debug(f"Retrieved {len(documents)} documents")
            return list(documents), total

        except Exception as e:
            logger.error(f"Failed to retrieve documents: {str(e)}")
            raise RepositoryException(
                f"Failed to retrieve documents: {str(e)}"
            )

    def get_by_document_type(
        self, document_type: str, skip: int = 0, limit: int = 100
    ) -> tuple[List[DocumentModel], int]:
        """
        Retrieve documents by type.

        Args:
            document_type: Type of document
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            tuple: (List of documents, total count)

        Raises:
            RepositoryException: If retrieval fails
        """
        try:
            logger.debug(
                f"Retrieving {document_type} documents - skip: {skip}, limit: {limit}"
            )

            # Get total count
            count_stmt = select(DocumentModel).where(
                DocumentModel.document_type == document_type
            )
            total = len(self.db.execute(count_stmt).scalars().all())

            # Get paginated results
            stmt = (
                select(DocumentModel)
                .where(DocumentModel.document_type == document_type)
                .offset(skip)
                .limit(limit)
            )
            documents = self.db.execute(stmt).scalars().all()

            logger.debug(
                f"Retrieved {len(documents)} {document_type} documents"
            )
            return list(documents), total

        except Exception as e:
            logger.error(
                f"Failed to retrieve {document_type} documents: {str(e)}"
            )
            raise RepositoryException(
                f"Failed to retrieve documents: {str(e)}"
            )

    def update(
        self, document_id: int, **kwargs
    ) -> Optional[DocumentModel]:
        """
        Update document record.

        Args:
            document_id: Document ID
            **kwargs: Fields to update

        Returns:
            DocumentModel: Updated document instance

        Raises:
            RepositoryException: If update fails
        """
        try:
            logger.debug(f"Updating document: {document_id}")

            document = self.get_by_id(document_id)
            if not document:
                return None

            for key, value in kwargs.items():
                if hasattr(document, key):
                    setattr(document, key, value)

            self.db.commit()
            self.db.refresh(document)

            logger.info(f"Document updated: {document_id}")
            return document

        except Exception as e:
            self.db.rollback()
            logger.error(f"Failed to update document: {str(e)}")
            raise RepositoryException(
                f"Failed to update document: {str(e)}"
            )

    def delete(self, document_id: int) -> bool:
        """
        Delete document record.

        Args:
            document_id: Document ID

        Returns:
            bool: True if deleted successfully

        Raises:
            RepositoryException: If deletion fails
        """
        try:
            logger.debug(f"Deleting document: {document_id}")

            document = self.get_by_id(document_id)
            if not document:
                return False

            self.db.delete(document)
            self.db.commit()

            logger.info(f"Document deleted: {document_id}")
            return True

        except Exception as e:
            self.db.rollback()
            logger.error(f"Failed to delete document: {str(e)}")
            raise RepositoryException(
                f"Failed to delete document: {str(e)}"
            )
