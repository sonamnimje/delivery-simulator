"""
Storage Service for managing file uploads and storage.
"""

import os
from datetime import datetime
from pathlib import Path
from typing import Optional

from loguru import logger

from app.core.config import get_settings
from app.core.exceptions import FileUploadException


class StorageService:
    """
    Manages file uploads and storage.
    """

    # Explicit Poppler path for Windows
    POPPLER_PATH = r"C:\poppler\poppler-26.02.0\Library\bin"

    def __init__(self):
        """Initialize storage service."""
        self.settings = get_settings()
        self.upload_dir = Path(self.settings.upload_dir)
        self._ensure_upload_dir_exists()

    def _ensure_upload_dir_exists(self):
        """Ensure upload directory exists."""
        self.upload_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"Upload directory ready: {self.upload_dir}")

    def save_uploaded_file(
        self, file_content: bytes, original_filename: str
    ) -> str:
        """
        Save uploaded file to disk.
        """
        try:
            self._validate_file_extension(original_filename)

            file_path = self._generate_file_path(original_filename)

            with open(file_path, "wb") as f:
                f.write(file_content)

            logger.info(f"File saved successfully: {file_path}")
            return str(file_path)

        except FileUploadException:
            raise
        except Exception as e:
            logger.error(f"File save failed: {str(e)}")
            raise FileUploadException(f"Failed to save file: {str(e)}")

    def _validate_file_extension(self, filename: str):
        """
        Validate file extension.
        """
        allowed_extensions = self.settings.allowed_extensions
        file_extension = Path(filename).suffix.lower().lstrip(".")

        if file_extension not in allowed_extensions:
            raise FileUploadException(
                f"File type .{file_extension} not allowed. "
                f"Allowed types: {', '.join(allowed_extensions)}"
            )

    def _generate_file_path(self, original_filename: str) -> Path:
        """
        Generate unique file path.
        """
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        unique_filename = f"{timestamp}_{original_filename}"

        return self.upload_dir / unique_filename

    def delete_file(self, file_path: str) -> bool:
        """
        Delete uploaded file.
        """
        try:
            file_path_obj = Path(file_path)

            if file_path_obj.exists():
                file_path_obj.unlink()
                logger.info(f"File deleted: {file_path}")
                return True

            logger.warning(f"File not found for deletion: {file_path}")
            return False

        except Exception as e:
            logger.error(f"File deletion failed: {str(e)}")
            raise FileUploadException(f"Failed to delete file: {str(e)}")

    def get_file_size_mb(self, file_path: str) -> float:
        """
        Get file size in MB.
        """
        try:
            file_size_bytes = os.path.getsize(file_path)
            return file_size_bytes / (1024 * 1024)

        except Exception as e:
            logger.error(f"Failed to get file size: {str(e)}")
            raise FileUploadException(f"Failed to get file size: {str(e)}")

    @staticmethod
    def convert_pdf_to_images(pdf_path: str) -> list[str]:
        """
        Convert PDF to images for OCR processing.
        """
        try:
            import pdf2image

            logger.info(f"Converting PDF to images: {pdf_path}")

            output_dir = Path(pdf_path).parent / "pdf_images"
            output_dir.mkdir(exist_ok=True)

            # Explicit poppler path
            images = pdf2image.convert_from_path(
                pdf_path,
                dpi=300,
                fmt="jpeg",
                output_folder=str(output_dir),
                poppler_path=StorageService.POPPLER_PATH
            )

            image_paths = []

            for i, image in enumerate(images):
                image_path = output_dir / f"page_{i+1}.jpeg"
                image.save(image_path, "JPEG")
                image_paths.append(str(image_path))

            logger.info(
                f"PDF conversion successful: {len(image_paths)} pages converted"
            )

            return image_paths

        except Exception as e:
            logger.error(f"PDF conversion failed: {str(e)}")
            raise FileUploadException(
                f"PDF conversion failed: {str(e)}"
            )