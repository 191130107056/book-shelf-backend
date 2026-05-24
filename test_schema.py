from app.schemas.book import BookCreate
from pydantic import ValidationError

print("--- Testing Pydantic Validation ---")

# Test 1: Valid Data
try:
    book = BookCreate(
        title="Test Book",
        author="John Doe",
        genre="Coding",
        total_pages=300,
        published_year=2024,
        isbn="1234567890"
    )
    print("✅ Valid book created successfully!")
except ValidationError as e:
    print(f"❌ Unexpected Error: {e}")

# Test 2: Edge Case - Negative Pages
try:
    invalid_book = BookCreate(
        title="Bad Book",
        author="John Doe",
        genre="Coding",
        total_pages=-10,  # This should fail
        published_year=2024,
        isbn="1234567890"
    )
except ValidationError as e:
     print("✅ Correctly caught error: Total pages must be positive.")

# Test 3: Edge Case - Future Year
try:
    future_book = BookCreate(
        title="Future Book",
        author="John Doe",
        genre="Sci-Fi",
        total_pages=100,
        published_year=2099, # This should fail
        isbn="1234567890"
    )
except ValidationError as e:
    print("✅ Correctly caught error: Year cannot be in the future.")
