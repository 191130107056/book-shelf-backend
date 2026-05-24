# Personal Bookshelf API

A RESTful backend API built with FastAPI and SQLAlchemy to manage a personal reading collection. This system allows users to track their books, manage reading progress, add personal notes, and view collection statistics.

## Features

- **Book Management (CRUD)**: Full support for adding, viewing, updating, and deleting books.
- **Reading Status Tracking**: Track books through `to_read`, `reading`, and `completed` statuses.
- **Automated Timestamps**: Automatically records `started_at` and `finished_at` dates based on status changes.
- **Ratings & Reviews**: Add 1-5 star ratings and text reviews for completed books.
- **Book Notes**: Add multiple timestamped personal notes to any book in your collection.
- **Filtering & Search**: Search by title/author and filter by status, genre, or minimum rating.
- **Collection Statistics**: View aggregate data including total books, average rating, total pages read, and most-read genre.
- **Rate Limiting**: Built-in protection limiting requests to 10 per minute per IP.

## Project Structure

```text
bookshelf_api/
├── app/
│   ├── core/      # Settings, Database connection, and Custom Exceptions
│   ├── crud/      # Database operations and Business Logic
│   ├── models/    # SQLAlchemy database models
│   ├── routers/   # API route handlers (Books, Stats, Notes)
│   ├── schemas/   # Pydantic data validation models
├── main.py        # Application entry point and Middleware
├── tests/         # Automated test suite (pytest)
├── .env           # Environment configuration
├── seed.py        # Database population script (15 sample books)
└── requirements.txt # Pinned dependencies
```
---

## Tech Stack

- **Framework**: FastAPI (Asynchronous support)
- **Database**: SQLite (Zero-friction setup)
- **ORM**: SQLAlchemy 2.0 (Modern Type-Safe approach)
- **Validation**: Pydantic v2
- **Config**: Pydantic Settings (Environment variables via `.env`)

---

## Installation & Setup

### 1. Clone the Project and Create Environment
```bash
# Create virtual environment
python -m venv venv

# Activate environment (Windows)
venv\Scripts\activate

# Activate environment (macOS/Linux)
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment
Create a .env file in the root directory:

```bash
PROJECT_NAME="Personal Bookshelf API"
DATABASE_URL="sqlite:///./bookshelf.db"
```

### 4. Seed the Database
Populate your database with 15 sample books across various statuses (to_read, reading, completed):

```bash
python seed.py
```

### 5. Run the API

```bash
python main.py
```
The API will be available at: http://127.0.0.1:8000
Interactive Documentation: http://127.0.0.1:8000/docs

### 6. Running Tests
```bash
pytest
```

## Example API Commands (CURL)
### 1. Add a New Book

```bash
curl -X 'POST' 'http://127.0.0.1:8000/books/' \
-H 'Content-Type: application/json' \
-d '{
  "title": "Clean Architecture",
  "author": "Robert C. Martin",
  "genre": "Technology",
  "total_pages": 400,
  "published_year": 2017,
  "isbn": "9780134494166"
}'
```

### 2. Get Paginated Books (Filtered)
```bash
curl 'http://127.0.0.1:8000/books/?status=completed&min_rating=4&sort_by=rating&order=desc'
```

### 3. Search Title or Author
```bash
curl 'http://127.0.0.1:8000/books/search?q=orwell'
```

### 4. Update Reading Status
```bash
curl -X 'PATCH' 'http://127.0.0.1:8000/books/1/status' \
-H 'Content-Type: application/json' \
-d '{"status": "reading"}'
```

### 5. Add Rating and Review
```bash
curl -X 'POST' 'http://127.0.0.1:8000/books/1/rate' \
-H 'Content-Type: application/json' \
-d '{
  "rating": 5,
  "review": "An absolute masterpiece of software design!"
}'
```
### 6. Add a Note to a Book
```bash
curl -X 'POST' 'http://127.0.0.1:8000/books/1/notes' \
-H 'Content-Type: application/json' \
-d '{"content": "Starting the second chapter today."}'
```

### 7. View Collection Statistics
```bash
curl 'http://127.0.0.1:8000/stats/'
```


## Technical Rules
**1. Business Logic:** A book cannot be marked completed unless it has first been moved to the reading status.

**2. Ratings:** Users can only rate and review books that have reached the completed status.

**3. Data Integrity:** ISBNs must be unique. Ratings must be between 1 and 5.

**4. Cascading Deletes:** If a book is deleted, all associated notes are automatically removed from the database.