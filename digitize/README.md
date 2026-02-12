# Book Digitization Pipeline

Digitize physical writing collections from books: **Scan → OCR → GPT → PostgreSQL**

## Architecture

```
┌─────────────┐     ┌──────────────┐     ┌──────────────┐     ┌────────────┐
│  Book Scans │────>│  OCR Engine  │────>│  GPT Process │────>│ PostgreSQL │
│  (images/   │     │  (Tesseract) │     │  (OpenAI)    │     │  Database  │
│   PDFs)     │     │              │     │              │     │            │
└─────────────┘     └──────────────┘     └──────────────┘     └────────────┘
  .jpg .png          Raw text +           Cleaned text,        Books, Pages,
  .tiff .pdf         confidence           metadata,            Passages,
                                          themes, summaries    Themes
```

## What It Does

1. **OCR** — Extracts raw text from scanned book pages using Tesseract with image preprocessing (denoising, deskewing, adaptive thresholding)
2. **GPT** — Sends raw OCR text to OpenAI GPT to:
   - Clean OCR artifacts and fix formatting
   - Detect the language (supports any language)
   - Extract metadata (title, author, chapter, genre, time period)
   - Identify themes and key passages
   - Generate summaries and describe writing style
3. **PostgreSQL** — Stores everything in a structured relational schema for querying, searching, and browsing

## Project Structure

```
digitize/
├── config/
│   ├── __init__.py
│   └── settings.py          # Dataclass-based config loaded from .env
├── ocr/
│   ├── __init__.py
│   └── extractor.py         # Tesseract OCR with image preprocessing
├── ai_processor/
│   ├── __init__.py
│   └── gpt_processor.py     # GPT text cleaning, analysis, structuring
├── storage/
│   ├── __init__.py
│   ├── models.py            # SQLAlchemy ORM models (books, pages, passages, themes)
│   └── repository.py        # CRUD operations, search, theme queries
├── pipeline/
│   ├── __init__.py
│   └── orchestrator.py      # Ties OCR → GPT → Postgres into pipeline.run()
├── __init__.py
├── main.py                  # CLI entry point (init, digitize, list, pages, search, themes)
├── requirements.txt         # Python dependencies
├── .env.example             # Environment variable template
├── docker-compose.yml       # PostgreSQL via Docker
└── README.md                # This file
```

## Modules

| Module | File | Purpose |
|--------|------|---------|
| **OCR** | `ocr/extractor.py` | Tesseract OCR with image preprocessing (denoise, deskew, adaptive threshold). Handles PNG, JPG, TIFF, BMP, multi-page PDF |
| **AI Processor** | `ai_processor/gpt_processor.py` | Sends raw OCR text to GPT to: clean artifacts, detect language, extract metadata (title/author/chapter/genre), identify themes & key passages, generate summaries |
| **Storage Models** | `storage/models.py` | SQLAlchemy schema — `books`, `pages`, `passages`, `themes` tables with relationships |
| **Storage Repository** | `storage/repository.py` | CRUD operations + full-text search + theme queries |
| **Pipeline** | `pipeline/orchestrator.py` | Ties OCR → GPT → Postgres into a single `pipeline.run()` call |
| **CLI** | `main.py` | Commands: `init`, `digitize`, `list`, `pages`, `search`, `themes` |
| **Config** | `config/settings.py` | Dataclass-based config loaded from `.env` |

## Setup

### Prerequisites

- Python 3.11+
- Tesseract OCR installed (`apt install tesseract-ocr` or `brew install tesseract`)
- PostgreSQL (or use the included docker-compose)
- OpenAI API key

### Install

```bash
cd digitize
pip install -r requirements.txt

# For additional language packs (e.g., Arabic, Russian):
# apt install tesseract-ocr-ara tesseract-ocr-rus
```

### Configure

```bash
cp .env.example .env
# Edit .env with your PostgreSQL credentials and OpenAI API key
```

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `POSTGRES_HOST` | `localhost` | PostgreSQL host |
| `POSTGRES_PORT` | `5432` | PostgreSQL port |
| `POSTGRES_DB` | `book_digitizer` | Database name |
| `POSTGRES_USER` | `postgres` | Database user |
| `POSTGRES_PASSWORD` | — | Database password |
| `OPENAI_API_KEY` | — | Your OpenAI API key |
| `OPENAI_MODEL` | `gpt-4o` | GPT model to use |
| `OPENAI_MAX_TOKENS` | `4096` | Max tokens per GPT response |
| `OPENAI_TEMPERATURE` | `0.2` | GPT temperature (lower = more deterministic) |
| `TESSERACT_LANG` | `eng` | Tesseract language pack(s) |
| `OCR_DPI` | `300` | DPI for PDF-to-image conversion |
| `BATCH_SIZE` | `10` | Processing batch size |
| `SCAN_DIRECTORY` | `./scans` | Default scan input directory |

