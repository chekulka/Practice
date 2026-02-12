"""
Configuration settings for the book digitization pipeline.
"""

import os
from dataclasses import dataclass, field
from dotenv import load_dotenv

load_dotenv()


@dataclass
class DatabaseConfig:
    host: str = os.getenv("POSTGRES_HOST", "localhost")
    port: int = int(os.getenv("POSTGRES_PORT", "5432"))
    database: str = os.getenv("POSTGRES_DB", "book_digitizer")
    user: str = os.getenv("POSTGRES_USER", "postgres")
    password: str = os.getenv("POSTGRES_PASSWORD", "")

    @property
    def connection_string(self) -> str:
        return f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"


@dataclass
class OpenAIConfig:
    api_key: str = os.getenv("OPENAI_API_KEY", "")
    model: str = os.getenv("OPENAI_MODEL", "gpt-4o")
    max_tokens: int = int(os.getenv("OPENAI_MAX_TOKENS", "4096"))
    temperature: float = float(os.getenv("OPENAI_TEMPERATURE", "0.2"))


@dataclass
class OCRConfig:
    tesseract_lang: str = os.getenv("TESSERACT_LANG", "eng")
    preprocessing: bool = True
    dpi: int = int(os.getenv("OCR_DPI", "300"))
    supported_formats: list[str] = field(
        default_factory=lambda: [".png", ".jpg", ".jpeg", ".tiff", ".bmp", ".pdf"]
    )


@dataclass
class PipelineConfig:
    db: DatabaseConfig = field(default_factory=DatabaseConfig)
    openai: OpenAIConfig = field(default_factory=OpenAIConfig)
    ocr: OCRConfig = field(default_factory=OCRConfig)
    batch_size: int = int(os.getenv("BATCH_SIZE", "10"))
    scan_directory: str = os.getenv("SCAN_DIRECTORY", "./scans")
