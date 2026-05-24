from click import option
from fastapi import APIRouter, Depends, HTTPException, Query, Path, status
from sqlalchemy.orm import Session
from typing import List, Literal, Optional
from app.core.database import get_db
from app.schemas.book import (
    BookCreate, BookResponse, BookUpdate, BookStatusUpdate, BookRatingUpdate, NoteCreate, NoteResponse, PaginatedBookResponse, 
)
from app.crud import book as crud_book

router = APIRouter(prefix="/books", tags=["Books Management"])

@router.post("/", response_model=BookResponse, status_code=status.HTTP_201_CREATED,  summary="Add a new book")
def add_book(book_in:BookCreate, db:Session = Depends(get_db)):
    """Add a new book to the collection."""
    return crud_book.create_book(db, book_in)

@router.patch("/{book_id}",response_model=BookResponse, summary="Update book details")
def update_book_details(
    book_id:int,
    book_in: BookUpdate,
    db : Session = Depends(get_db)
):
    """
    Allows partial updates to a book's metadata (title, author, etc.).
    Only the fields provided in the request body will be updated.
    """
    db_book = crud_book.update_book(db, book_id, book_in)
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book

@router.get("/", response_model=PaginatedBookResponse, summary="List all books")
def list_books(
    db:Session = Depends(get_db),
    page: int = Query(1, ge=1),
    limit:int = Query(10, ge=1, le=100),
    status: Optional[str] = Query(None, description="Filter by status (to_read, reading, completed)"),
    genre:Optional[str] = None,
    min_rating: Optional[float] = Query(None, ge=1, le=5),
    # sort_by: str = Query("created_at", regex="^(created_at|rating|title)$"),
    # order: str = Query("desc", regex="^(asc|desc)$")
    # Using Literal creates a dropdown in Swagger!
    sort_by: Literal["created_at", "rating", "title"] = "created_at",
    order: Literal["asc", "desc"] = "desc"
):
    """Get a paginated list of books with advanced filtering and sorting."""
    skip = (page - 1)*limit
    total, books = crud_book.get_books(db, skip, limit, status,genre, min_rating, sort_by, order)
    return {"total": total, "page":page, "limit":limit, "books":books}

@router.get("/search", response_model=List[BookResponse], summary="Search book by title or author")
def search_books(q:str = Query(...,min_length=1), db:Session = Depends(get_db)):
    """Search for books by title or author (case-insensitive)."""
    return crud_book.search_books(db, q)

@router.get("/{id}", response_model=BookResponse, summary="Get Single Book")
def get_book(id:int = Path(..., title="The ID of the book to get"), db:Session = Depends(get_db)):
    """Retrieve a single book by its unique ID."""
    db_book = crud_book.get_book_by_id(db, id)
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book

@router.patch("/{id}/status", response_model=BookResponse, summary="Update book's reading status")
def update_reading_status(id:int, status_in: BookStatusUpdate, db:Session=Depends(get_db)):
    """Update reading status. Automatically sets started_at/finished_at timestamps."""
    db_book = crud_book.update_book_status(db, id, status_in)
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book

@router.post("/{id}/rate", response_model=BookResponse, summary="Rate and Review the book")
def rate_and_review(id:int, rating_in:BookRatingUpdate, db:Session = Depends(get_db)):
    """Submit a rating (1-5) and a review. Only allowed if status is 'completed'."""
    return crud_book.add_rating(db, id, rating_in)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete book")
def remove_book(id:int, db:Session = Depends(get_db)):
    """Permanently delete a book from the collection."""
    success = crud_book.delete_book(db, id)
    if not success:
        raise HTTPException(status_code=404, detail="Book not found")
    return None

@router.post("/{book_id}/notes", response_model=NoteResponse)
def create_note_for_book(
    book_id: int,
    note_in: NoteCreate,
    db: Session = Depends(get_db)
):
    """Add a timestamped note to a specific book."""
    db_book = crud_book.get_book_by_id(db, book_id)
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    return crud_book.add_note(db, book_id, note_in)


@router.get("/{book_id}/notes", response_model = List[NoteResponse], summary="Get all notes for a book")
def list_book_notes(book_id:int, db:Session = Depends(get_db)):
    """Retrieve all timestamped notes for a specific book."""
    db_book = crud_book.get_book_by_id(db, book_id)
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    return crud_book.get_book_notes(db, book_id)