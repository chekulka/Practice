"""
Main pipeline orchestrator.

Flow: Scan Directory -> OCR -> GPT Processing -> PostgreSQL Storage

Usage:
    from digitize.pipeline.orchestrator import DigitizationPipeline
    from digitize.config.settings import PipelineConfig

    config = PipelineConfig()
    pipeline = DigitizationPipeline(config)
    pipeline.setup()
    book_id = pipeline.run("/path/to/scanned/book/images")
"""

import logging
from pathlib import Path

from digitize.config.settings import PipelineConfig
from digitize.ocr.extractor import BookOCR
from digitize.ai_processor.gpt_processor import GPTProcessor
from digitize.storage.repository import BookRepository

logger = logging.getLogger(__name__)


class DigitizationPipeline:
    """Orchestrates the full digitization pipeline: OCR -> GPT -> Postgres."""

    def __init__(self, config: PipelineConfig | None = None):
        self.config = config or PipelineConfig()
        self.ocr = BookOCR(self.config.ocr)
        self.processor = GPTProcessor(self.config.openai)
        self.repository = BookRepository(self.config.db)

    def setup(self):
        """Initialize database tables."""
        self.repository.create_tables()
        logger.info("Pipeline setup complete.")

    def run(self, source_path: str) -> int:
        """
        Run the full digitization pipeline on a file or directory.

        Args:
            source_path: Path to a single file or a directory of scanned pages.

        Returns:
            The database ID of the created book record.
        """
        path = Path(source_path)

        # Step 1: OCR — extract raw text from scans
        logger.info(f"[1/3] Running OCR on: {source_path}")
        if path.is_dir():
            ocr_results = self.ocr.process_directory(source_path)
        elif path.is_file():
            ocr_results = self.ocr.process_file(source_path)
        else:
            raise FileNotFoundError(f"Source not found: {source_path}")

        if not ocr_results:
            raise ValueError(f"No text could be extracted from: {source_path}")

        logger.info(f"  OCR complete: {len(ocr_results)} pages extracted")

        # Step 2: GPT — clean, understand, and structure the text
        logger.info(f"[2/3] Processing {len(ocr_results)} pages with GPT...")
        processed_pages = self.processor.process_batch(ocr_results)
        logger.info(f"  GPT processing complete: {len(processed_pages)} pages analyzed")

        # Step 3: Store in PostgreSQL
        logger.info("[3/3] Storing results in PostgreSQL...")
        book_id = self.repository.create_book(
            source_directory=source_path,
            processed_pages=processed_pages,
        )
        logger.info(f"  Stored as book ID: {book_id}")

        return book_id

    def run_batch(self, directories: list[str]) -> list[int]:
        """Run the pipeline on multiple book directories."""
        book_ids = []
        for i, directory in enumerate(directories, start=1):
            logger.info(f"\n{'='*60}")
            logger.info(f"Processing book {i}/{len(directories)}: {directory}")
            logger.info(f"{'='*60}")
            try:
                book_id = self.run(directory)
                book_ids.append(book_id)
            except Exception as e:
                logger.error(f"Failed to process {directory}: {e}")
        return book_ids
