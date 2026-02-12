"""
CLI entry point for the book digitization pipeline.

Usage:
    # Digitize a single file
    python -m digitize.main digitize --source /path/to/scan.pdf

    # Digitize a directory of scanned pages
    python -m digitize.main digitize --source /path/to/book_scans/

    # List all digitized books
    python -m digitize.main list

    # Search across all digitized text
    python -m digitize.main search --query "to be or not to be"

    # View pages of a specific book
    python -m digitize.main pages --book-id 1

    # List all discovered themes
    python -m digitize.main themes

    # Initialize the database (run once)
    python -m digitize.main init
"""

import argparse
import json
import logging
import sys

from digitize.config.settings import PipelineConfig
from digitize.pipeline.orchestrator import DigitizationPipeline
from digitize.storage.repository import BookRepository


def setup_logging(verbose: bool = False):
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def cmd_init(config: PipelineConfig):
    """Initialize the database schema."""
    repo = BookRepository(config.db)
    repo.create_tables()
    print("Database initialized successfully.")


def cmd_digitize(config: PipelineConfig, source: str):
    """Run the full digitization pipeline."""
    pipeline = DigitizationPipeline(config)
    pipeline.setup()
    book_id = pipeline.run(source)
    print(f"\nDigitization complete. Book saved with ID: {book_id}")


def cmd_list_books(config: PipelineConfig):
    """List all digitized books."""
    repo = BookRepository(config.db)
    books = repo.list_books()
    if not books:
        print("No books found.")
        return
    print(f"\n{'ID':<5} {'Title':<40} {'Author':<25} {'Lang':<10} {'Pages':<6}")
    print("-" * 90)
    for b in books:
        print(
            f"{b['id']:<5} {(b['title'] or 'Untitled'):<40} "
            f"{(b['author'] or 'Unknown'):<25} "
            f"{(b['language'] or '?'):<10} {b['pages']:<6}"
        )


def cmd_pages(config: PipelineConfig, book_id: int):
    """View pages of a specific book."""
    repo = BookRepository(config.db)
    pages = repo.get_book_pages(book_id)
    if not pages:
        print(f"No pages found for book ID {book_id}.")
        return
    for p in pages:
        print(f"\n--- Page {p['page_number']} ---")
        if p["chapter"]:
            print(f"Chapter: {p['chapter']}")
        if p["themes"]:
            print(f"Themes: {', '.join(p['themes'])}")
        if p["summary"]:
            print(f"Summary: {p['summary']}")
        print(f"\n{p['cleaned_text'][:500]}...")


def cmd_search(config: PipelineConfig, query: str):
    """Search across all digitized text."""
    repo = BookRepository(config.db)
    results = repo.search_text(query)
    if not results:
        print(f"No results for: '{query}'")
        return
    print(f"\nFound {len(results)} result(s) for '{query}':\n")
    for r in results:
        print(f"  Book: {r['book_title'] or 'Untitled'} (ID: {r['book_id']}), Page {r['page_number']}")
        if r["chapter"]:
            print(f"  Chapter: {r['chapter']}")
        print(f"  ...{r['snippet']}...")
        print()


def cmd_themes(config: PipelineConfig):
    """List all discovered themes."""
    repo = BookRepository(config.db)
    themes = repo.get_all_themes()
    if not themes:
        print("No themes found.")
        return
    print(f"\n{'Theme':<40} {'Pages':<6}")
    print("-" * 50)
    for t in themes:
        print(f"{t['name']:<40} {t['page_count']:<6}")


def main():
    parser = argparse.ArgumentParser(
        description="Digitize physical book collections: OCR -> GPT -> PostgreSQL"
    )
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable debug logging")

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # init
    subparsers.add_parser("init", help="Initialize the database schema")

    # digitize
    p_digitize = subparsers.add_parser("digitize", help="Digitize scanned book pages")
    p_digitize.add_argument("--source", "-s", required=True, help="Path to file or directory of scans")

    # list
    subparsers.add_parser("list", help="List all digitized books")

    # pages
    p_pages = subparsers.add_parser("pages", help="View pages of a book")
    p_pages.add_argument("--book-id", "-b", type=int, required=True, help="Book ID")

    # search
    p_search = subparsers.add_parser("search", help="Search across all digitized text")
    p_search.add_argument("--query", "-q", required=True, help="Search query")

    # themes
    subparsers.add_parser("themes", help="List all discovered themes")

    args = parser.parse_args()
    setup_logging(args.verbose)

    if not args.command:
        parser.print_help()
        sys.exit(1)

    config = PipelineConfig()

    commands = {
        "init": lambda: cmd_init(config),
        "digitize": lambda: cmd_digitize(config, args.source),
        "list": lambda: cmd_list_books(config),
        "pages": lambda: cmd_pages(config, args.book_id),
        "search": lambda: cmd_search(config, args.query),
        "themes": lambda: cmd_themes(config),
    }

    commands[args.command]()


if __name__ == "__main__":
    main()
