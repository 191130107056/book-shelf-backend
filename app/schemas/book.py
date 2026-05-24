from tkinter import NO
from pydantic import BaseModel, Field, ConfigDict, field_validator
from typing import Optional, List
from datetime import datetime
from app.models.book import BookStatus

# 1. Base Schema (Shared fields)
class BookBase(BaseModel):  
    title: str = Field(..., min_length=1, max_length=255, examples=["The Great Gatsby"])
    author: str = Field(..., min_length=1, max_length=255, examples=["F. Scott Fitzgerald"])
    genre: str = Field(..., min_length=2, examples=["Fiction"])
    total_pages:int = Field(..., gt=0, description="Must be a positive number")
    published_year:int = Field(..., le=datetime.now().year)
    isbn: str = Field(...,min_length=10, max_length=13, examples=["9780743273565"])

# 2. Schema for Creating a Book
class BookCreate(BookBase):
    pass # Exactly like Base for now

# 3. Schema for Partial Updates (PATCH)
# Every field is optional here because the user might only want to change one thing.
class BookUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1)
    author: Optional[str] = Field(None, min_length=1)
    genre: Optional[str] = None
    total_pages: Optional[int] = Field(None, gt=0)
    published_year: Optional[int] = Field(None, le = datetime.now().year)

# 4. Schema for Status Update
class BookStatusUpdate(BaseModel):
    status: BookStatus

# 5. Schema for Rating & Review
class BookRatingUpdate(BaseModel):
    rating: float = Field(..., ge=1, le=5, description="Rating must be between 1 and 5")
    review: str = Field(..., max_length=500, description="Review max 500 characters")

# 6. Schema for API Response
# This defines what the "outside world" sees
class BookResponse(BookBase):
    id:int
    status: BookStatus
    rating: Optional[float] = None
    review: Optional[str] = None
    started_at: Optional[datetime] = None
    finished_at: Optional[datetime] = None
    created_at: datetime

    # IMPORTANT: This tells Pydantic to read data from SQLAlchemy objects
    model_config = ConfigDict(from_attributes=True)

class PaginatedBookResponse(BaseModel):
    total: int
    page: int
    limit:int
    books: List[BookResponse]

# 7. Schema for Statistics
class StatsResponse(BaseModel):
    total_books: int
    status_counts: dict[str,int]
    average_rating: float
    total_pages_read: int
    most_read_genre: Optional[str]

class NoteCreate(BaseModel):
    content: str = Field(..., min_length=1, max_length=1000)
    
class NoteResponse(BaseModel):
    id:int
    content:str
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


