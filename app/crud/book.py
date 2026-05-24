from sqlalchemy.orm import Session
from sqlalchemy import select, func, or_
from app.models.book import Book, BookStatus, Note
from app.schemas.book import BookCreate, BookUpdate, BookStatusUpdate, BookRatingUpdate, NoteCreate
from fastapi import HTTPException, status
from datetime import datetime

# 1. CREATE
def create_book(db:Session, book_in:BookCreate):
    # Convert Pydantic model to SQLAlchemy Model
    db_book = Book(**book_in.model_dump())
    print(db_book)

    # Handle the "ISBN Unique" edge case
    existing = db.query(Book).filter(Book.isbn == db_book.isbn).first()

    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"A book with ISBN {db_book.isbn} already exists."
        )

    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

# 2. READ (Single)
def get_book_by_id(db: Session, book_id:int):
    return db.query(Book).filter(Book.id == book_id).first()

# 3. UPDATE book
def update_book(db:Session, book_id:int, book_in:BookUpdate):
    db_book = get_book_by_id(db, book_id)
    if not db_book:
        return None
    
    # It only updates fields the user actually sent.
    updated_data = book_in.model_dump(exclude_unset=True)

    for key,value in updated_data.items():
        setattr(db_book, key, value)
    
    db.commit()
    db.refresh(db_book)
    return db_book

# 3. READ (List with Filtering & Pagination)
def get_books(
    db: Session, 
    skip: int = 0, 
    limit: int = 10, 
    status: str = None, 
    genre: str = None, 
    min_rating: float = None,
    sort_by: str = "created_at",
    order: str = "desc"
):
    query = select(Book)

    # Apply Filters
    if status:
        query = query.where(Book.status == status)
    if genre:
        query = query.where(Book.genre.ilike(f"%{genre}%")) # Case-insensitive
    if min_rating:
        query = query.where(Book.rating >= min_rating)
    
    # Apply Sorting
    column = getattr(Book, sort_by, Book.created_at)
    if order == "desc":
        query = query.order_by(column.desc())
    else:
        query = query.order_by(column.asc())
    

    # Total count for pagination metadata
    total = db.scalar(select(func.count()).select_from(query.subquery()))

    # Execute with pagination
    result = db.execute(query.offset(skip).limit(limit))
    return total, result.scalars().all()
    
# 4. SEARCH (Title & Author)
def search_books(db:Session, q:str):
    query = select(Book).where(
        or_(
            Book.title.ilike(f"%{q}%"),
            Book.author.ilike(f"%{q}%")
        )
    )
    return db.execute(query).scalars().all()

# 5. UPDATE STATUS (Business Logic included)
def update_book_status(db:Session, book_id:int, status_update:BookStatusUpdate):
    db_book= get_book_by_id(db, book_id)
    if not db_book:
        return None

    new_status = status_update.status

    # BUSINESS RULE: Cannot mark completed without being in 'reading' first
    if new_status == BookStatus.completed and db_book.status != BookStatus.reading:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A book cannot be marked 'completed' without being in 'reading' status first."
        )
    
    # AUTO-TIMESTAMP
    if new_status == BookStatus.reading and not db_book.started_at:
        db_book.started_at = datetime.utcnow()

    if new_status == BookStatus.completed:
        db_book.finished_at = datetime.utcnow()
    
    db_book.status = new_status
    db.commit()
    db.refresh(db_book)
    return db_book

# 6. ADD RATING
def add_rating(db:Session, book_id:int, rating_in: BookRatingUpdate):
    db_book = get_book_by_id(db, book_id)
    if not db_book:
        return None
    
    # BUSINESS RULE: Only completed books can be rated
    if db_book.status != BookStatus.completed:
        raise HTTPException(
            status_code= status.HTTP_400_BAD_REQUEST,
            detail="You can only rate and review books that are marked as 'completed'."
        )
    
    db_book.rating = rating_in.rating
    db_book.review = rating_in.review
    db.commit()
    db.refresh(db_book)
    return db_book

# 7. DELETE
def delete_book(db:Session, book_id:int):
    db_book = get_book_by_id(db, book_id)
    if db_book:
        db.delete(db_book)
        db.commit()
        return True
    return False

def get_collection_stats(db:Session):
    total_books = db.query(Book).count()

    # Count by status
    status_counts = {
        status.value: db.query(Book).filter(Book.status == status).count()
        for status in BookStatus
    }

    # Avg Rating
    avg_rating = db.query(func.avg(Book.rating)).filter(Book.status == BookStatus.completed).scalar() or 0.0

    # Total Pages Read (Sum of total_pages for completed books only)
    total_pages= db.query(func.sum(Book.total_pages)).filter(Book.status==BookStatus.completed).scalar() or 0

    # Most read genre
    genre_query = db.query(Book.genre, func.count(Book.genre)).group_by(Book.genre).order_by(func.count(Book.genre).desc()).first()
    most_read_genre = genre_query[0] if genre_query else None

    return {
        "total_books":total_books,
        "status_counts": status_counts,
        "average_rating": round(float(avg_rating),2),
        "total_pages_read": int(total_pages),
        "most_read_genre":most_read_genre
    }

def add_note(db:Session, book_id:int, note_in: NoteCreate):
    db_note = Note(book_id=book_id, content= note_in.content)

    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note

def get_book_notes(db: Session, book_id:int):
    # Returns all notes for a specific book, newest first
    return db.query(Note).filter(Note.book_id == book_id).order_by(Note.created_at.desc()).all()