### Start PostgreSQL (Docker)

```bash
docker compose up -d
```

### Initialize Database

```bash
python -m digitize.main init
```

## Usage

### Digitize a book

```bash
# From a directory of scanned page images
python -m digitize.main digitize --source /path/to/book_scans/

# From a single PDF
python -m digitize.main digitize --source /path/to/book.pdf
```

### Browse and search

```bash
# List all digitized books
python -m digitize.main list

# View pages of a specific book
python -m digitize.main pages --book-id 1

# Full-text search across all books
python -m digitize.main search --query "love and war"

# List all discovered themes
python -m digitize.main themes
```

### Verbose mode

```bash
# Add -v for debug logging on any command
python -m digitize.main -v digitize --source /path/to/scans/
```

## Database Schema

| Table | Purpose |
|-------|---------|
| `books` | Top-level: title, author, genre, language, period |
| `pages` | Per-page: raw OCR, cleaned text, summary, style |
| `passages` | Notable quotes and excerpts per page |
| `themes` | Unique themes (many-to-many with pages) |
| `page_themes` | Join table linking pages to themes |

### Relationships

```
books 1───* pages 1───* passages
                  *───* themes
```

- A **book** has many **pages**
- A **page** has many **passages** (quotes, excerpts)
- A **page** has many **themes** (many-to-many via `page_themes`)

## OCR Preprocessing

The OCR module applies these steps to improve accuracy on book scans:

1. **Grayscale conversion** — removes color noise
2. **Denoising** — `cv2.fastNlMeansDenoising` to clean up scan artifacts
3. **Adaptive thresholding** — handles uneven lighting common in book photos
4. **Deskewing** — straightens rotated text using minimum area rectangle detection

Supported input formats: `.png`, `.jpg`, `.jpeg`, `.tiff`, `.bmp`, `.pdf`

## GPT Processing

For each page, GPT returns a structured JSON with:

| Field | Description |
|-------|-------------|
| `cleaned_text` | Full corrected text preserving original language |
| `detected_language` | Language name (e.g., English, Arabic, Russian) |
| `language_code` | ISO 639-1 code (e.g., `en`, `ar`, `ru`) |
| `metadata.title` | Detected book/chapter title |
| `metadata.author` | Detected author name |
| `metadata.chapter` | Chapter or section name |
| `metadata.genre` | Detected genre |
| `metadata.estimated_period` | Estimated time period of writing |
| `themes` | List of identified themes |
| `key_passages` | Notable quotes and passages |
| `summary` | Concise summary of the page content |
| `writing_style` | Description of the writing style |
| `confidence_notes` | Issues or uncertainties about OCR quality |

## Multi-Language Support

Set `TESSERACT_LANG` in `.env` for your books' language(s):

- English: `eng`
- Arabic: `ara`
- Russian: `rus`
- Japanese: `jpn`
- Chinese (Simplified): `chi_sim`
- French: `fra`
- German: `deu`
- Spanish: `spa`
- Multiple: `eng+ara+rus`

Install additional Tesseract language packs:

```bash
# Ubuntu/Debian
apt install tesseract-ocr-ara tesseract-ocr-rus tesseract-ocr-jpn

# macOS
brew install tesseract-lang
```

GPT will auto-detect the language and preserve the original text without translating.

## Programmatic Usage

```python
from digitize.config.settings import PipelineConfig
from digitize.pipeline.orchestrator import DigitizationPipeline

config = PipelineConfig()
pipeline = DigitizationPipeline(config)
pipeline.setup()

# Digitize a single book
book_id = pipeline.run("/path/to/scanned/book/images")

# Digitize multiple books
book_ids = pipeline.run_batch([
    "/path/to/book1/",
    "/path/to/book2/",
    "/path/to/book3.pdf",
])
```

## Dependencies

| Package | Purpose |
|---------|---------|
| `pytesseract` | Python wrapper for Tesseract OCR |
| `opencv-python` | Image preprocessing (denoise, threshold, deskew) |
| `Pillow` | Image loading and format handling |
| `pdf2image` | Convert PDF pages to images for OCR |
| `numpy` | Array operations for image processing |
| `openai` | OpenAI GPT API client |
| `sqlalchemy` | ORM for PostgreSQL database operations |
| `psycopg2-binary` | PostgreSQL driver |
| `python-dotenv` | Load environment variables from `.env` |
