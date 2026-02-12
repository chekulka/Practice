"""
OCR module for extracting text from scanned book pages.

Uses Tesseract OCR with image preprocessing for better accuracy.
Supports: PNG, JPG, TIFF, BMP, and multi-page PDF files.
"""

import os
import logging
from pathlib import Path
from dataclasses import dataclass

import cv2
import numpy as np
import pytesseract
from PIL import Image
from pdf2image import convert_from_path

from digitize.config.settings import OCRConfig

logger = logging.getLogger(__name__)


@dataclass
class OCRResult:
    file_path: str
    page_number: int
    raw_text: str
    confidence: float
    language: str


class BookOCR:
    """Extracts text from scanned book pages using Tesseract OCR."""

    def __init__(self, config: OCRConfig | None = None):
        self.config = config or OCRConfig()

    def preprocess_image(self, image: np.ndarray) -> np.ndarray:
        """Apply preprocessing to improve OCR accuracy on book scans."""
        # Convert to grayscale
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image

        # Denoise
        denoised = cv2.fastNlMeansDenoising(gray, h=10)

        # Adaptive thresholding for uneven lighting (common in book scans)
        binary = cv2.adaptiveThreshold(
            denoised, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 15, 11
        )

        # Deskew — straighten rotated text
        coords = np.column_stack(np.where(binary < 128))
        if len(coords) > 100:
            angle = cv2.minAreaRect(coords)[-1]
            if angle < -45:
                angle = 90 + angle
            if abs(angle) > 0.5:
                h, w = binary.shape
                center = (w // 2, h // 2)
                matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
                binary = cv2.warpAffine(
                    binary, matrix, (w, h),
                    flags=cv2.INTER_CUBIC,
                    borderMode=cv2.BORDER_REPLICATE,
                )

        return binary

    def extract_from_image(self, image_path: str, page_number: int = 1) -> OCRResult:
        """Extract text from a single image file."""
        logger.info(f"Processing image: {image_path}")

        image = cv2.imread(image_path)
        if image is None:
            raise ValueError(f"Could not read image: {image_path}")

        if self.config.preprocessing:
            image = self.preprocess_image(image)

        # Run OCR with detailed output for confidence
        ocr_data = pytesseract.image_to_data(
            image, lang=self.config.tesseract_lang, output_type=pytesseract.Output.DICT
        )

        # Extract text
        text = pytesseract.image_to_string(image, lang=self.config.tesseract_lang)

        # Calculate average confidence (excluding -1 entries which are non-text)
        confidences = [
            int(c) for c in ocr_data["conf"] if int(c) > 0
        ]
        avg_confidence = sum(confidences) / len(confidences) if confidences else 0.0

        return OCRResult(
            file_path=image_path,
            page_number=page_number,
            raw_text=text.strip(),
            confidence=round(avg_confidence, 2),
            language=self.config.tesseract_lang,
        )

    def extract_from_pdf(self, pdf_path: str) -> list[OCRResult]:
        """Extract text from all pages of a PDF file."""
        logger.info(f"Processing PDF: {pdf_path}")

        pages = convert_from_path(pdf_path, dpi=self.config.dpi)
        results = []

        for i, page_image in enumerate(pages, start=1):
            # Convert PIL Image to numpy array for OpenCV
            image_np = np.array(page_image)
            image_bgr = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)

            if self.config.preprocessing:
                processed = self.preprocess_image(image_bgr)
            else:
                processed = image_bgr

            text = pytesseract.image_to_string(
                processed, lang=self.config.tesseract_lang
            )

            ocr_data = pytesseract.image_to_data(
                processed,
                lang=self.config.tesseract_lang,
                output_type=pytesseract.Output.DICT,
            )
            confidences = [int(c) for c in ocr_data["conf"] if int(c) > 0]
            avg_confidence = sum(confidences) / len(confidences) if confidences else 0.0

            results.append(
                OCRResult(
                    file_path=pdf_path,
                    page_number=i,
                    raw_text=text.strip(),
                    confidence=round(avg_confidence, 2),
                    language=self.config.tesseract_lang,
                )
            )
            logger.info(f"  Page {i}/{len(pages)} done (confidence: {avg_confidence:.1f}%)")

        return results

    def process_file(self, file_path: str) -> list[OCRResult]:
        """Process a single file (image or PDF) and return OCR results."""
        ext = Path(file_path).suffix.lower()

        if ext not in self.config.supported_formats:
            raise ValueError(
                f"Unsupported format '{ext}'. Supported: {self.config.supported_formats}"
            )

        if ext == ".pdf":
            return self.extract_from_pdf(file_path)
        else:
            return [self.extract_from_image(file_path)]

    def process_directory(self, directory: str) -> list[OCRResult]:
        """Process all supported files in a directory."""
        dir_path = Path(directory)
        if not dir_path.is_dir():
            raise ValueError(f"Directory not found: {directory}")

        all_results = []
        files = sorted(
            f
            for f in dir_path.iterdir()
            if f.suffix.lower() in self.config.supported_formats
        )

        logger.info(f"Found {len(files)} files to process in {directory}")

        for file in files:
            try:
                results = self.process_file(str(file))
                all_results.extend(results)
            except Exception as e:
                logger.error(f"Failed to process {file}: {e}")

        return all_results
