import enum
from datetime import datetime
from sqlalchemy import ForeignKey, String, Integer, Float, DateTime, Enum , func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base


# 1. Define the Enum for status tracking
class BookStatus(str, enum.Enum):
    to_read = "to_read"
    reading = "reading"
    completed = "completed"

class Book(Base):
    __tablename__ = "books"

    # Primary Key
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    # Core Book Details (Indexed for fast search)
    title: Mapped[str] = mapped_column(String, index=True, nullable=False)
    author: Mapped[str] = mapped_column(String, index=True, nullable=False)
    genre: Mapped[str] = mapped_column(String, index=True)
    total_pages: Mapped[int] = mapped_column(Integer)
    published_year: Mapped[int] = mapped_column(Integer)
    isbn: Mapped[str] = mapped_column(String, unique=True, index=True)


    # Status & Tracking
    status: Mapped[BookStatus] = mapped_column(
        Enum(BookStatus),
        default=BookStatus.to_read,
        nullable=False
    )

    # Ratings (Optional until completed)
    rating: Mapped[float | None] = mapped_column(Float, nullable=True)
    review: Mapped[str | None] = mapped_column(String(500), nullable=True)

    # Timestamps for Reading Tracking
    started_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    finished_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    notes = relationship("Note", back_populates="book", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Book {self.title} by {self.author}>"


class Note(Base):
    __tablename__ = "book_notes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    book_id : Mapped[int] = mapped_column(ForeignKey("books.id", ondelete="CASCADE"))
    content : Mapped[str] = mapped_column(String(1000))
    created_at : Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    # Relationship back to book
    book = relationship("Book", back_populates="notes")
