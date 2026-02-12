"""
SQLAlchemy models for the book digitization database.

Schema:
- books: top-level collection (a physical book)
- pages: individual scanned pages belonging to a book
- passages: notable passages/quotes extracted from pages
- themes: unique themes with many-to-many relation to pages
"""

from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Float,
    DateTime,
    ForeignKey,
    Table,
    UniqueConstraint,
    create_engine,
)
from sqlalchemy.orm import DeclarativeBase, relationship, Session


class Base(DeclarativeBase):
    pass


# Many-to-many: pages <-> themes
page_themes = Table(
    "page_themes",
    Base.metadata,
    Column("page_id", Integer, ForeignKey("pages.id", ondelete="CASCADE"), primary_key=True),
    Column("theme_id", Integer, ForeignKey("themes.id", ondelete="CASCADE"), primary_key=True),
)


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(500), nullable=True)
    author = Column(String(300), nullable=True)
    genre = Column(String(200), nullable=True)
    detected_language = Column(String(100), nullable=True)
    language_code = Column(String(10), nullable=True)
    estimated_period = Column(String(200), nullable=True)
    source_directory = Column(String(1000), nullable=False)
    total_pages = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    pages = relationship("Page", back_populates="book", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Book(id={self.id}, title='{self.title}', author='{self.author}')>"


class Page(Base):
    __tablename__ = "pages"
    __table_args__ = (
        UniqueConstraint("book_id", "page_number", name="uq_book_page"),
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    book_id = Column(Integer, ForeignKey("books.id", ondelete="CASCADE"), nullable=False)
    page_number = Column(Integer, nullable=False)
    source_file = Column(String(1000), nullable=False)
    chapter = Column(String(500), nullable=True)

    # OCR data
    raw_ocr_text = Column(Text, nullable=True)
    ocr_confidence = Column(Float, nullable=True)

    # GPT-processed data
    cleaned_text = Column(Text, nullable=True)
    summary = Column(Text, nullable=True)
    writing_style = Column(String(500), nullable=True)
    confidence_notes = Column(Text, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)

    book = relationship("Book", back_populates="pages")
    passages = relationship("Passage", back_populates="page", cascade="all, delete-orphan")
    themes = relationship("Theme", secondary=page_themes, back_populates="pages")

    def __repr__(self):
        return f"<Page(id={self.id}, book_id={self.book_id}, page={self.page_number})>"


class Passage(Base):
    __tablename__ = "passages"

    id = Column(Integer, primary_key=True, autoincrement=True)
    page_id = Column(Integer, ForeignKey("pages.id", ondelete="CASCADE"), nullable=False)
    text = Column(Text, nullable=False)
    passage_type = Column(String(100), default="quote")  # quote, excerpt, highlight
    created_at = Column(DateTime, default=datetime.utcnow)

    page = relationship("Page", back_populates="passages")

    def __repr__(self):
        return f"<Passage(id={self.id}, page_id={self.page_id}, type='{self.passage_type}')>"


class Theme(Base):
    __tablename__ = "themes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(300), unique=True, nullable=False)

    pages = relationship("Page", secondary=page_themes, back_populates="themes")

    def __repr__(self):
        return f"<Theme(id={self.id}, name='{self.name}')>"


def init_db(connection_string: str):
    """Create all tables in the database."""
    engine = create_engine(connection_string)
    Base.metadata.create_all(engine)
    return engine
