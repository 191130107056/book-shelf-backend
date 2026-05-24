import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.core.database import Base, get_db
from app.models.book import Book, BookStatus, Note 
from main import app

# 1. Setup a clean, in-memory SQLite database for testing
# This ensures our real database isn't affected by tests
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 2. Dependency Override
# This replaces the real get_db with our test database
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_database():
    """
    Creates all tables in the test.db before each test, 
    then deletes them after the test is done.
    """
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

# 3. THE TESTS
def test_create_book():
    response = client.post("/books/",json={
        "title": "Test Driven Development",
        "author": "Kent Beck",
        "genre": "Tech",
        "total_pages": 336,
        "published_year": 2002,
        "isbn": "9780321146533"
    })
    assert response.status_code == 201
    assert response.json()['title'] == "Test Driven Development"

def test_get_stats_empty():
    response = client.get("/stats/")
    assert response.status_code == 200
    assert response.json()["total_books"] == 0

def test_invalid_isbn_fails():
    response = client.post("/books/", json={
        "title": "Invalid ISBN", "author": "A", "genre": "B", 
        "total_pages": 100, "published_year": 2020, "isbn": "short"
    })
    assert response.status_code == 422 # Validation Error

def test_business_rule_status_sequence():
    # 1. Add a book with a VALID ISBN (10+ characters)
    create_response = client.post("/books/", json={
        "title": "Logic Test", 
        "author": "A", 
        "genre": "Business",  ## for fail use B
        "total_pages": 100, 
        "published_year": 2020, 
        "isbn": "1234567890" # <--- \For fail case use less than short length isbn
    })
    # Senior Tip: Always assert that your setup worked!
    assert create_response.status_code == 201
    
    # 2. Try to mark as 'completed' directly from 'to_read'
    # Now that the book exists, this should return 400 (Business Rule)
    response = client.patch("/books/1/status", json={"status": "completed"})
    
    assert response.status_code == 400
    assert "reading" in response.json()["message"]

def test_rate_limiter():
    # Hit the health endpoint 12 times quickly
    for _ in range(10):
        client.get("/")

    response = client.get("/")
    # The 11th or 12th request should be rate limited
    assert response.status_code == 429
    assert response.json()['detail'] == "Too many requests. Please wait a minute."
