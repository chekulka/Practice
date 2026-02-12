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

## Database Schema

| Table | Purpose |
|-------|---------|
| `books` | Top-level: title, author, genre, language, period |
| `pages` | Per-page: raw OCR, cleaned text, summary, style |
| `passages` | Notable quotes and excerpts per page |
| `themes` | Unique themes (many-to-many with pages) |

## Multi-Language Support

Set `TESSERACT_LANG` in `.env` for your books' language(s):

- English: `eng`
- Arabic: `ara`
- Russian: `rus`
- Japanese: `jpn`
- Multiple: `eng+ara+rus`

GPT will auto-detect the language and preserve the original text without translating.
