from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.book import StatsResponse
from app.crud import book as crud_book


router = APIRouter(prefix="/stats", tags=["Collection Analytics"])

@router.get("/",response_model=StatsResponse)
def get_stats(db:Session=Depends(get_db)):
    """Get high-level statistics about your reading collection."""
    return crud_book.get_collection_stats(db)