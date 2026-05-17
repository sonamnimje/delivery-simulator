"""
OCR Service for text extraction from documents.
Supports PaddleOCR with fallback to Tesseract.
"""

import time
import os

from loguru import logger

from app.core.config import get_settings
from app.core.exceptions import OCRException, ConfigurationException
from app.schemas import OCRResponse


class OCRService:
    """
    OCR Service for extracting text from documents.
    Uses PaddleOCR as primary engine with Tesseract fallback.
    """

    def __init__(self):
        self.settings = get_settings()
        self.ocr_engine = self.settings.ocr_engine
        self._initialize_ocr_engine()

    def _initialize_ocr_engine(self):
        """Initialize OCR engine."""
        try:
            if self.ocr_engine == "paddleocr":
                try:
                    from paddleocr import PaddleOCR

                    logger.info("Initializing PaddleOCR engine")

                    self.ocr = PaddleOCR(
                        use_angle_cls=True,
                        lang="en",
                        use_gpu=False
                    )

                    logger.info("PaddleOCR initialized successfully")

                except ImportError:
                    logger.warning(
                        "PaddleOCR not installed, falling back to Tesseract"
                    )
                    self._initialize_tesseract()

            else:
                self._initialize_tesseract()

        except Exception as e:
            logger.error(f"OCR initialization failed: {str(e)}")
            raise ConfigurationException(
                f"OCR engine initialization failed: {str(e)}"
            )

    def _initialize_tesseract(self):
        """Initialize Tesseract OCR."""
        try:
            import pytesseract
            from PIL import Image

            logger.info("Initializing Tesseract OCR engine")

            # Explicit path to installed Tesseract
            tesseract_path = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

            if not os.path.exists(tesseract_path):
                raise ConfigurationException(
                    f"Tesseract executable not found at: {tesseract_path}"
                )

            pytesseract.pytesseract.tesseract_cmd = tesseract_path

            self.pytesseract = pytesseract
            self.Image = Image
            self.ocr_engine = "tesseract"

            logger.info(
                f"Tesseract initialized successfully from {tesseract_path}"
            )

        except ImportError:
            raise ConfigurationException(
                "Tesseract dependencies missing. Run: pip install pytesseract pillow"
            )

    def extract_text(self, image_path: str) -> OCRResponse:
        """Extract text from document."""
        logger.info(f"Starting OCR extraction from: {image_path}")
        start_time = time.time()

        try:
            if self.ocr_engine == "paddleocr":
                return self._extract_with_paddleocr(
                    image_path,
                    start_time
                )
            else:
                return self._extract_with_tesseract(
                    image_path,
                    start_time
                )

        except Exception as e:
            logger.error(f"OCR extraction failed: {str(e)}")
            raise OCRException(
                f"Text extraction failed: {str(e)}"
            )

    def _extract_with_paddleocr(
        self,
        image_path: str,
        start_time: float
    ) -> OCRResponse:
        """Extract text using PaddleOCR."""
        result = self.ocr.ocr(image_path, cls=True)

        extracted_text = ""

        for line in result:
            if line:
                for word_info in line:
                    extracted_text += word_info[1][0] + " "

        processing_time = (time.time() - start_time) * 1000

        return OCRResponse(
            raw_text=extracted_text.strip(),
            language="en",
            processing_time_ms=processing_time
        )

    def _extract_with_tesseract(
        self,
        image_path: str,
        start_time: float
    ) -> OCRResponse:
        """Extract text using Tesseract."""
        try:
            image = self.Image.open(image_path)

            extracted_text = self.pytesseract.image_to_string(image)

            processing_time = (time.time() - start_time) * 1000

            logger.info(
                f"Tesseract extracted {len(extracted_text)} characters"
            )

            return OCRResponse(
                raw_text=extracted_text.strip(),
                language="en",
                processing_time_ms=processing_time
            )

        except Exception as e:
            logger.error(f"Tesseract extraction error: {str(e)}")
            raise