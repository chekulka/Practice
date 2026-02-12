"""
AI processing module using OpenAI GPT to read, understand, and structure
raw OCR text from digitized book pages.

Responsibilities:
- Clean up OCR artifacts and formatting errors
- Detect the language of the text
- Extract structured metadata (title, author, chapter, genre, themes)
- Generate summaries
- Identify key passages and quotes
"""

import json
import logging
from dataclasses import dataclass, field

from openai import OpenAI

from digitize.config.settings import OpenAIConfig
from digitize.ocr.extractor import OCRResult

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """You are a literary scholar and expert text analyst. You receive raw OCR text
extracted from scanned physical books. Your job is to:

1. CLEAN the text: fix OCR errors, broken words, garbled characters, and formatting issues.
   Preserve the original language — do NOT translate.
2. DETECT the language of the writing.
3. EXTRACT metadata: identify title, author (if visible), chapter/section info, and genre.
4. IDENTIFY key themes, literary devices, and notable passages.
5. GENERATE a concise summary of the content.

Always respond in valid JSON with this exact structure:
{
  "cleaned_text": "the corrected full text preserving original language",
  "detected_language": "language name (e.g., English, Arabic, Russian, Japanese)",
  "language_code": "ISO 639-1 code (e.g., en, ar, ru, ja)",
  "metadata": {
    "title": "detected or null",
    "author": "detected or null",
    "chapter": "detected chapter/section name or null",
    "genre": "detected genre or null",
    "estimated_period": "estimated time period of writing or null"
  },
  "themes": ["theme1", "theme2"],
  "key_passages": ["notable quote or passage 1", "notable quote or passage 2"],
  "summary": "a concise summary of the content",
  "writing_style": "description of the writing style",
  "confidence_notes": "any issues or uncertainties about the OCR quality or interpretation"
}"""


@dataclass
class ProcessedText:
    original_ocr: str
    cleaned_text: str
    detected_language: str
    language_code: str
    title: str | None
    author: str | None
    chapter: str | None
    genre: str | None
    estimated_period: str | None
    themes: list[str]
    key_passages: list[str]
    summary: str
    writing_style: str
    confidence_notes: str
    ocr_confidence: float
    source_file: str
    page_number: int


class GPTProcessor:
    """Uses OpenAI GPT to read, understand, and structure OCR-extracted text."""

    def __init__(self, config: OpenAIConfig | None = None):
        self.config = config or OpenAIConfig()
        self.client = OpenAI(api_key=self.config.api_key)

    def process_text(self, ocr_result: OCRResult) -> ProcessedText:
        """Send OCR text to GPT for cleaning, understanding, and structuring."""
        if not ocr_result.raw_text.strip():
            logger.warning(f"Empty OCR text for {ocr_result.file_path} page {ocr_result.page_number}")
            return self._empty_result(ocr_result)

        logger.info(
            f"Processing with GPT: {ocr_result.file_path} page {ocr_result.page_number} "
            f"({len(ocr_result.raw_text)} chars)"
        )

        user_message = (
            f"Here is raw OCR text extracted from a scanned book page "
            f"(OCR confidence: {ocr_result.confidence}%):\n\n"
            f"---\n{ocr_result.raw_text}\n---\n\n"
            f"Please clean, analyze, and structure this text."
        )

        response = self.client.chat.completions.create(
            model=self.config.model,
            temperature=self.config.temperature,
            max_tokens=self.config.max_tokens,
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message},
            ],
        )

        raw_response = response.choices[0].message.content
        data = json.loads(raw_response)

        metadata = data.get("metadata", {})

        return ProcessedText(
            original_ocr=ocr_result.raw_text,
            cleaned_text=data.get("cleaned_text", ocr_result.raw_text),
            detected_language=data.get("detected_language", "Unknown"),
            language_code=data.get("language_code", "und"),
            title=metadata.get("title"),
            author=metadata.get("author"),
            chapter=metadata.get("chapter"),
            genre=metadata.get("genre"),
            estimated_period=metadata.get("estimated_period"),
            themes=data.get("themes", []),
            key_passages=data.get("key_passages", []),
            summary=data.get("summary", ""),
            writing_style=data.get("writing_style", ""),
            confidence_notes=data.get("confidence_notes", ""),
            ocr_confidence=ocr_result.confidence,
            source_file=ocr_result.file_path,
            page_number=ocr_result.page_number,
        )

    def process_batch(self, ocr_results: list[OCRResult]) -> list[ProcessedText]:
        """Process multiple OCR results through GPT."""
        processed = []
        for i, result in enumerate(ocr_results, start=1):
            logger.info(f"GPT processing {i}/{len(ocr_results)}")
            try:
                processed.append(self.process_text(result))
            except Exception as e:
                logger.error(f"GPT processing failed for {result.file_path} p{result.page_number}: {e}")
                processed.append(self._empty_result(result, error=str(e)))
        return processed

    def _empty_result(self, ocr_result: OCRResult, error: str = "") -> ProcessedText:
        return ProcessedText(
            original_ocr=ocr_result.raw_text,
            cleaned_text="",
            detected_language="Unknown",
            language_code="und",
            title=None,
            author=None,
            chapter=None,
            genre=None,
            estimated_period=None,
            themes=[],
            key_passages=[],
            summary="",
            writing_style="",
            confidence_notes=error or "Empty or unreadable OCR text",
            ocr_confidence=ocr_result.confidence,
            source_file=ocr_result.file_path,
            page_number=ocr_result.page_number,
        )
