"""
Repository layer for storing and querying digitized book data in PostgreSQL.
"""

import logging
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from digitize.config.settings import DatabaseConfig
from digitize.storage.models import Base, Book, Page, Passage, Theme
from digitize.ai_processor.gpt_processor import ProcessedText

logger = logging.getLogger(__name__)


class BookRepository:
    """Handles all database operations for the digitization pipeline."""

    def __init__(self, config: DatabaseConfig | None = None):
        self.config = config or DatabaseConfig()
        self.engine = create_engine(self.config.connection_string, echo=False)
        self.SessionLocal = sessionmaker(bind=self.engine)

    def create_tables(self):
        """Create all database tables if they don't exist."""
        Base.metadata.create_all(self.engine)
        logger.info("Database tables created/verified.")

    @contextmanager
    def get_session(self):
        """Provide a transactional session scope."""
        session = self.SessionLocal()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def create_book(self, source_directory: str, processed_pages: list[ProcessedText]) -> int:
        """Create a new book record with all its pages, passages, and themes."""
        # Use the first non-empty page to get book-level metadata
        meta_page = next((p for p in processed_pages if p.title or p.cleaned_text), None)

        with self.get_session() as session:
            book = Book(
                title=meta_page.title if meta_page else None,
                author=meta_page.author if meta_page else None,
                genre=meta_page.genre if meta_page else None,
                detected_language=meta_page.detected_language if meta_page else None,
                language_code=meta_page.language_code if meta_page else None,
                estimated_period=meta_page.estimated_period if meta_page else None,
                source_directory=source_directory,
                total_pages=len(processed_pages),
            )
            session.add(book)
            session.flush()  # Get the book.id

            for processed in processed_pages:
                page = Page(
                    book_id=book.id,
                    page_number=processed.page_number,
                    source_file=processed.source_file,
                    chapter=processed.chapter,
                    raw_ocr_text=processed.original_ocr,
                    ocr_confidence=processed.ocr_confidence,
                    cleaned_text=processed.cleaned_text,
                    summary=processed.summary,
                    writing_style=processed.writing_style,
                    confidence_notes=processed.confidence_notes,
                )
                session.add(page)
                session.flush()

                # Add key passages
                for passage_text in processed.key_passages:
                    passage = Passage(
                        page_id=page.id,
                        text=passage_text,
                        passage_type="quote",
                    )
                    session.add(passage)

                # Add themes (get or create)
                for theme_name in processed.themes:
                    theme = (
                        session.query(Theme)
                        .filter(Theme.name == theme_name)
                        .first()
                    )
                    if not theme:
                        theme = Theme(name=theme_name)
                        session.add(theme)
                        session.flush()
                    page.themes.append(theme)

            logger.info(f"Saved book '{book.title}' (id={book.id}) with {len(processed_pages)} pages")
            return book.id

    def get_book(self, book_id: int) -> Book | None:
        with self.get_session() as session:
            return session.query(Book).filter(Book.id == book_id).first()

    def list_books(self) -> list[dict]:
        with self.get_session() as session:
            books = session.query(Book).order_by(Book.created_at.desc()).all()
            return [
                {
                    "id": b.id,
                    "title": b.title,
                    "author": b.author,
                    "genre": b.genre,
                    "language": b.detected_language,
                    "pages": b.total_pages,
                    "created_at": str(b.created_at),
                }
                for b in books
            ]

    def get_book_pages(self, book_id: int) -> list[dict]:
        with self.get_session() as session:
            pages = (
                session.query(Page)
                .filter(Page.book_id == book_id)
                .order_by(Page.page_number)
                .all()
            )
            return [
                {
                    "page_number": p.page_number,
                    "chapter": p.chapter,
                    "cleaned_text": p.cleaned_text,
                    "summary": p.summary,
                    "ocr_confidence": p.ocr_confidence,
                    "themes": [t.name for t in p.themes],
                    "passages": [ps.text for ps in p.passages],
                }
                for p in pages
            ]

    def search_text(self, query: str) -> list[dict]:
        """Full-text search across all cleaned page text."""
        with self.get_session() as session:
            pages = (
                session.query(Page)
                .filter(Page.cleaned_text.ilike(f"%{query}%"))
                .all()
            )
            return [
                {
                    "book_id": p.book_id,
                    "book_title": p.book.title if p.book else None,
                    "page_number": p.page_number,
                    "chapter": p.chapter,
                    "snippet": self._extract_snippet(p.cleaned_text, query),
                }
                for p in pages
            ]

    def get_all_themes(self) -> list[dict]:
        with self.get_session() as session:
            themes = session.query(Theme).all()
            return [
                {"id": t.id, "name": t.name, "page_count": len(t.pages)}
                for t in themes
            ]

    def get_pages_by_theme(self, theme_name: str) -> list[dict]:
        with self.get_session() as session:
            theme = session.query(Theme).filter(Theme.name == theme_name).first()
            if not theme:
                return []
            return [
                {
                    "book_id": p.book_id,
                    "book_title": p.book.title if p.book else None,
                    "page_number": p.page_number,
                    "summary": p.summary,
                }
                for p in theme.pages
            ]

    @staticmethod
    def _extract_snippet(text: str, query: str, context_chars: int = 150) -> str:
        """Extract a snippet around the query match."""
        if not text:
            return ""
        lower_text = text.lower()
        idx = lower_text.find(query.lower())
        if idx == -1:
            return text[:context_chars * 2] + "..."
        start = max(0, idx - context_chars)
        end = min(len(text), idx + len(query) + context_chars)
        snippet = text[start:end]
        if start > 0:
            snippet = "..." + snippet
        if end < len(text):
            snippet = snippet + "..."
        return snippet
